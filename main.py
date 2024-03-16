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
canvas = pygame.display.set_mode((GlobalVar.width+400, GlobalVar.height))
pygame.display.set_caption("My Board")
Clock = pygame.time.Clock()
exit=False
cells = []
foods = []
_Populate(20,cells) #REMEMBER!!! CURRENTLY IN THE SAME ARRAY WITH FOOD, IF MORE THAN 1 IT CAUSES AN ERROR
_FoodPopulate(100,foods)
_InitializeCells(cells)
objs = []
objs.append(cells)
objs.append(foods)
print(objs)

#MAIN LOOP
time = 0
x = 0
y = 0
reprCell = None

while not exit:
    time+=1

    canvas.fill((200, 200, 200))

    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos( )
            print(f'Mouse clicked at {x}, {y}')


    for cell in objs[0]:
        cell.draw(canvas)
        cell.brain_step(objs)
        if x != None:
            xmin, xmax, ymin, ymax = cell.BOUNDARY_POS()
            if x > xmin and x < xmax and y > ymin and y < ymax:
                reprCell = cell



    if reprCell!=None:
        reprCell.REPR_CELL(canvas)
        print(reprCell.genome)


    for food in objs[1]:
        food.draw(canvas)


    Clock.tick(60)
    fps = Clock.get_fps( )
    GlobalVar.Render_Text(f"FPS: {str(int(fps))}",(0,0,0),[10,10], canvas)
    pygame.display.update( )