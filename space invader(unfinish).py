import pygame
import random

from pygame.constants import KEYDOWN, K_RIGHT

white = (255,255,255)
black = (0,0,0)
grey = (200,200,200)
red = (255,0,0)
blue = (0,255,255)
green = (0,255,0)
yellow = (255,255,0)
colours = [random.randint(0,255),random.randint(0,255),random.randint(0,255)] 

size = (width,height) = (500,650)
r_x = 220
r_y = 600
b_x = 247
b_y = 595
move_x = 0
move_y = 0
speed = 1

pygame.init()
sc = pygame.display.set_mode(size)
pygame.display.set_caption("Space Invader")
clock = pygame.time.Clock()

run = True
while run:

    sc.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # check if user want to close the window
            run = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_x = move_x + speed
            if event.key == pygame.K_LEFT:
                move_x = move_x - speed
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_x = 0
            if event.key == pygame.K_LEFT:
                move_x = 0
            if event.key == pygame.K_SPACE:
                pass

    r_x = r_x + move_x
    b_x = b_x + move_x

    if r_x >= width-60:
        r_x = width-60
    if r_x <= 0:
        r_x = 0
    if b_x >= width-33:
        b_x = width-33
    if b_x <= 27:
        b_x = 27

    pygame.draw.rect(sc, blue, [r_x,r_y,60,45])  #ship
    
    pygame.draw.rect(sc, grey, [150,10,15,15])
    pygame.draw.rect(sc, grey, [200,10,15,15])
    pygame.draw.rect(sc, grey, [250,10,15,15])
    pygame.draw.rect(sc, grey, [300,10,15,15])
    pygame.draw.rect(sc, grey, [350,10,15,15])
    pygame.draw.rect(sc, grey, [400,10,15,15])

    pygame.draw.rect(sc, red, [b_x,b_y,6,20])

    pygame.display.flip()
pygame.quit()