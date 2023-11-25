import pygame as pg
import sys
import random

pg.init()

class Snake(object):
    #init function like a constructor
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH/2, HEIGHT/2)]      # initial position is middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])     # initial direction is random
        self.color = green

    def get_head_pos(self):
        return self.positions[0]
    
    def turn(self, pt):
        #check if the snake is longer then one and the direction is going towards the new direction
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    def move(self):
        cur = self.get_head_pos()
        x, y = self.direction
        new_loc = (((cur[0] + (x * GRID_SIZE)) % WIDTH), (cur[1] + (y * GRID_SIZE)) % HEIGHT)

        # Handling collisions with self
        if len(self.positions) > 2 and new_loc in self.positions[2:]:
            self.reset()
        # Handle collisions with the walls
        elif (self.positions[0][0] == 0 and self.direction == LEFT) or (self.positions[0][0] == (WIDTH-1*GRID_SIZE) and self.direction == RIGHT) or (self.positions[0][1] == 0 and self.direction == UP) or (self.positions[0][1] == (HEIGHT-1*GRID_SIZE) and self.direction == DOWN):
            self.reset()
        else:
            self.positions.insert(0, new_loc)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH/2, HEIGHT/2)]      # initial position is middle of the screen
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])     # initial direction is random
        score = 0
    
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
                    self.turn(UP)
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.turn(DOWN)
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.turn(LEFT)
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.turn(RIGHT)
            

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

# GAME VARIABLES
SIZE = WIDTH, HEIGHT = 480, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH / GRID_SIZE
GRID_HEIGHT = HEIGHT / GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
font = pg.font.Font('freesansbold.ttf', 30)
# COLORS
grey1 = (120, 120, 120)
grey2 = (140, 140, 140)
green = (140, 255, 117)
black = (0,0,0)
red = (255,0,0)

# MAIN GAME
def main():
    clock = pg.time.Clock()    # create clock to control speed that the game runs
    screen = pg.display.set_mode(SIZE)      # set the screen
    surface = pg.Surface(screen.get_size()) # create a surface to draw on
    surface = surface.convert()

    draw_grid(surface)  # draw the grid onto the surface generated

    snake = Snake()     # create instances of the two classes for the game
    food = Food()

    # Gameplay loop
    score = 0
    while True:
        clock.tick(10)  #set the FPS
        # snake and food subfunctions
        snake.handle_keys()
        draw_grid(surface)
        snake.move()
        if snake.get_head_pos() == food.position:
            snake.length += 1
            score += 1
            food.randomize_pos()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = font.render("Score {0}".format(score), True, black)
        screen.blit(text, (200,20))

        # print(snake.positions)

        pg.display.update()

#call the main function
main()