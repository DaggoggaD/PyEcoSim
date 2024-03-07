import random
import numpy as np
import pygame
import math
import  CUSTOM_FNC
import copy
from GlobalVariables import *
import Neurons
import time


GLStats =[
    ["metabolism",1, 10],#0-10
    ["speed", 1, 10],#0-10
    ["atkP", 1, 10],#0-10
    ["m_food",10, 50],#0-50
    ["look", 10,100],#0-100
    ["look_food", 10, 100],# 0-100
    ["look_fight", 10,100],  # 0-100
    ["look_life", 10,100],  # 0-100
]

NeuronsType = {
    "0" : Neurons.LookAll,
    "1": Neurons.LookFood,
    "10": Neurons.LookFight,
    "11": Neurons.LookLife,
    "100": Neurons.AgeNeuron,
    "101": Neurons.LookAll,
    "110": Neurons.LookFood,
    "111": Neurons.LookFight,
    "1000" : "O1",
    "1001": "O2",
    "1010": "O3",
    "1011": "O4",
    "1100": "O5",
    "1101": "O6",
    "1110": "O7",
    "1111": "08"
}

def randomize_genome():
    Genome = []
    GenomeC = ""
    for i in range(Ngenes):
        randn = random.randint(0,GeneLen)
        randb = bin(randn)
        randb = randb[2:]
        Genome.append(randb)
        GenomeC+=randb
    for it in range(int(len(GLStats)/2)):
        number = random.getrandbits(StatLen)
        binary_string = format(number, '0b')
        binl = len(binary_string)
        for n in range(StatLen-binl):
            binary_string = "0" + binary_string
        Genome.append(binary_string)
        GenomeC+=binary_string
    return [Genome,GenomeC]

def decode_genome(Genome):
    GenomeSep = Genome[0]
    NeuronsI = []
    NeuronsO = []
    Stats = copy.deepcopy(GLStats)
    currstat = 0
    for gene in GenomeSep:
        if len(gene)==BiggestTwoPower+1:
            NeuronsO.append(NeuronsType[gene])
        elif len(gene)<BiggestTwoPower+1:
            if NeuronsType[gene] == Neurons.LookFood:
                NeuronsI.append(NeuronsType[gene])
            if NeuronsType[gene] == Neurons.LookLife:
                NeuronsI.append(NeuronsType[gene])
            if NeuronsType[gene] == Neurons.LookFight:
                NeuronsI.append(NeuronsType[gene])
            if NeuronsType[gene] == Neurons.LookAll:
                NeuronsI.append(NeuronsType[gene])
            if NeuronsType[gene] == Neurons.AgeNeuron:
                NeuronsI.append(NeuronsType[gene])

        else:
            intGene = int(gene, 2)
            value = (1*intGene)/(2**(StatLen)-1)*10
            connvalue = 10 - value
            Stats[2*currstat][1]=value*Stats[2*currstat][2]*0.1
            Stats[2*currstat+1][1]=connvalue*Stats[2*currstat+1][2]*0.1
            currstat+=1
            """SEED = int(gene, 2)
            np.random.seed(SEED)
            DividedLen = int(len(Stats)/2)
            Randv = np.random.rand(DividedLen)*10
            for n in range(DividedLen):
                #CHECK LATER IF IT WORKS!!!
                Stats[2*n][1]=Randv[n]
                Stats[2*n+1][1]=10-Randv[n]"""
    return NeuronsI, NeuronsO, Stats

def mutation_Exp(Genome):
    GenomeC = Genome[0]
    newGenomeC = ""
    newGenomeGenes = []
    for gene in GenomeC:
        newGene = ""
        for b in gene:
            if random.randint(0,mutationChance)==1:
                if b=="1":
                    newGene+="0"
                else:
                    newGene+="1"
            else:
                newGene+=b

        if len(newGene)<=BiggestTwoPower+1:
            intv = int(newGene, 2)
            newGene = bin(intv)
            newGene = newGene[2:]
        else:
            intv = int(newGene, 2)
            newGene = bin(intv)
            newGene = newGene[2:]
            glen = len(newGene)
            for it in range(StatLen-glen):
                newGene="0"+newGene

        newGenomeGenes.append(newGene)
        newGenomeC+=newGene

    NewGenome = [newGenomeGenes, newGenomeC]

    if DEBUG:
        print(NewGenome)
        print(Genome)
    #print(Genome==NewGenome)


    return NewGenome

def random_pos(width, height):
    x = random.randint(0,width)
    y = random.randint(0,width)
    return [x,y]

class Cell(object):
    def __init__(self, genome=None, INeurons=None, ONeurons=None, pos=None):
        self.genome = genome
        self.INeurons = INeurons
        self.ONeurons = ONeurons
        self.stats = copy.deepcopy(GLStats)
        self.pos = pos
        self.food = 0
        self.radius = 10
        self.lookradius = 50
        self.is_fighting = False
        self.age=0
        self.life = 10
        self.sqID = 0
        self.nearsqID = None
        self.testN = []
        self.initialize()

    def initialize(self):
        if self.pos==None:
            self.pos = random_pos(SCRWIDTH, SCRHEIGHT)
        self.Calc_sqid()
        if self.genome == None:
            self.genome = randomize_genome()
        self.INeurons, self.ONeurons, self.stats = decode_genome(self.genome)

    def Calc_sqid(self):
        pos = self.pos
        currentZoneX = math.floor(pos[0] / SquareDivSize)
        currentZoneY = math.floor(pos[1] / SquareDivSize)
        csqid = currentZoneX+int(width/SquareDivSize)*currentZoneY

        neighborsq = [csqid]
        neighborsq.append(csqid - lineWN)
        neighborsq.append(csqid + (lineWN))
        if csqid % lineWN == 0:
            # neighborsq.append(csqid - 1)
            neighborsq.append(csqid + 1)
            neighborsq.append(csqid - (lineWN - 1))
            # neighborsq.append(csqid - (lineWN + 1))
            # neighborsq.append(csqid + (lineWN - 1))
            neighborsq.append(csqid + (lineWN + 1))
        elif csqid % lineWN == lineWN - 1:
            neighborsq.append(csqid - 1)
            # neighborsq.append(csqid + 1)
            # neighborsq.append(csqid - (lineWN - 1))
            neighborsq.append(csqid - (lineWN + 1))
            neighborsq.append(csqid + (lineWN - 1))
            # neighborsq.append(csqid + (lineWN + 1))
        else:
            neighborsq.append(csqid - 1)
            neighborsq.append(csqid + 1)
            neighborsq.append(csqid - (lineWN - 1))
            neighborsq.append(csqid - (lineWN + 1))
            neighborsq.append(csqid + (lineWN - 1))
            neighborsq.append(csqid + (lineWN + 1))

        self.nearsqID = neighborsq
        self.sqID = csqid

    def play(self):
        print(f"-------------NEW CELL-------------")
        print(f"CELL GENOME:         {self.genome[0]} -> ({self.genome[1]})")
        print(f"CELL INPUT NEURONS:  {self.INeurons}")
        print(f"CELL OUTPUT NEURONS: {self.ONeurons}")
        print(f"CELL STATS:          {self.stats}")
        print(f"CELL POSITION:       {self.pos}")
        print(f"CELL FOOD:           {self.food}")
        return "-------------END CELL-------------"

    def reproduce(self):
        newCell = Cell(genome=mutation_Exp(self.genome), pos=self.pos)
        newCell.initialize()
        return newCell

    def Render_Text(self, what, color, where, font, canvas):
        text = font.render(what, 1, pygame.Color(color))
        canvas.blit(text, where)

    def DrawSelf(self, screen, font):
        #divide in 50x50 zones
        clr = (7, 59, 76)
        if DEBUG:
            clrx = self.sqID*int(math.floor(255/maxDivN))
            clry =self.sqID*int(math.floor(255/maxDivN))
            clr = (clrx, clry, ((clrx+clry)/2))
            self.Render_Text(str(self.nearsqID), (255, 0, 0), self.pos, font, screen)
        pygame.draw.circle(screen, clr, self.pos, self.radius)

    def UpdateSelf(self, direction):
        norm_dir = CUSTOM_FNC.normalize(direction, 1)
        self.pos=[self.pos[0]+(norm_dir[0])*dt*self.stats[1][1], self.pos[1]+norm_dir[1]*dt*self.stats[1][1]]
        if self.pos[0] > width:
            self.pos[0] = 0
        elif self.pos[1] > height:
            self.pos[1] = 0
        elif self.pos[0] < 0:
            self.pos[0] = width
        elif self.pos[1] < 0:
            self.pos[1] = height

        self.age+=dt
        self.Calc_sqid()

    def CalcDist(self, obj):

        dirx=-(self.pos[0]-obj.pos[0])
        diry=-(self.pos[1]-obj.pos[1])
        dist = math.sqrt((dirx)**2+(diry)**2)
        if dist > self.radius+obj.radius:
            return dist, False, dirx, diry,
        return dist, True, dirx, diry,

    def DrawLookRadius(self, screen, color):
        pygame.draw.circle(screen, color, self.pos, radius=self.stats[4][1], width=1)#all
        pygame.draw.circle(screen, (0,255,0), self.pos, radius=self.stats[5][1], width=1)#food
        pygame.draw.circle(screen, (0,0,255), self.pos, radius=self.stats[6][1], width=1)#fight
        pygame.draw.circle(screen, (0,255,255), self.pos, radius=self.stats[7][1], width=1)#life

    def DrawDirection(self, screen, direction):
        normdir = CUSTOM_FNC.normalize(direction, 10)
        endpos = [self.pos[0]+normdir[0], self.pos[1]+normdir[1]]
        pygame.draw.line(screen, (255,0,0), self.pos, endpos,width=2)

    def CheckIfAlive(self):
        if self.food<=0:
            self.life-=lifeLossForFood
        if self.life<=0:
            return self
        return None