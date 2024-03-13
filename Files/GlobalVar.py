#functions
def Normalize_dist(dist):
    adir = [abs(dist[0]), abs(dist[1])]
    mdir = max(adir)
    try:
        ndir = [dist[0] / mdir, dist[1] / mdir]
    except:
        ndir = [0,0]
    return ndir


#variables
width = 500
height = 500
dt = 1


#cell variables
metabolism = 1.5