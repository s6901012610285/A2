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
    if is_on:
        bg_col = color(255, 220, 80)    # Active cell background (Yellow)
        bulb_col = color(255, 255, 200) # Active bulb center (Bright White-Yellow)
    else:
        bg_col = color(50)             # Inactive cell background (Dark Grey)
        bulb_col = color(90)           # Inactive bulb center (Dim Grey)

    # 1. Fill cell interior using horizontal line scanlines
    stroke(bg_col)
    i = 0
    while i < CELL_SIZE:
        line(cx, cy + i, cx + CELL_SIZE, cy + i)
        i += 1

    # 2. Draw central bulb shape using ellipse
    fill(bulb_col)
    stroke(30)
    ellipse(cx + CELL_SIZE / 2, cy + CELL_SIZE / 2, 40, 40)

    # 3. Render cell outer borders using line primitives
    stroke(20)
    line(cx, cy, cx + CELL_SIZE, cy)                          # Top border
    line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE)  # Bottom border
    line(cx, cy, cx, cy + CELL_SIZE)                          # Left border
    line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE)  # Right border


def draw_grid_recursive(r, c):
    if r >= ROWS:
        return
    else:
        x = c * CELL_SIZE
        y = r * CELL_SIZE

        if grid[r][c] == 1:
            is_on = True
        else:
            is_on = False

        draw_bulb(x, y, is_on)

        if c + 1 >= COLS:
            draw_grid_recursive(r + 1, 0)
        else:
            draw_grid_recursive(r, c + 1)


def draw():
    background(30)
    draw_grid_recursive(0, 0)


def mousePressed():
    global moves, game_over

    # Stop accepting board clicks when game is already won
    if game_over:
        return
    else:
        pass

    # Translate mouse screen coordinates into grid array indices
    c = mouseX // CELL_SIZE
    r = mouseY // CELL_SIZE

    # Boundary Guard: Ensure click is inside valid grid coordinates
    if 0 <= r < ROWS and 0 <= c < COLS:
        toggle(r, c)
        moves += 1

        # Check for victory condition after every move
        if check_win():
            game_over = True
        else:
            pass
    else:
        pass
