import numpy as np

data = []
keys = []
locks = []
with open('d25.dat') as f:
    while True:
        lines = []
        for i in range(7):
            lines.append(f.readline().strip())
        if lines[0] == '#####':
            seq = [0]*5
            for i in range(0,7):
                for j in range(0,5):
                    if lines[i][j] == '#':
                        seq[j] = i
            locks.append(np.array(seq))
        if lines[0] == '.....':
            seq = [0]*5
            for i in range(6,-1,-1):
                for j in range(0,5):
                    if lines[i][j] == '#':
                        seq[j] = 6-i
            keys.append(np.array(seq))
        if not f.readline():
            break
print(locks)
print(keys)

nfit = 0
for lock in locks:
    for key in keys:
        if np.any(key >= 6-lock):
            print(f'lock {lock} and key {key} overlap')
        else:
            nfit += 1
print(nfit)