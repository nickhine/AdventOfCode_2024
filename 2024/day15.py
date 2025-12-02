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
    
lx = len(mapl[0])
ly = len(mapl)
mapa = np.zeros((ly,lx),dtype=int)
boxes = []
for i in range(ly):
    for j in range(lx):
        if mapl[i][j] == '#':
            mapa[i,j] = 1
        if mapl[i][j] == '.' or mapl[i][j] == '@' or mapl[i][j] == 'O':
            mapa[i,j] = 0
        if mapl[i][j] == '@':
            rx,ry = j,i
        if mapl[i][j] == 'O':
            boxes.append((j,i))
boxes = np.array(boxes)
print(boxes)
print(mapa)
dirch = ['>','v','<','^']
dp = [(1,0),(0,1),(-1,0),(0,-1)]
instra = np.zeros((len(instr)),dtype=int)
for i,inst in enumerate(instr):
    for j in range(4):
        if inst == dirch[j]:
            instra[i] = j
print(instra)

def add_boxes(mapa,mapb,boxes):
    mapb[:,:] = mapa[:,:]
    for box in boxes:
        mapb[box[1],box[0]] = 2

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
                mapstr += 'O'
            else:
                mapstr += '.'
        mapstr += '\n'
    print(mapstr)

def push_boxes(rx,ry,inst,mapb,boxes):
    p = np.array((rx + dp[inst][0],ry + dp[inst][1]))
    for i,box in enumerate(boxes):
        if (box==p).all():
            print("Pushing box")
            while p[0] >= 0 and p[0] < lx and p[1] >= 0 and p[1] < ly:
                p += dp[inst]
                if mapb[p[1],p[0]] == 1:
                    break # found a wall
                if mapb[p[1],p[0]] == 2:
                    continue # found a box, hop over it
                if mapb[p[1],p[0]] == 0:
                    boxes[i] = p # found an empty space, move box to here
                    return True
    return False # no box can be pushed

def get_GPS(boxes):
    tot = 0
    # The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map.
    for box in boxes:
        tot = tot + box[1]*100 + box[0]
    return tot

mapb = np.zeros((ly,lx),dtype=int)
for inst in instra:
    print(f"Move {dirch[inst]}:")
    mapb[:,:] = mapa[:,:]
    add_boxes(mapa,mapb,boxes)
    if mapa[ry+dp[inst][1],rx+dp[inst][0]] == 1:
        pass
        #print("Cannot move")
    else:
        if push_boxes(rx,ry,inst,mapb,boxes):
            add_boxes(mapa,mapb,boxes)
        if mapb[ry+dp[inst][1],rx+dp[inst][0]] == 0:
            rx += dp[inst][0]
            ry += dp[inst][1]
            #print("Moved")
    #print_map(mapb,rx,ry)
    #print("")
print('Final GPS: ', get_GPS(boxes))