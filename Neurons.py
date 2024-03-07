import copy
import random
from operator import itemgetter
import CUSTOM_FNC
import GeneHandling
from GlobalVariables import *
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

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


class LookNeurons:
    def __init__(self, obj, objs):
        self.obj = obj
        self.objs = objs
        self.weight=1
        self.bias=0
        self.look_index = -1
        self.mfl = None

    def SetCalcDist(self, currobj, colliding_objs):
        look_dist = self.obj.stats[self.look_index][1]

        if self.mfl == None:
            self.mfl = (10 - 0) / (self.obj.radius - look_dist)
        M_fitting_line = self.mfl

        tot_direction = [0, 0]
        if currobj != self.obj:
            if currobj.sqID in self.obj.nearsqID:
                dist, is_colliding, dir_x, dir_y = self.obj.CalcDist(currobj)
                if is_colliding:
                    tot_direction[0] += dir_x
                    tot_direction[1] += dir_y
                    colliding_objs.insert(0, [10, currobj, tot_direction])
                else:
                    if dist < look_dist:
                        tot_direction[0] += dir_x
                        tot_direction[1] += dir_y
                        retVal = M_fitting_line * (dist - self.obj.radius) + 10
                        for ID in range(len(colliding_objs) + 1):
                            if ID == len(colliding_objs):
                                colliding_objs.append([retVal, currobj, tot_direction])
                            elif retVal > colliding_objs[ID][0]:
                                colliding_objs.insert(ID, [retVal, currobj, tot_direction])
        return colliding_objs

    def InRange(self):
        colliding_objs=[]

        for obj in self.objs:
            self.SetCalcDist(obj, colliding_objs)

        """args = [self.objs, colliding_objs]
        with Pool() as pool:
            pool.imap(self.SetCalcDist, args)"""

        return colliding_objs

    def Calc(self):
        in_range = self.InRange()

class LookAll(LookNeurons):
    def __init__(self, obj, objs):
        LookNeurons.__init__(self, obj, objs)
        self.look_index = 4

class LookFood(LookNeurons):
    def __init__(self, obj, objs):
        LookNeurons.__init__(self, obj, objs)
        self.look_index = 5

class LookLife(LookNeurons):
    def __init__(self, obj, objs):
        LookNeurons.__init__(self, obj, objs)
        self.look_index = 7

class LookFight:
    def __init__(self, obj, objs):
        self.obj = obj
        self.objs = objs
        self.weight = 1
        self.bias = 0
        self.look_index = 6

    def InRange(self):
        look_dist = self.obj.stats[self.look_index][1]
        M_fitting_line = (10 - 0) / (self.obj.radius - look_dist)
        colliding_objs = []

        for currobj in self.objs:
            tot_direction = [0, 0]
            if currobj!=self.obj:
                if self.obj.sqID in currobj.nearsqID:
                    dist, is_colliding, dir_x, dir_y = self.obj.CalcDist(currobj)
                    if currobj.is_fighting:
                        if is_colliding:
                            tot_direction[0] += dir_x
                            tot_direction[1] += dir_y
                            colliding_objs.append([10, currobj,tot_direction])
                        else:
                            if dist<look_dist:
                                tot_direction[0]+=dir_x
                                tot_direction[1]+=dir_y
                                colliding_objs.append([M_fitting_line*(dist-self.obj.radius)+10, currobj,tot_direction])
        return colliding_objs

class AgeNeuron:
    def __init__(self, obj, maxAge):
        self.obj=obj
        self.weight=1
        self.bias=0
        self.maxAge = maxAge

    def Calc(self):
        out = 10*((self.maxAge - self.obj.age)/self.maxAge)
        return out

class MoveToNeuron:
    def __init__(self, obj, direction, inputv):
        self.obj = obj
        self.direction = direction
        self.inputv = inputv

    def Calc(self):
        MultDir = [self.direction[0]*self.inputv, self.direction[1]*self.inputv]
        self.obj.UpdateSelf(MultDir)

class MoveAwayNeuron:
    def __init__(self, obj, direction, inputv):
        self.obj = obj
        self.direction = direction
        self.inputv = inputv

    def Calc(self):
        MultDir = [-self.direction[0]*self.inputv, -self.direction[1]*self.inputv]
        self.obj.UpdateSelf(MultDir)

class EatNeuron:
    def __init__(self, obj, foods, food, inputv, activation_val):
        self.obj = obj
        self.inputv = inputv
        self.foods = foods
        self.food = food
        self.activation_val = activation_val

    def Calc(self):
        if self.inputv >= self.activation_val:
            if self.food in self.foods:
                self.foods.remove(self.food)
                self.obj.food += self.food.energy

class MoveRNDNeuron:
    def __init__(self, obj, inputv, activation_val):
        self.obj = obj
        self.inputv = inputv
        self.activation_val = activation_val

    def Calc(self):
        if self.inputv>=self.activation_val:
            Dir = [random.randint(-width, width), random.randint(-height,height)]
            normDir =CUSTOM_FNC.normalize(Dir,1)
            MULTDIR = [Dir[0]*self.inputv, Dir[1]*self.inputv]
            self.obj.UpdateSelf(MULTDIR)

class ReproduceNeuron:
    def __init__(self, obj, objs, inputv, activation_val):
        self.obj = obj
        self.objs = objs
        self.inputv = inputv
        self.activation_val = activation_val

    def Calc(self, foods, cells):
        if self.obj.food>=foodForRepr:
            self.obj.food-=foodForRepr
            newGenome = mutation_Exp(self.obj.genome)
            newCellPos = [self.obj.pos[0]+random.randint(-10,10), self.obj.pos[1]+random.randint(-10,10)]
            newCell = GeneHandling.Cell(newGenome, pos=newCellPos)

            LookN = LookFood(newCell, foods)
            LookInfo = LookN.InRange( )
            MoveN = MoveToNeuron(newCell, None, None)
            EatN = EatNeuron(newCell, foods, None, None, 8)
            MoveRND = MoveRNDNeuron(newCell, 10, 5)
            ReprNeuron = ReproduceNeuron(newCell, cells, 10, 5)
            newCell.testN = [LookN, MoveN, EatN, MoveRND, ReprNeuron]
            self.objs.append(newCell)

class AttackNeuron:
    def __init__(self, obj, objs, inputv, activation_val):
        self.obj = obj
        self.objs = objs
        self.inputv = inputv
        self.activation_val = activation_val

    def Calc(self):
        thisATK = self.obj.stats[2][1]
        otherATK = self.inputv[0][1].stats[2][1]
        otherOBJ = self.inputv[0][1]
