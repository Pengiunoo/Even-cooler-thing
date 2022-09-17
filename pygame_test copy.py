import pygame

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
light_Blue = (0, 255, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

size = (w, h) = (800, 400)

pygame.init()
sc = pygame.display.set_mode(size)
pygame.display.set_caption("The game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 100)  # text font and size

run = True
while run == True:  # game running

    '''   process events   '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # check if user want to close the window
            run = False

    '''   draw objects   '''
    sc.fill(white)
    colours = (0, 0, 0)

    text1 = font.render("loading ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading. ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading.. ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading... ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading.... ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading..... ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    text1 = font.render("loading...... ", True, colours)
    sc.blit(text1, (200, 100))
    pygame.time.delay(500)
    pygame.display.flip()

    clock.tick(30)


pygame.quit()
