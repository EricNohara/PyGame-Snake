import pygame as pg

pg.init()

SIZE = WIDTH, HEIGHT = 480, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH / GRID_SIZE
GRID_HEIGHT = HEIGHT / GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

font = pg.font.Font('freesansbold.ttf', 30)
menu_font = pg.font.Font('freesansbold.ttf', 60)
screen = pg.display.set_mode(SIZE)      # set the screen

# COLORS
grey1 = (120, 120, 120)
grey2 = (140, 140, 140)
green = (140, 255, 117)
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)