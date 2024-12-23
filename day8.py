import numpy as np

with open('d8.dat') as f:
    data = [line.rstrip() for line in f]
lx = len(data[0])
ly = len(data)
ant_grid = np.zeros((lx,ly),dtype=int)
antinodes = np.zeros_like(ant_grid,dtype=int)
antennae = {}
for y in range(ly):
    for x in range(lx):
        ch = data[ly-y-1][x]
        ant_grid[x,y] = ord(ch)
        if ant_grid[x,y] == ord('.'):
            ant_grid[x,y] = 0
        else:
            if ch not in antennae:
                antennae[ch] = []
            antennae[ch].append((x,y))

#print(ant_grid)
def printmap(map):
    print()
    for y in range(ly-1,-1,-1):
        for x in range(0,lx,1):
            ch = chr(map[x,y])
            if map[x,y] == 0:
                ch = '.'
            print(ch,end='')
        print()

#printmap(ant_grid)
#print(antennae)

for antch in antennae:
    for x1,y1 in antennae[antch]:
        for x2,y2 in antennae[antch]:
            if x1 == x2 and y1 == y2:
                continue
            for m in range(0,lx):
                if (x1 < x2 and y1 < y2) or (x1 > x2 and y1 > y2):
                    axp = max(x1,x2) + m*abs(x1-x2)
                    ayp = max(y1,y2) + m*abs(y1-y2)
                    axm = min(x1,x2) - m*abs(x1-x2)
                    aym = min(y1,y2) - m*abs(y1-y2)
                else:
                    axp = max(x1,x2) + m*abs(x1-x2)
                    ayp = min(y1,y2) - m*abs(y1-y2)
                    axm = min(x1,x2) - m*abs(x1-x2)
                    aym = max(y1,y2) + m*abs(y1-y2)
                #if antch == 'A':
                #    print(f'{antch} ({x1},{y1}) ({x2},{y2}) : ({axp},{ayp}) ({axm},{aym})')
                #    print(max(x1,x2),abs(x1-x2))
                if axp < lx and axp>=0 and ayp < ly and ayp>=0:
                    antinodes[axp,ayp] = ord('#')
                if axm < lx and axm>=0 and aym < ly and aym>=0:
                    antinodes[axm,aym] = ord('#')

#print(antinodes)
finalmap = np.copy(antinodes)
for y in range(ly):
    for x in range(lx):
        if antinodes[x,y] == 0:
            finalmap[x,y] = ant_grid[x,y]
        else:
            antinodes[x,y] = ord('#')
tot = np.count_nonzero(antinodes)
printmap(finalmap)
           
#with open('r8b.dat') as f:
#    data = [line.rstrip() for line in f]
#print('\n')
#for d in data:
#    print(d)

print(tot)