import numpy as np

d = np.genfromtxt('d4.dat',dtype='str',delimiter='')

dp = []
for i in range(len(d)):
    dpp=[]
    for j in range(len(d[i])):
        dpp.append('.')
    dp.append(dpp)
print(d)

lims = [len(d),len(d[0])]
targ = 'AMS'
offs = [
        [  [[0,0]],  [[-1,-1],[ 1,-1]],  [[-1, 1],[ 1, 1]] ],
        [  [[0,0]],  [[-1,-1],[-1, 1]],  [[ 1,-1],[ 1, 1]] ],
        [  [[0,0]],  [[-1, 1],[ 1, 1]],  [[-1,-1],[ 1,-1]] ],
        [  [[0,0]],  [[ 1,-1],[ 1, 1]],  [[-1,-1],[-1, 1]] ],
       ]

print(lims)
tot = 0
for i in range(lims[0]):
    for j in range(lims[1]):
        if d[i][j]!=targ[0]:
            continue
        print(f'({i},{j}) {d[i][j]}')
        for off in offs:
            print(off)
            fail = False
            for o in range(len(targ)):
                if fail:
                    break
                for p in range(len(off[o])):
                    ip=i+off[o][p][0]
                    jp=j+off[o][p][1]
                    if ip<0 or ip>=lims[0] or jp<0 or jp>=lims[1]:
                        fail = True
                        break
                    print(f'({i},{j}) {off[o][p]} {o} {p}:',ip,jp,d[ip][jp],targ[o])
                    if d[ip][jp]!=targ[o]:
                        fail = True
                        break
                    if o==len(targ)-1 and p==len(off[o])-1:
                        print('found')
                        dp[i][j]='A'
                        tot = tot+1
print(tot)
for i in range(len(dp)):
    print(''.join(s for s in dp[i]))
                