from turtle import Turtle, Screen
from ball import Ball
import time

screen = Screen()
screen.bgcolor("black")
screen.setup(height=600, width=800)
screen.title("Break out game")
screen.tracer(0)

ball = Ball()



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







screen.exitonclick()