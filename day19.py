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

#print(patterns)
ways = {}
nposs = 0
for ipat,pattern in enumerate(patterns):
    #print(f'\n\n\nNow on pattern {ipat}: {pattern}')
    #print('towels=',towels)
    ways[pattern] = 0
    ways[""] = 1
    pos = 0
    past = ""
    order = []
    nskip = 0
    skiptarg = 0
    prevpos = 0
    jtow = 0
    while True:
        found = False
        for itow,towel in enumerate(towels):
            match = towel == pattern[pos:pos+len(towel)]
            #print(f'testing if {towel} is next for {past} to make {pattern} at {pos}: {match}, nskip={nskip},skiptarg={skiptarg}')
            if match:
                if itow < jtow:
                    continue
                if nskip == skiptarg:
                    rest = pattern[pos+len(towel):]
                    if rest in ways:
                        #print(f'appending {towel} since rest={rest} is solved ({ways[rest]} ways):  (itow,nskip,skiptarg+1,pos)=({itow},{nskip},{skiptarg+1},{pos}) len(order)={len(order)}')
                        order.append((itow,nskip,skiptarg+1,pos))
                        pos = len(pattern)
                        break
                        #ways[towel+rest] += ways[rest]
                    else:
                        #print(f'Creating new entry for rest: {rest}')
                        ways[rest] = 0
                    order.append((itow,nskip,skiptarg+1,pos))
                    #print(f'appending {towel}:  (itow,nskip,skiptarg+1,pos)=({itow},{nskip},{skiptarg+1},{pos}) len(order)={len(order)}')
                    past += towel
                    pos += len(towel)
                    jtow = 0
                    found = True
                    break # for i,towel
                else:
                    #print(f'not yet skipped enough to add {towel}:  (ktow,nskip,skiptarg+1,pos)=({itow},{nskip},{skiptarg+1},{pos})')
                    nskip += 1
        complete = (pos == len(pattern))
        if complete:
            spacepat = str([towels[j[0]]+", " for j in order])
            orderstr = "".join([str(j[0])+"," for j in order])
            rest2 = rest
            #print(f'pat = {pattern} order= {orderstr} rest = {rest}')
            for itow,nskip,skiptarg,pos in reversed(order):
                rest2 = towels[itow] + rest2
                ways[rest2] += ways[rest]
                #print(f'ways[rest2={rest2}] is now {ways[rest2]}')
            #print(f'found {ways[pattern]} ways to make pat={ipat} {pattern} : {orderstr}') # {spacepat}')
        if (not found) or complete:
            if order:
                jtow,nskip,skiptarg,pos = order.pop()
                #past = "".join([towels[j[0]] for j in order])
                #print(f'backtracked to:  (jtow,nskip,skiptarg,pos)=({jtow},{nskip},{skiptarg},{pos}) now skipping {skiptarg} matches, pos={pos}, pat={ipat}, len(order)={len(order)}')
                #print(f'')
                continue
        if itow==len(towels)-1 and not found:
            if pos==prevpos:
                #print(f'all matching towels skipped, breaking loop for pat={ipat} with ways={ways[pattern]}')
                break # no more matches at this position, all possible towels now skipped
    if ways[pattern]>0:
        nposs += 1
# (2 + 1 + 4 + 6 + 0 + 1 + 2 + 0) = 16
# pattern 2:  g, b, b, r | g, b, br | gb, b, r | gb, br

nways = 0
for pat in patterns:
    nways += ways[pat]
print(f'{nposs} of {len(patterns)} possible, total of ways=',nways)