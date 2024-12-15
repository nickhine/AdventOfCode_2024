import numpy as np

mapl = []
instr = ""
with open('d15.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        mapl.append(line)
    while True:
        line = f.readline().strip()
        if not line:
            break
        instr += line
lx = len(mapl[0])*2
ly = len(mapl)
mapa = np.zeros((ly,lx),dtype=int)
boxes = []
WALL = -100
FLOOR = -200
for i in range(ly):
    for j in range(lx):
        if j % 2 == 1:
            continue
        jp = int(j/2)
        if mapl[i][jp] == '#':
            mapa[i,j] = WALL
            mapa[i,j+1] = WALL
        if mapl[i][jp] == '.' or mapl[i][jp] == '@' or mapl[i][jp] == 'O':
            mapa[i,j] = FLOOR
            mapa[i,j+1] = FLOOR
        if mapl[i][jp] == '@':
            rx,ry = j,i
        if mapl[i][jp] == 'O':
            boxes.append((j,i))
boxes = np.array(boxes)
nboxes = len(boxes)

def add_boxes(mapa,mapb,boxes):
    mapb[:,:] = mapa[:,:]
    for ibox,box in enumerate(boxes):
        mapb[box[1],box[0]] = ibox
        mapb[box[1],box[0]+1] = ibox + nboxes

def print_map(mapb,rx,ry):
    mapstr = ""
    for i in range(ly):
        for j in range(lx):
            if i == ry and j == rx:
                mapstr += '@'
                continue
            if mapb[i,j] == WALL:
                mapstr += '#'
            elif nboxes > mapb[i,j] >= 0:
                mapstr += '['
            elif 2*nboxes > mapb[i,j] >= nboxes:
                mapstr += ']'
            elif mapb[i,j] == FLOOR:
                mapstr += '.'
        mapstr += '\n'
    print(mapstr)

dirch = ['>','v','<','^']
dp = [(1,0),(0,1),(-1,0),(0,-1)]
instra = np.zeros((len(instr)),dtype=int)
for i,inst in enumerate(instr):
    for j in range(4):
        if inst == dirch[j]:
            instra[i] = j

def box_in(p,mapb):
    if mapb[p[1],p[0]] >= 0:
        return mapb[p[1],p[0]] % nboxes
    else:
        return -1
    
spots = np.array([[0,0],[1,0]],dtype=int)

def push_boxes(rx,ry,inst,mapb,boxes):
    p = np.array((rx + dp[inst][0],ry + dp[inst][1]))
    i = box_in(p,mapb)
    if i < 0:
        return
    stuck = False
    moving = False
    pushed = np.zeros((nboxes),dtype=int)
    pushed[0] = i
    npshd = 1
    fpshd = 0
    while not stuck and not moving:
        moving = True
        for j in range(fpshd,npshd):
            oldpushd = npshd
            for spot in spots:
                q = np.array(boxes[pushed[j]][:])
                q += dp[inst] + spot
                if mapb[q[1],q[0]] == WALL:
                    stuck = True
                    break # found a wall
                k = box_in(q,mapb)
                if k >= 0 and not np.any(pushed[0:npshd] == k):
                    pushed[npshd] = k
                    npshd += 1
                    break
            if oldpushd != npshd:
                moving = False # not done yet, keep finding boxes
            else:
                fpshd = j
            if stuck:
                break
    if not stuck:
        for j in range(npshd):
            boxes[pushed[j]][:] += dp[inst][:]
    return moving and not stuck

def get_GPS(boxes):
    tot = 0
    for box in boxes:
        tot = tot + box[1]*100 + box[0]
    return tot

mapb = np.zeros((ly,lx),dtype=int)
add_boxes(mapa,mapb,boxes)
for inst in instra:
    moved = push_boxes(rx,ry,inst,mapb,boxes)
    if moved:
        add_boxes(mapa,mapb,boxes)
    if mapb[ry+dp[inst][1],rx+dp[inst][0]] == FLOOR:
        rx += dp[inst][0]
        ry += dp[inst][1]
print('Final GPS: ', get_GPS(boxes))