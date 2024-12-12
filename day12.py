import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=np.inf)
with open('d12.dat') as f:
    data = f.read().splitlines()
lx = len(data[0])
ly = len(data)
data = np.array([list(x) for x in data],dtype=str)
pmap_full = np.zeros((ly,lx),dtype=int)
pmap = np.zeros((ly,lx),dtype=int)
plants = np.unique(data.flat)
for ip,plant in enumerate(plants):
    pmap_full[data == plant] = ip + 1

def inside(x,y,cmap,vtarg):
    if x >= 0 and x < lx and y >= 0 and y < ly:
        return cmap[y,x] == vtarg
    else:
        return False

def fill(x,y,cmap,vtarg,vfill):
    if not inside(x,y,cmap,vtarg):
        return
    seeds = [[x,x,y,1],[x,x,y-1,-1]]
    while len(seeds) > 0:
        x1,x2,yp,dy = seeds.pop()
        xp = x1
        if inside(xp,yp,cmap,vtarg):
            while inside(xp-1,yp,cmap,vtarg):
                cmap[yp,xp-1] = vfill
                xp = xp - 1
            if xp < x1:
                seeds.append([xp, x1-1, yp - dy, -dy])
        while x1 <= x2:
            while inside(x1, yp, cmap, vtarg):
                cmap[yp,x1] = vfill
                x1 = x1 + 1
            if x1 > xp:
                seeds.append([xp, x1-1, yp + dy, dy])
            if x1 - 1 > x2:
                seeds.append([x2 + 1, x1 - 1, yp - dy, -dy])
            x1 = x1 + 1
            while x1 < x2 and not inside(x1, yp, cmap, vtarg):
                x1 = x1 + 1
            xp = x1

dirs = np.array([(0,1),(1,0),(0,-1),(-1,0)])
def find_perim(pmap,vtarg):
    perim = 0
    rlist = np.where(pmap==vtarg)
    for rx,ry in zip(rlist[1],rlist[0]):
        for i in range(4):
            x,y = rx + dirs[i][0], ry + dirs[i][1]
            if not inside(x,y,pmap,-1):
                perim = perim + 1
    return perim,rlist

pcorner = np.array([0,1,1,0,1,0,2,1,1,2,0,1,0,1,1,0],dtype=int)
bits = np.array([1,2,4,8])
def find_edges(pmap,vtarg):
    corners = 0
    ploc = np.zeros((2,2),dtype=int)
    rlist = np.where(pmap==vtarg)
    minx = np.min(rlist[1])
    maxx = np.max(rlist[1])
    miny = np.min(rlist[0])
    maxy = np.max(rlist[0])
    for ry in range(miny,maxy+2):
        for rx in range(minx,maxx+2):
            ploc[:,:] = 0
            if rx > 0 and ry > 0:
                ploc[0,0] = pmap[ry-1,rx-1]
            if rx <= lx-1 and ry > 0:
                ploc[0,1] = pmap[ry-1,rx]
            if rx > 0 and ry <= ly-1:
                ploc[1,0] = pmap[ry,rx-1]
            if rx <= lx-1 and ry <= ly-1:
                ploc[1,1] = pmap[ry,rx]
            pval = np.sum((ploc==-1).flatten()*bits)
            corners = corners + pcorner[pval]
    return corners,rlist

tot1,tot2 = 0,0
# loop over plants
for ipp,plant in enumerate(plants):
    ip = ipp + 1
    pmap[:,:] = 0
    # Make a map of just this plant
    pmap[pmap_full == ip] = ip
    while np.any(pmap>0):
        # Find first remaining plant of this type in map
        plist = np.where(pmap>0)
        oy,ox = plist[0][0],plist[1][0]
        # Flood fill to find connected region
        fill(ox,oy,pmap,ip,-1)
        # Find area of region
        area = np.sum(pmap==-1)
        # Find perimeter of region
        perim,rlist = find_perim(pmap,-1)
        # Find number of edges of region
        edges,rlist = find_edges(pmap,-1)
        tot1 += area*perim
        tot2 += area*edges
        # Clear region from map of this plant
        pmap[pmap == -1] = 0
print(tot1,tot2)