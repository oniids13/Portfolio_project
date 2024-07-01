from turtle import Turtle


class Ship(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("green")
        self.shapesize(stretch_wid=2, stretch_len=1)
        self.penup()
        self.goto(position)
        print(f"Ship created at position: {position}")

    def left_move(self):
        new_x = self.xcor() - 10
        if new_x - 50 > -300:
            self.goto(new_x, self.ycor())
            print(f"Ship moved left to: ({new_x}, {self.ycor()})")

    def right_move(self):
        new_x = self.xcor() + 10
        if new_x + 50 < 300:
            self.goto(new_x, self.ycor())
            print(f"Ship moved right to: ({new_x}, {self.ycor()})")
