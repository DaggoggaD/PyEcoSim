import pygame
pygame.init()

#variables
width = 500
height = 500
dt = 1
font = pygame.font.Font('freesansbold.ttf', 20)

#functions
def Normalize_dist(dist):
    adir = [abs(dist[0]), abs(dist[1])]
    mdir = max(adir)
    try:
        ndir = [dist[0] / mdir, dist[1] / mdir]
    except:
        ndir = [0,0]
    return ndir

def Render_Text(what, color, where, canvas):
    text = font.render(what, 1, pygame.Color(color))
    canvas.blit(text, where)

def Average_cell_food(arr):
    tot = 0
    for v in arr:
        tot+=v.food
    return tot/len(arr)

#cell variables
metabolism = 0.7
mutation_chance = 10 #a number extracted between 0-100, if num is less than mutation_chance it changes
debug = False