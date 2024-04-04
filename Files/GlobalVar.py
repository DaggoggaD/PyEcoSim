import pygame
import math
pygame.init()

###Variables###

#Simulation variables
width = 900
height = 900
dt = 1
font = pygame.font.SysFont("segoeuisymbol", 20)
sim_len = 15
sim_len = sim_len * 60
Walls = []
Area_Sub = 5
foodN = 300

#Cell variables
metabolism = 0.1
mutation_chance = 10
debug = False
maxGeneVal = 5*5+5*5
###Functions###

#Normalizes previously calculated distances.
def Normalize_dist(dist):
    adir = [abs(dist[0]), abs(dist[1])]
    mdir = max(adir)
    try:
        ndir = [dist[0] / mdir, dist[1] / mdir]
    except:
        ndir = [0,0]
    return ndir

#Renders text to the canvas.
def Render_Text(what, color, where, canvas,right=False):
    text = font.render(what, 1, pygame.Color(color))
    if right:
        text_width = text.get_width( )
        canvas.blit(text, [where[0]-text_width, where[1]])
    else:
        canvas.blit(text, where)

#Calcs the average food between all cells.
def Average_cell_food(arr):
    tot = 0
    for v in arr:
        tot+=v.food
    return tot/len(arr)

#Trasform a single int to a (r,g,b) color
def num_to_rgb(val, max_val=3):
    if (val > max_val):
        raise ValueError("val must not be greater than max_val")
    if (val < 0 or max_val < 0):
        raise ValueError("arguments may not be negative")

    i = (val * 255 / max_val);
    r = round(math.sin(0.024 * i + 0) * 127 + 128);
    g = round(math.sin(0.024 * i + 2) * 127 + 128);
    b = round(math.sin(0.024 * i + 4) * 127 + 128);
    return (r,g,b)