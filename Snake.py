from random import randint
import pygame
import time

class block():
    def __init__(self, direction, x = 30, y = 120, colour = (0,0,255)):
        self.directions = [direction]
        self.init_dir = direction
        self.size = 30
        self.colour = colour
        self.x = x
        self.y = y

    def move(self, direction):
        """Method move the block in specified direction"""
        if direction == "right":
            self.x += self.size

        elif direction == "left":
            self.x -= self.size

        elif direction == "down":
            self.y += self.size

        elif direction == "up":
            self.y -= self.size
            
        else:
            pass

    def draw(self):
        """Method to draw the block"""
        pygame.draw.rect(screen, self.colour,
                         (self.x, self.y, self.size, self.size))    

class snake():
    def __init__(self):
        self.items = []
        self.length = len(self.items)
    
    def add(self, block):
        """Method to add a block to the snake"""
        self.items.append(block)
        self.length = len(self.items)
        if len(self.items) > 1:
            block.directions = block.directions + self.items[self.length-2].directions 

    def move(self, direction):
        """Method to move all blocks in the snake"""
        for block in self.items:
            block.directions.append(direction)
            block.move(block.directions[0])
            block.directions.remove(block.directions[0])

    def tail_coords(self):
        """Method to return tail coords for adding new block"""
        x = self.items[-1].x
        y = self.items[-1].y       
        return x, y

    def tail_dir(self):
        """Method to return tail direction for adding new block"""
        return self.items[-1].directions[-1]

    def draw(self):
        """Method to draw all block in the snake"""
        for block in self.items:
            block.draw()

    def boundary(self):
        """Method to check if the snake leaves the game window"""
        crossed = False
        if self.items[0].x < 0 or self.items[0].x >= width:
            crossed = True
        elif self.items[0].y < 0 or self.items[0].y >= height:
            crossed = True
        return crossed

    def suicide(self):
        """Method to check if the snake eats itself"""
        if self.length > 3:
            death = False
            for block in self.items[2:]:
                if self.items[0].x == block.x and self.items[0].y == block.y:
                    death = True
            return death

    def flash(self, freq):
        """Flash animation for snakes death"""
        original = self.items[0].colour
        for block in self.items:
            block.colour = (255,255,255)
        self.draw()
        pygame.display.flip()
        time.sleep(freq)
        for block in self.items:
            block.colour = original
        self.draw()
        pygame.display.flip()
        time.sleep(freq)
            
            
def random_direction():
    """Return a random direction"""
    dirs = {0:"up", 1:"down", 2:"left", 3:"right"}
    num = randint(0, 3)
    return dirs[num]

def random_pos():
    """Return a random position in the game window that's
       multiple of snake.size"""
    size = 30
    x_limit = (width-size)/size
    y_limit = (height-size)/size
    x_pos = randint(0, x_limit)
    y_pos = randint(0, y_limit)

    x_pos *= size
    y_pos *= size
    return x_pos, y_pos

def food_pos(snake):
    """Return position for food that isnt on the snake"""
    while 1:
        unique = True
        x, y = random_pos()
        for block in snake.items:
            if block.x == x and block.y == y:
                unique = False
        if unique:
            break            
    return x, y

def random_start(snake):
    """Return x, y coords & a direction for """
    size = 30
    while 1:
        x, y = random_pos()
        if x > size and x < width-size:
            if y < size and y < height-size:
                direction = random_direction()
                break
    return direction, x, y
    

        
if __name__ == "__main__":
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 22)
    menuFont = pygame.font.SysFont("comicsans", 64)
    clock = pygame.time.Clock()
    (width, height) = (630, 480)
    background_colour = (255,255,255)
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_colour)
    pygame.display.set_caption("Snake")
    
    snake = snake()
    head = block(random_start(snake))
    snake.items.append(head)
    
    direction = None #head.init_dir[0]
    final_dir = direction

    counter = 0
    gameover = False

    food_x, food_y = food_pos(snake)
    food = block(None, food_x, food_y, colour = (255,0,0))
            
    running = True
    while running:
        clock.tick(30)
        counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and final_dir != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and final_dir != "left":
                    direction = "right"
                elif event.key == pygame.K_DOWN and final_dir != "up":
                    direction = "down"
                elif event.key == pygame.K_UP and final_dir != "down":
                    direction = "up"
                elif event.key == pygame.K_ESCAPE and gameover == True:
                    running = False

        if gameover == False:
            if snake.items[0].x == food.x and snake.items[0].y == food.y:
                screen.fill(background_colour)
               
                food_x, food_y = food_pos(snake)
                food = block(None, food_x, food_y, colour = (255,0,0))
                food.draw()

                new_x, new_y = snake.tail_coords()
                newBlock = block(snake.tail_dir, new_x, new_y)
                snake.add(newBlock)
                                
                counter = 0
                snake.move(direction)
                snake.draw()

            elif counter % 5 == 0:
                final_dir = direction
                screen.fill(background_colour)
                snake.move(direction)
                snake.draw()
                food.draw()
                counter = 0             
            
            if snake.boundary() or snake.suicide():
                for i in range(5):
                    snake.flash(0.25)
                print snake.length
                gameover = True
                  
            

        if gameover:
            over = menuFont.render("Game Over", 1, (0,0,0))
            scoreTxt = "You scored: " + str(snake.length)
            scr = myfont.render(scoreTxt, 1, (50,50,50))
            screen.blit(over, (200, 45))
            screen.blit(scr, (240, 90))
            pygame.display.flip()
            time.sleep(2)
            screen.fill(background_colour)

            esc = menuFont.render("Press escape to quit", 1, (0,0,0))
            screen.blit(esc, (120, 220))
            
                     
        pygame.display.flip()
        
    pygame.quit()

