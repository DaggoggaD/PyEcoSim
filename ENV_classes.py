import pygame
from GlobalVariables import *
import math

class Food:
    def __init__(self, pos, energy):
        self.pos = pos
        self.energy = energy
        self.radius = 10
        self.sqID = None
        self.nearsqID = None
        self.Calc_sqid( )

    def Calc_sqid(self):
        pos = self.pos
        currentZoneX = math.floor(pos[0] / SquareDivSize)
        currentZoneY = math.floor(pos[1] / SquareDivSize)
        csqid = currentZoneX+int(width/SquareDivSize)*currentZoneY
        neighborsq = [csqid]

        neighborsq.append(csqid - lineWN)
        neighborsq.append(csqid + (lineWN))
        if csqid%lineWN==0:
            #neighborsq.append(csqid - 1)
            neighborsq.append(csqid + 1)
            neighborsq.append(csqid - (lineWN - 1))
            #neighborsq.append(csqid - (lineWN + 1))
            #neighborsq.append(csqid + (lineWN - 1))
            neighborsq.append(csqid + (lineWN + 1))
        elif csqid%lineWN==lineWN-1:
            neighborsq.append(csqid - 1)
            #neighborsq.append(csqid + 1)
            #neighborsq.append(csqid - (lineWN - 1))
            neighborsq.append(csqid - (lineWN + 1))
            neighborsq.append(csqid + (lineWN - 1))
            #neighborsq.append(csqid + (lineWN + 1))
        else:
            neighborsq.append(csqid - 1)
            neighborsq.append(csqid + 1)
            neighborsq.append(csqid - (lineWN - 1))
            neighborsq.append(csqid - (lineWN + 1))
            neighborsq.append(csqid + (lineWN - 1))
            neighborsq.append(csqid + (lineWN + 1))
        self.sqID = csqid
        self.nearsqID = neighborsq

    def Render_Text(self, what, color, where, font, canvas):
        text = font.render(what, 1, pygame.Color(color))
        canvas.blit(text, where)

    def DrawSelf(self, screen, font):
        clr = (6, 214, 160)
        """clrx = self.sqID * int(math.floor(255 / maxDivN))
        clry = self.sqID * int(math.floor(255 / maxDivN))
        clr = (clrx, clry, ((clrx + clry) / 2))
        """
        pygame.draw.circle(screen, clr, self.pos, self.radius)
        if DEBUG:
            self.Render_Text(str(self.sqID), (0, 0, 0), self.pos, font, screen)
