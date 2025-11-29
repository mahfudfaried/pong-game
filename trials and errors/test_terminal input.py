import turtle as t
import random
from pygame import mixer
import sys
import os

# --- FUNGSI MEMBERSIHKAN TERMINAL (Biar Rapi) ---
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_console()
print("="*40)
print("      SETUP GAME PONG (CONSOLE)      ")
print("="*40)

# --- 1. INPUT DARI TERMINAL ---
# Kita gunakan input() standar Python.
# Logika 'or "Default"' artinya kalau kamu langsung Enter (kosong), pakai nama default.

try:
    print("\n[1/4] PENGATURAN NAMA")
    p1_input = input("   > Nama Player A (Kiri)  [Default: Player A]: ")
    p1_name = p1_input if p1_input.strip() != "" else "Player A"

    p2_input = input("   > Nama Player B (Kanan) [Default: Player B]: ")
    p2_name = p2_input if p2_input.strip() != "" else "Player B"

    print("\n[2/4] PENGATURAN SKOR")
    score_input = input("   > Skor Kemenangan (Angka) [Default: 5]: ")
    if score_input.strip() == "":
        max_score = 5
    else:
        max_score = int(score_input)
        if max_score < 1: max_score = 5 # Safety kalau user isi 0/negatif

    print("\n[3/4] PENGATURAN LEVEL")
    print("   Pilihan: (1) Easy, (2) Medium, (3) Hard")
    level_choice = input("   > Masukkan pilihanmu [Default: Medium]: ").lower()

except ValueError:
    print("\n[ERROR] Input salah! Harap masukkan angka untuk skor.")
    print("Menggunakan pengaturan default...")
    max_score = 5
    level_choice = "medium"

print("\n" + "="*40)
print("   PENGATURAN SELESAI! GAME DIMULAI...  ")
print("="*40)


# --- 2. LOGIKA LEVEL ---
# Default variables (Medium)
ball_speed_list = [-0.3, -0.2, 0.2, 0.3]
base_dx = 0.3
paddle_speed = 0.8
level_name = "MEDIUM"

if level_choice == "1" or level_choice == "easy":
    level_name = "EASY"
    ball_speed_list = [-0.2, -0.15, 0.15, 0.2]
    base_dx = 0.2
    paddle_speed = 0.6

elif level_choice == "3" or level_choice == "hard":
    level_name = "HARD"
    ball_speed_list = [-0.5, -0.4, 0.4, 0.5]
    base_dx = 0.5
    paddle_speed = 1.0

# --- 3. SETUP AUDIO ---
mixer.init()
try:
    mixer.music.load(r"../music_background.mp3")
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)
except:
    print("Info: Musik background tidak ditemukan.")

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


# --- 4. SETUP WINDOW (Baru Muncul Sekarang) ---
window = t.Screen()
window.title(f"Pong Game: {p1_name} vs {p2_name} ({level_name} MODE)")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)

canvas = window.getcanvas()
root = canvas.winfo_toplevel()
root.resizable(False, False)

# --- 5. OBJEK GAME ---
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

ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("#acacac")
ball.penup()
ball.goto(0, 0)
ball_dx = base_dx * random.choice([1, -1])
ball_dy = random.choice(ball_speed_list)

pen = t.Turtle()
pen.speed(0)
pen.color("#acacac")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"{p1_name}: 0          {p2_name}: 0", align="center", font=("VT323", 24, "normal"))

game_over_pen = t.Turtle()
game_over_pen.speed(0)
game_over_pen.color("#acacac")
game_over_pen.penup()
game_over_pen.hideturtle()
game_over_pen.goto(0, 0)

# --- KONTROL ---
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

playerA_score = 0
playerB_score = 0
game_on = True

# --- LOOP UTAMA ---
while True:
    try:
        window.update()
    except Exception:
        print("\nWindow ditutup. Terima kasih sudah bermain!")
        mixer.music.stop()
        mixer.quit()
        break

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
        ball_dx = -1 * base_dx
        ball_dy = random.choice(ball_speed_list)

        score_sound.play()
        playerA_score += 1
        pen.clear()
        pen.write(f"{p1_name}: {playerA_score}          {p2_name}: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerA_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write(f"VICTORY!\n{p1_name} Wins!", align="center", font=("Press Start 2P", 18, "bold"))

    # SKOR (KIRI)
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx = 1 * base_dx
        ball_dy = random.choice(ball_speed_list)

        score_sound.play()
        playerB_score += 1
        pen.clear()
        pen.write(f"{p1_name}: {playerA_score}          {p2_name}: {playerB_score}",
                  align="center", font=("VT323", 24, "normal"))

        if playerB_score == max_score:
            game_on = False
            win_sound.play()
            game_over_pen.write(f"VICTORY!\n{p2_name} Wins!", align="center", font=("Press Start 2P", 18, "bold"))

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