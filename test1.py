import turtle as t
import random
from pygame import mixer
import sys  # [BARU] Tambahkan ini untuk exit yang bersih

# --- 1. SETUP AUDIO (MUSIK & SFX) ---
mixer.init()

# A. Background Music
try:
    mixer.music.load(r"music_background.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
except Exception as e:
    print(f"Musik tidak ditemukan: {e}")

# B. Sound Effects (SFX)
try:
    bounce_sound = mixer.Sound(r"bounce.mp3")
    score_sound = mixer.Sound(r"score.mp3")
    win_sound = mixer.Sound(r"win.mp3")

    bounce_sound.set_volume(1.0)
    score_sound.set_volume(1.0)
    win_sound.set_volume(1.0)
except Exception as e:
    print(f"File SFX error: {e}")


    class DummySound:
        def play(self): pass


    bounce_sound = DummySound()
    score_sound = DummySound()
    win_sound = DummySound()

# --- 2. SETUP GAME & WINDOW ---
playerA_score = 0
playerB_score = 0
max_score = 5
game_on = True

window = t.Screen()
window.title("The Pong Game by E4")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

# Kunci Ukuran Window (Matikan Maximize)
canvas = window.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(False, False)

# --- [BARU] FUNGSI INPUT NAMA ---
# Kita coba ambil nama. Jika window diclose saat input, program exit aman.
try:
    p1_name = window.textinput("Game Setup", "Masukkan Nama Player A (Kiri):") or "Player A"
    p2_name = window.textinput("Game Setup", "Masukkan Nama Player B (Kanan):") or "Player B"
except:
    # Jika user menutup window saat dimintai nama
    print("Program ditutup saat input nama.")
    sys.exit()

p1_name = p1_name[:10]
p2_name = p2_name[:10]

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
pen.write(f"{p1_name}: 0          {p2_name}: 0", align="center", font=("VT323", 24, "normal"))

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
    # [PERBAIKAN UTAMA DI SINI]
    try:
        window.update()
    except Exception:
        # Jika window ditutup (error update), jalankan ini:
        print("Window ditutup. Mematikan program...")
        mixer.music.stop()  # Matikan musik
        mixer.quit()  # Matikan mixer pygame
        break  # Hentikan loop while True (Program Selesai)

    if not game_on:
        continue

    # Gerakan Paddle
    left_next_y = leftpaddle.ycor() + leftpaddle.dy
    if -240 < left_next_y < 250:
        leftpaddle.sety(left_next_y)

    right_next_y = rightpaddle.ycor() + rightpaddle.dy
    if -240 < right_next_y < 250:
        rightpaddle.sety(right_next_y)

    # Gerakan Bola
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # Pantulan Dinding
    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1
        bounce_sound.play()

    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1
        bounce_sound.play()

    # SKOR (KANAN)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx = -1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        score_sound.play()
        playerA_score += 1
        pen.clear()
        pen.write(f"{p1_name}: {playerA_score}          {p2_name}: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerA_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write(f"Selamat, {p1_name} menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # SKOR (KIRI)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx = 1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)

        score_sound.play()
        playerB_score += 1
        pen.clear()
        pen.write(f"{p1_name}: {playerA_score}          {p2_name}: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerB_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write(f"Selamat, {p2_name} menang!",
                                align="center", font=("Press Start 2P", 14, "bold"))

    # Pantulan Paddle
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