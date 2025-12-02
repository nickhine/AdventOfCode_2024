import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=np.inf)
with open('d11.dat') as f:
    data = f.readlines()
data = [int(x) for x in data[0].split()]
lenatb = []
maxn = 10000
nums = np.zeros((2,maxn),dtype=int)
counts = np.zeros((2,maxn),dtype=int)
lnum = 0
nums[:,0] = 0
nums[:,1] = 1
counts[:,0] = 0
counts[:,1] = 0
lnum = 2
for j in range(len(data)):
    if data[j] not in nums:
        nums[:,lnum] = data[j]
        counts[:,lnum] = 1
        lnum+=1
    else:
        idx = np.where(nums[0,:]==data[j])[0][0]
        counts[:,idx]+=1
print(-1,lnum,nums[0,0:lnum],counts[0,0:lnum])
nb = 75
p = 0
q = 1
plnum = lnum
qlnum = lnum
for b in range(nb):
    counts[q,:] = 0
    # Apply first rule
    counts[q,1] += counts[p,0]
    # Apply second and third rules
    for j in range(1,plnum):
        if counts[p,j]==0:
           continue 
        strd = str(nums[p,j])
        if len(strd)%2==0:
            lh = int(strd[0:int(len(strd)/2)])
            rh = int(strd[int(len(strd)/2):])
            for h in [lh,rh]:
                i = np.where(nums[q,0:qlnum]==h)[0]
                if len(i) == 0:
                    nums[q,qlnum] = h
                    counts[q,qlnum] = counts[p,j]
                    qlnum += 1
                else:
                    counts[q,i] += counts[p,j]
        else:
            h = nums[p,j]*2024
            i = np.where(nums[q,0:qlnum]==h)[0]
            if len(i) == 0:
                nums[q,qlnum] = h
                counts[q,qlnum] = counts[p,j]
                qlnum += 1
            else:
                counts[q,i] += counts[p,j]
    # update q with p values
    plnum = qlnum
    counts[p,0:qlnum] = counts[q,0:qlnum]
    nums[p,0:qlnum] = nums[q,0:qlnum]
np.savetxt('counts.txt',np.column_stack([nums[q,:],counts[q,:]]))
print(qlnum,np.sum(counts[q,0:qlnum]))
