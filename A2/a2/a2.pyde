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
    moves = 0
    game_over = False

    # Initialize 5x5 grid with all lights OFF (0) using while loops
    grid = []
    r = 0
    while r < ROWS:
        row = []
        c = 0
        while c < COLS:
            row.append(0)
            c += 1
        grid.append(row)
        r += 1

    # Scramble board by simulating 15 random toggles from solved state
    # Guarantees the board is 100% solvable
    i = 0
    while i < 15:
        rand_r = int(random(ROWS))
        rand_c = int(random(COLS))
        toggle(rand_r, rand_c)
        i += 1

    # Reset player move count back to 0 after board generation
    moves = 0


def toggle(r, c):
    global grid
    if 0 <= r < ROWS and 0 <= c < COLS:
        # Array of target cell and 4 adjacent neighbors (Up, Down, Left, Right)
        positions = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        i = 0
        while i < len(positions):
            nr, nc = positions[i]
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                grid[nr][nc] = 1 - grid[nr][nc]
            else:
                pass
            i += 1
    else:
        pass


def check_win():
    if not any(1 in row for row in grid):
        return True
    else:
        return False


def draw_bulb(cx, cy, is_on):
    # TODO: Render bulb graphics using line & ellipse (To be implemented in Commit 3)
    pass


def draw_grid_recursive(r, c):
    if r >= ROWS:
        return
    else:
        # TODO: Render grid recursively (To be implemented in Commit 3)
        pass


def draw():
    background(30)
    draw_grid_recursive(0, 0)


def mousePressed():
    global moves, game_over
    if game_over:
        return
    else:
        c = mouseX // CELL_SIZE
        r = mouseY // CELL_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            toggle(r, c)
            moves += 1
            if check_win():
                game_over = True
            else:
                pass
        else:
            pass