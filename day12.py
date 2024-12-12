import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=np.inf)

with open('d12.dat') as f:
    data = f.read().splitlines()

print(data)
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

regions = []
tot = 0
for ipp,plant in enumerate(plants):
    ip = ipp + 1
    pmap[:,:] = 0
    pmap[pmap_full == ip] = ip
    while np.any(pmap>0):
        plist = np.where(pmap>0)
        # Flood fill to find connected region)
        oy,ox = plist[0][0],plist[1][0]
        fill(ox,oy,pmap,ip,-1)
        perim,rlist = find_perim(pmap,-1)
        area = np.sum(pmap == -1)
        minx = np.min(rlist[1])
        maxx = np.max(rlist[1])
        miny = np.min(rlist[0])
        maxy = np.max(rlist[0])
        if ip==24:
            print(-pmap[miny:maxy+1,minx:maxx+1])
            print(f'ip={ip} plant={plant} ox,oy={ox},{oy} area={area} perim={perim} prod={area*perim}')
        tot += area*perim
        pmap[pmap == -1] = 0
print(tot)