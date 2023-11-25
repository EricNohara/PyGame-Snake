import pygame as pg
import sys
import random
from button import Button

pg.init()

##########################################################################################################################
# CLASSES
##########################################################################################################################

class Snake(object):
    #init function like a constructor
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH/2, HEIGHT/2)]      # initial position is middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])     # initial direction is random
        self.color = green
        self.score = 0

    def get_head_pos(self):
        return self.positions[0]
    
    def increase_score(self):
        self.score += 1
    
    def turn(self, pt):
        #check if the snake is longer then one and the direction is going towards the new direction
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH/2, HEIGHT/2)]      # initial position is middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])     # initial direction is random
        self.score = 0
    
    def draw(self, surface):
        for pos in self.positions:
            rect = pg.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, self.color, rect)
            pg.draw.rect(surface, black, rect, 1)       #defining the outline (last arg is width)

    def handle_keys(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()  #closing the program
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    pg.mixer.Sound.play(turn_up)
                    self.turn(UP)
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    pg.mixer.Sound.play(turn_down)
                    self.turn(DOWN)
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    pg.mixer.Sound.play(turn_left)
                    self.turn(LEFT)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    pg.mixer.Sound.play(turn_right)
                    self.turn(RIGHT)
                elif event.key == pg.K_ESCAPE:
                    pg.mixer.Sound.play(exit_sound)
                    main_menu()
            
class Food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = red
        self.randomize_pos()

    def randomize_pos(self):
        self.position = random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE
        
    def draw(self, surface):
        rect = pg.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.color, rect)
        pg.draw.rect(surface, black, rect, 1)       #defining the outline (last arg is width)

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
difficulty_setting = 10
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


##########################################################################################################################
# HELPER FUNCTION
##########################################################################################################################

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

##########################################################################################################################
# MAIN GAME
##########################################################################################################################

def play():
    pg.display.set_caption("Play")
    clock = pg.time.Clock()    # create clock to control speed that the game runs
    surface = pg.Surface(screen.get_size()) # create a surface to draw on
    surface = surface.convert()
    screen.fill(black)

    draw_grid(surface)  # draw the grid onto the surface generated

    snake = Snake()     # create instances of the two classes for the game
    food = Food()

    food_eaten = False

    # Gameplay loop
    while True:
        clock.tick(difficulty_setting)  #set the FPS
        # snake and food subfunctions
        snake.handle_keys()
        draw_grid(surface)
        move_snake(snake, food)
        if snake.get_head_pos() == food.position:
            food_eaten = True
            pg.mixer.Sound.play(eat)
            snake.length += 1
            snake.increase_score()
            food.randomize_pos()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = font.render("Score {0}".format(snake.score), True, black)
        screen.blit(text, (200,20))

        if food_eaten and snake.score > 0:
            if snake.score % 10 == 0 and snake.score % 50 != 0:
                food_eaten = False
                pg.mixer.Sound.play(ten_point)
            if snake.score % 50 == 0:
                food_eaten = False
                pg.mixer.Sound.play(fifty_point)

        pg.display.update()

def options():
    global difficulty_setting

    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()

        screen.fill(grey1)

        OPTIONS_TEXT = menu_font.render("OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, 60))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(WIDTH/2, HEIGHT-60), 
                            text_input="BACK", font=font, base_color="Black", hovering_color=white)
        EASY_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2 - 70), 
                            text_input="EASY", font=font, base_color=grey2, hovering_color=white)
        MEDIUM_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2), 
                            text_input="MEDIUM", font=font, base_color=grey2, hovering_color=white)
        HARD_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2+70), 
                            text_input="HARD", font=font, base_color=grey2, hovering_color=white)
        
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.Sound.play(exit_sound)
                    main_menu()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    pg.mixer.Sound.play(exit_sound)
                    main_menu()
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    difficulty_setting = 6
                    main_menu()
                if MEDIUM_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    difficulty_setting = 10
                    main_menu()
                if HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    difficulty_setting = 14
                    main_menu()

        pg.display.update()

def main_menu():
    pg.display.set_caption("Main Menu")

    while True:
        screen.fill(grey1)

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = menu_font.render("MAIN MENU", True, black)
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, 60))

        PLAY_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2 - 70), 
                            text_input="PLAY", font=font, base_color=grey2, hovering_color=white)
        OPTIONS_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2), 
                            text_input="OPTIONS", font=font, base_color=grey2, hovering_color=white)
        QUIT_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2+70), 
                            text_input="QUIT", font=font, base_color=grey2, hovering_color=white)
        
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    pg.quit()
                    sys.exit()

        pg.display.update()

#call the main function
main_menu()