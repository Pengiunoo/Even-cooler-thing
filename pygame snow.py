import pygame
import random
 
#   '''   Define colours   '''
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Light_Blue = (0,255,255)
Green = (0,255,0)
Yellow = (255,255,0)
Colours = [Yellow, Green, Light_Blue, Red, White, Black]
Size = (Width,Height) = (600,650)
 
 
 
#   '''   creating a screen   '''
pygame.init()
SC = pygame.display.set_mode(Size)
pygame.display.set_caption("Snowing")
Clock = pygame.time.Clock()
 
 
 
SnowList = []
for i in range(10):
    x = random.randrange(600)
    y = random.randrange(650)
    speed = random.randint(1,5)
    SnowList.append([x, y, speed, "number"+str(i+1)])
print(SnowList)
 
#   '''    Main loop    '''
Done = False
while Done == False:
   
#       '''  Process events  '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # check if user want to close the window
            Done = True

 
#       '''  Draw/Render  '''
    SC.fill(Black)
    for i in range(len(SnowList)): 
        pygame.draw.circle(SC, White, (SnowList[i][0],SnowList[i][1]), 1)
 
        SnowList[i][1] += SnowList[i][2]
        print(SnowList[i][3])
 
        if SnowList[i][1] > Height:
            SnowList[i][1] = 0
            SnowList[i][0] = random.randint(0,600)
 
 
    pygame.display.flip()
    Clock.tick(90)
 
pygame.quit()