import pygame as pg
import sys
import random
from button import Button
from globvars import *
from helper import *

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
        self.scores = SCORES

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

    def insert_score(self):
        self.scores.append(self.score)
        self.scores.sort()
        self.scores = self.scores[-3:]

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH/2, HEIGHT/2)]      # initial position is middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])     # initial direction is random
        self.insert_score()
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
                    pg.mixer.Sound.play(click)
                    self.reset()
                    global SCORES
                    SCORES = self.scores
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

##########################################################################################################################
# MAIN GAME
##########################################################################################################################

def play():
    pg.display.set_caption("Play")
    clock = pg.time.Clock()    # create clock to control speed that the game runs
    surface = pg.Surface(screen.get_size()).convert() # create a surface to draw on
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
                    pg.mixer.Sound.play(click)
                    main_menu()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    pg.mixer.Sound.play(click)
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

def scoreboard():
    pg.display.set_caption("Score Board")

    while True:
        screen.fill(grey1)

        SCORE_MOUSE_POS = pg.mouse.get_pos()

        SCOREBOARD_TEXT = menu_font.render("SCOREBOARD", True, black)
        SCOREBOARD_RECT = SCOREBOARD_TEXT.get_rect(center=(WIDTH/2, 60))
        SCORE_ONE = font.render("1. {0}".format(SCORES[2]), True, black)
        SCORE_ONE_RECT = SCORE_ONE.get_rect(center=(WIDTH/2, HEIGHT/2-70))
        SCORE_TWO = font.render("2. {0}".format(SCORES[1]), True, black)
        SCORE_TWO_RECT = SCORE_ONE.get_rect(center=(WIDTH/2, HEIGHT/2))
        SCORE_THREE = font.render("3. {0}".format(SCORES[0]), True, black)
        SCORE_THREE_RECT = SCORE_ONE.get_rect(center=(WIDTH/2, HEIGHT/2+70))

        for (text, rect) in [(SCOREBOARD_TEXT, SCOREBOARD_RECT),(SCORE_ONE, SCORE_ONE_RECT),(SCORE_TWO, SCORE_TWO_RECT),(SCORE_THREE, SCORE_THREE_RECT)]:
            screen.blit(text, rect)

        BACK_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2 + 175), 
                            text_input="BACK", font=font, base_color=grey2, hovering_color=white)
        
        BACK_BUTTON.changeColor(SCORE_MOUSE_POS)
        BACK_BUTTON.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SCORE_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    main_menu()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.Sound.play(click)
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
        SCORE_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2+70), text_input="SCORES", font=font, base_color=grey2, hovering_color=white)
        QUIT_BUTTON = Button(image=pg.image.load("assets/Btn-Rect2.png"), pos=(WIDTH/2, HEIGHT/2+140), 
                            text_input="QUIT", font=font, base_color=grey2, hovering_color=white)
        
        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SCORE_BUTTON, QUIT_BUTTON]:
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
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    scoreboard()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.mixer.Sound.play(click)
                    pg.quit()
                    sys.exit()

        pg.display.update()

#call the main function
main_menu()