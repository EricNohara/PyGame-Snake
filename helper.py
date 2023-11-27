import pygame as pg
import random
from globvars import *

##########################################################################################################################
# HELPER FUNCTION
##########################################################################################################################

def draw_grid(surface):
    for y in range (0, int(GRID_HEIGHT)):
        for x in range (0, int(GRID_WIDTH)):
            # setting up the checkereboard pattern
            if ((x + y) % 2) == 0:
                rect = pg.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))  #create rect with correct position and size
                pg.draw.rect(surface, grey1, rect)                                  #draw the rect with the first grey value
            else:
                rect = pg.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pg.draw.rect(surface, grey2, rect)

def move_snake(snake, food):
    cur = snake.get_head_pos()
    x, y = snake.direction
    new_loc = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)

    # Handling collisions with snake
    if len(snake.positions) > 2 and new_loc in snake.positions[2:]:
        pg.mixer.Sound.play(die)
        snake.reset()
        food.position = random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
    # Handle collisions with the walls
    elif (cur[0] == 0 and snake.direction == LEFT) or (cur[0] == (WIDTH-1*GRID_SIZE) and snake.direction == RIGHT) or (cur[1] == 0 and snake.direction == UP) or (cur[1] == (HEIGHT-1*GRID_SIZE) and snake.direction == DOWN):
        pg.mixer.Sound.play(die)
        snake.reset()
        food.position = random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
    else:
        snake.positions.insert(0, new_loc)
        if len(snake.positions) > snake.length:
            snake.positions.pop()