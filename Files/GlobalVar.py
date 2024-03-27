import pygame

pygame.init()

###Variables###

#Simulation variables
width = 500
height = 500
dt = 1
font = pygame.font.Font('freesansbold.ttf', 20)
sim_len = 15
sim_len = sim_len * 60
Walls = []

#Cell variables
metabolism = 0.2
mutation_chance = 10
debug = False


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
def Render_Text(what, color, where, canvas):
    text = font.render(what, 1, pygame.Color(color))
    canvas.blit(text, where)

#Calcs the average food between all cells.
def Average_cell_food(arr):
    tot = 0
    for v in arr:
        tot+=v.food
    return tot/len(arr)