import numpy as np

mapl = []
instr = ""
with open('d16.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        mapl.append(line)

lx = len(mapl[0])
ly = len(mapl)
mapa = np.zeros((ly,lx),dtype=int)
mapbest = np.zeros((ly,lx,4),dtype=int)
onbest = np.zeros((ly,lx),dtype=int)
mapbest[:][:] = 100000
stpos = np.zeros(2,dtype=int)
endpos = np.zeros(2,dtype=int)
for i in range(ly):
    for j in range(lx):
        if mapl[i][j] == '#':
            mapa[i,j] = 1
        if mapl[i][j] == '.' or mapl[i][j] == 'S' or mapl[i][j] == 'E':
            mapa[i,j] = 0
        if mapl[i][j] == 'S':
            stpos[0] = j
            stpos[1] = i
        if mapl[i][j] == 'E':
            endpos[0] = j
            endpos[1] = i

def print_map(mapb,pos,path,npath):
    mapstr = ""
    for i in range(ly):
        for j in range(lx):
            if j == pos[0] and i == pos[1]:
                mapstr += '@'
                continue
            if j == stpos[0] and i == stpos[1]:
                mapstr += 'S'
                continue
            if j == endpos[0] and i == endpos[1]:
                mapstr += 'E'
                continue
            if (path[0:npath]==(j,i)).all(axis=1).any():
                index = np.where((path[0:npath]==(j,i)).all(axis=1))[0][0]
                if index > 0:
                    prev = path[index-1]
                    mdir = np.where((dp==path[index]-prev).all(axis=1))[0]
                    if len(mdir) > 0:
                        mapstr += dirch[mdir[0]]
                    continue
            if mapb[i,j] == 1:
                mapstr += '#'
            else:
                mapstr += '.'
        mapstr += '\n'
    print(mapstr,end='' )

def turn_cost(dir,pdir):
    cost = 0
    if dir != pdir:
        x = abs(dir-pdir)
        x = x if x<3 else 1
        cost = x*1000
    return cost

dirch = ['>','v','<','^']
dp = [(1,0),(0,1),(-1,0),(0,-1)]
pos = np.zeros(2,dtype=int)
npos = np.zeros(2,dtype=int)
dir = 0
cdirs = np.zeros(4,dtype=int)
nodes = []

maxpath=1000
path = np.zeros((maxpath,2),dtype=int)
path[:][:] = -1
path[0][:] = stpos[:]
npath = 1
pos[:] = stpos[:]
nodes = []
ldir = 0
pdir = 0
score = 0
bestnpath = 1000000
bestscore = 1000000
bestpath = np.zeros((maxpath,2),dtype=int)
from heapq import heappush, heappop
while True:
    cdirs[:] = 0
    ddirs = [pdir,(pdir-1)%4,(pdir+1)%4]
    for idir in ddirs:
        if ddirs.index(idir) < ddirs.index(dir):
            continue # already visited
        npos = pos + dp[idir]
        if mapa[npos[1],npos[0]] == 1:
            continue # wall
        if score + turn_cost(idir,dir) + 1 > mapbest[npos[1],npos[0],idir]:
            continue # better path here already found
        cdirs[idir] = 1
    if np.sum(cdirs) > 1:
        skipped1st = False
        for dm in ddirs:
            d = dm%4
            if cdirs[d]:
                if not skipped1st:
                    skipped1st = True
                else:
                    nodes.append((score,path[0:npath].copy(),d,pdir))
                    checksum = np.sum(path[0:npath,0]*np.arange(npath)) + np.sum(path[0:npath,1]*np.arange(npath))*1000
                    #print(score,npath,d,pdir,checksum)
                    #heappush(nodes,(score,npath,d,pdir,checksum,path[0:npath].copy()))
    if np.sum(cdirs) == 0:
        if len(nodes) == 0:
            print('Dead end and no more nodes')
            break
        score,lp,dir,pdir = nodes.pop(0)
        #print('nodes=',nodes)
        #try:
        #    score,npath,dir,pdir,_,lp = heappop(nodes)
        #except:
        #    print("Error in heappop")
        #    for nn in nodes:
        #        print(nn[0:7])
        ldir = dir
        npath = len(lp)
        path[0:npath] = lp[0:npath]
        pos[:] = path[npath-1][:]
        continue
    for ndir in ddirs:
        mdir = ndir%4
        if cdirs[mdir]:
            dir = mdir
            break
    score += turn_cost(dir,pdir)
    pdir = dir
    npos = pos + dp[dir]
    score += 1
    ldir = 0
    pos[:] = npos[:]
    if score < mapbest[pos[1],pos[0],dir]:
        mapbest[pos[1],pos[0],dir] = score
    path[npath][:] = pos[:]
    npath += 1
    if (pos==endpos).all() or score > bestscore:
        if score == bestscore:
            #print("Equal best score:",score,' (nodes=',len(nodes),')')
            for i in range(npath):
                onbest[path[i][1],path[i][0]] = 1
        if score < bestscore:
            print("New best score:",score,' (nodes=',len(nodes),')')
            #print_map(mapa,pos,path,npath)
            onbest[:,:] = 0
            for i in range(npath):
                onbest[path[i][1],path[i][0]] = 1
            bestscore = score
            bestnpath = npath
            bestpath[:,:] = path[:,:]
        if len(nodes) == 0:
            print('No more nodes')
            break
        score,lp,dir,pdir = nodes.pop(0)
        #score,npath,dir,pdir,_,lp = heappop(nodes)
        ldir = dir
        npath = len(lp)
        path[0:npath] = lp
        pos[:] = path[npath-1][:]
        continue

print("\n\n\nBest path:",bestnpath,bestscore)
print_map(mapa,endpos,bestpath,bestnpath)
print('onbest=',np.sum(onbest))
