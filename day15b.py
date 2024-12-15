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
for i in range(ly):
    for j in range(lx):
        if j % 2 == 1:
            continue
        jp = int(j/2)
        if mapl[i][jp] == '#':
            print(i,j,jp,mapa.shape)
            mapa[i,j] = 1
            mapa[i,j+1] = 1
        if mapl[i][jp] == '.' or mapl[i][jp] == '@' or mapl[i][jp] == 'O':
            mapa[i,j] = 0
            mapa[i,j+1] = 0
        if mapl[i][jp] == '@':
            rx,ry = j,i
        if mapl[i][jp] == 'O':
            boxes.append((j,i))
boxes = np.array(boxes)
print(boxes)
print(mapa)

def add_boxes(mapa,mapb,boxes):
    mapb[:,:] = mapa[:,:]
    for box in boxes:
        mapb[box[1],box[0]] = 2
        mapb[box[1],box[0]+1] = 3

def print_map(mapb,rx,ry):
    mapstr = ""
    for i in range(ly):
        for j in range(lx):
            if i == ry and j == rx:
                mapstr += '@'
                continue
            if mapb[i,j] == 1:
                mapstr += '#'
            elif mapb[i,j] == 2:
                mapstr += '['
            elif mapb[i,j] == 3:
                mapstr += ']'
            else:
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
print(instra)

def box_in(p,boxes):
    for ibox,box in enumerate(boxes):
        if (box==p).all():
            return ibox
        if (box+np.array((1,0))==p).all():
            return ibox
    return -1

def push_boxes(rx,ry,inst,mapb,boxes):
    p = np.array((rx + dp[inst][0],ry + dp[inst][1]))
    i = box_in(p,boxes)
    if i < 0:
        return
    #print(f"Pushing box {i}")
    stuck = False
    moving = False
    pushed = [i]
    npshd = 1
    while not stuck and not moving:
        moving = True
        for j in range(npshd-1,-1,-1):
            oldpushd = npshd
            for spots in (0,1):
                q = np.array(boxes[pushed[j]][:])
                if spots==1:
                    q[0] += 1
                q += dp[inst]
                #print(boxes)
                if mapb[q[1],q[0]] == 1:
                    stuck = True
                    break # found a wall
                if mapb[q[1],q[0]] == 2 or mapb[q[1],q[0]] == 3:
                    k = box_in(q,boxes)
                    if k < 0:
                        continue
                    if k not in pushed:
                        pushed.append(k)
                        npshd += 1
                        break
            if oldpushd != npshd:
                moving = False # not done yet, keep finding boxes
    if not stuck:
        #print(f'Moving boxes {pushed}')
        for j in range(npshd):
            boxes[pushed[j]][:] += dp[inst][:]
    return moving and not stuck

def get_GPS(boxes):
    tot = 0
    # The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map.
    for box in boxes:
        tot = tot + box[1]*100 + box[0]
    return tot

mapb = np.zeros((ly,lx),dtype=int)
add_boxes(mapa,mapb,boxes)
print("Initial state:")
print_map(mapb,rx,ry)
for inst in instra:
    print(f"Move {dirch[inst]}:")
    mapb[:,:] = mapa[:,:]
    add_boxes(mapa,mapb,boxes)
    if mapa[ry+dp[inst][1],rx+dp[inst][0]] == 1:
        pass
        #print("Cannot move")
    else:
        moving = push_boxes(rx,ry,inst,mapb,boxes)
        if moving:
            #print_map(mapb,rx,ry)
            add_boxes(mapa,mapb,boxes)
        if mapb[ry+dp[inst][1],rx+dp[inst][0]] == 0:
            rx += dp[inst][0]
            ry += dp[inst][1]
            #print("Moved")
        if moving:
            pass #print_map(mapb,rx,ry)
    #print("")
print('Final GPS: ', get_GPS(boxes))