from turtle import Turtle

class Enemy(Turtle):
    def __init__(self, position):
        super().__init__()
        self.shape("turtle")
        self.color("green")
        self.shapesize(stretch_wid=1, stretch_len=1)
        self.penup()
        self.goto(position)
        self.right(90)
        self.move_direction = 1  # Initial movement direction (1 for right, -1 for left)

def create_enemy_grid(rows, cols, start_x, start_y, enemy_width, enemy_height, x_gap, y_gap):
    enemies = []

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (enemy_width + x_gap)
            y = start_y - row * (enemy_height + y_gap)
            enemy = Enemy((x, y))
            enemies.append(enemy)

    return enemies
