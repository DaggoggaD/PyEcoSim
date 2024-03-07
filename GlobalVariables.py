CHEAP = True
fps = 60
SCRWIDTH = 800
SCRHEIGHT = 800
Ngenes = 10
BiggestTwoPower = 3
GeneLen = 2 ** (BiggestTwoPower+1) -1
StatLen = 5
DEBUG= False
dt=0.1
maxCellAge = fps*60
width = 800
height = 800
# CREATING CANVAS
fps=60
# TITLE OF CANVAS
exit = False
#135 -> 7
SquareDivSize = 200
maxDivN = 2**(width/SquareDivSize)-1
print(maxDivN)
prolificgen = 0
deadgen = 0
lineWN = int(width / SquareDivSize)


cellN = 30
foodN = 300
Foodincircle=False
FoodSpawnRadius = 300
FoodSpawnX = 400
FoodSpawnY = 400
SQFoodSpawnX = 0
SQFoodSpawnY = 0
FSwidth = 800
FSheight = 800

remainingCells = cellN

mutationChance = 100
stillEnergyCons = 0.1*10*dt
lifeLossForFood = 0.1*10*dt
foodForRepr = 20