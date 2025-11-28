import turtle as t
import random
from pygame import mixer

# --- 1. SETUP MUSIK ---
mixer.init()
try:
    # Menggunakan path file musikmu
    mixer.music.load(r"music_background.mp3")
    mixer.music.play(-1)
except Exception as e:
    print(f"Musik gagal dimuat: {e}")

# --- 2. VARIABEL GAME ---
playerA_score = 0
playerB_score = 0
max_score = 5     # Batas skor untuk menang
game_on = True    # Saklar utama permainan

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

rightpaddle = t.Turtle()
rightpaddle.speed(0)
rightpaddle.shape("square")
rightpaddle.color("#acacac")
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.goto(350, 0)

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

# --- 3. PENULIS GAME OVER (BARU) ---
# Pen ini khusus untuk nulis siapa yang menang di tengah layar
game_over_pen = t.Turtle()
game_over_pen.speed(0)
game_over_pen.color("#acacac")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# --- FUNGSI GERAK ---
# Ditambah pengecekan 'if game_on:' agar paddle tidak gerak kalau game selesai
def leftpaddle_up():
    if game_on: 
        y = leftpaddle.ycor()
        if y < 250:
            leftpaddle.sety(y + 40)

def leftpaddle_down():
    if game_on:
        y = leftpaddle.ycor()
        if y > -240:
            leftpaddle.sety(y - 40)

def rightpaddle_up():
    if game_on:
        y = rightpaddle.ycor()
        if y < 250:
            rightpaddle.sety(y + 40)

def rightpaddle_down():
    if game_on:
        y = rightpaddle.ycor()
        if y > -240:
            rightpaddle.sety(y - 40)

window.listen()
window.onkeypress(leftpaddle_up, "w")
window.onkeypress(leftpaddle_down, "s")
window.onkeypress(rightpaddle_up, "Up")
window.onkeypress(rightpaddle_down, "Down")

# --- LOOP UTAMA ---
while True:
    window.update()

    # Jika game sudah berakhir (game_on = False), hentikan pergerakan bola
    if not game_on:
        continue 

    # Gerakan Bola
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    # Border checking (Atas/Bawah)
    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1

    # --- SCORE CHECKING & MENENTUKAN PEMENANG ---

    # Jika Player A mencetak gol (Bola ke Kanan)
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx = -1 * random.choice([0.2, 0.25, 0.3]) 
        ball_dy = random.choice(speeds)
        
        playerA_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))
        
        # Cek apakah Player A menang
        if playerA_score == max_score:
            game_on = False
            game_over_pen.write("Selamat, Player A menang!", 
                                align="center", font=("Press Start 2P", 14, "bold"))

    # Jika Player B mencetak gol (Bola ke Kiri)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx = 1 * random.choice([0.2, 0.25, 0.3])
        ball_dy = random.choice(speeds)
        
        playerB_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        # Cek apakah Player B menang
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