from turtle import Turtle
import random



class Bricks(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color(self.random_color())
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.goto(position)

    def random_color(self):
        colors = ["red","blue", "green", "yellow", "orange", "purple", "pink", "brown"]
        return random.choice(colors)

    def destroy(self):
        self.hideturtle()



def create_bricks(rows, cols,start_x, start_y, brick_width, brick_height, x_gap, y_gap):
    bricks = []
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (brick_width + x_gap)
            y = start_y - row * (brick_height + y_gap)
            brick = Bricks((x, y))
            bricks.append(brick)
    return bricks
