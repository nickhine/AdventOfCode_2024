import numpy as np
with open('d11.dat') as f:
    data = f.readlines()
data = [int(x) for x in data[0].split()]
print(data)
nb = 75
for b in range(nb):
    datanew = []
    for i in range(len(data)):
        strd = str(data[i])
        #print(data[i],strd,len(strd))
        if data[i]==0:
            datanew.append(1)
        elif len(strd)%2==0:
            lh = strd[0:int(len(strd)/2)]
            rh = strd[int(len(strd)/2):]
            datanew.append(int(lh))
            datanew.append(int(rh))
        else:
            datanew.append(data[i]*2024)
    data = datanew
    print(b,len(data))