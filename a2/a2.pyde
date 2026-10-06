# Grid configuration constants
COLS = 5
ROWS = 5
CELL_SIZE = 80

# Global game state variables
grid = []
moves = 0
best_moves = None
game_over = False

# Save/Load visual feedback status variables
# Status: 0 = Normal, 1 = Success (Green), -1 = Fail (Red)
save_status = 0
save_timer = 0
load_status = 0
load_timer = 0

# UI Button Layout Coordinates
BTN_SAVE_X = 165
BTN_SAVE_Y = 410
BTN_SAVE_W = 55
BTN_SAVE_H = 30

BTN_LOAD_X = 225
BTN_LOAD_Y = 410
BTN_LOAD_W = 55
BTN_LOAD_H = 30

BTN_RESET_X = 285
BTN_RESET_Y = 410
BTN_RESET_W = 100
BTN_RESET_H = 30


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
    i = 0
    while i < 15:
        rand_r = int(random(ROWS))
        rand_c = int(random(COLS))
        toggle(rand_r, rand_c)
        i += 1

    # Reset player move count back to 0 after board scrambling completes
    moves = 0


def save_game(filename="save.txt"):
    global save_status, save_timer
    save_timer = millis()
    try:
        with open(filename, "w") as f:
            f.write("count=\n")
            f.write(str(moves) + "\n")

            f.write("check_win=\n")
            if game_over:
                f.write("1\n")
            else:
                f.write("0\n")

            f.write("grid=\n")

            # Write 2D grid array row by row using while loop
            r = 0
            while r < ROWS:
                row_str = ""
                c = 0
                while c < COLS:
                    row_str += str(grid[r][c])
                    if c < COLS - 1:
                        row_str += " "
                        
                    c += 1
                f.write(row_str + "\n")
                r += 1

        save_status = 1  # Success (Green)
    except Exception:
        save_status = -1  # Fail (Red)


def load_game(filename="save.txt"):
    global grid, moves, game_over, load_status, load_timer
    load_timer = millis()
    try:
        with open(filename, "r") as f:
            lines = f.readlines()

        if len(lines) >= 10:
            # Parse move count from line 2
            moves = int(lines[1].strip())

            # Parse win status from line 4
            win_val = int(lines[3].strip())
            if win_val == 1:
                game_over = True
            else:
                game_over = False

            # Parse grid matrix starting from line 6 (index 5)
            new_grid = []
            r = 0
            while r < ROWS:
                line_idx = 5 + r
                parts = lines[line_idx].strip().split()
                row = []
                c = 0
                while c < COLS:
                    row.append(int(parts[c]))
                    c += 1
                new_grid.append(row)
                r += 1

            grid = new_grid
            load_status = 1  # Success (Green)
        else:
            load_status = -1  # Fail (Red)
    except Exception:
        load_status = -1  # Fail (Red)


def toggle(r, c):
    global grid
    if 0 <= r < ROWS and 0 <= c < COLS:
        positions = [(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        i = 0
        while i < len(positions):
            nr, nc = positions[i]
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                if grid[nr][nc] == 0: #simplify grid[nr][nc] = 1 - grid[nr][nc]
                    grid[nr][nc] = 1
                else:
                    grid[nr][nc] = 0
            i += 1



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

    # 2. Render central bulb shape using ellipse
    fill(bulb_col)
    stroke(30)
    ellipse(cx + CELL_SIZE / 2, cy + CELL_SIZE / 2, 40, 40)

    # 3. Render cell outer borders
    stroke(20)
    line(cx, cy, cx + CELL_SIZE, cy)
    line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE)
    line(cx, cy, cx, cy + CELL_SIZE)
    line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE)


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
    global save_status, load_status
    background(30)
    draw_grid_recursive(0, 0)

    # Reset button status color feedback after 1000ms (1 second)
    if millis() - save_timer > 1000:
        save_status = 0


    if millis() - load_timer > 1000:
        load_status = 0


    # ------------------ Bottom Control Panel UI ------------------
    fill(20)
    noStroke()
    rect(0, ROWS * CELL_SIZE, width, 50)

    # Display move counter and best score
    fill(255)
    textSize(13)
    textAlign(LEFT, CENTER)
    text("Moves: " + str(moves), 10, ROWS * CELL_SIZE + 25)

    if best_moves is not None:
        best_str = str(best_moves)
    else:
        best_str = "-"

    text("Best: " + best_str, 95, ROWS * CELL_SIZE + 25)

    # Render SAVE button with visual feedback colors
    if save_status == 1:
        fill(40, 180, 80)    # Green on Success
    else:
        if save_status == -1:
            fill(220, 50, 50)  # Red on Fail
        else:
            if BTN_SAVE_X <= mouseX <= BTN_SAVE_X + BTN_SAVE_W and BTN_SAVE_Y <= mouseY <= BTN_SAVE_Y + BTN_SAVE_H:
                fill(70, 150, 220)  # Default hover blue
            else:
                fill(40, 100, 180)  # Default blue

    rect(BTN_SAVE_X, BTN_SAVE_Y, BTN_SAVE_W, BTN_SAVE_H, 0)
    fill(255)
    textAlign(CENTER, CENTER)
    text("SAVE", BTN_SAVE_X + BTN_SAVE_W / 2, BTN_SAVE_Y + BTN_SAVE_H / 2)

    # Render LOAD button with visual feedback colors
    if load_status == 1:
        fill(40, 180, 80)    # Green on Success
    else:
        if load_status == -1:
            fill(220, 50, 50)  # Red on Fail
        else:
            if BTN_LOAD_X <= mouseX <= BTN_LOAD_X + BTN_LOAD_W and BTN_LOAD_Y <= mouseY <= BTN_LOAD_Y + BTN_LOAD_H:
                fill(220, 160, 60)  # Default hover orange
            else:
                fill(180, 120, 40)  # Default orange

    rect(BTN_LOAD_X, BTN_LOAD_Y, BTN_LOAD_W, BTN_LOAD_H, 0)
    fill(255)
    textAlign(CENTER, CENTER)
    text("LOAD", BTN_LOAD_X + BTN_LOAD_W / 2, BTN_LOAD_Y + BTN_LOAD_H / 2)

    # Render RESET button
    if BTN_RESET_X <= mouseX <= BTN_RESET_X + BTN_RESET_W and BTN_RESET_Y <= mouseY <= BTN_RESET_Y + BTN_RESET_H:
        fill(220, 60, 60)
    else:
        fill(180, 40, 40)
    rect(BTN_RESET_X, BTN_RESET_Y, BTN_RESET_W, BTN_RESET_H, 0)
    fill(255)
    textAlign(CENTER, CENTER)
    text("RESET", BTN_RESET_X + BTN_RESET_W / 2, BTN_RESET_Y + BTN_RESET_H / 2)

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

        play_x = width / 2 - 60
        play_y = height / 2 + 65
        play_w = 120
        play_h = 35

        if play_x <= mouseX <= play_x + play_w and play_y <= mouseY <= play_y + play_h:
            fill(90, 200, 100)
        else:
            fill(60, 160, 70)

        rect(play_x, play_y, play_w, play_h, 0)

        fill(255)
        textSize(14)
        text("NEXT GAME", width / 2, play_y + play_h / 2)


def mousePressed():
    global moves, game_over, best_moves

    # Handle SAVE button click
    if BTN_SAVE_X <= mouseX <= BTN_SAVE_X + BTN_SAVE_W and BTN_SAVE_Y <= mouseY <= BTN_SAVE_Y + BTN_SAVE_H:
        save_game()
        return


    # Handle LOAD button click
    if BTN_LOAD_X <= mouseX <= BTN_LOAD_X + BTN_LOAD_W and BTN_LOAD_Y <= mouseY <= BTN_LOAD_Y + BTN_LOAD_H:
        load_game()
        return


    # Handle RESET button click
    if BTN_RESET_X <= mouseX <= BTN_RESET_X + BTN_RESET_W and BTN_RESET_Y <= mouseY <= BTN_RESET_Y + BTN_RESET_H:
        reset_game()
        return

    # Handle NEXT GAME button click when in win screen
    if game_over:
        play_x = width / 2 - 60
        play_y = height / 2 + 65
        play_w = 120
        play_h = 35

        if play_x <= mouseX <= play_x + play_w and play_y <= mouseY <= play_y + play_h:
            reset_game()
        return
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


def keyPressed():
    # Support keyboard shortcuts: 'S' for Save, 'L' for Load
    if key == 's' or key == 'S':
        save_game()
    else:
        if key == 'l' or key == 'L':
            load_game()
