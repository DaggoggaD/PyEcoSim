import copy
import math
import random
import pygame
import Neurons
import GlobalVar
from shapely.geometry import Polygon
from pygame import gfxdraw

###VARIABLES###

#Input neurons types dictionary.
INeuronsDict = {
    0: Neurons.Look("Look", 0),  #
    1: Neurons.LookFood("Look_food", 0),  #
    2: Neurons.Look("Look_fight", 0),
    3: Neurons.LookCell("Look_life", 0),  #
    4: Neurons.Lifetime("Lifetime", 0),   #
    5: Neurons.FoodQty("FoodQTY", 0)      #
}

#Output neurons types dictionary.
ONeuronsDict = {
    0: Neurons.MoveTowards("Move_to", 1), #
    1: Neurons.MoveAway("Move_away", 1),  #
    2: Neurons.Eat("Eat", 1),             #
    3: Neurons.Eat("Move_rnd", 1),
    4: Neurons.MoveTowards("Attack", 1),
    5: Neurons.Share("Share", 1)          #
}

#Instantiate foods and checks if it's in a legal position.
#   If not, a new one is instantiated.
def _check_food_coll():
    cf = Food([random.randint(0, GlobalVar.width), random.randint(0, GlobalVar.height)], random.randint(10, 50))

    #Foods shape placeholder, used to check collision with walls
    p1 = Polygon([
        (cf.pos[0] - cf.radius * 0.7, cf.pos[1] + cf.radius * 0.7),
        (cf.pos[0] + cf.radius * 0.7, cf.pos[1] + cf.radius * 0.7),
        (cf.pos[0] - cf.radius * 0.7, cf.pos[1] - cf.radius * 0.7),
        (cf.pos[0] + cf.radius * 0.7, cf.pos[1] - cf.radius * 0.7)
    ])

    #Checks if instantiated food is inside a wall
    coll = 0
    for pol in GlobalVar.Walls:
        p2 = Polygon(pol)
        try:
            collV = p1.intersects(p2)
        except:
            collV = False
        if collV == True:
            coll += 1

    #If a collision is detected, a new food is instantiated
    if coll != 0:
        cf = _check_food_coll()

    return cf

###CLASSES###

#Food class.
class Food:
    def __init__(self, pos, foodEnergy=[]):
        self.pos = pos
        self.foodEnergy = foodEnergy
        self.radius = self.foodEnergy
        self.color = (0,200,0)
        self.area = None
        self.closeAreas = None
        self._calc_area()

    #Draw method
    def draw(self, canvas):
        self.radius = self.foodEnergy
        pygame.draw.circle(canvas,self.color,self.pos,self.radius/3,0)

    # Calculates current and close areas, used for performance improvements
    def _calc_area(self):
        final_area = []

        # Current slot calc
        Nslot = GlobalVar.width / GlobalVar.Area_Sub
        xslot = math.floor(self.pos[0] / Nslot)
        yslot = math.floor(self.pos[1] / Nslot)
        area = xslot + GlobalVar.Area_Sub * yslot

        # Checks for special cases
        notRight = (area + 1) % GlobalVar.Area_Sub != 0
        notLeft = area % GlobalVar.Area_Sub != 0
        notTop = yslot != 0
        notBot = yslot != GlobalVar.Area_Sub

        # Appends same row areas
        if notRight: final_area.append(area + 1)
        if notLeft: final_area.append(area - 1)

        # Appends top row areas
        if notTop: final_area.append(area - GlobalVar.Area_Sub)
        if notTop and notRight: final_area.append(area - GlobalVar.Area_Sub + 1)
        if notTop and notLeft: final_area.append(area - GlobalVar.Area_Sub - 1)

        # Appends bottom row areas
        if notBot: final_area.append(area + GlobalVar.Area_Sub)
        if notBot and notRight: final_area.append(area + GlobalVar.Area_Sub + 1)
        if notBot and notLeft: final_area.append(area + GlobalVar.Area_Sub - 1)

        self.closeAreas = final_area
        self.area = area

#Cell class
class Cell:
    def __init__(self, genome=None, pos=None):
        self.genome = genome
        self.INeurons = []
        self.INeuronsCOMP = []
        self.ONeurons = []
        self.Stats = []
        self.pos = pos
        self.wobble = random.randint(-10,10)
        self.food = 10
        self.radius = 10
        self.spawn_gen = 0
        self.color = (200,0,0)
        self.age = 0
        self.shared = 0
        self.area = None
        self.closeAreas = None
        self.genome_code = None

    #Represents the cell's genome in the console.
    def REPR_GENOME(self):
        #IN, OUT, WEIGHT, STATS, BIAS
        print("IN, OUT, WEIGHT, STATS, BIAS")
        print(self.genome)
        print(f"[{self.INeurons},{self.ONeurons},{self.Stats}]\n")

    #Draws the cell's brain in the right side of the simulator.
    def REPR_CELL(self, canvas):
        lastrow = 0
        for i in range(len(self.INeuronsCOMP)):
            IN = self.INeuronsCOMP[i][0]
            ON = self.ONeurons[i]
            strV=f"Bias: {IN.bias}; {IN.name}:{round(ON.lastCalcVal[0][0],2)} -> {ON.name}"
            GlobalVar.Render_Text(strV, (0,0,0), [GlobalVar.width,10+30*i], canvas)
            lastrow+=1

        GlobalVar.Render_Text(f"Food: {int(self.food)}", (0,0,0), [GlobalVar.width,10+30*lastrow], canvas)
        GlobalVar.Render_Text(f"Area: {int(self.area)}", (0,0,0), [GlobalVar.width,10+30*(lastrow+1)], canvas)
        GlobalVar.Render_Text(f"Area: {self.closeAreas}", (0,0,0), [GlobalVar.width,10+30*(lastrow+2)], canvas)


    #Returns the boundaries of the cell.
    def BOUNDARY_POS(self):
        return self.pos[0]-self.radius, self.pos[0]+self.radius, self.pos[1]-self.radius, self.pos[1]+self.radius

    #Generates the cells genome in the first generation
    #   The cell's genome is composed by an array divided in five sections:
    #   Input Genome  -> a total of geneLen ints between 0 and 5,
    #   Output Genome -> a total of geneLen ints between 0 and 5,
    #   Weight Genome -> a total of geneLen floats between 0 and 1,
    #   Stats Genome  -> a total of geneLen floats between 0 and 10,
    #   Bias Genome   -> a total of geneLen floats between 0 and 1.
    #   A finished genome of geneLen = 5 looks like this:
    #   [[a,b,c,d,e],[f,g,h,i,j],[k,l,m,n,o],[p,q,r,s,t],[u,v,x,y,z]].
    def _generate_genome(self, geneLen, statLen):
        genome = []

        #INgenome
        inGenome = [random.randint(0,5) for x in range(geneLen)]
        genome.append(inGenome)

        #OUTgenome
        outGenome = [random.randint(0,5) for x in range(geneLen)]
        genome.append(outGenome)

        #WEIGHTgenome
        weightGenome = [round(random.random(), 4) for x in range(geneLen)]
        genome.append(weightGenome)

        #STATSgenome
        statsGenome = [round(random.random()*10, 4) for x in range(statLen)]
        genome.append(statsGenome)

        #BIAS genome
        biasGenome = [round(random.random( ), 4) for x in range(geneLen)]
        genome.append(biasGenome)

        return genome


    #Decodes the cell's genome dividing them in Input neurons and Output neurons.
    #   Input neurons are initially added with an array containing weights and biases.
    def _decode_genome(self, gen):
        IN = []
        ON = []
        ST = []
        for sec in gen:
            for gene in sec:
                if gen.index(sec) == 0:
                    IN.append([copy.copy(INeuronsDict[gene]), gen[2][sec.index(gene)], gen[4][sec.index(gene)]])
                elif gen.index(sec) == 1:
                    ON.append(copy.copy(ONeuronsDict[gene]))
                elif gen.index(sec) == 3:
                    ST.append(gene)

        return IN, ON, ST

    #Connects Input neurons and Output neurons and sets Input neurons' weights and biases.
    #   Debugging needed.
    def _connect_neurons(self, IN, ON):
        for i in range(len(IN)):
            try:
                currIN = IN[i]
                currON = ON[i]
                currIN[0].weight = currIN[1]
                currIN[0].bias = currIN[2]
                currIN[0].connected = currON
                currON.connected = currIN[0]
            except:
                print("error in _connect_neurons, check for reason")

    #Sets a new cell's random position.
    def _random_pos(self):
        self.pos = [random.randint(0, GlobalVar.width), random.randint(0, GlobalVar.height)]

    #Separes Input neurons and it's weights and biases for later use.
    def _separeIN(self):
        for N in self.INeuronsCOMP:
            self.INeurons.append(N[0])

    #Updates cell position
    #   Checks if next movement is outside the screen or inside a custom wall.
    #   If so, it reverts the movement and changes the cell's direction.
    def _moveCell(self, changePOS):
        prevpos = copy.deepcopy(self.pos)
        self.pos[0]+=changePOS[0]*GlobalVar.dt
        self.pos[1]+=changePOS[1]*GlobalVar.dt

        #Outside of the screen checks.
        if self.pos[0] >= GlobalVar.width:
            self.pos[0] = GlobalVar.width
        if self.pos[0] <= 0:
            self.pos[0]=0
        if self.pos[1] >= GlobalVar.height:
            self.pos[1]= GlobalVar.height
        if self.pos[1] <= 0:
            self.pos[1] = 0

        ###CELL-WALL COLLISION###

        #Cell's rect placeholder (used for collisions).
        p1 = Polygon([
            (self.pos[0]-self.radius*0.7, self.pos[1]+self.radius*0.7),
            (self.pos[0]+self.radius*0.7, self.pos[1]+self.radius*0.7),
            (self.pos[0]-self.radius*0.7, self.pos[1]-self.radius*0.7),
            (self.pos[0]+self.radius*0.7, self.pos[1]-self.radius*0.7)
        ])

        #Checks for a collision between the cell and every custom wall.
        coll = 0
        for pol in GlobalVar.Walls:
            p2 = Polygon(pol)
            try:
                collV = p1.intersects(p2)
            except:
                collV = False
            if collV==True:
                coll+=1

        #Reverts cell's movement and direction if a collision is detected.
        if coll!=0:
            self.pos=prevpos
            self.pos[0] -= changePOS[0] * GlobalVar.dt
            self.pos[1] -= changePOS[1] * GlobalVar.dt

    #Removes the food from foods array which gets digested.
    def _remove_food_arr(self, removeFOOD, objs):
        for C in removeFOOD:
            if C == "SHARED":
                if self.food <= 10:
                    self.food+=10
                elif self.shared < 5:
                    fd = _check_food_coll( )
                    fd.color = (100,255,0)
                    objs.append(fd)
                    self.shared+=1
            if C in objs:
                objs.remove(C)
                fd = _check_food_coll()
                objs.append(fd)

    #Adds nutrients to the cell after food digestion.
    def _add_cell_food(self, toAdd):
        self.food+=toAdd

    #Calcs metabolism cost each frame
    def _calc_metabolism(self):
        self.food-=GlobalVar.metabolism

    #Same as _generate_genome, but it only mutates the son's genome.
    #   Mutation chance is in GlobalVar.py.
    #   If the value is inside it's custom spectrum a single gene gets mutated,
    #   changing either a neuron, a bias, a weight or a single stat.
    def _mutate_genome(self):
        genome = copy.deepcopy(self.genome)

        # INgenome
        inGenome = genome[0]
        for i in range(len(inGenome)):
            randv = random.randint(0,100)
            if randv <= GlobalVar.mutation_chance:
                inGenome[i] = random.randint(0,5)

        # OUT_genome
        outGenome = genome[1]
        for i in range(len(outGenome)):
            randv = random.randint(0,100)
            if randv <= GlobalVar.mutation_chance:
                outGenome[i] = random.randint(0,5)

        # WEIGHT_genome
        weightGenome = genome[2]
        for i in range(len(weightGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                weightGenome[i] = round(random.random( ), 4)

        # STATS_genome
        statsGenome = genome[3]
        for i in range(len(statsGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                statsGenome[i] = round(random.random( ) * 10, 4)

        # BIAS_genome
        biasGenome = genome[4]
        for i in range(len(biasGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                biasGenome[i] = round(random.random( ), 4)

        Ngenome = [inGenome, outGenome,weightGenome, statsGenome, biasGenome]
        return Ngenome

    #Calculates current and close areas, used for performance improvements
    def _calc_area(self):
        final_area = []

        #Current slot calc
        #220, 130
        Nslot = GlobalVar.width/GlobalVar.Area_Sub  #100
        xslot = math.floor(self.pos[0]/Nslot) #2.2->2
        yslot = math.floor(self.pos[1]/Nslot) #1.3->1
        area = xslot+GlobalVar.Area_Sub*yslot #2+5*1

        #Checks for special cases
        notRight = (area+1)%GlobalVar.Area_Sub!=0
        notLeft = area%GlobalVar.Area_Sub!=0
        notTop = yslot != 0
        notBot = yslot != GlobalVar.Area_Sub

        #Appends same row areas
        final_area.append(area)
        if notRight: final_area.append(area+1)
        if notLeft: final_area.append(area-1)

        #Appends top row areas
        if notTop: final_area.append(area - GlobalVar.Area_Sub)
        if notTop and notRight : final_area.append(area - GlobalVar.Area_Sub + 1)
        if notTop and notLeft : final_area.append(area - GlobalVar.Area_Sub - 1)

        #Appends bottom row areas
        if notBot: final_area.append(area + GlobalVar.Area_Sub)
        if notBot and notRight : final_area.append(area + GlobalVar.Area_Sub + 1)
        if notBot and notLeft : final_area.append(area + GlobalVar.Area_Sub - 1)

        self.closeAreas = final_area
        self.area = area

    #Calculates color based on genome variation.
    #   Also used to have a genome variance value
    def _calc_color(self):
        ig = self.genome[0]
        og = self.genome[1]
        tot = (sum(ig)+sum(og))
        r,g,b=GlobalVar.num_to_rgb(tot,GlobalVar.maxGeneVal)
        self.color=(r,g,b)
        self.genome_code = tot

    #Initializes cell.
    #   Genome is generated (if needed);
    #   Genome is decoded and represented in the console;
    #   Neurons get connected;
    #   New position is set.
    def initialize(self):
        if self.genome==None:
            self.genome = self._generate_genome(5,5)
        self.INeuronsCOMP, self.ONeurons, self.Stats = self._decode_genome(self.genome)
        self._connect_neurons(self.INeuronsCOMP, self.ONeurons)
        self._separeIN()
        self._random_pos()
        self._calc_area()
        self._calc_color()
        self.REPR_GENOME()
        self.food=0

    #Perform a single brain step
    #   Gets all Input neurons results and sends them to the respective Output neuron, modified by weights and biases.
    #   Updates on the cell are then performed (pos change, food change and status)
    def brain_step(self, objs):
        self.age+=1
        cells = objs[0]
        foods = objs[1]

        #Calculates Input values
        for IN in self.INeurons:
            Neuron_result = IN.Calc(self, objs)  # -> [retv, Fdirection, Fobj]
            connectedON = IN.connected
            connectedON.inputVal.append(Neuron_result)

        #Calculates Output values
        changePOS=[0,0]
        changeFOOD=0
        removeFOOD = []
        removeCELL = []
        for ON in self.ONeurons:
            LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL = ON.Calc()
            changePOS[0]+=LChangePOS[0]
            changePOS[1]+=LChangePOS[1]
            if changeFOOD==0:
                changeFOOD+=LChangeFOOD
            [removeFOOD.append(a) for a in LRemoveFOOD]
            [removeCELL.append(a) for a in LRemoveCELL]

            ON.resetIN()

        changePOS = GlobalVar.Normalize_dist(changePOS)
        removeFOOD = list(dict.fromkeys(removeFOOD))
        removeCELL = list(dict.fromkeys(removeCELL))

        #Cell update
        self._moveCell(changePOS)
        self._remove_food_arr(removeFOOD, foods)
        self._add_cell_food(changeFOOD)
        self._calc_metabolism()
        self._calc_area()

        """
        self._remove_cell()"""

    #Handles all steps to reproduce (genome mutation and cell instantiation).
    def reproduce(self):
        mut_genome = self._mutate_genome()
        newCell = Cell(mut_genome)
        newCell.initialize()
        return newCell

    #Draws the cell on the canvas.
    def draw(self, canvas):

        pygame.draw.circle(canvas,self.color,self.pos,self.radius,0)
        if GlobalVar.debug:
            GlobalVar.Render_Text(f"{str(int(self.food))}", (0, 0, 0), self.pos, canvas)

    #Debug function
    def TEST_INEURONS(self, obj, objs):
        print(f"{obj} -> { self.INeurons[0].Calc(obj, objs) }")