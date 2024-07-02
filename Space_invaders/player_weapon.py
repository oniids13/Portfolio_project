from turtle import Turtle

class PlayerWeapon(Turtle):
    def __init__(self, ship_position):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(ship_position)
        self.y_move = 10
        self.move_speed = 1
        self.active = True

    def move(self):
        if self.active:
            new_y = self.ycor() + self.y_move
            self.goto(self.xcor(), new_y)

    def reset_position(self,ship_position):
        self.goto(ship_position)
        self.active = False

    def is_off_screen(self, screen_height):
        return self.ycor() > screen_height / 2