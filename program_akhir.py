import turtle as t
import random
from pygame import mixer

# --- 1. SETUP MUSIK ---
mixer.init()
try:
    # Menggunakan path file musikmu (pastikan file ada)
    mixer.music.load(r"music_background.mp3")
    mixer.music.play(-1)
except Exception as e:
    print(f"Musik gagal dimuat: {e}")

# --- 2. VARIABEL GAME ---
playerA_score = 0
playerB_score = 0
max_score = 5
game_on = True

# --- SETUP LAYAR ---
window = t.Screen()
window.title("The Pong Game - First to 5 Wins!")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# --- PADDLES ---
leftpaddle = t.Turtle()
leftpaddle.speed(0)
leftpaddle.shape("square")
leftpaddle.color("#acacac")
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-350, 0)
# [BARU] Menambahkan atribut kecepatan awal (dy) pada paddle
leftpaddle.dy = 0

rightpaddle = t.Turtle()
rightpaddle.speed(0)
rightpaddle.shape("square")
rightpaddle.color("#acacac")
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.goto(350, 0)
# [BARU] Menambahkan atribut kecepatan awal (dy) pada paddle
rightpaddle.dy = 0

# [BARU] Variabel kecepatan gerak paddle (bisa diatur)
paddle_speed = 0.8

# --- BOLA ---
ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("#acacac")
ball.penup()
ball.goto(0, 0)

speeds = [-0.35, -0.25, -0.15, 0.15, 0.25, 0.35]
ball_dx = random.choice([0.25, -0.25])
ball_dy = random.choice(speeds)

# --- PENULIS SKOR ---
pen = t.Turtle()
pen.speed(0)
pen.color("#acacac")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0          Player B: 0", align="center", font=("VT323", 24, "normal"))

# --- PENULIS GAME OVER ---
game_over_pen = t.Turtle()
game_over_pen.speed(0)
game_over_pen.color("#acacac")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)


# --- FUNGSI INPUT (BARU) ---
# Fungsi ini hanya mengubah KECEPATAN (dy), bukan posisi
def leftpaddle_up():
    leftpaddle.dy = paddle_speed


def leftpaddle_down():
    leftpaddle.dy = -paddle_speed


def leftpaddle_stop():
    leftpaddle.dy = 0


def rightpaddle_up():
    rightpaddle.dy = paddle_speed


def rightpaddle_down():
    rightpaddle.dy = -paddle_speed


def rightpaddle_stop():
    rightpaddle.dy = 0


# --- BINDING KEYBOARD (BARU) ---
window.listen()
# Saat tombol DITEKAN -> Set kecepatan
window.onkeypress(leftpaddle_up, "w")
window.onkeypress(leftpaddle_down, "s")
window.onkeypress(rightpaddle_up, "Up")
window.onkeypress(rightpaddle_down, "Down")

# Saat tombol DILEPAS -> Set kecepatan jadi 0 (Stop)
window.onkeyrelease(leftpaddle_stop, "w")
window.onkeyrelease(leftpaddle_stop, "s")
window.onkeyrelease(rightpaddle_stop, "Up")
window.onkeyrelease(rightpaddle_stop, "Down")

# --- LOOP UTAMA ---
while True:
    window.update()

    # Jika game selesai, hentikan semua update
    if not game_on:
        continue

        # --- GERAKAN PADDLE (BARU) ---
    # Posisi diupdate setiap frame berdasarkan kecepatan (dy)

    # Paddle Kiri
    left_next_y = leftpaddle.ycor() + leftpaddle.dy
    # Cek batas agar tidak keluar layar (-240 sampai 250)
    if -240 < left_next_y < 250:
        leftpaddle.sety(left_next_y)

    # Paddle Kanan
    right_next_y = rightpaddle.ycor() + rightpaddle.dy
    if -240 < right_next_y < 250:
        rightpaddle.sety(right_next_y)

    # --- GERAKAN BOLA ---
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # Border checking (Atas/Bawah)
    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1

    # --- SCORE CHECKING ---
    # Player A Score
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx = -1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        playerA_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerA_score == max_score:
            game_on = False
            game_over_pen.write("Selamat, Player A menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # Player B Score
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx = 1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        playerB_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerB_score == max_score:
            game_on = False
            game_over_pen.write("Selamat, Player B menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # Paddle collisions
    if (340 < ball.xcor() < 350) and \
            (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50):
        ball.setx(340)
        ball_dx *= -1

    if (-350 < ball.xcor() < -340) and \
            (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
        ball.setx(-340)
        ball_dx *= -1