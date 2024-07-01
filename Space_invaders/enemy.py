from turtle import Turtle

class Enemy(Turtle):
    MOVE_DISTANCE = 5
    DROP_DISTANCE = 20
    DROP_INTERVAL = 8  # in seconds for dropping down

    def __init__(self, position):
        super().__init__()
        self.shape("turtle")
        self.color("green")
        self.shapesize(stretch_wid=2, stretch_len=2)
        self.penup()
        self.goto(position)
        self.move_direction = 1  # Initial movement direction (1 for right, -1 for left)

    def move_side_to_side(self):
        new_x = self.xcor() + self.move_direction * self.MOVE_DISTANCE
        self.setposition(new_x, self.ycor())

    def drop_down(self):
        self.setposition(self.xcor(), self.ycor() - self.DROP_DISTANCE)

    def check_edges(self, screen_width):
        if self.xcor() > screen_width / 2 - 20 or self.xcor() < -screen_width / 2 + 20:  # Adjust boundary
            return True
        return False

def create_enemy_grid(rows, cols, start_x, start_y, enemy_width, enemy_height, x_gap, y_gap):
    enemies = []

    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (enemy_width + x_gap)
            y = start_y - row * (enemy_height + y_gap)
            enemy = Enemy((x, y))
            enemies.append(enemy)

    return enemies
