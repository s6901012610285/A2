# Constants for grid dimensions
COLS = 5
ROWS = 5
CELL_SIZE = 80

# Global game state variables
grid = []
moves = 0
best_moves = None
game_over = False

# Reset button UI coordinates and dimensions
BTN_X = 285
BTN_Y = 410
BTN_W = 100
BTN_H = 30


def setup():
    size(COLS * CELL_SIZE, ROWS * CELL_SIZE + 50)
    reset_game()


def reset_game():
    global grid, moves, game_over
    # TODO: Initialize 2D array and scramble lights
    pass


def toggle(r, c):
    global grid
    if 0 <= r < ROWS and 0 <= c < COLS:
        # TODO: Toggle light state at (r, c) and 4 adjacent neighbors
        pass
    else:
        pass


def check_win():
    # TODO: Return True if all lights are off, else False
    return False


def draw_bulb(cx, cy, is_on):
    # TODO: Render bulb using line scanline fill and borders
    pass


def draw_grid_recursive(r, c):
    if r >= ROWS:
        return
    else:
        # TODO: Recursively draw each grid cell
        pass


def draw():
    background(30)
    # TODO: Render game grid and UI elements
    if game_over:
        pass
    else:
        pass


def mousePressed():
    global moves, game_over
    if game_over:
        return
    else:
        # TODO: Handle grid cell and button click interactions
        pass
