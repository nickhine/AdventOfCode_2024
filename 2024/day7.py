import numpy as np

with open('d7.dat') as f:
    data = [line.rstrip().split(':') for line in f]
res = np.zeros(len(data),dtype=int)
lens = np.zeros(len(data),dtype=int)
maxvals = 1
rnge = range(len(data))
for i in rnge:
    res[i] = int(data[i][0])
    lens[i] = len(data[i][1].split())
maxvals = np.max(lens)
qvals = np.zeros(maxvals,dtype=int)
tot = 0
for i in rnge:
    anytrue = False
    qvals = [int(x) for x in data[i][1].split()]
    for perm in range(3**(lens[i]-1)):
        pres = qvals[0]
        qlen = lens[i]
        for j in range(1,qlen):
            op = int(perm / 3**(j-1)) % 3
            if op==0:
                pres = pres + qvals[j]
            elif op==1:
                pres = pres * qvals[j]
            elif op==2:
                pres = int(str(pres) + str(qvals[j]))
            #print(i,perm,j,op,pres)
        if pres == res[i]:
            anytrue = True
            break
    print(i,perm,'res=',res[i],'qvals=',qvals[0:qlen],anytrue)
    if anytrue:
        tot += res[i]
print(tot)