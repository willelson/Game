import pygame
import math
import random
import time

class particle():
    def __init__(self):
        self.size = 20
        self.x = 320
        self.y = 240
        self.angle = 0
        self.speed = 0

    def move(self):
        self.x += self.speed*math.cos(self.angle)
        self.y += self.speed*math.sin(self.angle)

    def rightBounce(self):
        if self.x > width - self.size:
            self.angle = math.pi - self.angle
            self.x -= (self.x - width) + self.size

    def leftBounce(self):
        if self.x < self.size:
            self.angle = math.pi - self.angle
            self.x = self.size

    def bottomBounce(self):
        if self.y > height - self.size:
            self.y = height - (self.size + 2)
            self.angle = -self.angle

    def topBounce(self):
        if self.y < self.size:
            self.y = (self.size + 2)
            self.angle = -self.angle
            
    def draw(self):
        pygame.draw.circle(screen, (0,0,255), (int(self.x), int(self.y)),
                           self.size, 2 )


class block():
    def __init__(self, x, y, width, height, colour = (255,0,0)):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def draw(self):
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))

    def moveRight(self):
        if self.x < width - self.width:
            self.x += 10

    def moveLeft(self):
        if self.x > 5:
            self.x -= 10

def collision(bar, ball):
    y_collision = False
    x_collision = False
    if ball.x > bar.x and ball.x < bar.x + bar.width:
        x_collision = True
    if ball.y < bar.y + bar.height + ball.size:
        y_collision = True
    if y_collision == True and x_collision == True:
        ball.speed += 1
        ball.y = (ball.size + bar.height + 2)
        ball.angle = -ball.angle
        return True
    

if __name__ == '__main__':
    """Initialise boolean variables, objects and pygame window"""
    background_colour = (255,255,255)
    (width, height) = (640, 480)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Messing around')
    screen.fill(background_colour)
    clock = pygame.time.Clock()

    bar = block(40, 0, 80, 15) 

    ball = particle()
    ball.angle = random.uniform(0.1*math.pi, 0.9*math.pi)
    ball.speed = 12
    gameOver = False
    left = False
    right = False
    lives = 3
    pygame.init()
    myfont = pygame.font.SysFont("monospace", 22)
    menuFont = pygame.font.SysFont("comicsans", 64)
    state = "Play"
    play = "Play"
    quit = "Quit"
    topMenu = {play:170, quit:270}
    menuList = []

    for text in sorted(topMenu.keys()): 
        menuList.append(text)
    selected = play

    upDown = None
    gameOver = False
    i = 0
    score = 0

    """Main game loop"""
    running = True
    while running:
        clock.tick(30)
        screen.fill(background_colour)
        life = "lives remaining: " + str(lives)
        label = myfont.render(life, 1, (0,0,0))
        screen.blit(label, (15, 450))
        points = "score: " + str(score)
        label2 = myfont.render(points, 1, (0,0,0))
        screen.blit(label2, (500, 450))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN or left == True:
                if event.key == pygame.K_LEFT:
                    left = True
                elif event.key == pygame.K_RIGHT or right == True:
                    right = True
                elif event.key == pygame.K_p:
                    state = "Paused"
                if event.key == pygame.K_DOWN:
                    upDown = 'down'
                elif event.key == pygame.K_UP:
                    upDown = 'up'
                if event.key == pygame.K_RETURN:
                    if selected == quit:
                        pygame.quit()
                    elif selected == play:
                        state = "Play"
                        gameOver = False
                
            if event.type == pygame.KEYUP:
                right = False
                left = False
                upDown = None
                

        if state == "Play":
            if collision(bar, ball):
                score += ball.speed - 9
            if right == True:
                bar.moveRight()
            elif left == True:
                bar.moveLeft()
            ball.leftBounce()
            ball.bottomBounce()
            ball.rightBounce()
            ball.move()

            ball.draw()
            bar.draw()

            if ball.y < 0:
                lives -= 1
                ball.angle = random.uniform(0.1*math.pi, 0.9*math.pi)
                ball.speed = 8
                ball.x = 320
                ball.y = 240
            
            pygame.display.flip()

        elif state == "Paused":
            ball.draw()
            bar.draw()
            if upDown == 'down':
                try:
                    i += 1
                    selected = menuList[i]
                except:
                    i = 1
            elif upDown == 'up':
                i -= 1
                if i < 0:
                    i = 0
                selected = menuList[i]

            for text, y_pos in topMenu.items():
                if text == selected:
                    label = menuFont.render(text, 1, (0,255,0))
                else:
                    label = menuFont.render(text, 1, (0,0,0))
                screen.blit(label, (270, y_pos))

            if gameOver:
                over = menuFont.render("Game Over", 1, (0,0,0))
                scoreTxt = "You scored: " + str(lastScore)
                scr = myfont.render(scoreTxt, 1, (50,50,50))
                screen.blit(over, (200, 45))
                screen.blit(scr, (240, 90))
            
            pygame.display.flip()

        if lives == 0:
            gameOver = True
            lives = 3
            state = "Paused"
            lastScore = score
            score = 0
            bar.x = 320 - 0.5*bar.width
               
    pygame.quit()


