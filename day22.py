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
bestcomb = -1
for ic in range(combinations.shape[0]):
    comb = combinations[ic,:]
    seq = (comb[0]+9)*19**3+(comb[1]+9)*19**2+(comb[2]+9)*19**1+(comb[3]+9)*19**0
    bananas = 0
    #print(f'testing combination {ic}: {comb} {seq} progress: {ic/combinations.shape[0]*100:5.3f}%')
    mask = (seqint[:,:] == seq)
    first_time = np.argmax(mask,axis=-1)
    first_time = np.where(mask.any(axis=-1),first_time,-1)
    #print(prices[np.arange(buyers),first_time])
    #print('prices:',prices[np.arange(buyers),first_time]*(first_time >= 0))
    bananas += np.sum(prices[np.arange(buyers),first_time]*(first_time >= 0))
    if bananas > maxbananas:
        maxbananas = bananas
        bestcomb = comb
print(f'new maxbananas: {maxbananas} with combination {bestcomb}')


            