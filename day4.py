import numpy as np

d = np.genfromtxt('d4.dat',dtype='str',delimiter='')

print(d)

dirs = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]
lims = [len(d),len(d[0])]
targ = 'XMAS'
print(lims)
tot = 0
for i in range(lims[0]):
    for j in range(lims[1]):
        print(f'({i},{j}) {d[i][j]}')
        for dir in dirs:
            for o in range(len(targ)):
                ip=i+dir[0]*o
                jp=j+dir[1]*o
                if ip<0 or ip>=lims[0] or jp<0 or jp>=lims[1]:
                    break
                print(f'({i},{j}) {dir} {o} :',ip,jp,d[ip][jp],targ[o])
                if d[ip][jp]!=targ[o]:
                    break
                if o==len(targ)-1:
                    tot = tot+1
print(tot)
                