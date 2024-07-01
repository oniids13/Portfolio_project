from turtle import Turtle

class LifeBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.lives = 3
        self.update_lifeboard()


    def update_lifeboard(self):
        self.clear()
        self.goto(220, 300)
        self.write(f"Life:{self.lives}", align="center",font=("Courier", 20, "normal"))

    def decrease_life(self):
        self.lives -= 1
        self.update_lifeboard()

    def game_over(self, score):
        self.goto(0, -200)
        self.write(f"Game over!\nFinal Score is: {score}", align="center", font=("Courier", 20, "normal"))