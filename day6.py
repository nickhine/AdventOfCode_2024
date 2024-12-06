import numpy as np

with open('d6.dat') as f:
    lines = [line.rstrip() for line in f]
    lx = len(lines[0])
    ly = len(lines)
    map = np.zeros((lx,ly),dtype=int)
    for y in range(ly):
        for x in range(lx):
            map[x,y] = 1 if lines[y][x]=='#' else 0
            if lines[y][x]=='^':
                gx,gy = x,y
print(gx,gy)

def printmap(map,gx,gy,dir):
    print()
    for y in range(ly-1,-1,-1):
        for x in range(0,lx,1):
            if x==gx and y==gy:
                ch = vecstr[dir] 
            elif visited[x,y]==1:
                ch = 'X'
            elif map[x,y]==1:
                ch = '#'
            else:
                ch = '.'
            print(ch,end='')
        print()

def check_map(gx,gy,dir,map):
    onmap = True
    foundloop = False
    while(onmap):
        if visited[gx,gy]==1 and dirvisited[gx,gy,dir]==1:
            print('loop detected')
            foundloop = True
            break
        visited[gx,gy] = 1
        dirvisited[gx,gy,dir] = 1
        newx = gx+vec[dir][0]
        newy = gy+vec[dir][1]
        #printmap(map,gx,gy,dir)
        if newx<0 or newx>lx-1 or newy<0 or newy>ly-1:
            onmap = False
            break
        if map[newx,newy]==1:
            dir = (dir+1)%4
        else:
            gx,gy = newx,newy
    return foundloop

vec = [(0,-1),(1,0),(0,1),(-1,0)]
vecstr = ['^','>','v','<']
origmap = np.copy(map)
tot = 0
for py in range(ly):
    for px in range(lx):
        dir = 0
        visited = np.zeros((lx,ly),dtype=int)
        dirvisited = np.zeros((lx,ly,4),dtype=int)
        map = np.copy(origmap)
        print(px,py)
        if map[px,py]==1:
            continue
        map[px,py] = 1
        if check_map(gx,gy,dir,map):
            tot += 1

printmap(map,gx,gy,dir)
print(np.sum(visited),tot)