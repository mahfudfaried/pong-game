import turtle as t
import random
from pygame import mixer

# --- 1. SETUP AUDIO ---
mixer.init()
try:
    mixer.music.load(r"../music_background.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
except:
    pass

try:
    bounce_sound = mixer.Sound(r"../bounce.mp3")
    score_sound = mixer.Sound(r"../score.mp3")
    win_sound = mixer.Sound(r"../win.mp3")
    bounce_sound.set_volume(1.0)
    score_sound.set_volume(1.0)
    win_sound.set_volume(1.0)
except:
    class DummySound:
        def play(self): pass


    bounce_sound = DummySound()
    score_sound = DummySound()
    win_sound = DummySound()

# --- 2. SETUP VARIABEL & WINDOW ---
playerA_score = 0
playerB_score = 0
max_score = 5
game_on = True

window = t.Screen()
window.title("The Pong Game - Final Responsive Fix")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Aktifkan Resize
canvas = window.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(True, True)
root.minsize(600, 400)

# --- PADDLES ---
leftpaddle = t.Turtle()
leftpaddle.speed(0)
leftpaddle.shape("square")
leftpaddle.color("#acacac")
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.dy = 0

rightpaddle = t.Turtle()
rightpaddle.speed(0)
rightpaddle.shape("square")
rightpaddle.color("#acacac")
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.dy = 0

paddle_speed = 1.2

# --- BOLA ---
ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("#acacac")
ball.penup()
ball.goto(0, 0)
ball_dx = 0.4
ball_dy = 0.4

# --- PENULIS SKOR ---
pen = t.Turtle()
pen.speed(0)
pen.color("#acacac")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0          Player B: 0", align="center", font=("VT323", 24, "normal"))

game_over_pen = t.Turtle()
game_over_pen.speed(0)
game_over_pen.color("#acacac")
game_over_pen.penup()
game_over_pen.hideturtle()


# --- FUNGSI INPUT ---
def leftpaddle_up(): leftpaddle.dy = paddle_speed


def leftpaddle_down(): leftpaddle.dy = -paddle_speed


def leftpaddle_stop(): leftpaddle.dy = 0


def rightpaddle_up(): rightpaddle.dy = paddle_speed


def rightpaddle_down(): rightpaddle.dy = -paddle_speed


def rightpaddle_stop(): rightpaddle.dy = 0


window.listen()
window.onkeypress(leftpaddle_up, "w")
window.onkeypress(leftpaddle_down, "s")
window.onkeypress(rightpaddle_up, "Up")
window.onkeypress(rightpaddle_down, "Down")
window.onkeyrelease(leftpaddle_stop, "w")
window.onkeyrelease(leftpaddle_stop, "s")
window.onkeyrelease(rightpaddle_stop, "Up")
window.onkeyrelease(rightpaddle_stop, "Down")

# Variabel pelacak ukuran layar
last_win_width = window.window_width()
last_win_height = window.window_height()


# Fungsi KHUSUS UI (Hanya Skor)
def update_score_position(h):
    pen.clear()
    pen.goto(0, (h / 2) - 40)
    pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
              align="center", font=("VT323", 24, "normal"))


# Panggil sekali di awal
update_score_position(last_win_height)

# --- LOOP UTAMA ---
while True:
    window.update()

    # Ambil ukuran layar saat ini
    current_w = window.window_width()
    current_h = window.window_height()
    w_half = current_w / 2
    h_half = current_h / 2

    # --- PERBAIKAN: Update Posisi Paddle SETIAP FRAME ---
    # Ini memastikan paddle selalu "menempel" di pinggir, mau di-resize secepat apapun
    leftpaddle.setx(-(w_half - 50))
    rightpaddle.setx(w_half - 50)

    # --- Optimasi Skor ---
    # Update posisi teks skor HANYA jika ukuran layar berubah (biar gak berat)
    if current_w != last_win_width or current_h != last_win_height:
        last_win_width = current_w
        last_win_height = current_h
        update_score_position(current_h)

    if not game_on:
        continue

    # --- GERAKAN PADDLE (Y-Axis) ---
    left_next_y = leftpaddle.ycor() + leftpaddle.dy
    if -(h_half - 60) < left_next_y < (h_half - 60):
        leftpaddle.sety(left_next_y)

    right_next_y = rightpaddle.ycor() + rightpaddle.dy
    if -(h_half - 60) < right_next_y < (h_half - 60):
        rightpaddle.sety(right_next_y)

    # --- GERAKAN BOLA ---
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # Pantulan Dinding
    if ball.ycor() > (h_half - 10):
        ball.sety(h_half - 10)
        ball_dy *= -1
        bounce_sound.play()

    if ball.ycor() < -(h_half - 10):
        ball.sety(-(h_half - 10))
        ball_dy *= -1
        bounce_sound.play()

    # --- SKOR / GOL ---
    if ball.xcor() > (w_half - 10):  # Gol Kanan
        ball.goto(0, 0)
        ball_dx = -1 * random.choice([0.3, 0.4, 0.5])
        ball_dy = random.choice([-0.4, 0.4])
        score_sound.play()

        playerA_score += 1
        # Update skor visual
        pen.clear()
        pen.goto(0, (h_half - 40))
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerA_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write("Selamat, Player A menang!", align="center", font=("Press Start 2P", 14, "bold"))

    if ball.xcor() < -(w_half - 10):  # Gol Kiri
        ball.goto(0, 0)
        ball_dx = 1 * random.choice([0.3, 0.4, 0.5])
        ball_dy = random.choice([-0.4, 0.4])
        score_sound.play()

        playerB_score += 1
        # Update skor visual
        pen.clear()
        pen.goto(0, (h_half - 40))
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerB_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write("Selamat, Player B menang!", align="center", font=("Press Start 2P", 14, "bold"))

    # --- TABRAKAN PADDLE ---
    if (ball.xcor() > rightpaddle.xcor() - 20) and (ball.xcor() < rightpaddle.xcor() + 20) and \
            (ball.ycor() < rightpaddle.ycor() + 60) and (ball.ycor() > rightpaddle.ycor() - 60):
        ball.setx(rightpaddle.xcor() - 20)
        ball_dx *= -1.05
        bounce_sound.play()

    if (ball.xcor() < leftpaddle.xcor() + 20) and (ball.xcor() > leftpaddle.xcor() - 20) and \
            (ball.ycor() < leftpaddle.ycor() + 60) and (ball.ycor() > leftpaddle.ycor() - 60):
        ball.setx(leftpaddle.xcor() + 20)
        ball_dx *= -1.05
        bounce_sound.play()