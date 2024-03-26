import copy
import math
import random

import CellClass
import GlobalVar


class Neuron:
    def __init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=[]):
        self.weight = weight            #IN
        self.bias = bias                #IN
        self.connected = connected
        self.testNAME = testNAME
        self.IO = IO
        self.inputVal = inputVal        #OUT -> [retv, Fdirection, Fobj]
        self.lastCalcVal = None

    def resetIN(self):
        self.lastCalcVal = self.inputVal
        self.inputVal=[]

class Look(Neuron):
    def __init__(self, testNAME, IO, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK"
        self.look_range = look_range

    def _calc_dist(self, obj, cobj):
        pos = obj.pos
        cpos = cobj.pos
        distx = cpos[0]-pos[0]
        disty = cpos[1]-pos[1]
        dist = math.sqrt(distx**2+disty**2)

        return dist, GlobalVar.Normalize_dist([distx, disty])

    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for dict in objs: ###TO CHANGE INTO LOOKFOOD/LOOKCELL, REMOVE THIS FOR AND PUT OBJS[1] OR OBJS[2] AS ITARR
            for c_obj in dict:
                if c_obj!=obj:
                    dist, direction = self._calc_dist(obj, c_obj)
                    if mindist > dist:
                        mindist = dist
                        Fdirection = direction
                        Fobj = c_obj

        if self.look_range >= mindist:
            small_step = 10/self.look_range
            retv = 10 - small_step*mindist
            return [retv*self.weight+self.bias, Fdirection, Fobj, mindist]
        return [-10, [0,0], None, 1000]

class LookFood(Look):
    def __init__(self, testNAME, IO, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Look.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK FOOD"

    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for c_obj in objs[1]:
            if c_obj != obj:
                dist, direction = self._calc_dist(obj, c_obj)
                if mindist > dist:
                    mindist = dist
                    Fdirection = direction
                    Fobj = c_obj

        if self.look_range >= mindist:
            small_step = 10 / self.look_range
            retv = 10 - small_step * mindist
            return [retv*self.weight+self.bias, Fdirection, Fobj, mindist]
        return [-10, [0, 0], None, 1000]

class LookCell(Look):
    def __init__(self, testNAME, IO, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Look.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK CELL"

    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for c_obj in objs[0]:
            if c_obj != obj:
                dist, direction = self._calc_dist(obj, c_obj)
                if mindist > dist:
                    mindist = dist
                    Fdirection = direction
                    Fobj = c_obj

        if self.look_range >= mindist:
            small_step = 10 / self.look_range
            retv = 10 - small_step * mindist
            return [retv*self.weight+self.bias, Fdirection, Fobj, mindist]
        return [-10, [0, 0], None, 1000]

class MoveTowards(Neuron):
    def __init__(self, testNAME, IO, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "MOVE TOWARDS"


    def Calc(self):
        tdir = [0,0]
        for sd in self.inputVal:
            tdir[0]+=sd[0]*sd[1][0]+random.randint(-10,10)/100
            tdir[1]+=sd[0]*sd[1][1]+random.randint(-10,10)/100
        tdir = GlobalVar.Normalize_dist(tdir)
        return tdir, 0, [], []
        #LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL

class Eat(Neuron):
    def __init__(self, testNAME, IO, look_range=10, weight=None, bias=None, connected=None, inputVal=None, activation_val=3):
        self.activation_val = activation_val
        Neuron.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "EAT"
        self.look_range = look_range

    def Calc(self):
        returnFood = 0
        returnRFood = []
        for sd in self.inputVal:
            if sd[0] >= self.activation_val and type(sd[2])==CellClass.Food and sd[2] not in returnRFood and sd[3] < self.look_range:
                returnFood += sd[2].foodEnergy
                returnRFood.append(sd[2])
        return [0,0], returnFood, returnRFood, []