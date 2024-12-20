import numpy as np
from heapq import heappush,heappop,nlargest,nsmallest
from collections import deque
np.set_printoptions(threshold=np.inf,linewidth=np.inf)

mapl = []
with open('d20.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        mapl.append(line)

lx = len(mapl[0])
ly = len(mapl)
mapa = np.zeros((ly,lx),dtype=int)
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

def print_map(mapb,time,pos,path,npath,numpath=False):
    mapstr = ""
    for ip in range(len(path)):
        if path[ip,0]==0 and path[ip,1]==0:
            print('ERROR in path at ',ip)
    #print(path[0:20])
    for i in range(0,ly):
        for j in range(0,lx):
            if j == pos[0] and i == pos[1]:
                mapstr += '@'
                continue
            if j == stpos[0] and i == stpos[1]:
                mapstr += 'S'
                continue
            if j == endpos[0] and i == endpos[1]:
                mapstr += 'E'
                continue
            if (path[0:npath]==(j,i)).all(axis=1).any() and numpath:
                index = np.where((path[0:npath]==(j,i)).all(axis=1))[0][0]
                if index > 0:
                    if numpath:
                        mapstr += chr(ord('A')+int(index/(npath/58)))
                        continue
                    prev = path[index-1]
                    mdir = np.where((dp==path[index]-prev).all(axis=1))[0]
                    if len(mdir) > 0:
                        mapstr += dirch[mdir[0]]
                    else:
                        print(path[index-3:index+3])
                        print('Error in path:',prev,path[index])
                    continue
            if mapb[i,j] < -1:
                mapstr += 'C'
            elif mapb[i,j] == -1 or mapb[i,j] == 1:
                mapstr += '#' #chr(ord('0')+int(mapb[i,j]/4))
            elif mapb[i,j] == -999:
                mapstr += 'X'
            else:
                mapstr += '.'
        mapstr += '\n'
    print(mapstr,end='' )

dirch = ['>','v','<','^']
dp = [(1,0),(0,1),(-1,0),(0,-1)]
pos = np.zeros(2,dtype=int)
npos = np.zeros(2,dtype=int)
cdirs = np.zeros(4,dtype=int)
maxpath=10000
path = np.zeros((maxpath,2),dtype=int)
while True:
    dir = 0
    nodes = deque([])
    path[:][:] = -1
    path[0][:] = stpos[:]
    npath = 1
    pos[:] = stpos[:]
    ldir = 0
    pdir = 0
    score = 1
    bestscore = 100000
    mapbestpath = -np.ones((ly,lx,maxpath,2),dtype=int)
    mapbestpath[stpos[1],stpos[0],0,:] = stpos[:]
    mapbest = np.ones((ly,lx),dtype=int)*100000
    mapbest[stpos[1],stpos[0]] = 1
    while True:
        cdirs[:] = 0
        ddirs = [pdir,(pdir-1)%4,(pdir+1)%4]
        for idir in ddirs:
            if ddirs.index(idir) < ddirs.index(dir):
                continue # already visited
            npos = pos + dp[idir]
            if mapa[npos[1],npos[0]] == 1:
                continue # wall
            if score + 1 > mapbest[npos[1],npos[0]]:
                continue # better path there already found
            if mapbest[npos[1],npos[0]] + 1 < score:
                #cdirs[:] = 0 # better path to here!
                npath = mapbest[npos[1],npos[0]]
                mapbestpath[pos[1],pos[0],0:npath,:] = mapbestpath[npos[1],npos[0],0:npath,:] # copy path
                mapbestpath[pos[1],pos[0],npath,:] = pos[:]
                npath += 1
                mapbest[npos[1],npos[0]] = npath
                break
            cdirs[idir] = 1
        if np.sum(cdirs) > 1:
            skipped1st = False
            for dm in ddirs:
                d = dm%4
                if cdirs[d]:
                    if not skipped1st:
                        skipped1st = True
                    else:
                        besttohere = True
                        del_list = []
                        for inode,nn in enumerate(nodes):
                            if pos[0]==nn[3] and pos[1]==nn[4]:
                                if score>=nn[0]:
                                    besttohere = False
                                    break
                                elif score<nn[0]:
                                    del_list.append(inode)
                        if besttohere:
                            for inode in reversed(del_list):
                                del nodes[inode]
                            nodes.append((score,d,pdir,pos[0],pos[1]))
                            #print_map(mapa,time,pos,path,npath)
                            #print(f'Added node at {pos},{d}: {len(nodes)},{score},{npath}')
                        #heappush(nodes,(score,d,pdir,pos[0],pos[1]))
        if np.sum(cdirs) == 0:
            if len(nodes) == 0:
                print('Dead end and no more nodes, len(nodes)=',len(nodes))
                break
            while True:
                #print(f'Dead end at {pos}',end="")
                #print_map(mapa,time,pos,path,npath)
                #score,dir,pdir,pos[0],pos[1] = heappop(nodes)
                p = np.random.rand()
                if p < 0.3:
                    score,dir,pdir,pos[0],pos[1] = nodes.popleft()
                else:
                    score,dir,pdir,pos[0],pos[1] = nodes.pop()
                #print(f', backtracking {p<0.3} to ',pos,'len(nodes)=',len(nodes),'score=',score)
                npath = score #mapbest[pos[1],pos[0]]
                if score > mapbest[pos[1],pos[0]]:
                    #print(f'Skipping node, score={score}, mapbest={mapbest[pos[1],pos[0]]}')
                    continue
                path[0:npath] = mapbestpath[pos[1],pos[0],0:npath,:]
                ldir = dir
                break
            continue
        for ndir in ddirs:
            mdir = ndir%4
            if cdirs[mdir]:
                dir = mdir
                break
        pdir = dir
        npos = pos + dp[dir]
        ldir = 0
        pos[:] = npos[:]
        #print_map(mapa,pos,time,path,npath)
        npath += 1
        score += 1
        path[npath-1][:] = pos[:]
        if score < mapbest[pos[1],pos[0]]:
            mapbest[pos[1],pos[0]] = score
            mapbestpath[pos[1],pos[0],0:npath,:] = path[0:npath,:]
        if (pos==endpos).all() or score > bestscore:
            if score < bestscore:
                #print("New best score:",score-1,' (nodes=',len(nodes),')')
                #print_map(mapa,time,pos,path,npath)
                bestscore = score
            if len(nodes) == 0:
                #print('No more nodes')
                break
            while True:
                #score,dir,pdir,pos[0],pos[1] = heappop(nodes)
                score,dir,pdir,pos[0],pos[1] = nodes.pop()
                print('Returning to ',pos,'len(nodes)=',len(nodes))
                #npath = mapbest[pos[1],pos[0]]
                npath = score
                if score > mapbest[pos[1],pos[0]]:
                    #print('Skipping node')
                    continue
                path[0:npath] = mapbestpath[pos[1],pos[0],0:npath,:]
                ldir = dir
                break
            continue

    if bestscore == 5000:
        print(f'No path found')
    else:
        print(f"Path found Best path:{bestscore-1}")
        pass
    break
#print(mapbestpath[endpos[1],endpos[0],0:26],mapbestpath[endpos[1],endpos[0],npath-28:npath])
time = 0
mapt = np.ones((ly,lx),dtype=int)*-1
mapt[stpos[1],stpos[0]] = 0
for y in range(0,ly):
    for x in range(0,lx):
        if mapa[y,x] == 1:
            mapt[y,x] = -1
for ipath,pos in enumerate(mapbestpath[endpos[1],endpos[0],0:mapbest[endpos[1],endpos[0]]]):
    mapt[pos[1],pos[0]] = ipath
print_map(mapt,time,pos,mapbestpath[endpos[1],endpos[0],0:mapbest[endpos[1],endpos[0]]],mapbest[endpos[1],endpos[0]],numpath=True)
print('stpos:',stpos)
print(mapbestpath[endpos[1],endpos[0],0:10])
dse = np.zeros(2,dtype=int)
cspos = np.zeros(2,dtype=int) # cheat start pos
cepos = np.zeros(2,dtype=int) # cheat end pos
cheatfound = {}
ngoodcheats = 0
goodcheatval = 100
cheatcount = {}
#for x in range(1,lx-1):
#    for y in range(1,ly-1):
for ipath,cspos in enumerate(mapbestpath[endpos[1],endpos[0],0:mapbest[endpos[1],endpos[0]]]):
        if mapt[cspos[1],cspos[0]] == -1:
            continue # can't start in wall
        cheatfound = {}
        for dse[0] in range(-20,21):
            for dse[1] in range(-20,21):
                cepos[:] = cspos[:] + dse[:]
                if cepos[1] < 1 or cepos[1] >= ly or cepos[0] < 1 or cepos[0] >= lx:
                    continue # out of bounds
                if mapt[cepos[1],cepos[0]] == -1: # check end pos of cheat not in wall
                    continue
                dist = abs(dse[0]) + abs(dse[1])
                if dist > 20:
                    continue # too far
                cheatvalue = mapt[cepos[1],cepos[0]] - mapt[cspos[1],cspos[0]] - dist
                if cheatvalue >= goodcheatval:
                    if (cepos[1],cepos[0]) in cheatfound:
                        if cheatvalue<cheatfound[(cepos[1],cepos[0])]:
                            cheatfound[(cepos[1],cepos[0])] = cheatvalue
                    else:
                        cheatfound[(cepos[1],cepos[0])] = cheatvalue
                    #print(f'Cheat saving {cheatvalue} ps, dist={dist} from {cspos}({mapt[cspos[1],cspos[0]]}) to {cepos}({mapt[cepos[1],cepos[0]]}), {dse}')
        #mapvis = mapa.copy()
        for cepos[0] in range(1,lx-1):
            for cepos[1] in range(1,ly-1):
                if (cepos[1],cepos[0]) not in cheatfound:
                    continue
                cheatvalue = cheatfound[cepos[1],cepos[0]]
                #if cheatvalue > 0:
                #    mapvis[cepos[1],cepos[0]] = -cheatvalue
                ngoodcheats += 1
                if cheatvalue in cheatcount:
                    cheatcount[cheatvalue] += 1
                else:
                    cheatcount[cheatvalue] = 1
                #print(f'Cheat saving {cheatvalue} ps from {cspos}({mapt[cspos[1],cspos[0]]}) to {cepos}({mapt[cepos[1],cepos[0]]})')
        #print("\n\n\n",cspos)
        #print_map(mapvis,time,cspos,mapbestpath[endpos[1],endpos[0]],mapbest[endpos[1],endpos[0]],numpath=False)

#print_map(mapa,time,pos,mapbestpath[endpos[1],endpos[0]],mapbest[endpos[1],endpos[0]])
#for cheatvalue in sorted(cheatcount.keys()):
#    print(f'Cheats saving {cheatvalue} ps: {cheatcount[cheatvalue]}')
print(f'Cheats saving {goodcheatval} ps or more: {ngoodcheats}')
# 994165 too low ~1200000 too high 1022345 wrong 1022005 wrong 1026104 wrong
# 9452 best path, 9424 = path length 28