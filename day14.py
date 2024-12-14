import numpy as np
import re
np.set_printoptions(threshold=np.inf,linewidth=np.inf)
with open("d14.dat") as f:
    data = f.readlines()
nrobots = len(data)
robotpos = np.zeros((nrobots,2),dtype=int)
robotvel = np.zeros((nrobots,2),dtype=int)
for i,l in enumerate(data):
    ls = l.strip()
    rproc = re.split(r'[=|,| ]', l.strip())
    robotpos[i,:] = rproc[1:3]
    robotvel[i,:] = rproc[4:6]
lx = 101
ly = 103
cmap = np.zeros((ly,lx),dtype=int)
qb = np.array(((0,int(lx/2),0,int(ly/2)), # upper left
               (int(lx/2+1),lx,0,int(ly/2)), # upper right
               (0,int(lx/2),int(ly/2+1),ly), # lower left
               (int(lx/2+1),lx,int(ly/2+1),ly))) # lower right
q=1
for t in range(0,10000):
    finalpos = np.mod(robotpos + robotvel*t,(lx,ly))
    inq = np.zeros(4,dtype=int)
    for i in range(nrobots):
        for q in range(4):
            inq[q] += qb[q,0]<=finalpos[i,0]<qb[q,1] and qb[q,2]<=finalpos[i,1]<qb[q,3]
    if t==100:
        print(t,inq,np.prod(inq))
    if True:
        cmap[:,:] = 0
        for i in range(nrobots):
            cmap[finalpos[i,1],finalpos[i,0]] += 1
        printit = False
        for y in range(ly):
            for x in range(0,lx-10):
                if all(cmap[y,x:x+10]):
                    printit = True
        if (printit):
            print(t)
            #print('\n'.join(''.join(str(cell) for cell in row) for row in cmap))