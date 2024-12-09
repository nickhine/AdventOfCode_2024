import numpy as np
np.set_printoptions(linewidth=np.inf)
with open("d9.dat") as f:
    inp = f.read()+"0"
nf = int(len(inp)/2)
start = np.zeros(nf,dtype='int')
lens = np.zeros(nf,dtype='int')
gaps = np.zeros(nf,dtype='int')
for i in range(0,int(len(inp)/2)):
    lens[i] = inp[2*i]
    gaps[i] = inp[2*i+1]
disk = np.zeros(np.sum(lens)+np.sum(gaps),dtype='int')
disk[:] = -1
j = 0
for i in range(0,nf):
    start[i] = j
    disk[j:j+lens[i]] = i
    j += lens[i]+gaps[i]
p = 0
print(disk)
fullto = np.zeros(10,dtype='int')
for j in range(nf-1,-1,-1):
    k = fullto[lens[j]]
    while k<start[j]:
        if (disk[k:k+lens[j]]==-1).all():
            p = k
            disk[k:k+lens[j]] = j
            disk[start[j]:start[j]+lens[j]] = -1
            fullto[lens[j]] = k
            break
        k += 1
    print(j)
checksum = 0
for j in range(0,len(disk)):
    if disk[j] == -1:
        continue
    checksum += j*disk[j]
print(checksum)