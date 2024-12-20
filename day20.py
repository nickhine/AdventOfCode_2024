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

def print_map(mapb,time,pos,path,npath):
    mapstr = ""
    for ip in range(len(path)):
        if path[ip,0]==0 and path[ip,1]==0:
            print('ERROR in path at ',ip)
    #print(path[0:20])
    for i in range(1,ly-1):
        for j in range(1,lx-1):
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
                    else:
                        print(path[index-3:index+3])
                        print('Error in path:',prev,path[index])
                    continue
            if mapb[i,j] >= 0 and mapb[i,j] < time:
                mapstr += '#' #chr(ord('0')+int(mapb[i,j]/4))
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
    mapbestpath[1,1,0,:] = stpos[:]
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
        #print(f"Path found Best path:{bestscore-1}")
        pass
    break
#print(mapbestpath[endpos[1],endpos[0],0:26],mapbestpath[endpos[1],endpos[0],npath-28:npath])
time = 0
mapt = np.zeros((ly,lx),dtype=int)
mapt[:,:] = -mapa[:,:]
dp1 = np.zeros(2,dtype=int)
dp2 = np.zeros(2,dtype=int)
for ipath,pos in enumerate(mapbestpath[endpos[1],endpos[0],1:mapbest[endpos[1],endpos[0]]]):
    mapt[pos[1],pos[0]] = ipath
    #print(ipath,mapt[pos[1],pos[0]])
ngoodcheats = 0
for x in range(1,lx-1):
    for y in range(1,ly-1):
        if mapt[y,x] == -1:
            for d1 in range(4):
                dp1[0] = dp[d1][0]
                dp1[1] = dp[d1][1]
                for d2 in range(4):
                    dp2[0] = dp[d2][0]
                    dp2[1] = dp[d2][1]
                    if mapt[y+dp1[1],x+dp1[0]] >= 0 and mapt[y+dp2[1],x+dp2[0]] >= 0:
                        cheatvalue = mapt[y+dp2[1],x+dp2[0]] - mapt[y+dp1[1],x+dp1[0]] - 2
                        if cheatvalue>=100:
                            ngoodcheats += 1
                            print(f'Cheat saving {cheatvalue} ps at {x},{y} from {x+dp1[0]}, {y+dp1[1]} to {x+dp2[0]}, {y+dp2[1]}')
#print_map(mapt,time,pos,mapbestpath[endpos[1],endpos[0]],mapbest[endpos[1],endpos[0]])
print('Cheats saving 100ps:',ngoodcheats)
