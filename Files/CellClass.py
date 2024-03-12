import copy
import random
import pygame
import Neurons
import GlobalVar

INeuronsDict = {
    0: Neurons.Look("Look", 0),
    1: Neurons.Look("Look_food", 0),
    2: Neurons.Look("Look_fight", 0),
    3: Neurons.Look("Look_life", 0),
    4: Neurons.Look("Lifetime", 0),
    5: Neurons.Look("FoodQTY", 0)
}

ONeuronsDict = {
    0: Neurons.MoveTowards("Move_to", 1),
    1: Neurons.MoveTowards("Move_away", 1),
    2: Neurons.MoveTowards("Eat", 1),
    3: Neurons.MoveTowards("Move_rnd", 1),
    4: Neurons.MoveTowards("Attack", 1),
    5: Neurons.MoveTowards("Reproduce", 1)
}

class Cell:
    def __init__(self, genome=None, pos=None):
        self.genome = genome
        self.INeurons = []
        self.INeuronsCOMP = []
        self.ONeurons = []
        self.Stats = []
        self.pos = pos
        self.wobble = random.randint(-10,10)

    def REPR_GENOME(self):
        #IN, OUT, WEIGHT, STATS, BIAS
        print("IN, OUT, WEIGHT, STATS, BIAS")
        print(self.genome)
        print(f"[{self.INeurons},{self.ONeurons},{self.Stats}]\n")

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

    def _random_pos(self):
        self.pos = [random.randint(0, GlobalVar.width), random.randint(0, GlobalVar.height)]

    def _separeIN(self):
        for N in self.INeuronsCOMP:
            self.INeurons.append(N[0])

    def _moveCell(self, changePOS):
        self.pos[0]+=changePOS[0]*GlobalVar.dt
        self.pos[1]+=changePOS[1]*GlobalVar.dt

    def initialize(self):
        if self.genome==None:
            self.genome = self._generate_genome(5,5)
        self.INeuronsCOMP, self.ONeurons, self.Stats = self._decode_genome(self.genome)
        self._connect_neurons(self.INeuronsCOMP, self.ONeurons)
        self._separeIN()
        self._random_pos()
        self.REPR_GENOME()

    def brain_step(self, objs):
        for IN in self.INeurons:
            Neuron_result = IN.Calc(self, objs)  # -> [retv, Fdirection, Fobj]
            connectedON = IN.connected

            connectedON.inputVal.append(Neuron_result)

        changePOS=[0,0]
        changeFOOD=0
        removeFOOD = []
        removeCELL = []
        for ON in self.ONeurons:
            LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL = ON.Calc()
            changePOS[0]+=LChangePOS[0]
            changePOS[1]+=LChangePOS[1]
            changeFOOD+=LChangeFOOD
            [removeFOOD.append(a) for a in LRemoveFOOD]
            [removeCELL.append(a) for a in LRemoveCELL]

            ON.resetIN()

        changePOS = GlobalVar.Normalize_dist(changePOS)

        self._moveCell(changePOS)
        """self._add_cell_food()
        self._remove_food()
        self._remove_cell()"""

    def draw(self, canvas):
        pygame.draw.circle(canvas,(0,200,0),self.pos,10,0)

    def TEST_INEURONS(self, obj, objs):
        print(f"{obj} -> { self.INeurons[0].Calc(obj, objs) }")
