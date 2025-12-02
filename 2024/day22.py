import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=np.inf)
secrets = []
with open('d22.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        secrets.append(int(line))
combinations = []
for i in range(-9,9):
    for j in range(-9,9):
        if abs(i+j) > 9:
            continue
        for k in range(-9,9):
            if abs(i+j+k) > 9 or abs(j+k) > 9:
                continue
            for l in range(-9,9):
                if abs(i+j+k+l) > 9 or abs(j+k+l) > 9 or abs(k+l) > 9:
                    continue
                combinations.append((i,j,k,l))
print('combinations=',len(combinations))
combinations = np.array(combinations)
maxtime = 2000
secrets = np.array(secrets)
buyers = len(secrets)
prices = np.zeros((buyers,maxtime),dtype=int)
oldprices = np.zeros((len(secrets)),dtype=int)
seqint = -np.ones((buyers,maxtime),dtype=int)
for time in range(maxtime):
    prices[:,time] = secrets % 10
    sec0 = secrets
    sec1 = ((sec0 <<  6)^sec0) % (1 << 24)
    sec2 = ((sec1 >>  5)^sec1) % (1 << 24)
    sec3 = ((sec2 << 11)^sec2) % (1 << 24)
    secrets = sec3
    if time < 4:
        continue
    sequences = np.diff(prices[:,time-4:time+1],axis=1)
    seqint[:,time] = (sequences[:,0]+9)*19**3+(sequences[:,1]+9)*19**2+(sequences[:,2]+9)*19**1+(sequences[:,3]+9)*19**0
print('Sum of secrets:',sum(secrets))
maxbananas = 0
all_seqs = (combinations[:,0]+9)*19**3+(combinations[:,1]+9)*19**2+(combinations[:,2]+9)*19**1+(combinations[:,3]+9)*19**0
chunk_size = 1
for i in range(0, len(all_seqs), chunk_size):
    masks = (seqint[:,:,None] == all_seqs[i:i + chunk_size])
    first_time = np.where(masks.any(axis=1),np.argmax(masks,axis=1),-1)
    maxbananas = max(maxbananas, np.max(np.sum(prices[np.arange(buyers)[:,None],first_time]*(first_time >= 0), axis=0)))
print(f'maxbananas: {maxbananas}')


            