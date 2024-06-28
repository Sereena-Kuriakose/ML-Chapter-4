import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Define constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Define Tetromino shapes
tetrominos = [
    [[1, 1, 1, 1]],  # I shape
    [[1, 1, 1], [0, 1, 0]],  # T shape
    [[1, 1, 1], [1, 0, 0]],  # L shape
    [[1, 1, 1], [0, 0, 1]],  # J shape
    [[1, 1], [1, 1]],  # O shape
    [[1, 1, 0], [0, 1, 1]],  # Z shape
    [[0, 1, 1], [1, 1, 0]]   # S shape
]

# Initialize game variables
board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
current_piece = random.choice(tetrominos)
current_color = random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE])
piece_x = SCREEN_WIDTH // 2 - len(current_piece[0]) // 2 * BLOCK_SIZE
piece_y = 0

# Initialize Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Tetris')

clock = pygame.time.Clock()
fps = 10

def draw_board():
    screen.fill(BLACK)
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x]:
                pygame.draw.rect(screen, board[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    draw_piece()

def draw_piece():
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x]:
                pygame.draw.rect(screen, current_color, (piece_x + x * BLOCK_SIZE, piece_y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision():
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x]:
                if piece_y + y * BLOCK_SIZE >= SCREEN_HEIGHT - BLOCK_SIZE or \
                   piece_x + x * BLOCK_SIZE < 0 or \
                   piece_x + x * BLOCK_SIZE >= SCREEN_WIDTH or \
                   board[(piece_y + y * BLOCK_SIZE) // BLOCK_SIZE][(piece_x + x * BLOCK_SIZE) // BLOCK_SIZE]:
                    return True
    return False

def merge_piece():
    for y in range(len(current_piece)):
        for x in range(len(current_piece[y])):
            if current_piece[y][x]:
                board[(piece_y + y * BLOCK_SIZE) // BLOCK_SIZE][(piece_x + x * BLOCK_SIZE) // BLOCK_SIZE] = current_color

def check_line_clear():
    lines_cleared = 0
    for y in range(len(board)):
        if all(board[y]):
            del board[y]
            board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
    return lines_cleared

def game_over():
    font = pygame.font.SysFont('Arial', 36)
    text = font.render('Game Over', True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    quit()

def game_loop():
    global piece_x, piece_y, current_piece, current_color
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece_x -= BLOCK_SIZE
                    if check_collision():
                        piece_x += BLOCK_SIZE
                elif event.key == pygame.K_RIGHT:
                    piece_x += BLOCK_SIZE
                    if check_collision():
                        piece_x -= BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    piece_y += BLOCK_SIZE
                    if check_collision():
                        piece_y -= BLOCK_SIZE
                elif event.key == pygame.K_UP:
                    rotated_piece = list(zip(*current_piece[::-1]))
                    if piece_x + len(rotated_piece[0]) * BLOCK_SIZE <= SCREEN_WIDTH and \
                       piece_y + len(rotated_piece) * BLOCK_SIZE <= SCREEN_HEIGHT and \
                       not any(board[(piece_y + y * BLOCK_SIZE) // BLOCK_SIZE][(piece_x + x * BLOCK_SIZE) // BLOCK_SIZE] for y in range(len(rotated_piece)) for x in range(len(rotated_piece[y]))):
                        current_piece = rotated_piece
                elif event.key == pygame.K_SPACE:
                    while not check_collision():
                        piece_y += BLOCK_SIZE
                    piece_y -= BLOCK_SIZE

        piece_y += BLOCK_SIZE
        if check_collision():
            piece_y -= BLOCK_SIZE
            merge_piece()
            lines_cleared = check_line_clear()
            if lines_cleared:
                print(f"Lines cleared: {lines_cleared}")
            current_piece = random.choice(tetrominos)
            current_color = random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, PURPLE])
            piece_x = SCREEN_WIDTH // 2 - len(current_piece[0]) // 2 * BLOCK_SIZE
            piece_y = 0
            if check_collision():
                game_over()

        draw_board()
        pygame.display.flip()
        clock.tick(fps)

# Start the game loop
game_loop()

pygame.quit()
quit()
