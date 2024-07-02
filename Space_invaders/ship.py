from turtle import Turtle


class Ship(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("triangle")
        self.color("green")
        self.shapesize(stretch_wid=2, stretch_len=1)
        self.penup()
        self.left(90)
        self.goto(position)


    def left_move(self):
        new_x = self.xcor() - 10
        if new_x - 50 > -400:
            self.goto(new_x, self.ycor())


    def right_move(self):
        new_x = self.xcor() + 10
        if new_x + 50 < 400:
            self.goto(new_x, self.ycor())

    def reset_position(self):
        self.goto(0, -320)

