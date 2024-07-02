from turtle import Turtle

class EnemyWeapon(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.penup()
        self.goto(position)
        self.y_move = -10

    def move(self):
        new_y = self.ycor() + self.y_move
        self.goto(self.xcor(), new_y)

    def is_off_screen(self, screen_height):
        return self.ycor() < -screen_height /2
