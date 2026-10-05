# Grid configuration constants
COLS = 5
ROWS = 5
CELL_SIZE = 80

# Global game state variables
grid = []
moves = 0
best_moves = None
game_over = False

# Reset button UI panel layout coordinates
BTN_X = 285
BTN_Y = 410
BTN_W = 100
BTN_H = 30


def setup():
    # Set main window size with extra 50px vertical height for bottom UI panel
    size(COLS * CELL_SIZE, ROWS * CELL_SIZE + 50)
    reset_game()


def reset_game():
    global grid, moves, game_over
    moves = 0
    game_over = False

    # Initialize 5x5 grid with all lights turned OFF (0) using while loops
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

    # Scramble board by simulating 15 random toggles starting from solved state
    # Guarantees that the generated board configuration is 100% solvable
    i = 0
    while i < 15:
        rand_r = int(random(ROWS))
        rand_c = int(random(COLS))
        toggle(rand_r, rand_c)
        i += 1

    # Reset player move count back to 0 after board scrambling completes
    moves = 0


def toggle(r, c):
    global grid
    if 0 <= r < ROWS and 0 <= c < COLS:
        # Define target cell and its 4 adjacent neighbors (Up, Down, Left, Right)
        positions = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        i = 0
        while i < len(positions):
            nr, nc = positions[i]
            # Boundary guard to prevent array out of bounds exception
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                grid[nr][nc] = 1 - grid[nr][nc]
            else:
                pass
            i += 1
    else:
        pass


def check_win():
    # Board is cleared when no ON lights (1) remain in any row
    if not any(1 in row for row in grid):
        return True
    else:
        return False


def draw_bulb(cx, cy, is_on):
    # Determine color palette based on current cell state
    if is_on:
        bg_col = color(255, 220, 80)    # Active cell background (Yellow)
        bulb_col = color(255, 255, 200) # Active bulb center (Bright White-Yellow)
    else:
        bg_col = color(50)             # Inactive cell background (Dark Grey)
        bulb_col = color(90)           # Inactive bulb center (Dim Grey)

    # 1. Fill cell interior using horizontal line scanlines (No rect allowed)
    stroke(bg_col)
    i = 0
    while i < CELL_SIZE:
        line(cx, cy + i, cx + CELL_SIZE, cy + i)
        i += 1

    # 2. Render central bulb graphic using ellipse shape
    fill(bulb_col)
    stroke(30)
    ellipse(cx + CELL_SIZE / 2, cy + CELL_SIZE / 2, 40, 40)

    # 3. Draw outer grid lines for cell borders using line primitives
    stroke(20)
    line(cx, cy, cx + CELL_SIZE, cy)                          # Top border
    line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE)  # Bottom border
    line(cx, cy, cx, cy + CELL_SIZE)                          # Left border
    line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE)  # Right border


def draw_grid_recursive(r, c):
    # Base case: stop recursive rendering when row index reaches maximum
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

        # Recurse to next column or wrap down to next row
        if c + 1 >= COLS:
            draw_grid_recursive(r + 1, 0)
        else:
            draw_grid_recursive(r, c + 1)


def draw():
    background(30)
    draw_grid_recursive(0, 0)

    # ------------------ Bottom Control Panel UI ------------------
    fill(20)
    noStroke()
    rect(0, ROWS * CELL_SIZE, width, 50)

    # Display move counter and best score status
    fill(255)
    textSize(15)
    textAlign(LEFT, CENTER)
    text("Moves: " + str(moves), 15, ROWS * CELL_SIZE + 25)

    if best_moves is not None:
        best_str = str(best_moves)
    else:
        best_str = "-"

    text("Best: " + best_str, 135, ROWS * CELL_SIZE + 25)

    # Render RESET button with hover color highlight
    if BTN_X <= mouseX <= BTN_X + BTN_W and BTN_Y <= mouseY <= BTN_Y + BTN_H:
        fill(220, 60, 60)  # Highlighted red on hover
    else:
        fill(180, 40, 40)  # Default red button color

    rect(BTN_X, BTN_Y, BTN_W, BTN_H, 6)

    fill(255)
    textSize(13)
    textAlign(CENTER, CENTER)
    text("RESET", BTN_X + BTN_W / 2, BTN_Y + BTN_H / 2)

    # ------------------ Win Overlay Screen ------------------
    if game_over:
        fill(0, 220)
        rect(0, 0, width, height)

        fill(255, 215, 0)
        textAlign(CENTER, CENTER)
        textSize(32)
        text("YOU WIN!", width / 2, height / 2 - 50)

        fill(255)
        textSize(18)
        text("Moves used: " + str(moves), width / 2, height / 2 - 10)
        text("Best Score: " + str(best_moves), width / 2, height / 2 + 20)

        # Render NEXT GAME button with hover effect
        play_x = width / 2 - 60
        play_y = height / 2 + 65
        play_w = 120
        play_h = 35

        if play_x <= mouseX <= play_x + play_w and play_y <= mouseY <= play_y + play_h:
            fill(90, 200, 100)  # Highlighted green on hover
        else:
            fill(60, 160, 70)   # Default green button color

        rect(play_x, play_y, play_w, play_h, 6)

        fill(255)
        textSize(14)
        text("NEXT GAME", width / 2, play_y + play_h / 2)
    else:
        pass


def mousePressed():
    global moves, game_over, best_moves

    # Handle bottom panel RESET button click
    if BTN_X <= mouseX <= BTN_X + BTN_W and BTN_Y <= mouseY <= BTN_Y + BTN_H:
        reset_game()
        return
    else:
        pass

    # Handle NEXT GAME button click when in win screen
    if game_over:
        play_x = width / 2 - 60
        play_y = height / 2 + 65
        play_w = 120
        play_h = 35

        if play_x <= mouseX <= play_x + play_w and play_y <= mouseY <= play_y + play_h:
            reset_game()
        else:
            pass
        return
    else:
        pass

    # Handle grid cell toggling during active game loop
    c = mouseX // CELL_SIZE
    r = mouseY // CELL_SIZE

    if 0 <= r < ROWS and 0 <= c < COLS:
        toggle(r, c)
        moves += 1

        if check_win():
            game_over = True
            if best_moves is None or moves < best_moves:
                best_moves = moves
            else:
                pass
        else:
            pass
    else:
        pass
