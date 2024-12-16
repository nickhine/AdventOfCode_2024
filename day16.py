import numpy as np

mapl = []
instr = ""
with open('t16b.dat') as f:
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
#print('stpos,endpos=',stpos,endpos)

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
                    #print(index,path[0:npath])
                    #print(path[index],prev)
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
    if dir != pdir:
        x = abs(dir-pdir)
        x = x if x<3 else 1
        score = x*1000
        #print(pos,endpos,'Turn',dirch[pdir],'->',dirch[dir],'score:',score)
    else:
        score = 0
    return score

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
worstbt = 0
bestnpath = 100000
bestscore = 100000
bestpath = np.zeros((maxpath,2),dtype=int)
while True:
    cdirs[:] = 0
    for i in range(ldir,4):
        npos = pos + dp[i]
        if mapa[npos[1],npos[0]] == 1:
            continue
        #if pos[0] == 15 and pos[1] == 7 and score<11090:
        #    print('Checking pos',pos,'i',i,'dir',dir,'npos',npos,'mapbest',mapbest[npos[1],npos[0]],'score',score,turn_cost(i,dir),'cdirs',cdirs)
        if score + turn_cost(i,dir) > mapbest[npos[1],npos[0],i]:
            continue
        pathcheck = (path[0:npath]==npos).all(axis=1).any()
        #print(i,npos,path[0:npath],pathcheck)
        cdirs[i] = (mapa[npos[1],npos[0]] != 1 and not pathcheck)
    if np.sum(cdirs) > 1:
        skipped1st = False
        #for dm in range(4): 
        for dm in [0,1,2,3]:
            d = dm%4
            if cdirs[d]:
                if not skipped1st:
                    skipped1st = True
                else:
                    nodes.append((path[0:npath].copy(),d,pdir,score))
                    #print('adding node ',len(nodes),' at pos',pos,'npath',npath,'dir',d,'pdir',pdir,'score',score)
        #print_map(mapa,pos,path,npath)
        #print("Intersection at ",pos,": available dirs:",cdirs)
    if np.sum(cdirs) == 0:
        if len(nodes) == 0:
            print('Dead end and no more nodes')
            break
        lp,ldir,pdir,score = nodes.pop(0)
        dir = ldir
        npath = len(lp)
        path[0:npath] = lp[0:npath]
        pos[:] = path[npath-1][:]
        #print('Backtracking to:',pos,'ldir:',ldir,'path length:',npath,'score:',score)
        #print_map(mapa,pos,path,npath)
        continue
    #for ndir in range(4):
    for ndir in [0,1,2,3]:
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
    #print('pos=',pos,'dir=',dirch[dir],'score=',score)
    if score < mapbest[pos[1],pos[0],dir]:
        mapbest[pos[1],pos[0],dir] = score
    path[npath][:] = pos[:]
    npath += 1
    if (pos==endpos).all():
        #print("End, score =",score)
        if score == bestscore:
            print("Equal best score:",score,' (nodes=',len(nodes),')')
            #if bestscore<91000:
            #    print_map(mapa,pos,path,npath)
            for i in range(npath):
                onbest[path[i][1],path[i][0]] = 1
        if score < bestscore:
            print("New best score:",score,' (nodes=',len(nodes),')')
            print_map(mapa,pos,path,npath)
            onbest[:,:] = 0
            for i in range(npath):
                onbest[path[i][1],path[i][0]] = 1
            bestscore = score
            bestnpath = npath
            bestpath[:,:] = path[:,:]
        if len(nodes) == 0:
            print('No more nodes')
            break
        lp,ldir,pdir,score = nodes.pop(0)
        npath = len(lp)
        path[0:npath] = lp
        pos[:] = path[npath-1][:]
        continue
    #print_map(mapa,pos,path,npath)

print("\n\n\nBest path:",bestnpath,bestscore)
print_map(mapa,endpos,bestpath,bestnpath)
print('onbest=',np.sum(onbest))
