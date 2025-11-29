import turtle as t

playerA_score = 0
playerB_score = 0

window = t.Screen()
window.title("The Pong Game")
window.bgcolor("green")
window.setup(width=800, height=600)
window.tracer(0)

leftpaddle = t.Turtle()
leftpaddle.speed(0)
leftpaddle.shape("square")
leftpaddle.color("white")
leftpaddle.shapesize(stretch_wid=5, stretch_len=1)
leftpaddle.penup()
leftpaddle.goto(-350, 0)

rightpaddle = t.Turtle()
rightpaddle.speed(0)
rightpaddle.shape("square")
rightpaddle.color("white")
rightpaddle.shapesize(stretch_wid=5, stretch_len=1)
rightpaddle.penup()
rightpaddle.goto(350, 0)

ball = t.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("red")
ball.penup()
ball.goto(0, 0)
ball_dx = 0.25
ball_dy = 0.25

pen = t.Turtle()
pen.speed(0)
pen.color("blue")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0          Player B: 0", align="center", font=("Arial", 24, "normal"))

def leftpaddle_up():
    y = leftpaddle.ycor()
    leftpaddle.sety(y + 40)

def leftpaddle_down():
    y = leftpaddle.ycor()
    leftpaddle.sety(y - 40)

def rightpaddle_up():
    y = rightpaddle.ycor()
    rightpaddle.sety(y + 40)

def rightpaddle_down():
    y = rightpaddle.ycor()
    rightpaddle.sety(y - 40)

window.listen()
window.onkeypress(leftpaddle_up, "w")
window.onkeypress(leftpaddle_down, "s")
window.onkeypress(rightpaddle_up, "Up")
window.onkeypress(rightpaddle_down, "Down")

while True:
    window.update()

    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx *= -1
        playerA_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("Arial", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx *= -1
        playerB_score += 1
        pen.clear()
        pen.write(f"Player A: {playerA_score}          Player B: {playerB_score}",
                  align="center", font=("Arial", 24, "normal"))

    if (340 < ball.xcor() < 350) and \
       (rightpaddle.ycor() - 50 < ball.ycor() < rightpaddle.ycor() + 50):
        ball.setx(340)
        ball_dx *= -1

    if (-350 < ball.xcor() < -340) and \
       (leftpaddle.ycor() - 50 < ball.ycor() < leftpaddle.ycor() + 50):
        ball.setx(-340)
        ball_dx *= -1