import CellClass
import pygame
import GlobalVar

pygame.init( )

#FUNCTIONS
def _Populate(N, arr):
    for i in range(N):
        arr.append(CellClass.Cell())

def _InitializeCells(arr):
    for cell in arr:
        cell.initialize( )

#VARIABLES
canvas = pygame.display.set_mode((GlobalVar.width, GlobalVar.height))
pygame.display.set_caption("My Board")
Clock = pygame.time.Clock()
exit=False
objs = []
_Populate(5,objs)
_InitializeCells(objs)


#MAIN LOOP
while not exit:
    canvas.fill((200, 200, 200))
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True

    for cell in objs:
        cell.draw(canvas)
        cell.brain_step(objs)

    pygame.display.update( )
    Clock.tick(60)