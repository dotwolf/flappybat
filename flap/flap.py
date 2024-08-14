import pygame
import time
import random

pygame.init()
pygame.font.init()

def clamp(n, minn, maxn): return min(max(n, minn), maxn)

pygame.display.set_caption('Flappy Bat')
Icon = pygame.image.load('bat.png')
pygame.display.set_icon(Icon)

width = 800
height = 600

screen = pygame.display.set_mode((width,height))
background = pygame.image.load('background.png')

player = pygame.Rect((150,250,96,48))

bat1 = pygame.image.load('bat1.png').convert_alpha()
bat2 = pygame.image.load('bat2.png').convert_alpha()

obs = [
    pygame.image.load('obs1.png').convert_alpha(), pygame.image.load('obs2.png').convert_alpha()
]
iobs = [
    pygame.image.load('iobs1.png').convert_alpha(), pygame.image.load('iobs2.png').convert_alpha()
]

starttime = time.time()
lastobs = [time.time(),0]
lastpoint = time.time()
t = time.time()
lastjump = time.time()

points = 0

my_font = pygame.font.SysFont('inkfree', 45)
text_surface = my_font.render('Score: '+str(points), False, (255, 255, 255))

clock = pygame.time.Clock()
current_frame = 0
bat_frame = 0
angle = 0

obstacles = {}

run = True
jumping = False

while run:
    screen.blit(background, (0,0))

    key = pygame.key.get_pressed()

    bat_frame += 1

    if bat_frame % 400 < 200:
        rotated_image = pygame.transform.rotate(bat1, angle)

        screen.blit(rotated_image, (player.x,player.y))
    else:
        rotated_image = pygame.transform.rotate(bat2, angle)

        screen.blit(rotated_image, (player.x,player.y))

    if jumping and angle < 20 and bat_frame % 2 == 0: angle += 1
    if not jumping and angle > -20 and bat_frame % 4 == 0: angle -= 1
    
    if not jumping and key[pygame.K_SPACE] == True and (time.time() - t) > 0.3:
        jumping = True
        t = time.time()
    elif jumping:
        if (time.time() - t) > 0.3:
            jumping = False
            lastjump = time.time()
        elif player.top > 0 and current_frame >= (round((time.time() - t)*40)):
            player.move_ip(0,-1)
            current_frame = 0
        else:
            current_frame += 1
    else:
        if player.bottom < height and bat_frame % 2 == 0 and current_frame >= 3-clamp(round((time.time() - lastjump)*3),0,2):
            player.move_ip(0,1)
            current_frame = 0
        else:
            current_frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if (time.time() - lastobs[0]) >= 1.5:
        lastobs[0] = time.time()
        lastobs[1] += 1
        if lastobs[1] > 6: lastobs[1] = 0

        n = random.randint(0, 1)

        oHeight = random.randint(-600,-200)

        obstacle = pygame.Rect((950,oHeight,135,585))
        obstacles[lastobs[1]] = [obstacle,n,True,oHeight]
        
        lastobs[1] += 1
        n = random.randint(0, 1) 

        oHeight2 = random.randint(750,800) + oHeight

        obstacle = pygame.Rect((950,oHeight2,135,585))
        obstacles[lastobs[1]] = [obstacle,n,False,oHeight2]

 
    for x in list(obstacles):
        if obstacles[x][2] == True: 
            screen.blit(iobs[obstacles[x][1]], (obstacles[x][0].x,obstacles[x][0].y))
        else:
            screen.blit(obs[obstacles[x][1]], (obstacles[x][0].x,obstacles[x][0].y))
        if bat_frame % 3 == 0:
            obstacles[x][0].move_ip(-1,0)

        if obstacles[x][0].x == 100 and time.time() - lastpoint >= 1.2:
            lastpoint = time.time()
            points += 1
            text_surface = my_font.render('Score: '+str(points), False, (255, 255, 255))

        if obstacles[x][0].x <= 200 and obstacles[x][0].x >= 122:
           col = obstacles[x][0].colliderect(player)
           if col:
            lastpoint = time.time()
            points = 0
            text_surface = my_font.render('Score: '+str(points), False, (255, 255, 255))

            starttime = time.time()
            lastobs = [time.time(),0]
            lastpoint = time.time()
            t = time.time()
            lastjump = time.time() 
            obstacles = {}

            player = pygame.Rect((150,250,96,48))
            jumping = False
            
            current_frame = 0
            bat_frame = 0
            angle = 0
            break

    screen.blit(text_surface, (340,0))
    pygame.display.update()

pygame.quit()