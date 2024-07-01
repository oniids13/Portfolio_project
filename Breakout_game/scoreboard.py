from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        with open("data.txt") as file:
            self.high_score = int(file.read())
        self.update_scoreboard()



    def update_scoreboard(self):
        self.clear()
        self.goto(-220, 200)
        self.write(f"High Score: {self.high_score}\nScore: {self.score}", align="center", font=("Courier", 30, "normal"))


    def point(self):
        self.score +=1
        self.update_scoreboard()


    def high_score_reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("data.txt", mode="w") as file:
                file.write(f"{self.high_score}")
        self.score = 0
        self.update_scoreboard()

