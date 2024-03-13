import random

import CellClass
import pygame
import GlobalVar

pygame.init( )

#FUNCTIONS
def _Populate(N, arr):
    for i in range(N):
        arr.append(CellClass.Cell())

def _FoodPopulate(N, arr):
    for i in range(N):
        arr.append(CellClass.Food([random.randint(0,GlobalVar.width), random.randint(0,GlobalVar.height)], 10))

def _InitializeCells(arr):
    for cell in arr:
        cell.initialize( )

#VARIABLES
canvas = pygame.display.set_mode((GlobalVar.width, GlobalVar.height))
pygame.display.set_caption("My Board")
Clock = pygame.time.Clock()
exit=False
objs = []
foods = []
_Populate(1,objs)
_FoodPopulate(100,foods)
_InitializeCells(objs)


#MAIN LOOP
time = 0
while not exit:
    time+=1
    canvas.fill((200, 200, 200))
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True

    for cell in objs:
        cell.draw(canvas)
        cell.brain_step(foods)
        #print(cell.food)

    for food in foods:
        food.draw(canvas)
    print(time)
    pygame.display.update( )
    Clock.tick(60)