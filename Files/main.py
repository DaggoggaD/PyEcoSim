import json
import random
import copy
import CellClass
import pygame
import GlobalVar
from matplotlib import pyplot as plt
from shapely.geometry import Polygon

pygame.init( )

###FUNCTIONS###

#Adds the initial population.
def _Populate(N, arr):
    for i in range(N):
        arr.append(CellClass.Cell())

#Populates the food array, making sure they  don't intersect custom wall borders.
def _FoodPopulate(N, arr):
    for i in range(N):
        fd = CellClass._check_food_coll()
        arr.append(fd)

#Each cell needs to be initialized, decoding/creating it's genome,
#   connecting it's neurons and setting weights and biases.
def _InitializeCells(arr):
    for cell in arr:
        cell.initialize()

#Custom walls can be added by oressing B to initialize wall building,
#   and P to add wall points.
def _Draw_Walls(scr):
    file = open("Blocks.txt", "r")
    GlobalVar.Walls = []
    for line in file:
        currarr = json.loads(line)
        if GlobalVar.debug:
            pygame.draw.polygon(scr, (70,70,70, 50), currarr, 5)
        else:
            pygame.draw.polygon(scr, (70,70,70, 50), currarr, 0)
        GlobalVar.Walls.append(currarr)

    file.close()


###VARIABLES###

#UI info vars.
gen=0
avgfood=0
maxfood=0

#PYGAME related vars.
canvas = pygame.display.set_mode((GlobalVar.width+400, GlobalVar.height))
pygame.display.set_caption("My Board")
Clock = pygame.time.Clock()
exit=False

#Simulation vars.
cells = []
foods = []
current_blocks = []
avg_food_history = []
blockStarted = False

#Initialization calls and vars.
_Draw_Walls(canvas)
_Populate(20,cells)
_FoodPopulate(100,foods)
_InitializeCells(cells)
objs = []
objs.append(cells)
objs.append(foods)

###MAIN LOOP###
time = 0
x = 0
y = 0
reprCell = None

while not exit:
    #Background color.
    canvas.fill((200, 200, 200))

    #Safety cells food reset.
    if time<=10:
        for cell in cells:
            cell.food=0
            cell.age = 0
    time+=1

    #Check pygame events.
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True
        #Gets mouse pos for a single cell INFO.
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos( )
            print(f'Mouse clicked at {x}, {y}')
        if event.type == pygame.KEYDOWN:
            #DEBUG MODE
            if event.key == pygame.K_d:
                if GlobalVar.debug==True:
                    GlobalVar.debug = False
                else:
                    GlobalVar.debug = True
            #START BUILDING MODE
            if event.key == pygame.K_b:
                if blockStarted == False:
                    blockStarted = True
                else:
                    blockStarted = False
                    if current_blocks!=[]:
                        #Writes custom walls in a text file, written as a normal array.
                        file = open("Blocks.txt", "a")
                        file.write(str(current_blocks)+"\n")
                        file.close( )
                        current_blocks = []
            #Adds a wall point.
            if event.key == pygame.K_p:
                xb, yb = pygame.mouse.get_pos()
                if blockStarted:
                    current_blocks.append([xb,yb])
            #Clears all custom walls.
            if event.key == pygame.K_c:
                file = open("Blocks.txt", "w")
                GlobalVar.Walls=[]
                file.close()


    #Updates and draws on canvas all cells (draw and brain_step func).
    for cell in objs[0]:
        if time==0:
            cell.food=0
        cell.draw(canvas)
        cell.brain_step(objs)
        #Gets cell in mouse pos to display its info.
        if x != None:
            xmin, xmax, ymin, ymax = cell.BOUNDARY_POS()
            if x > xmin and x < xmax and y > ymin and y < ymax:
                reprCell = cell

    #Draws brain's map.
    if reprCell!=None:
        reprCell.REPR_CELL(canvas)

    #Draws all foods.
    for food in objs[1]:
        food.draw(canvas)

    #Resets simulation every sim_len seconds.
    #   Kills underperforming cells and reproduces the top ones.
    #   Calculates the average food between all cells and finds the top one.
    #   Decreases or increases metabolism cost according to the previous cycle result.
    if(time >= GlobalVar.sim_len):
        gen+=1
        time = 0

        #Max food and average food calculators.
        maxfood = max(cells,key=lambda x: x.food)
        maxfood = maxfood.food
        avgfood = GlobalVar.Average_cell_food(cells)
        avg_food_history.append(avgfood)

        #Kills and reproduces top cells.
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

        #Increases/decreases metabolism cost.
        if avgfood >= 100:
            GlobalVar.metabolism += 0.05
        if avgfood <=-200:
            GlobalVar.metabolism -= 0.05

    #Fps getter.
    Clock.tick(60)
    fps = Clock.get_fps( )

    #Display simulation info.
    GlobalVar.Render_Text(f"METABOLISM: {str(round(GlobalVar.metabolism, 2))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height - 170], canvas)
    GlobalVar.Render_Text(f"FPS: {str(int(fps))}",(0,0,0),[GlobalVar.width,GlobalVar.height-140], canvas)
    GlobalVar.Render_Text(f"GEN: {str(int(gen))}",(0,0,0),[GlobalVar.width,GlobalVar.height-110], canvas)
    GlobalVar.Render_Text(f"AVG FOOD: {str(int(avgfood))}",(0,0,0),[GlobalVar.width,GlobalVar.height-80], canvas)
    GlobalVar.Render_Text(f"MAX FOOD: {str(int(maxfood))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height-50], canvas)
    GlobalVar.Render_Text(f"POP: {str(int(len(cells)))}", (0, 0, 0), [GlobalVar.width, GlobalVar.height-20], canvas)

    #Draws all walls.
    _Draw_Walls(canvas)

    pygame.display.update( )

plt.plot(avg_food_history)
plt.show()