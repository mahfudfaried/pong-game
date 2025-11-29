import turtle as t
import random
from pygame import mixer

# --- 1. SETUP AUDIO (MUSIK & SFX) ---
mixer.init()

# A. Background Music
try:
    # Ganti path sesuai lokasi filemu
    mixer.music.load(r"music_background.mp3")
    mixer.music.set_volume(0.5)  # Volume musik background (0.0 - 1.0)
    mixer.music.play(-1)
except Exception as e:
    print(f"Musik tidak ditemukan: {e}")

# B. Sound Effects (SFX)
try:
    # Pastikan file ada di folder yang sama
    bounce_sound = mixer.Sound(r"bounce.mp3")
    score_sound = mixer.Sound(r"score.mp3")
    win_sound = mixer.Sound(r"win.mp3")

    bounce_sound.set_volume(1.0)
    score_sound.set_volume(1.0)
    win_sound.set_volume(1.0)
except Exception as e:
    print(f"File SFX tidak ditemukan ({e}). Game berjalan hening.")


    class DummySound:
        def play(self): pass


    bounce_sound = DummySound()
    score_sound = DummySound()
    win_sound = DummySound()

# --- 2. SETUP GAME ---
playerA_score = 0
playerB_score = 0
max_score = 5
game_on = True

window = t.Screen()
window.title("The Pong Game by E4")
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
leftpaddle.dy = 0

rightpaddle = t.Turtle()
rightpaddle.speed(0)
rightpaddle.shape("square")
rightpaddle.color("#acacac")
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.goto(350, 0)
rightpaddle.dy = 0

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

# --- LOOP UTAMA ---
while True:
    window.update()

    if not game_on:
        continue

    # Gerakan Paddle (Smooth)
    left_next_y = leftpaddle.ycor() + leftpaddle.dy
    if -240 < left_next_y < 250:
        leftpaddle.sety(left_next_y)

    right_next_y = rightpaddle.ycor() + rightpaddle.dy
    if -240 < right_next_y < 250:
        rightpaddle.sety(right_next_y)

    # Gerakan Bola
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # --- LOGIKA PANTULAN DINDING ---
    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1
        bounce_sound.play()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1
        bounce_sound.play()

    # --- LOGIKA SKOR (KANAN) ---
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx = -1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        score_sound.play()
        playerA_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        # LOGIKA MENANG PLAYER A
        if playerA_score == max_score:
            game_on = False
            # mixer.music.stop() <--- BARIS INI SAYA HAPUS/KOMENTAR
            win_sound.play()
            game_over_pen.write("Selamat, Player A menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # --- LOGIKA SKOR (KIRI) ---
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx = 1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        score_sound.play()
        playerB_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        # LOGIKA MENANG PLAYER B
        if playerB_score == max_score:
            game_on = False
            # mixer.music.stop() <--- BARIS INI SAYA HAPUS/KOMENTAR
            win_sound.play()
            game_over_pen.write("Selamat, Player B menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # --- LOGIKA PANTULAN PADDLE ---
    if (340 < ball.xcor() < 350) and \
            (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50):
        ball.setx(340)
        ball_dx *= -1
        bounce_sound.play()

    if (-350 < ball.xcor() < -340) and \
            (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
        ball.setx(-340)
        ball_dx *= -1
        bounce_sound.play()