import math

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
        self.inputVal=[]


class Look(Neuron):
    def __init__(self, testNAME, IO, look_range=100, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=None)
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
        for c_obj in objs:
            if c_obj!=obj:
                dist, direction = self._calc_dist(obj, c_obj)
                if mindist > dist:
                    mindist = dist
                    Fdirection = direction
                    Fobj = c_obj
        if self.look_range >= mindist:
            small_step = 10/self.look_range
            retv = 10 - small_step*mindist
            return [retv, Fdirection, Fobj]
        return [-10, [0,0], None]

class MoveTowards(Neuron):
    def __init__(self, testNAME, IO, look_range=10, weight=None, bias=None, connected=None, inputVal=None):
        Neuron.__init__(self, testNAME, IO, weight=None, bias=None, connected=None, inputVal=[])

    def Calc(self):
        tdir = [0,0]
        for sd in self.inputVal:
            tdir[0]+=sd[0]*sd[1][0]
            tdir[1]+=sd[0]*sd[1][1]
        tdir = GlobalVar.Normalize_dist(tdir)
        return tdir, 0, [], []
        #LChangePOS, LChangeFOOD, LRemoveFOOD, LRemoveCELL