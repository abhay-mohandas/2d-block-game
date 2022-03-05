import pygame
import random
import sys
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()
window =pygame.display.set_mode()
pygame.mouse.set_visible(False)
pygame.display.set_caption('Escape')
width,height = window.get_size()
window = pygame.display.set_mode((width,height),FULLSCREEN)
TEXTCOLOR = (0, 200, 255)
BLACK = (0, 0, 0)
WHITE = (255,255,255)
Speedup = 0
FPS = 60
Level=1
min_obstacle_size = 15
max_obstacle_size = 40
min_obstacle_speed = 1
max_obstacle_speed = 4
new_obstacle_rate = 18
player_speed = 5
developer_mode = False

def terminate():
    pygame.quit()
    sys.exit()

def keypress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_SPACE:
                    return

def collision(player_rect, obstacle):
    for b in obstacle:
        if player_rect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

fontlarge = pygame.font.SysFont(None, 80)
font = pygame.font.SysFont(None, 60)
fontsmall = pygame.font.SysFont(None, 40)
player_image = pygame.image.load('2d-block-game/player.png')
player_rect = player_image.get_rect()
obstacle_image = pygame.image.load('2d-block-game/obstacle.png')
for n in range(100):
    locations = (random.randint(0,width),random.randint(0,height))
    for x in range(1):
        pygame.draw.circle(window,WHITE, locations, 1)
drawText('Escape!', fontlarge, window, 42*(width /100), 42*(height/100))
drawText('Press SPACE to start.', fontsmall, window, 39*(width /100) ,50*(height / 100))
pygame.display.update()
keypress()
topScore = 0
while True:
    Lives = 3
    obstacle = []
    score = 0
    Loop = True
    player_rect.topleft = (width / 2, height - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    add_obsticle = 0
    while True:
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                elif event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                elif event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                elif event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                elif event.key == K_TAB:
                    if developer_mode:
                        developer_mode = False
                    else:
                        developer_mode = True
                elif event.key == K_SPACE:
                    drawText('PAUSED', font, window, (43*(width /100) ), 42*(height /100))
                    drawText('Press SPACE to play again.', fontsmall, window, 36*(width /100) ,48*(height / 100))
                    pygame.display.update()
                    keypress()
                    moveLeft = moveRight = moveUp = moveDown = False
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == ord('a'):
                    moveLeft = False
                elif event.key == ord('d'):
                    moveRight = False
                elif event.key == ord('w'):
                    moveUp = False
                elif event.key == ord('s'):
                    moveDown = False
        add_obsticle += 1
        if add_obsticle == new_obstacle_rate:
            add_obsticle = 0
            obstacleize = random.randint(min_obstacle_size, max_obstacle_size)
            new_obstacle = {'rect': pygame.Rect(random.randint(0, width-obstacleize), 0 - obstacleize, obstacleize, obstacleize),
                        'speed': random.randint(min_obstacle_speed, max_obstacle_speed),
                        'surface':pygame.transform.scale(obstacle_image, (obstacleize, obstacleize)),
                        }
            obstacle.append(new_obstacle)
        if moveLeft and player_rect.left > 0:
            player_rect.move_ip(-1 * player_speed, 0)
        if moveRight and player_rect.right < width:
            player_rect.move_ip(player_speed, 0)
        if moveUp and player_rect.top > 0:
            player_rect.move_ip(0, -1 * player_speed)
        if moveDown and player_rect.bottom < height:
            player_rect.move_ip(0, player_speed)
        for b in obstacle:
            b['rect'].move_ip(0, b['speed'])
        for b in obstacle[:]:
            if b['rect'].top > height:
                obstacle.remove(b)
        window.fill(BLACK)
        drawText('Score: %s' % (score), fontsmall, window, 10, 0)
        drawText('Top Score: %s' % (topScore), fontsmall, window, 10, 40)
        drawText('Level: %s' % (Level), fontsmall, window, 10, 80)
        if Level>13:
            drawText('Difficulty: Impossible', fontsmall, window, 10, 120)
        elif Level>10:
            drawText('Difficulty: Extreme', fontsmall, window, 10, 120)
        elif Level>7:
            drawText('Difficulty: High', fontsmall, window, 10, 120)
        elif Level>4:
            drawText('Difficulty: Medium', fontsmall, window, 10, 120)
        else:
            drawText('Difficulty: Easy', fontsmall, window, 10, 120)
        drawText('Lives Left: %s' % (Lives), fontsmall, window,45*(width/100), 10)
        if developer_mode:
            drawText('Developer', fontsmall, window,89*(width/100), 10)
        window.blit(player_image, player_rect)
        for b in obstacle:
            window.blit(b['surface'], b['rect'])
        pygame.display.update()
        if developer_mode == False:
            if collision(player_rect, obstacle):
                Lives-=1
                obstacle=[]
                if Lives<1:
                    if score > topScore:
                        topScore = score
                    FPS=60
                    Level=1
                    new_obstacle_rate = 18
                    window.fill(BLACK)
                    drawText('GAME OVER', fontlarge, window,38*(width /100), 37*(height /100))
                    drawText('Your Score:'+ str(score), font, window,40*(width /100) ,44*(height /100))
                    drawText('Press SPACE to play again.', fontsmall, window, 38*(width /100) , 50*(height / 100))
                    pygame.display.update()
                    keypress()
                    break
                window.fill(BLACK)
                drawText('Lives Left:'+ str(Lives), font, window, 41*(width /100), 43*(height /100))
                drawText('Press SPACE to play again.', fontsmall, window, 36*(width /100) ,49*(height / 100))
                pygame.display.update()
                keypress()
                moveLeft = moveRight = moveUp = moveDown = False
        Speedup+=1
        if Speedup==(1000):
            FPS += 5
            Speedup = 0
            Level += 1
            add_obsticle = 0
            new_obstacle_rate -= 1
        if Level > 15 :
            if score > topScore:
                    topScore = score
            window.fill(BLACK)
            for n in range(300):
                locations = (random.randint(0,width),random.randint(0,height))
                for x in range(1):
                    pygame.draw.circle(window,WHITE, locations, 1)
            drawText('GAME COMPLETED!', fontlarge, window, 31*(width /100), 37*(height /100))
            drawText('Your Score:'+ str(score), fontsmall, window,43*(width /100),45*(height /100))
            drawText('Press SPACE to play again.', fontsmall, window, 36*(width /100) ,50*(height / 100))
            pygame.display.update()
            keypress()
            FPS=60
            Level=1
            new_obstacle_rate = 18
            break
        mainClock.tick(FPS)
    pygame.display.update()
