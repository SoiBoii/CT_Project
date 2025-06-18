import pygame
import numpy as np

pygame.init()

ROWS, COLS = 50, 50
button_height = 50
fullscreen = False
screen_width, screen_height = 800, 850

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)
RED = (200, 50, 50)
GREEN = (0, 200, 0)

framerates = [1, 5, 10, 15, 30]
current_framerate_index = 1 

grid = np.zeros((ROWS, COLS), dtype=int)

def place_glider(grid, r, c):
    for dr, dc in [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_blinker(grid, r, c):
    for dr, dc in [(0, 0), (0, 1), (0, 2)]:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_gosper_gun(grid, r, c):
    coords = [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11), (4, 12), (8, 12),
        (3, 13), (9, 13), (3, 14), (9, 14), (6, 15),
        (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18),
        (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22),
        (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36)
    ]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_toad(grid, r, c):
    coords = [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2)]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_beacon(grid, r, c):
    coords = [(0,0), (0,1), (1,0), (1,1), (2,2), (2,3), (3,2), (3,3)]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_pulsar(grid, r, c):
    base = [
        (2,4), (2,5), (2,6), (2,10), (2,11), (2,12),
        (7,4), (7,5), (7,6), (7,10), (7,11), (7,12),
        (4,2), (5,2), (6,2), (10,2), (11,2), (12,2),
        (4,7), (5,7), (6,7), (10,7), (11,7), (12,7),
        (4,9), (5,9), (6,9), (10,9), (11,9), (12,9),
        (4,14), (5,14), (6,14), (10,14), (11,14), (12,14),
        (14,4), (14,5), (14,6), (14,10), (14,11), (14,12),
        (9,2), (9,7), (9,9), (9,14)
    ]
    for dr, dc in base:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_lwss(grid, r, c):
    coords = [(0,1), (0,4), (1,0), (2,0), (3,0), (3,4), (4,0), (4,1), (4,2), (4,3)]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1
            
def place_and_gate(grid, r, c):
    coords = [
        (0, 0), (0, 1), (1, 0), (1, 1), 
        (4, 4), (4, 5), (5, 4), (5, 5),  
        (2, 10), (3, 11), (4, 9), (4, 10), (4, 11)  
    ]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_or_gate(grid, r, c):
    coords = [
        (0, 0), (0, 1), (1, 0), (1, 1),
        (0, 8), (1, 8), (1, 9), (2, 9),
        (3, 11), (4, 11), (4, 12), (5, 12)  
    ]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1

def place_not_gate(grid, r, c):
    coords = [
        (0, 0), (0, 1), (1, 0), (1, 1),  
        (4, 3), (5, 4), (6, 2), (6, 3), (6, 4)  
    ]
    for dr, dc in coords:
        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS:
            grid[r + dr][c + dc] = 1



presets = {
    "Start/Stop": None,
    "Reset": None,
    "Framerate": None,
    "Glider": place_glider,
    "Blinker": place_blinker,
    "Gosper Gun": place_gosper_gun,
    "Toad": place_toad,
    "Beacon": place_beacon,
    "Pulsar": place_pulsar,
    "LWSS": place_lwss,
    "AND Gate": place_and_gate,
    "OR Gate": place_or_gate,
    "NOT Gate": place_not_gate,
}



selected_preset = None
running_sim = False
clock = pygame.time.Clock()

def toggle_fullscreen():
    global fullscreen, screen, screen_width, screen_height
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen_width, screen_height = 800, 850
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    screen_width, screen_height = screen.get_size()

def draw(win, grid):
    cell_w = screen_width // COLS
    cell_h = (screen_height - button_height) // ROWS

    win.fill(BLACK)

    bw = screen_width // len(presets)
    for i, name in enumerate(presets):
        rect = pygame.Rect(i * bw, 0, bw, button_height)
        color = RED if name == "Reset" else GREEN if name == "Start/Stop" and running_sim else BLUE
        if selected_preset == name:
            color = YELLOW
        pygame.draw.rect(win, color, rect)
        font = pygame.font.SysFont(None, 24)
        label = f"{name} ({framerates[current_framerate_index]}fps)" if name == "Framerate" else name
        text = font.render(label, True, BLACK)
        win.blit(text, text.get_rect(center=rect.center))


    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 1 else GRAY
            pygame.draw.rect(
                win,
                color,
                pygame.Rect(
                    col * cell_w,
                    row * cell_h + button_height,
                    cell_w - 1,
                    cell_h - 1
                )
            )
    pygame.display.flip()

def get_neighbors(grid, row, col):
    return sum(grid[(row + dr) % ROWS][(col + dc) % COLS]
               for dr in (-1, 0, 1) for dc in (-1, 0, 1)
               if not (dr == 0 and dc == 0))

def update(grid):
    new_grid = np.copy(grid)
    for r in range(ROWS):
        for c in range(COLS):
            n = get_neighbors(grid, r, c)
            if grid[r][c] == 1 and (n < 2 or n > 3):
                new_grid[r][c] = 0
            elif grid[r][c] == 0 and n == 3:
                new_grid[r][c] = 1
    return new_grid

running = True
while running:
    clock.tick(framerates[current_framerate_index])
    cell_w = screen_width // COLS
    cell_h = (screen_height - button_height) // ROWS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                toggle_fullscreen()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if y < button_height:
                idx = x // (screen_width // len(presets))
                btn_name = list(presets.keys())[idx]
                if btn_name == "Start/Stop":
                    running_sim = not running_sim
                elif btn_name == "Reset":
                    grid = np.zeros((ROWS, COLS), dtype=int)
                    running_sim = False
                    selected_preset = None 
                elif btn_name == "Framerate":
                    current_framerate_index = (current_framerate_index + 1) % len(framerates)
                else:
                    selected_preset = btn_name

            else:
                col = x // cell_w
                row = (y - button_height) // cell_h
                if selected_preset in presets and presets[selected_preset]:
                    presets[selected_preset](grid, row, col)
                else:
                    grid[row][col] = 1 - grid[row][col]

    if running_sim:
        grid = update(grid)

    draw(screen, grid)

pygame.quit()
