import pygame as pg
import random
import sys

pg.init()

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
                    pg.mixer.Sound.play(exit_sound)
                    self.reset()
                    global SCORES
                    SCORES = self.scores
                    main_menu()