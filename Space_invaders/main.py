import random
import turtle
from ship import Ship
from enemy import create_enemy_grid
from life_board import LifeBoard
from score_board import Scoreboard
from player_weapon import PlayerWeapon
from enemy_weapon import EnemyWeapon
import time


# Constants
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 20
X_GAP = 5
Y_GAP = 20
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
START_X = -SCREEN_WIDTH / 2 + ENEMY_WIDTH / 2
START_Y = 300 - ENEMY_HEIGHT / 2 - 20
# Number of enemies
COLS = 8
ROWS = 6


# Screen Setup
screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(height=SCREEN_HEIGHT, width=SCREEN_WIDTH)
screen.title("Turtle Invaders")
screen.tracer(0)




# Importing modules
ship = Ship((0, -320))
player_weapons = []
enemy_weapons = []
scoreboard = Scoreboard()
lifeBoard = LifeBoard()


screen.listen()
screen.onkeypress(ship.left_move, "Left")
screen.onkeypress(ship.right_move, "Right")

def fire_weapon():
    new_weapon = PlayerWeapon(ship.position())
    player_weapons.append(new_weapon)


screen.onkeypress(fire_weapon, "space")

def fire_enemy_weapon():
    if enemies:
        shooting_enemy = random.choice(enemies)
        new_weapon = EnemyWeapon(shooting_enemy.position())
        enemy_weapons.append(new_weapon)
    if game_is_on:
        screen.ontimer(fire_enemy_weapon, random.randint(1000, 3000))


screen.ontimer(fire_enemy_weapon, random.randint(1000, 3000))

# Movement Settings
MOVE_DISTANCE = 10
DROP_DISTANCE = 20
MOVE_INTERVAL = 500
CYCLE_COUNT = 0
CYCLES_BEFORE_DROP = 2

move_direction = 1

game_is_on = True


def move_enemies_side_to_side():
    global move_direction, CYCLE_COUNT

    if not game_is_on:
        return

    reached_edge = False
    for enemy in enemies:
        new_x = enemy.xcor() + move_direction * MOVE_DISTANCE
        enemy.setposition(new_x, enemy.ycor())

        if new_x + ENEMY_WIDTH / 2 >= SCREEN_WIDTH / 2 or new_x - ENEMY_WIDTH / 2 <= -SCREEN_WIDTH / 2:
            reached_edge = True

    if reached_edge:
        move_direction *= -1
        CYCLE_COUNT += 1

        if CYCLE_COUNT >= CYCLES_BEFORE_DROP:
            drop_enemies_down()
            CYCLE_COUNT = 0

    screen.update()
    screen.ontimer(move_enemies_side_to_side, MOVE_INTERVAL)

def drop_enemies_down():
    global game_is_on
    for enemy in enemies:
        enemy.setposition(enemy.xcor(), enemy.ycor() - DROP_DISTANCE)
        if enemy.ycor() <= -SCREEN_HEIGHT / 2:
            game_is_on = False
            lifeBoard.game_over(scoreboard.score)
            scoreboard.high_score_reset()
            break

def create_enemies():
    global enemies, MOVE_INTERVAL, CYCLE_COUNT
    ship.reset_position()
    enemies = create_enemy_grid(ROWS, COLS, START_X, START_Y, ENEMY_WIDTH, ENEMY_HEIGHT, X_GAP, Y_GAP)
    MOVE_INTERVAL -= 50
    CYCLE_COUNT = 0
    move_enemies_side_to_side()

# Creating enemies
enemies = create_enemy_grid(ROWS, COLS, START_X, START_Y, ENEMY_WIDTH, ENEMY_HEIGHT, X_GAP, Y_GAP)

for enemy_turtle in enemies:
    enemy_turtle.showturtle()

screen.ontimer(move_enemies_side_to_side, MOVE_INTERVAL)

screen.update()



while game_is_on:

    for weapon in player_weapons:
        weapon.move()

    for weapon in enemy_weapons:
        weapon.move()

    for weapon in player_weapons:
        for enemy in enemies:
            if weapon.distance(enemy) < 20:
                enemy.hideturtle()
                enemies.remove(enemy)
                player_weapons.remove(weapon)
                weapon.hideturtle()
                scoreboard.point()
                break

    for weapon in enemy_weapons:
        if weapon.distance(ship) < 20:
            weapon.hideturtle()
            enemy_weapons.remove(weapon)
            lifeBoard.decrease_life()
            if lifeBoard.lives == 0:
                lifeBoard.game_over(scoreboard.score)
                scoreboard.high_score_reset()
                ship.reset_position()
                game_is_on = False
                break

    for weapon in player_weapons:
        if weapon.is_off_screen(SCREEN_HEIGHT):
            player_weapons.remove(weapon)
            weapon.hideturtle()

    for weapon in enemy_weapons:
        if weapon.is_off_screen(SCREEN_HEIGHT):
            enemy_weapons.remove(weapon)
            weapon.hideturtle()

    if not enemies:
        create_enemies()




    screen.update()
    time.sleep(0.05)  # Adjust as needed for smoother gameplay

screen.exitonclick()