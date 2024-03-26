import random
import copy
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
        cell.initialize()



#VARIABLES
gen=0
avgfood=0
maxfood=0
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
    #safety reset
    if time<=10:
        for cell in cells:
            cell.food=0
    time+=1
    canvas.fill((200, 200, 200))

    #check events
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos( )
            print(f'Mouse clicked at {x}, {y}')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if GlobalVar.debug==True:
                    GlobalVar.debug = False
                else:
                    GlobalVar.debug = True

    #updates all cells
    for cell in objs[0]:
        if time==0:
            cell.food=0
        cell.draw(canvas)
        cell.brain_step(objs)
        if x != None:
            xmin, xmax, ymin, ymax = cell.BOUNDARY_POS()
            if x > xmin and x < xmax and y > ymin and y < ymax:
                reprCell = cell

    #Draw brain's map
    if reprCell!=None:
        reprCell.REPR_CELL(canvas)

    #Cycles foods
    for food in objs[1]:
        food.draw(canvas)

    #resets simulation after N seconds
    if(time >= 30*30):
        gen+=1
        time = 0

        maxfood = max(cells,key=lambda x: x.food)
        maxfood = maxfood.food
        avgfood = GlobalVar.Average_cell_food(cells)
        sortList = sorted(cells, key=lambda x: x.food, reverse=True)
        sortList = sortList[:10]
        ranc = random.randint(0,255)
        cells = [cell for cell in sortList]

        for cell in sortList:
            cell.food = 0
            reprC = cell.reproduce()
            reprC.spawn_gen = gen
            reprC.color = (150, ranc, 200)
            reprC.food = 0
            cells.append(reprC)

        objs[0]=cells

        for cell in cells:
            print(cell.food)

        if avgfood >= 100:
            GlobalVar.metabolism += 0.05
        if avgfood <=-200:
            GlobalVar.metabolism -= 0.05

    Clock.tick(60)
    fps = Clock.get_fps( )
    GlobalVar.Render_Text(f"METABOLISM: {str(round(GlobalVar.metabolism, 2))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height - 170], canvas)
    GlobalVar.Render_Text(f"FPS: {str(int(fps))}",(0,0,0),[GlobalVar.width,GlobalVar.height-140], canvas)
    GlobalVar.Render_Text(f"GEN: {str(int(gen))}",(0,0,0),[GlobalVar.width,GlobalVar.height-110], canvas)
    GlobalVar.Render_Text(f"AVG FOOD: {str(int(avgfood))}",(0,0,0),[GlobalVar.width,GlobalVar.height-80], canvas)
    GlobalVar.Render_Text(f"MAX FOOD: {str(int(maxfood))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height-50], canvas)
    GlobalVar.Render_Text(f"POP: {str(int(len(cells)))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height-20], canvas)

    pygame.display.update( )