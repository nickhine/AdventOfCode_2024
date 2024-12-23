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
dirs_num = {'0A': ">",'02': "^",'A3': "^",'A0': "<",
            '12': ">", '14': "^", '21': "<", '23': ">",'25': "^", '20': "v", '32': "<", '36': "^",'3A': "v",
            '41': "v", '45': ">", '47': "^", '54': "<", '56': ">", '58': "^", '52': "v", '65': "<", '69': "^", '63': "v",
            '74': "v", '78': ">", '87': "<", '89': ">", '85': "v", '98': "<", '96': "v"}
dirs_dir = {'<v': ">", 'v<': "<", 'v>': ">", 'v^': "^", '>v': "<", '>A': "^",
            '^A': ">", '^v': "v", 'A^': "<", 'A>': "v"}

#https://www.reddit.com/r/adventofcode/comments/1hjgyps/2024_day_21_part_2_i_got_greedyish/
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
            # check any instances of each character are consecutive
            for ic,c in enumerate(perm):
                if ic>1 and c in perm[0:ic-1] and not (c == perm[ic-1]):
                    addthis = False
            if addthis:
                perms.append(perm)
        perms = sorted(list(set(perms)))
        if len(perms) > 1:
            # check if we have diagonal moves, in which case choose one option
            if dp[0] < 0 and dp[1] > 0: # up and left
                if perms[0].index('^')<perms[0].index('<'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] < 0 and dp[1] < 0: # down and left
                if perms[0].index('v')<perms[0].index('<'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] > 0 and dp[1] < 0: # down and right
                if perms[0].index('v')>perms[0].index('>'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] > 0 and dp[1] > 0: # up and right
                if perms[0].index('^')>perms[0].index('>'):
                    del perms[0]
                else:
                    del perms[1]
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
            # check any instances of each character are consecutive
            for ic,c in enumerate(perm):
                if ic>1 and c in perm[0:ic-1] and not (c == perm[ic-1]):
                    addthis = False
            if addthis:
                perms.append(perm)
        perms = sorted(list(set(perms)))
        if len(perms) > 1:
            # check if we have diagonal moves, in which case choose one option
            if dp[0] < 0 and dp[1] > 0: # up and left
                if perms[0].index('^')<perms[0].index('<'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] < 0 and dp[1] < 0: # down and left
                if perms[0].index('v')<perms[0].index('<'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] > 0 and dp[1] < 0: # down and right
                if perms[0].index('v')>perms[0].index('>'):
                    del perms[0]
                else:
                    del perms[1]
            if dp[0] > 0 and dp[1] > 0: # up and right
                if perms[0].index('^')>perms[0].index('>'):
                    del perms[0]
                else:
                    del perms[1]
        if pair in dirs_dir:
            if dstr != dirs_dir[pair]:
                print("ERROR")
        dirs_dir[pair] = sorted(list(set(perms)))
            
dirs_level = [dirs_num] + [dirs_dir]*2
nlevels = 4
compsum = 0
for icode,code in enumerate(codes[0:]):
    ip_record = {}
    seqdir = [[code]] + [[]]*nlevels
    for il in range(nlevels-1):
        if il not in ip_record:
            ip_record[il] = {}
        pos = 'A'
        if il<nlevels-2:
            for seq in seqdir[il]:
                for c in seq:
                    pos = c
        permprod = 1
        seqdir[il+1] = []
        for seq in seqdir[il]:
            for c in seq:
                ip = 0
                seqdir[il+1].append(str(dirs_level[il][pos+c][ip] + 'A'))
                pos = c

    complexity = len(''.join(seqdir[nlevels-1])) * int(code[0:-1])
    compsum = compsum + complexity
    print('code,length,code_compsum=',code,len(seqdir[nlevels-1]),complexity)
    #for il in range(nlevels-1,-1,-1):
    #    print(il,len(''.join(seqdir[il])),''.join(seqdir[il]))
    #print(len(seqdir[nlevels-1]),seqdir[nlevels-1])
print('total complexity at nlevels=4:',compsum)

nlevels = 27
counts = []
newcounts = []
for il in range(nlevels):
    counts.append({})
    newcounts.append({})
seqs = {}

dirs_level = [dirs_num] + [dirs_dir]*(nlevels-2)
compsum = 0
ip = 0
for icode,code in enumerate(codes[0:]):
    for il in range(nlevels):
        for seq in counts[il]:
            counts[il][seq] = 0
    counts[0][code] = 1
    for il in range(nlevels-1):
        newcounts[il+1] = {}
        for seq in counts[il]:
            pos = 'A'
            if counts[il][seq] == 0:
                continue
            for c in seq:
                ip = 0
                newstr = str(dirs_level[il][pos+c][ip] + 'A')
                pos = c
                if newstr not in newcounts[il+1]:
                    newcounts[il+1][newstr] = counts[il][seq]
                else:
                    newcounts[il+1][newstr] += counts[il][seq]
        counts[il+1] = newcounts[il+1]
    #for il in range(3,-1,-1):
    #    print(code,il,counts[il])
    code_compsum = 0
    length = 0
    for seq in counts[nlevels-1]:
        length += len(seq) * counts[nlevels-1][seq]
    code_compsum = length * int(code[0:-1])
    print('code,length,code_compsum=',code,length,code_compsum)
    compsum = compsum + code_compsum
print('Compsum with counts:', compsum)