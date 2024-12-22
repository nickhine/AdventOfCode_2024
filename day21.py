import numpy as np
from itertools import permutations
codes = []
with open("d21.dat") as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        codes.append(line)
#print(codes)

# numeric:
#+---+---+---+
#| 7 | 8 | 9 |
#+---+---+---+
#| 4 | 5 | 6 |
#+---+---+---+
#| 1 | 2 | 3 |
#+---+---+---+
#    | 0 | A |
#    +---+---+
# directional:
#    +---+---+
#    | ^ | A |
#+---+---+---+
#| < | v | > |
#+---+---+---+

num_locs = {'0': (1,0), '1': (0,1), '2': (1,1), '3': (2,1), '4': (0,2), '5': (1,2), '6': (2,2), '7': (0,3), '8': (1,3), '9': (2,3), 'A': (2,0)}
dir_locs = {'<': (0,0), 'v': (1,0), '>': (2,0), '^': (1,1), 'A': (2,1)}
dir_dpos = {'<': (-1,0), 'v': (0,-1), '>': (1,0), '^': (0,1)}

num_buts = list("0123456789A")
dir_buts = list("<v>^A")
#print(num_buts)
dirs_num = {'0A': ">",'02': "^",'A3': "^",'A0': "<",
            '12': ">", '14': "^", '21': "<", '23': ">",'25': "^", '20': "v", '32': "<", '36': "^",'3A': "v",
            '41': "v", '45': ">", '47': "^", '54': "<", '56': ">", '58': "^", '52': "v", '65': "<", '69': "^", '63': "v",
            '74': "v", '78': ">", '87': "<", '89': ">", '85': "v", '98': "<", '96': "v"}
dirs_dir = {'<v': ">", 'v<': "<", 'v>': ">", 'v^': "^", '>v': "<", '>A': "^",
            '^A': ">", '^v': "v", 'A^': "<", 'A>': "v"}

for str1 in num_buts:
    loc1 = np.array(num_locs[str1])
    for str2 in num_buts:
        loc2 = np.array(num_locs[str2])
        pair = str1+str2
        dp = loc2-loc1
        dstr = ('>'*dp[0] if dp[0]>0 else '<'*-dp[0]) + ('^'*dp[1] if dp[1]>0 else 'v'*-dp[1])
        allperms = [''.join(p) for p in permutations(dstr)]
        perms = []
        for perm in allperms:
            addthis = True
            loc = loc1.copy()
            for c in perm:
                loc += np.array(dir_dpos[c])
                if np.all(loc == np.array((0,0))):
                    addthis = False
            if addthis:
                perms.append(perm)
        if pair in dirs_num:
            if dstr != dirs_num[pair]:
                print("ERROR")
        dirs_num[pair] = sorted(list(set(perms)))

for str1 in dir_buts:
    loc1 = np.array(dir_locs[str1])
    for str2 in dir_buts:
        loc2 = np.array(dir_locs[str2])
        pair = str1+str2
        dp = loc2-loc1
        dstr = ('>'*dp[0] if dp[0]>0 else '<'*-dp[0]) + ('^'*dp[1] if dp[1]>0 else 'v'*-dp[1])
        allperms = [''.join(p) for p in permutations(dstr)]
        perms = []
        for perm in allperms:
            addthis = True
            loc = loc1.copy()
            for c in perm:
                loc += np.array(dir_dpos[c])
                if np.all(loc == np.array((0,1))):
                    addthis = False
            if addthis:
                perms.append(perm)
        if pair in dirs_dir:
            if dstr != dirs_dir[pair]:
                print("ERROR")
        dirs_dir[pair] = sorted(list(set(perms)))


def validate(seq3,code):
    pos3 = np.array(dir_locs['A'])
    pos2 = np.array(dir_locs['A'])
    pos1 = np.array(num_locs['A'])
    seq2 = ''
    seq1 = ''
    seq0 = ''
    for c3 in seq3:
        if c3 in dir_dpos: # non-A presses, only pos3 updates
            pos3 += np.array(dir_dpos[c3])
            continue
        # A pressed at lv3, increment level above
        for dl in dir_locs:
            if np.all(pos3 == dir_locs[dl]):
                seq2 += dl
                if dl in dir_dpos:
                    pos2 += dir_dpos[dl]
                    continue
                # A pressed at lv2, increment level above
                for el in dir_locs:
                    if np.all(pos2 == dir_locs[el]):
                        seq1 += el
                        if el in dir_dpos:
                            pos1 += dir_dpos[el]
                            continue
                        # A pressed at lv1, increment final level
                        for fl in num_locs:
                            if np.all(pos1 == num_locs[fl]):
                                seq0 += fl
                                pos0 = num_locs[fl]
    print('validate:',seq3)
    print('validate:',seq2)
    print('validate:',seq1)
    print('validate:',seq0)
    assert(seq0 == code)           
            
nlevels = 4
dirs_level = [dirs_num] + [dirs_dir,dirs_dir]*(nlevels-2)
compsum = 0
for icode,code in enumerate(codes):
    nperms = [1]*(nlevels-1)
    bestseqdir = ['A'*5000]*nlevels
    perm = [0]*nlevels
    while (perm[0] < nperms[0]):
        seqdir = [code] + ['','','']*nlevels
        for il in range(nlevels-1):
            nperms[il] = 1
            pos = 'A'
            if il<nlevels-2:
                for c in seqdir[il]:
                    nperms[il] *= len(dirs_level[il][pos+c])
                    pos = c
            permprod = 1
            seqdir[il+1] = ''
            ncurr = perm[il]
            for c in seqdir[il]:
                permprod *= len(dirs_level[il][pos+c]) if il<2 else 1
                ip = ncurr // (nperms[il]//permprod)
                ncurr = ncurr % (nperms[il]//permprod)
                seqdir[il+1] += dirs_level[il][pos+c][ip] + 'A'
                pos = c
            if il==nlevels-2:
                perm[il] += 1
                for jl in range(nlevels-2,0,-1):
                    if perm[jl] == nperms[jl]:
                        perm[jl] = 0
                        perm[jl-1] += 1
        if len(seqdir[nlevels-1]) < len(bestseqdir[nlevels-1]):
            bestseqdir = seqdir
    complexity = len(bestseqdir[nlevels-1]) * int(code[0:-1])
    compsum = compsum + complexity
    print('\n',code,len(bestseqdir[nlevels-1]),int(code[0:-1]),nperms,complexity)
    for il in range(nlevels-1,-1,-1):
        print(il,len(bestseqdir[il]),bestseqdir[il])
    #validate(bestseqdir[nlevels-1],code)
    #print(len(bestseqdir[nlevels-1]),bestseqdir[nlevels-1])
print('total complexity:',compsum)

        