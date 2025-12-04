# The Pong Game
# Developed by E4 Group
import turtle as t # untuk merender grafik game
import random # untuk mengacak arah gerak bola
from pygame import mixer # untuk mengontrol audio
import sys # untuk terminasi
import tkinter as tk # untuk membuat UI konfigurasi awal
from tkinter import messagebox #window pop up
import time # untuk memberi jeda

# Setup Audio
mixer.init()
def play_music(): # memutar musik background
    try:
        mixer.music.load(r"music_background.mp3")
        mixer.music.set_volume(0.5);
        mixer.music.play(-1)
    except:
        pass

# Sound effect
def load_sfx():
    try:
        # Load semua audio
        return (mixer.Sound(f"{name}.mp3") for name in ["bounce", "score", "win"])
    except:
        class Dummy:
            def play(self): pass

        return Dummy(), Dummy(), Dummy()


bounce_sound, score_sound, win_sound = load_sfx()


# Game launcher (konfigurasi awal permainan)
def run_launcher(master_root, is_first_run):
    if is_first_run: play_music()

    setup_data = {"mode": "2p", "p1": "Player 1", "p2": "Player 2", "score": 5, "level": "easy", "ready": False}

    launcher_win = tk.Toplevel(master_root)
    launcher_win.title("The Pong Game")

    # UI Setup
    w, h = 500, 520
    ws, hs = launcher_win.winfo_screenwidth(), launcher_win.winfo_screenheight()
    launcher_win.geometry(f"{w}x{h}+{int((ws - w) / 2)}+{int((hs - h) / 2)}")
    launcher_win.configure(bg="black")
    launcher_win.resizable(False, False)
    launcher_win.lift()
    launcher_win.attributes('-topmost', True)
    launcher_win.after_idle(launcher_win.attributes, '-topmost', False)
    launcher_win.focus_force()

    # Vars
    var_mode = tk.StringVar(value="2p")
    var_p1 = tk.StringVar(value="Player 1")
    var_p2 = tk.StringVar(value="Player 2")
    var_score = tk.StringVar(value="5")
    var_level = tk.StringVar(value="easy")

    # Welcome Screen
    frm_welcome = tk.Frame(launcher_win, bg="black")
    tk.Label(frm_welcome, text="THE PONG GAME", font=("Press Start 2P", 24, "bold"), bg="black", fg="white").pack(
        pady=(100, 10))
    tk.Label(frm_welcome, text="Developed with Love by E4 Group", font=("Press Start 2P", 8), bg="black",
             fg="#acacac").pack(pady=(0, 60))

    def go_to_setup():
        frm_welcome.pack_forget();
        frm_setup.pack(fill="both", expand=True)

    tk.Button(frm_welcome, text="MULAI", font=("Press Start 2P", 12, "bold"), bg="white", fg="black", width=15,
              command=go_to_setup).pack(pady=(100, 0))

    group_names = "©2025 E4 Group\n\nManda | Evan | Rio | Faried"
    tk.Label(frm_welcome, text=group_names, font=("Press Start 2P", 7), bg="black", fg="#555555").pack(pady=(20, 0))

    # Konfigurasi awal permainan
    frm_setup = tk.Frame(launcher_win, bg="black")
    tk.Label(frm_setup, text="PENGATURAN", font=("Press Start 2P", 20, "bold"), bg="black", fg="white").pack(
        pady=(15, 15))

    frm_form = tk.Frame(frm_setup, bg="black");
    frm_form.pack()

    # Selector mode permainan
    tk.Label(frm_form, text="Mode Permainan:", font=("Press Start 2P", 10), bg="black", fg="#acacac", anchor="w").pack(
        fill="x", pady=(5, 5))
    frm_radios_mode = tk.Frame(frm_form, bg="black");
    frm_radios_mode.pack(fill="x")

    def update_p2_name():
        var_p2.set("Bot" if var_mode.get() == "1p" else "Player 2")

    tk.Radiobutton(frm_radios_mode, text="Lawan teman", variable=var_mode, value="2p", command=update_p2_name,
                   font=("Press Start 2P", 10), bg="black", fg="white", selectcolor="#444444", activebackground="black",
                   activeforeground="white").pack(side="left", expand=True)
    tk.Radiobutton(frm_radios_mode, text="Lawan bot", variable=var_mode, value="1p", command=update_p2_name,
                   font=("Press Start 2P", 10), bg="black", fg="white", selectcolor="#444444", activebackground="black",
                   activeforeground="white").pack(side="left", expand=True)

    # Kotak input nama pemain dan skor maksimal
    def create_retro_entry(label_text, variable):
        tk.Label(frm_form, text=label_text, font=("Press Start 2P", 10), bg="black", fg="#acacac", anchor="w").pack(
            fill="x", pady=(10, 0))
        tk.Entry(frm_form, textvariable=variable, font=("Press Start 2P", 10), bg="#222222", fg="white",
                 insertbackground="white", relief="flat").pack(fill="x", ipady=5)

    create_retro_entry("Nama Pemain A (Kiri):", var_p1)
    create_retro_entry("Nama Pemain B atau Bot (Kanan):", var_p2)
    create_retro_entry("Skor Maksimal:", var_score)

    # Selector level game
    tk.Label(frm_form, text="Level:", font=("Press Start 2P", 10), bg="black", fg="#acacac", anchor="w").pack(fill="x",
                                                                                                              pady=(15,
                                                                                                                    5))
    frm_radios = tk.Frame(frm_form, bg="black");
    frm_radios.pack(fill="x")

    tk.Radiobutton(frm_radios, text="Easy", variable=var_level, value="easy", font=("Press Start 2P", 10), bg="black",
                   fg="white", selectcolor="#444444", activebackground="black", activeforeground="white").pack(
        side="left", expand=True)
    tk.Radiobutton(frm_radios, text="Medium", variable=var_level, value="medium", font=("Press Start 2P", 10),
                   bg="black", fg="white", selectcolor="#444444", activebackground="black",
                   activeforeground="white").pack(side="left", expand=True)
    tk.Radiobutton(frm_radios, text="Hard", variable=var_level, value="hard", font=("Press Start 2P", 10), bg="black",
                   fg="white", selectcolor="#444444", activebackground="black", activeforeground="white").pack(
        side="left", expand=True)

    def finish_setup():
        setup_data.update({"mode": var_mode.get(), "p1": var_p1.get() or "Player 1", "p2": var_p2.get() or "Bot",
                           "level": var_level.get()})
        try:
            setup_data["score"] = max(1, int(var_score.get()))
        except:
            setup_data["score"] = 5
        setup_data["ready"] = True;
        launcher_win.destroy()

    tk.Button(frm_setup, text="MAIN SEKARANG", font=("Press Start 2P", 12, "bold"), bg="white", fg="black", width=24,
              command=finish_setup).pack(pady=30)

    # Menampilkan welcome screen
    frm_welcome.pack(fill="both", expand=True) if is_first_run else frm_setup.pack(fill="both", expand=True)

    def on_close():
        launcher_win.destroy(); master_root.destroy(); sys.exit()

    launcher_win.protocol("WM_DELETE_WINDOW", on_close)
    master_root.wait_window(launcher_win)
    return setup_data


# Logika level game
def get_level_settings(c):
    c = c.lower() if c else "medium"
    if c in ["1", "easy", "mudah"]:
        return "Easy", [-0.5, -0.3, 0.3, 0.5], 0.5, 1.0
    elif c in ["3", "hard", "sulit"]:
        return "Hard", [-1.5, -1.0, 1.0, 1.5], 1.5, 3.0
    return "Medium", [-0.9, -0.6, 0.6, 0.9], 0.9, 2.0


# Memulai sesi game
def start_game_session(window, config):
    p1, p2, mode = config["p1"][:10], config["p2"][:10], config["mode"]
    lvl_name, speeds, base_dx, p_spd = get_level_settings(config["level"])

    window.clearscreen();
    window.title(f"Pong: {p1} vs {p2} ({lvl_name})")
    window.bgcolor("black");
    window.setup(width=800, height=600);
    window.tracer(0)
    canvas = window.getcanvas();
    root = canvas.winfo_toplevel();
    root.resizable(False, False)

    # Helper untuk membuat objek turtle
    def create_obj(shape, color, pos):
        obj = t.Turtle(shape);
        obj.speed(0);
        obj.color(color);
        obj.penup()
        if shape == "square": obj.shapesize(5, 1)
        obj.goto(pos);
        obj.dy = 0 if shape == "square" else None
        return obj

    lp = create_obj("square", "#acacac", (-350, 0))
    rp = create_obj("square", "#acacac", (350, 0))
    ball = create_obj("circle", "#acacac", (0, 0))
    ball.dx = base_dx * random.choice([1, -1]);
    ball.dy = random.choice(speeds)

    pen = t.Turtle();
    pen.speed(0);
    pen.color("#acacac");
    pen.penup();
    pen.hideturtle();
    pen.goto(0, 260)
    pen.write(f"{p1}: 0          {p2}: 0", align="center", font=("VT323", 24, "normal"))

    over_pen = t.Turtle();
    over_pen.hideturtle();
    over_pen.color("#acacac")

    # Kontrol
    def set_dy(obj, val):
        obj.dy = val

    window.listen()
    window.onkeypress(lambda: set_dy(lp, p_spd), "w");
    window.onkeypress(lambda: set_dy(lp, -p_spd), "s")
    window.onkeyrelease(lambda: set_dy(lp, 0), "w");
    window.onkeyrelease(lambda: set_dy(lp, 0), "s")

    if mode == "2p":
        window.onkeypress(lambda: set_dy(rp, p_spd), "Up");
        window.onkeypress(lambda: set_dy(rp, -p_spd), "Down")
        window.onkeyrelease(lambda: set_dy(rp, 0), "Up");
        window.onkeyrelease(lambda: set_dy(rp, 0), "Down")

    sc_a, sc_b, playing, winner = 0, 0, True, ""
    # Logika utama game
    while playing:
        try:
            window.update()
        except:
            return False

        # Algoritma bot
        if mode == "1p":
            rp.dy = p_spd if rp.ycor() < ball.ycor() - 20 else (-p_spd if rp.ycor() > ball.ycor() + 20 else 0)

        # Gerak bola dan paddle
        for p in [lp, rp]:
            if -240 < p.ycor() + p.dy < 250: p.sety(p.ycor() + p.dy)
        ball.setx(ball.xcor() + ball.dx);
        ball.sety(ball.ycor() + ball.dy)

        # Cek tumbukan
        if abs(ball.ycor()) > 290:
            ball.sety(290 if ball.ycor() > 0 else -290);
            ball.dy *= -1;
            bounce_sound.play()

        # Skor dan reset
        if abs(ball.xcor()) > 390:
            if ball.xcor() > 0:
                sc_a += 1; winner = p1
            else:
                sc_b += 1; winner = p2

            score_sound.play();
            ball.goto(0, 0);
            ball.dx *= -1;
            ball.dy = random.choice(speeds)
            pen.clear();
            pen.write(f"{p1}: {sc_a}          {p2}: {sc_b}", align="center", font=("VT323", 24, "normal"))
            if max(sc_a, sc_b) >= config['score']: playing = False

        # Area tumbukan
        if (330 < ball.xcor() < 360 and rp.ycor() - 55 < ball.ycor() < rp.ycor() + 55) or \
                (-360 < ball.xcor() < -330 and lp.ycor() - 55 < ball.ycor() < lp.ycor() + 55):
            ball.dx *= -1;
            bounce_sound.play()

    ball.hideturtle();
    win_sound.play()
    over_pen.write(f"MENANG!\n{winner} Juara!", align="center", font=("Press Start 2P", 18, "bold"))
    window.update();
    time.sleep(5)
    return messagebox.askyesno("Permainan Selesai", f"Selamat {winner} Menang!\n\nIngin main lagi?")


# Fungsi utama program
def main():
    win = t.Screen();
    win.title("Memuat...")
    root = win.getcanvas().winfo_toplevel();
    first = True
    while True:
        root.withdraw();
        cfg = run_launcher(root, first)
        if not cfg["ready"]: break
        root.deiconify()
        if not start_game_session(win, cfg): break
        first = False
    mixer.quit()
    try:
        win.bye()
    except:
        pass


if __name__ == "__main__": main()