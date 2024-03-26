import copy
import math
import random
import pygame
import Neurons
import GlobalVar

INeuronsDict = {
    0: Neurons.Look("Look", 0),
    1: Neurons.LookFood("Look_food", 0),
    2: Neurons.Look("Look_fight", 0),
    3: Neurons.LookCell("Look_life", 0),
    4: Neurons.Look("Lifetime", 0),
    5: Neurons.Look("FoodQTY", 0)
}

ONeuronsDict = {
    0: Neurons.MoveTowards("Move_to", 1),
    1: Neurons.MoveTowards("Move_away", 1),
    2: Neurons.Eat("Eat", 1),
    3: Neurons.Eat("Move_rnd", 1),
    4: Neurons.MoveTowards("Attack", 1),
    5: Neurons.Eat("Reproduce", 1)
}

class Food:
    def __init__(self, pos, foodEnergy=[]):
        self.pos = pos
        self.foodEnergy = foodEnergy

    def draw(self, canvas):
        pygame.draw.circle(canvas,(0,200,0),self.pos,10,0)

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

    def REPR_GENOME(self):
        #IN, OUT, WEIGHT, STATS, BIAS
        print("IN, OUT, WEIGHT, STATS, BIAS")
        print(self.genome)
        print(f"[{self.INeurons},{self.ONeurons},{self.Stats}]\n")


    def REPR_CELL(self, canvas):
        lastrowind = 0
        for i in range(len(self.INeuronsCOMP)):
            IN = self.INeuronsCOMP[i][0]
            ON = self.ONeurons[i]
            strV=f"BIAS:{IN.bias}; {IN.name}:{round(ON.lastCalcVal[0][0],2)}--->{ON.name}"
            GlobalVar.Render_Text(strV, (0,0,0), [GlobalVar.width,10+30*i], canvas)
            lastrowind = 10+30*i


    def BOUNDARY_POS(self):
        return self.pos[0]-self.radius, self.pos[0]+self.radius, self.pos[1]-self.radius, self.pos[1]+self.radius

    def _generate_genome(self, geneLen, statLen):
        #instead of a long string of bin numbers, a single string of decimal numbers
        #genome divided in: INgenome OUgenome WGgenome STgenome Bias
        genome = []

        #INgenome: 0-5 * genomeLen
        inGenome = [random.randint(0,5) for x in range(geneLen)]
        genome.append(inGenome)

        #OUTgenome: 0-5 * genomeLen
        outGenome = [random.randint(0,5) for x in range(geneLen)]
        genome.append(outGenome)

        #WEIGHTgenome: 0-1 * genomeLen
        weightGenome = [round(random.random(), 4) for x in range(geneLen)]
        genome.append(weightGenome)

        #STATSgenome: 0-10 * genomeLen
        statsGenome = [round(random.random()*10, 4) for x in range(statLen)]
        genome.append(statsGenome)

        #BIAS genome: 0-1 * genomeLen
        biasGenome = [round(random.random( ), 4) for x in range(geneLen)]
        genome.append(biasGenome)

        return genome

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

    def _connect_neurons(self, IN, ON):
        for i in range(len(IN)):
            try:
                currIN = IN[i]
                currON = ON[i]
                currIN[0].weight = currIN[1]
                currIN[0].bias = currIN[2]
                currIN[0].connected = currON
                currON.connected = currIN[0]
                #check connections
                """
                print(f"{currIN[0]} -> {currIN[0].connected}")
                print(f"{currON} -> {currON.connected}\n")"""
            except:
                print("error in _connect_neurons, check for reason")

    def _random_pos(self):
        self.pos = [random.randint(0, GlobalVar.width), random.randint(0, GlobalVar.height)]

    def _separeIN(self):
        for N in self.INeuronsCOMP:
            self.INeurons.append(N[0])

    def _moveCell(self, changePOS):
        self.pos[0]+=changePOS[0]*GlobalVar.dt
        self.pos[1]+=changePOS[1]*GlobalVar.dt

        if self.pos[0] >= GlobalVar.width:
            self.pos[0] = GlobalVar.width
        elif self.pos[0] <= 0:
            self.pos[0]=0
        if self.pos[1] >= GlobalVar.height:
            self.pos[1]= GlobalVar.height
        if self.pos[1] <= 0:
            self.pos[1] = 0

    def _remove_food_arr(self, removeFOOD, objs):
        for C in removeFOOD:
            if C in objs:
                objs.remove(C)
                objs.append(Food([random.randint(0,GlobalVar.width), random.randint(0,GlobalVar.height)], 10))

    def _add_cell_food(self, toAdd):
        self.food+=toAdd

    def _calc_metabolism(self):
        self.food-=GlobalVar.metabolism

    def _mutate_genome(self):
        # instead of a long string of bin numbers, a single string of decimal numbers
        # genome divided in: INgenome OUgenome WGgenome STgenome Bias
        genome = copy.deepcopy(self.genome)
        # INgenome: 0-5 * genomeLen
        inGenome = genome[0]
        for i in range(len(inGenome)):
            randv = random.randint(0,100)
            if randv <= GlobalVar.mutation_chance:
                inGenome[i] = random.randint(0,5)

        # OUTgenome: 0-5 * genomeLen
        outGenome = genome[1]
        for i in range(len(outGenome)):
            randv = random.randint(0,100)
            if randv <= GlobalVar.mutation_chance:
                outGenome[i] = random.randint(0,5)

        # WEIGHTgenome: 0-1 * genomeLen
        weightGenome = genome[2]
        for i in range(len(weightGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                weightGenome[i] = round(random.random( ), 4)


        # STATSgenome: 0-10 * genomeLen
        statsGenome = genome[3]
        for i in range(len(statsGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                statsGenome[i] = round(random.random( ) * 10, 4)


        # BIAS genome: 0-1 * genomeLen
        biasGenome = genome[4]
        for i in range(len(biasGenome)):
            randv = random.randint(0, 100)
            if randv <= GlobalVar.mutation_chance:
                biasGenome[i] = round(random.random( ), 4)

        Ngenome = [inGenome, outGenome,weightGenome, statsGenome, biasGenome]
        return Ngenome

    def initialize(self):
        if self.genome==None:
            self.genome = self._generate_genome(5,5)
        self.INeuronsCOMP, self.ONeurons, self.Stats = self._decode_genome(self.genome)
        #print(f"catch: {self.genome}, { self.ONeurons }")
        self._connect_neurons(self.INeuronsCOMP, self.ONeurons)
        self._separeIN()
        self._random_pos()
        self.REPR_GENOME()
        self.food=0

    def brain_step(self, objs):
        cells = objs[0]
        foods = objs[1]
        ###Calc Input values
        for IN in self.INeurons:
            Neuron_result = IN.Calc(self, objs)  # -> [retv, Fdirection, Fobj]
            connectedON = IN.connected
            connectedON.inputVal.append(Neuron_result)

        ###Calc Output values
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

        ###Update Cell
        self._moveCell(changePOS)
        self._remove_food_arr(removeFOOD, foods)
        self._add_cell_food(changeFOOD)
        self._calc_metabolism()

        """
        self._remove_food()
        self._remove_cell()"""

    def reproduce(self):
        mut_genome = self._mutate_genome()
        newCell = Cell(mut_genome)
        newCell.initialize()
        return newCell

    def draw(self, canvas):
        pygame.draw.circle(canvas,self.color,self.pos,self.radius,0)
        if GlobalVar.debug:
            GlobalVar.Render_Text(f"{str(int(self.food))}", (0, 0, 0), self.pos, canvas)

    def TEST_INEURONS(self, obj, objs):
        print(f"{obj} -> { self.INeurons[0].Calc(obj, objs) }")
