import pygame as pg

pg.init()

##########################################################################################################################
# GAME VARIABLES
##########################################################################################################################

SIZE = WIDTH, HEIGHT = 480, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH / GRID_SIZE
GRID_HEIGHT = HEIGHT / GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
SCORES = [0,0,0]
RANDOM_SETTING = False

DIFFICULTY_SETTING = 10
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

# AUDIO
turn_left = pg.mixer.Sound("assets/Left.mp3")
turn_right = pg.mixer.Sound("assets/Right.mp3")
turn_up = pg.mixer.Sound("assets/Up.mp3")
turn_down = pg.mixer.Sound("assets/Down.mp3")
die = pg.mixer.Sound("assets/Die.mp3")
eat = pg.mixer.Sound("assets/Eat.mp3")
click = pg.mixer.Sound("assets/Click.wav")
ten_point = pg.mixer.Sound("assets/Every-ten.mp3")
fifty_point = pg.mixer.Sound("assets/Every-fifty.mp3")
exit_sound = pg.mixer.Sound("assets/Exit.mp3")