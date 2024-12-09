import numpy as np
np.set_printoptions(linewidth=np.inf)
with open("d9.dat") as f:
    inp = f.read()+"0"
nf = int(len(inp)/2)
lens = np.zeros(nf,dtype='int')
gaps = np.zeros(nf,dtype='int')
for i in range(0,int(len(inp)/2)):
    lens[i] = inp[2*i]
    gaps[i] = inp[2*i+1]
disk = np.zeros(np.sum(lens)+np.sum(gaps),dtype='int')
disk[:] = -1
j = 0
for i in range(0,nf):
    disk[j:j+lens[i]] = i
    j += lens[i]+gaps[i]
p = 0
for j in range(len(disk)-1,-1,-1):
    for k in range(p,j):
        if disk[k] == -1:
            p = k
            disk[k] = disk[j]
            disk[j] = -1
            break
    if p == j:
        break
    print(disk)
checksum = 0
for j in range(0,len(disk)):
    if disk[j] == -1:
        break
    checksum += j*disk[j]
print(checksum)