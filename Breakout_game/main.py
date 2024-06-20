from turtle import Turtle, Screen
from ball import Ball
from paddle import Paddle
from bricks import Bricks, create_bricks
import time




screen = Screen()
screen.bgcolor("black")
screen.setup(height=600, width=800)
screen.title("Break out game")
screen.tracer(0)

ball = Ball()
paddle = Paddle((0,-270))
bricks = Bricks

# Setting up bricks
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
X_GAP = 10
Y_GAP = 5
screen_width = 800
screen_height = 600
start_x = -screen_width / 2 + BRICK_WIDTH / 2
start_y = screen_height / 2 - BRICK_HEIGHT / 2
cols = int((screen_width - X_GAP) / (BRICK_WIDTH + X_GAP))
rows = int((screen_height / 2 + Y_GAP) / (BRICK_HEIGHT + Y_GAP))
# Creating the bricks
create_bricks(rows,cols, start_x, start_y, BRICK_WIDTH, BRICK_HEIGHT, X_GAP, Y_GAP)


screen.listen()
screen.onkeypress(paddle.left_move, "Left")
screen.onkeypress(paddle.right_move, "Right")


game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    #Collision with the roof
    if ball.ycor() > 280:
        ball.bounce_y()
    #Collision with the side walls
    if ball.xcor() > 380 or ball.xcor() < -380:
        ball.bounce_x()

    #Collision with the floor
    if ball.ycor() < -290:
        ball.reset_position()

    #Collision with the paddle
    if ball.distance(paddle) < 50 and ball.ycor() < -250:
        ball.bounce_y()







screen.exitonclick()