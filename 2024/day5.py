import numpy as np
goodtot=0
badtot=0
enabled = True
rules = []
pages = []
onpages = False
with open('d5.dat') as f:
    lines = [line for line in f] 
    for l in lines:
        if l=='\n':
            onpages = True
            continue
        if not onpages:
            rules.append(l.rstrip().split('|'))
        else:
            pages.append(l.rstrip().split(','))
    print(rules)
    #print(pages)
for p in pages:
    obeys = True
    for r in rules:
        if r[0] in p and r[1] in p:
            if p.index(r[0])>p.index(r[1]):
                obeys = False
                break
    if obeys:
        midpage = p[int(len(p)/2)]
        #print(p,':',midpage)
        goodtot = goodtot + int(midpage)
    else:
        q = []
        pleft = p.copy()
        while len(pleft)>0:
            for it,t in enumerate(pleft):
                notnext = False
                for r in rules:
                    if t==r[1] and r[0] in pleft:
                        notnext = True
                        break
                    #print(it,t,r,t in r)
                if not notnext:
                    q.append(t)
                    del pleft[it]
                #print(pleft,'|',q)
        print(p,':',q)
        badtot = badtot + int(q[int(len(q)/2)])
print(badtot)