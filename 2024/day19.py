import numpy as np
with open('d19.dat') as f:
    towelstr = f.readline().strip()
    towels = [x.strip() for x in towelstr.split(",")]
    f.readline() # skip empty line
    patterns = []
    while True:
        line = f.readline().strip()
        if not line:
            break
        patterns.append(line)
ways = {}
nposs = 0
for ipat,pattern in enumerate(patterns):
    ways[pattern] = 0
    ways[""] = 1
    pos = 0
    order = []
    nskip = 0
    skiptarg = 0
    prevpos = 0
    jtow = 0
    while True:
        found = False
        for itow,towel in enumerate(towels):
            match = towel == pattern[pos:pos+len(towel)]
            if match:
                if itow < jtow:
                    continue
                if nskip == skiptarg:
                    rest = pattern[pos+len(towel):]
                    if rest in ways:
                        order.append((itow,nskip,skiptarg+1,pos))
                        pos = len(pattern)
                        break
                    else:
                        ways[rest] = 0
                    order.append((itow,nskip,skiptarg+1,pos))
                    pos += len(towel)
                    jtow = 0
                    found = True
                    break # for i,towel
                else:
                    nskip += 1
        complete = (pos == len(pattern))
        if complete:
            rest2 = rest
            for itow,nskip,skiptarg,pos in reversed(order):
                rest2 = towels[itow] + rest2
                ways[rest2] += ways[rest]
        if (not found) or complete:
            if order:
                jtow,nskip,skiptarg,pos = order.pop()
                continue
        if itow==len(towels)-1 and not found:
            if pos==prevpos:
                break # no more matches at this position, all possible towels now skipped
    if ways[pattern]>0:
        nposs += 1
nways = 0
for pat in patterns:
    nways += ways[pat]
print(f'{nposs} of {len(patterns)} possible, total of ways=',nways)