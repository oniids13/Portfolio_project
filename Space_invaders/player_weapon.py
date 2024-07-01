from turtle import Turtle

class PlayerWeapon(Turtle):
    def __init__(self, ship_position):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.goto(ship_position)
        self.y_move = 10
        self.move_speed = 1


    def move(self):
            new_y = self.ycor() + self.y_move
            self.sety(new_y)

    def fire(self):
        self.move()

    def reset_position(self,ship_position):
        self.goto(ship_position)

    def is_off_screen(self, screen_height):
        return self.ycor() > screen_height / 2