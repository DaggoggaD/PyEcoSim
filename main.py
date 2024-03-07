import random
import matplotlib.pyplot as plt
import pygame
import math
import GeneHandling
import Neurons
import ENV_classes
from GlobalVariables import *
import copy
import time as TIME
pygame.init( )

font = pygame.font.Font('freesansbold.ttf', 32)

#Functions
def SpawnCells(N):
    cellarr = []
    for i in range(N):
        newcell = GeneHandling.Cell( )
        print(newcell.sqID)
        cellarr.append(newcell)
        newcell.play()
    return cellarr

def addTestNeuron():
    for newcell in cells:
        LookN = Neurons.LookFood(newcell, foods)
        #MoveN = Neurons.MoveToNeuron(newcell, LookInfo[0][2], LookInfo[0][0])
        MoveN = Neurons.MoveToNeuron(newcell, None, None)

        #EatN = Neurons.EatNeuron(newcell, foods, LookInfo[0][1], LookInfo[0][0], 8)
        EatN = Neurons.EatNeuron(newcell, foods, None, None, 8)


        MoveRND = Neurons.MoveRNDNeuron(newcell, 10, 5)
        ReprNeuron = Neurons.ReproduceNeuron(newcell, cells, 10, 5)
        newcell.testN = [LookN, MoveN, EatN, MoveRND, ReprNeuron]

def Random_circle_point(circle_r, circle_x, circle_y):

    # random angle
    alpha = 2 * math.pi * random.random( )
    # random radius
    r = circle_r * math.sqrt(random.random( ))
    # calculating coordinates
    x = r * math.cos(alpha) + circle_x
    y = r * math.sin(alpha) + circle_y

    return [x, y]

def Start_food_spawn(N, iscircle):
    foodarr=[]
    for i in range(N):
        if iscircle==False:
            newfood = ENV_classes.Food([SQFoodSpawnX + random.randint(0,FSwidth), SQFoodSpawnY + random.randint(0,FSheight)],5)
        else:
            newfood = ENV_classes.Food(Random_circle_point(FoodSpawnRadius,FoodSpawnX,FoodSpawnY),5)
        foodarr.append(newfood)
    return foodarr

def Render_Text(what, color, where):
    text = font.render(what, 1, pygame.Color(color))
    canvas.blit(text, where)

#Vars
cells = SpawnCells(cellN)
foods = Start_food_spawn(foodN, Foodincircle)
addTestNeuron()
OBJS = foods+cells
Clock = pygame.time.Clock()
canvas = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Board")
infoT = []
infoV = []
time=0

while not exit:
    time+=0.1
    canvas.fill((200, 200, 200))
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            exit = True
    #cells
    toremovecells = []
    LOOKTIME = 0
    MOVETIME = 0
    EATTIME = 0
    RNDTIME = 0
    REPRTIME = 0
    for i in range(len(cells)):
        #TestDraw1
        #cells[i].DrawLookRadius(canvas, (255, 0, 0))
        currc = cells[i]

        currc.DrawSelf(canvas, font)

        LookN = currc.testN[0]
        LookN.objs = foods


        start = TIME.time()
        LookInfo = LookN.InRange()
        end =TIME.time()
        LOOKTIME += end-start

        if LookInfo!=[]:
            cells[i].DrawDirection(canvas,LookInfo[0][2])
            MoveN = currc.testN[1]
            MoveN.direction = LookInfo[0][2]
            MoveN.inputv = LookInfo[0][0]
            start = TIME.time()

            MoveN.Calc( )
            end = TIME.time()
            MOVETIME += end-start

            EatN = currc.testN[2]
            EatN.foods = foods
            EatN.food = LookInfo[0][1]
            EatN.inputv = LookInfo[0][0]
            start = TIME.time()
            EatN.Calc()
            end = TIME.time()
            EATTIME += end - start
        else:
            MoveRND = currc.testN[3]
            start = TIME.time()
            MoveRND.Calc()
            end = TIME.time()
            RNDTIME += end-start


        ReprNeuron = currc.testN[4]
        ReprNeuron.objs = cells
        start = TIME.time()
        ReprNeuron.Calc(foods,cells)
        end = TIME.time()
        REPRTIME += end-start

        cells[i].food-=stillEnergyCons
        deadOBJ = cells[i].CheckIfAlive()
        if deadOBJ!=None:
            new_foodPos= copy.copy(deadOBJ.pos)
            new_food = ENV_classes.Food(new_foodPos, 5)
            foods.append(new_food)
            toremovecells.append(deadOBJ)


    #print(f"LOOK: {LOOKTIME}, MOVE: {MOVETIME}, EAT:{EATTIME}, RND: {RNDTIME}, REPR: {REPRTIME}")
    #foods
    for i in range(len(foods)):
        foods[i].DrawSelf(canvas,font)


    newfood=None
    while 120+len(foods)<foodN:
        if Foodincircle:
            newfood = ENV_classes.Food(Random_circle_point(FoodSpawnRadius,FoodSpawnX,FoodSpawnY), 5)
        else:
            newfood = ENV_classes.Food([SQFoodSpawnX + random.randint(0, FSwidth), SQFoodSpawnY + random.randint(0, FSheight)], 5)
        foods.append(newfood)

    infoT.append(time)

    for dead in toremovecells:
        cells.remove(dead)
    remainingCells=len(cells)
    infoV.append(remainingCells)

    Render_Text("FPS: "+str(int(Clock.get_fps( ))), (0, 0, 0), (10, 10))
    Render_Text("ALIVE CELLS: "+str(remainingCells), (0, 0, 0), (10, 50))
    Render_Text("DG: "+str(deadgen), (0, 0, 0), (10, 90))
    Render_Text("PG: "+str(prolificgen), (0, 0, 0), (10, 130))

    pygame.display.update()
    Clock.tick(60)
    if len(cells)>120:
        foods = []
        cells = []
        cells = SpawnCells(cellN)
        foods = Start_food_spawn(foodN, Foodincircle)
        addTestNeuron()
        prolificgen += 1
    if time > 100 and (Clock.get_fps() < 2 and len(cells)!=50):
        foods=[]
        cells = []
        cells=SpawnCells(cellN)
        foods=Start_food_spawn(foodN,Foodincircle)
        addTestNeuron( )
        #exit = True
    if len(cells)==0:
        foods = []
        cells = SpawnCells(cellN)
        foods = Start_food_spawn(foodN, Foodincircle)
        addTestNeuron( )
        deadgen+=1


plt.plot(infoT,infoV)
plt.show()