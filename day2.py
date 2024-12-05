import numpy as np
tot=0
with open('d2.dat') as f:
    for ir,rep in enumerate(f.read().split('\n')):
        onesafe = False
        for ind in range(len(rep.split())):
            rsplit = rep.split()
            # comment out to return to part 1
            del rsplit[ind]
            allup = True
            alldn = True
            for i,n in enumerate(rsplit):
                n=int(n)
                if i==0:
                    prev = n
                    continue
                if n<=prev or n>prev+3:
                    allup = False
                if n>=prev or n<prev-3:
                    alldn = False
                prev= n
            if alldn or allup:
                onesafe = True
        if onesafe:
            tot+=1
        
print(tot)
