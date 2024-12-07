import numpy as np

with open('t7.dat') as f:
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
concat = np.zeros(maxvals,dtype=int)
tot = 0
for i in rnge:
    anytrue = False
    for qerm in range(1<<(lens[i]-1)):
        ovals = data[i][1].split()
        ix = 1
        qvals[0] = ovals[0]
        concat[0] = 0
        for j in range(1,lens[i]):
            concat[j] = (qerm >> j-1) & 1
        strval = ''
        qlen = 0
        #print(qerm,'concat=',concat[0:lens[i]])
        for j in range(0,lens[i]):
            if concat[j]:
                strval += ovals[j]
            if not concat[j]:
                strval = ovals[j]
                qlen += 1
            if strval != '':
                qvals[qlen-1] = int(strval)
            #print(j,concat,f'"{strval}"',qlen,qvals[0:qlen])
        for perm in range(1<<(qlen-1)):
            pres = qvals[0]
            for j in range(1,qlen):
                bit = (perm >> j-1) & 1
                if bit:
                    pres = pres + qvals[j]
                else:
                    pres = pres * qvals[j]
            if pres == res[i]:
                anytrue = True
                break
        print(i,qerm,'concat=',concat[0:lens[i]],'res=',res[i],'qvals=',qvals[0:qlen],anytrue)
        if anytrue:
            break
    if anytrue:
        tot += res[i]
print(tot)