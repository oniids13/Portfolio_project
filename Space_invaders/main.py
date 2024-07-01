import turtle
from ship import Ship
from enemy import create_enemy_grid
from life_board import LifeBoard
from score_board import Scoreboard
from player_weapon import PlayerWeapon
import time

ENEMY_WIDTH = 60
ENEMY_HEIGHT = 20
X_GAP = 20
Y_GAP = 20
screen_width = 600
screen_height = 700
start_x = -screen_width / 2 + ENEMY_WIDTH / 2
start_y = 250 - ENEMY_HEIGHT / 2 - 20
cols = 7
rows = 5



screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(height=700, width=600)
screen.title("Space Invaders")
screen.tracer(0)

enemies = create_enemy_grid(rows, cols, start_x, start_y, ENEMY_WIDTH, ENEMY_HEIGHT, X_GAP, Y_GAP)

for enemy_turtle in enemies:
    enemy_turtle.showturtle()



ship = Ship((0, -320))
scoreboard = Scoreboard()
lifeBoard = LifeBoard()
player_weapon = PlayerWeapon(ship.position())

screen.listen()
screen.onkeypress(ship.left_move, "Left")
screen.onkeypress(ship.right_move, "Right")
screen.onkeypress(player_weapon.fire, "space")

screen.update()

game_is_on = True
last_drop_time = time.time()

while game_is_on:
    for enemy in enemies:
        # Move enemies side-to-side and drop down
        enemy.move_side_to_side()

        # Check if enemy reaches the screen edges and reverse direction if needed
        if enemy.check_edges(screen_width):
            for e in enemies:
                e.move_direction *= -1
            for e in enemies:
                e.drop_down()

    # Move player's weapon if fired
    player_weapon.move()

    # Check for collision between weapon and enemies
    for enemy in enemies:
        if player_weapon.distance(enemy) < 20:  # Adjust distance for collision
            enemy.hideturtle()
            enemies.remove(enemy)
            player_weapon.reset_position(ship.position())
            # Update scoreboard or perform other actions upon successful hit

    if player_weapon.is_off_screen(screen_height):
        player_weapon.reset_position(ship.position())

    screen.update()
    time.sleep(0.05)  # Adjust as needed for smoother gameplay

screen.exitonclick()