import pygame
pygame.init()

#variables
width = 500
height = 500
dt = 1
font = pygame.font.Font('freesansbold.ttf', 25)

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




#cell variables
metabolism = 1.5