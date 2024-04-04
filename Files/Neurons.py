import copy
import math
import random
import CellClass
import GlobalVar

###CLASSES###

#Neuron prefab.
#   Contains the resetIN function for Output neruons.
class Neuron:
    def __init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[]):
        self.weight = weight            #IN
        self.bias = bias                #IN
        self.connected = connected
        self.testNAME = testNAME
        self.IO = IO
        self.inputVal = inputVal        #OUT -> [retv, Fdirection, Fobj]
        self.lastCalcVal = None
        self.index = index

    def resetIN(self):
        self.lastCalcVal = self.inputVal
        self.inputVal=[]

#Lifetime Neuron
#   Each frame the cell's age increases.
#   A value between 0 (the cell is instantiated)
#   and 10 (the cell reached the cycle length age).
class Lifetime(Neuron):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LIFETIME"

    #Calculates return value
    def Calc(self, obj, objs):
        maxAge = GlobalVar.sim_len
        retv = (obj.age*10)/maxAge
        return [retv*self.weight+self.bias, [0,0], None, 1000]


#Food quantity neuron.
#   Returns a value between 0 and 10, based on the food stored in the cell.
#   0  is returned if stored food is below -100;
#   10 is returned if stored food is above  100;
#   The return value increases linearly between 0 and 10.
class FoodQty(Neuron):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "FOOD QTY"

    #Calculates return value
    def Calc(self, obj, objs):
        if obj.food < -100:
            return [0*self.weight+self.bias, [0,0], None, 1000]
        elif obj.food > 100:
            return [10*self.weight+self.bias, [0,0], None, 1000]
        else:
            custmFood = obj.food + 100
            retv = custmFood/20
            return [retv*self.weight+self.bias, [0,0], None, 1000]

#Look neuron.
#   This neuron is used both as a prefab as the LookAll neuron.
#   Checks all cells and foods in close areas, and if they're at less
#   than look_range distance, it's added to the found objs.
#   The found objs are then sorted in an increasing order based on distance.
#   The return value ranges between 0 (far) and 10 (close) based on distance and look_range.
class Look(Neuron):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK"
        self.look_range = look_range

    #Calculates distance between two objects
    def _calc_dist(self, obj, cobj):
        pos = obj.pos
        cpos = cobj.pos
        distx = cpos[0]-pos[0]
        disty = cpos[1]-pos[1]
        dist = 0.5 * (abs(distx) + abs(disty) + max(abs(distx), abs(disty)))
        #old:   dist = math.sqrt(distx**2+disty**2)

        return dist, GlobalVar.Normalize_dist([distx, disty])

    #Calculates return value
    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for dict in objs:
            for c_obj in dict:
                if c_obj!=obj and c_obj.area in obj.closeAreas:
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

#Look Food neuron.
#   Checks all foods in close areas, and if they're at less
#   than look_range distance, it's added to the found foods.
#   The found foods are then sorted in an increasing order based on distance.
#   The return value ranges between 0 (far) and 10 (close) based on distance and look_range.
class LookFood(Look):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Look.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK FOOD"

    # Calculates return value
    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for c_obj in objs[1]:
            if c_obj != obj and c_obj.area in obj.closeAreas:
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

#Look Cell neuron.
#   Checks all cells in close areas, and if they're at less
#   than look_range distance, it's added to the found cells.
#   The found cells are then sorted in an increasing order based on distance.
#   The return value ranges between 0 (far) and 10 (close) based on distance and look_range.
class LookCell(Look):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Look.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK CELL"

    # Calculates return value
    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for c_obj in objs[0]:
            if c_obj != obj and c_obj.area in obj.closeAreas:
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

#Look Cell neuron.
#   Checks all cells in close areas, and if they're at less
#   than look_range distance, it's added to the found cells.
#   It then checks if that cell is fighting, an if so it finds its distance.
#   The found cells are then sorted in an increasing order based on distance.
#   The return value ranges between 0 (far) and 10 (close) based on distance and look_range.
class LookFight(Look):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Look.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=None)
        self.name = "LOOK FIGHT"

    # Calculates return value
    def Calc(self, obj, objs):
        mindist = math.inf
        Fdirection = None
        Fobj = None
        for c_obj in objs[0]:
            if c_obj != obj and c_obj.area in obj.closeAreas and c_obj.isFighting:
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

#Move towards neuron.
#   This neurons needs an input_val and a direction.
#   It then returns a normalized vector in the same direction.
class MoveTowards(Neuron):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "MOVE TOWARDS"


    def Calc(self):
        tdir = [0,0]
        for sd in self.inputVal:
            tdir[0]+=sd[0]*sd[1][0]
            tdir[1]+=sd[0]*sd[1][1]
        tdir = GlobalVar.Normalize_dist(tdir)
        return tdir, 0, [], []
        #LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL

#Move towards neuron.
#   This neuron needs an input_val and a direction.
#   It then returns a normalized vector in the opposite direction.
class MoveAway(Neuron):
    def __init__(self, testNAME, IO, index, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "MOVE AWAY"


    def Calc(self):
        tdir = [0,0]
        for sd in self.inputVal:
            tdir[0]+=sd[0]*sd[1][0]
            tdir[1]+=sd[0]*sd[1][1]
        tdir[0]=-tdir[0]
        tdir[1]=-tdir[1]
        tdir = GlobalVar.Normalize_dist(tdir)
        return tdir, 0, [], []
        #LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL

#Eat neuron
#   This neuron needs an input_val and a food object.
#   If said object is indeed a food, it proceeds to slowly eating
#   it until there's nothing left.
#   It returns a change in food and the eaten food object, once it's finished.
class Eat(Neuron):
    def __init__(self, testNAME, IO, index, look_range=10, weight=None, bias=None, connected=None, inputVal=None, activation_val=3):
        self.activation_val = activation_val
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "EAT"
        self.look_range = look_range

    def Calc(self):
        returnFood = 0
        returnRFood = []
        for sd in self.inputVal:
            if sd[0] >= self.activation_val and type(sd[2])==CellClass.Food and sd[2] not in returnRFood and sd[3] < self.look_range:
                if sd[2].foodEnergy > GlobalVar.metabolism + 0.2:
                    returnFood+=GlobalVar.metabolism + 0.2
                    sd[2].foodEnergy-=GlobalVar.metabolism + 0.2
                else:
                    returnFood += sd[2].foodEnergy
                    returnRFood.append(sd[2])

        return [0,0], returnFood, returnRFood, []

#Share neuron.
#   When a certain amount of food is stored (checked in CellClass.Cell._remove_food_arr())
#   food is shared to the ecosystem, spawned in a random location.
class Share(Neuron):
    def __init__(self, testNAME, IO, index, look_range=10, weight=None, bias=None, connected=None, inputVal=None, activation_val=3):
        self.activation_val = activation_val
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "SHARE"
        self.look_range = look_range

    def Calc(self):
        return [0,0], -10, ["SHARED"], []

#Attack neuron
#   This neuron needs an input_val and a cell object.
#   If said object is indeed a cell, it proceeds to attack
#   it until there's nothing left.
#   It returns the attacked cell object, once it's finished.
class Attack(Neuron):
    def __init__(self, testNAME, IO, index, look_range=10, weight=None, bias=None, connected=None, inputVal=None, activation_val=0):
        self.activation_val = activation_val
        Neuron.__init__(self, testNAME, IO, index, weight=None, bias=None, connected=None, inputVal=[])
        self.name = "ATTACK"
        self.look_range = look_range

    def Calc(self):
        returnRCell = []
        for sd in self.inputVal:
            if type(sd[2])==CellClass.Cell and  sd[2] not in returnRCell and sd[3] < self.look_range:
                returnRCell.append(sd[2])
        return [0,0], 0, [], returnRCell