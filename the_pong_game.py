import turtle as t
import random
from pygame import mixer
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import time

# --- 1. GLOBAL AUDIO SETUP ---
mixer.init()


def play_music():
    try:
        mixer.music.load(r"music_background.mp3")
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
    except:
        pass


def load_sfx():
    try:
        bounce = mixer.Sound(r"bounce.mp3")
        score = mixer.Sound(r"score.mp3")
        win = mixer.Sound(r"win.mp3")
        return bounce, score, win
    except:
        class Dummy:
            def play(self): pass

        return Dummy(), Dummy(), Dummy()


bounce_sound, score_sound, win_sound = load_sfx()


# --- 2. GAME LAUNCHER (INPUT MENU) ---
def run_launcher(master_root, is_first_run):
    # [PERBAIKAN DI SINI]
    # Hanya putar musik jika ini adalah pertama kali program dijalankan.
    # Jika user main lagi (restart), lewati baris ini agar musik tidak reset.
    if is_first_run:
        play_music()

    # Default data (if user cancels)
    setup_data = {"p1": "Player A", "p2": "Player B", "score": 5, "level": "medium", "ready": False}

    # --- HELPER FUNCTION: ASK FOR INPUT (ENGLISH) ---
    def ask_player_data(parent_window):
        p1 = simpledialog.askstring("Setup", "Player A Name (Left):", parent=parent_window)
        if p1: setup_data["p1"] = p1

        p2 = simpledialog.askstring("Setup", "Player B Name (Right):", parent=parent_window)
        if p2: setup_data["p2"] = p2

        s = simpledialog.askinteger("Setup", "Winning Score (1-20):", parent=parent_window, minvalue=1, maxvalue=20)
        if s: setup_data["score"] = s

        l = simpledialog.askstring("Setup", "Difficulty Level (easy/medium/hard):", parent=parent_window)
        if l: setup_data["level"] = l

        setup_data["ready"] = True

    # --- BRANCH LOGIC ---
    if not is_first_run:
        # IF RESTART: Skip title screen, ask input directly
        dummy_win = tk.Toplevel(master_root)
        dummy_win.withdraw()
        ask_player_data(dummy_win)
        dummy_win.destroy()
        return setup_data

    else:
        # IF FIRST RUN: Show Title Window
        launcher_win = tk.Toplevel(master_root)
        launcher_win.title("The Pong Game")

        w, h = 400, 300
        ws, hs = launcher_win.winfo_screenwidth(), launcher_win.winfo_screenheight()
        x, y = (ws / 2) - (w / 2), (hs / 2) - (h / 2)
        launcher_win.geometry(f"{w}x{h}+{int(x)}+{int(y)}")
        launcher_win.configure(bg="black")
        launcher_win.resizable(False, False)

        launcher_win.lift()
        launcher_win.attributes('-topmost', True)
        launcher_win.after_idle(launcher_win.attributes, '-topmost', False)
        launcher_win.focus_force()

        lbl_title = tk.Label(launcher_win, text="THE PONG GAME", font=("Press Start 2P", 20, "bold"), bg="black", fg="white")
        lbl_title.pack(pady=(40, 10))

        lbl_sub = tk.Label(launcher_win, text="Developed with love by E4 Group", font=("Press Start 2P", 7), bg="black",
                           fg="#acacac")
        lbl_sub.pack(pady=(0, 40))

        def on_start():
            launcher_win.withdraw()
            ask_player_data(launcher_win)
            launcher_win.destroy()

        btn = tk.Button(launcher_win, text="Start Game", font=("Press Start 2P", 12, "bold"), command=on_start, width=15)
        btn.pack(pady=20)

        def on_close():
            launcher_win.destroy()
            master_root.destroy()
            sys.exit()

        launcher_win.protocol("WM_DELETE_WINDOW", on_close)
        master_root.wait_window(launcher_win)

        return setup_data


# --- 3. LEVEL LOGIC (ENGLISH INPUTS) ---
def get_level_settings(choice):
    # Check input: accepts numbers (1/3) or text (easy/medium/hard)
    c = choice.lower() if choice else "medium"

    if c in ["1", "easy"]:
        return "EASY", [-0.15, -0.1, 0.1, 0.15], 0.15, 0.5

    elif c in ["3", "hard"]:
        return "HARD", [-0.4, -0.3, 0.3, 0.4], 0.35, 0.9

    else:
        # Default to MEDIUM
        return "MEDIUM", [-0.25, -0.2, 0.2, 0.25], 0.25, 0.7


# --- 4. GAME ENGINE ---
def start_game_session(window, config):
    p1_name = config["p1"][:10]
    p2_name = config["p2"][:10]
    max_score = config["score"]
    lvl_name, ball_speeds, base_dx, paddle_spd = get_level_settings(config["level"])

    window.clearscreen()
    window.title(f"Pong: {p1_name} vs {p2_name} (Level: {lvl_name})")
    window.bgcolor("black")
    window.setup(width=800, height=600)
    window.tracer(0)

    canvas = window.getcanvas()
    root = canvas.winfo_toplevel()
    root.resizable(False, False)

    # Game Objects
    leftpaddle = t.Turtle("square")
    leftpaddle.speed(0);
    leftpaddle.color("#acacac");
    leftpaddle.penup()
    leftpaddle.shapesize(5, 1);
    leftpaddle.goto(-350, 0);
    leftpaddle.dy = 0

    rightpaddle = t.Turtle("square")
    rightpaddle.speed(0);
    rightpaddle.color("#acacac");
    rightpaddle.penup()
    rightpaddle.shapesize(5, 1);
    rightpaddle.goto(350, 0);
    rightpaddle.dy = 0

    ball = t.Turtle("circle")
    ball.speed(0);
    ball.color("#acacac");
    ball.penup()
    ball.dx = base_dx * random.choice([1, -1])
    ball.dy = random.choice(ball_speeds)

    pen = t.Turtle()
    pen.speed(0);
    pen.color("#acacac");
    pen.penup();
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write(f"{p1_name}: 0          {p2_name}: 0", align="center", font=("VT323", 24, "normal"))

    game_over_pen = t.Turtle()
    game_over_pen.speed(0);
    game_over_pen.color("#acacac");
    game_over_pen.penup();
    game_over_pen.hideturtle()

    # Keyboard Controls
    def lp_up():
        leftpaddle.dy = paddle_spd

    def lp_down():
        leftpaddle.dy = -paddle_spd

    def lp_stop():
        leftpaddle.dy = 0

    def rp_up():
        rightpaddle.dy = paddle_spd

    def rp_down():
        rightpaddle.dy = -paddle_spd

    def rp_stop():
        rightpaddle.dy = 0

    window.listen()
    window.onkeypress(lp_up, "w");
    window.onkeypress(lp_down, "s");
    window.onkeyrelease(lp_stop, "w");
    window.onkeyrelease(lp_stop, "s")
    window.onkeypress(rp_up, "Up");
    window.onkeypress(rp_down, "Down");
    window.onkeyrelease(rp_stop, "Up");
    window.onkeyrelease(rp_stop, "Down")

    score_a = 0
    score_b = 0
    playing = True
    winner = ""

    # GAME LOOP
    while playing:
        try:
            window.update()
        except:
            return False

            # Movement
        if -240 < leftpaddle.ycor() + leftpaddle.dy < 250: leftpaddle.sety(leftpaddle.ycor() + leftpaddle.dy)
        if -240 < rightpaddle.ycor() + rightpaddle.dy < 250: rightpaddle.sety(rightpaddle.ycor() + rightpaddle.dy)
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Borders
        if ball.ycor() > 290: ball.sety(290); ball.dy *= -1; bounce_sound.play()
        if ball.ycor() < -290: ball.sety(-290); ball.dy *= -1; bounce_sound.play()

        # Scoring
        if ball.xcor() > 390:
            ball.goto(0, 0);
            ball.dx = -base_dx;
            ball.dy = random.choice(ball_speeds)
            score_a += 1;
            score_sound.play();
            pen.clear()
            pen.write(f"{p1_name}: {score_a}          {p2_name}: {score_b}", align="center",
                      font=("VT323", 24, "normal"))
            if score_a >= max_score: winner = p1_name; playing = False

        if ball.xcor() < -390:
            ball.goto(0, 0);
            ball.dx = base_dx;
            ball.dy = random.choice(ball_speeds)
            score_b += 1;
            score_sound.play();
            pen.clear()
            pen.write(f"{p1_name}: {score_a}          {p2_name}: {score_b}", align="center",
                      font=("VT323", 24, "normal"))
            if score_b >= max_score: winner = p2_name; playing = False

        # Collisions
        if (340 < ball.xcor() < 350) and (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50):
            ball.setx(340);
            ball.dx *= -1;
            bounce_sound.play()
        if (-350 < ball.xcor() < -340) and (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
            ball.setx(-340);
            ball.dx *= -1;
            bounce_sound.play()

    # --- GAME OVER (ENGLISH) ---
    ball.hideturtle()  # <--- [BARU] Sembunyikan bola saat game selesai
    win_sound.play()
    game_over_pen.write(f"VICTORY!\n{winner} Wins!", align="center", font=("Press Start 2P", 18, "bold"))

    window.update()
    time.sleep(5)

    retry = messagebox.askyesno("Game Over", f"Congratulations {winner}!\n\nDo you want to play again?")
    return retry


# --- 5. MAIN PROGRAM ---
def main():
    window = t.Screen()
    window.title("Loading...")

    root_tk = window.getcanvas().winfo_toplevel()

    first_run = True

    while True:
        root_tk.withdraw()

        config = run_launcher(root_tk, first_run)

        if not config["ready"]:
            break

        root_tk.deiconify()

        play_again = start_game_session(window, config)

        if not play_again:
            break

        first_run = False

    mixer.quit()
    try:
        window.bye()
    except:
        pass


if __name__ == "__main__":
    main()