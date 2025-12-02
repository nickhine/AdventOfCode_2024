import numpy as np
from heapq import heappush,heappop
np.set_printoptions(threshold=np.inf,linewidth=np.inf)
mapl = []
with open('d20.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        mapl.append(line)
lx,ly = len(mapl[0]),len(mapl)
mapa = np.zeros((ly,lx),dtype=int)
char_to_value = {'#': 1, '.': 0, 'S': 0, 'E': 0}
stpos = np.zeros(2, dtype=int)
endpos = np.zeros(2, dtype=int)
for i, row in enumerate(mapl):
    for j, char in enumerate(row):
        mapa[i, j] = char_to_value.get(char, 0)
        if char == 'S':
            stpos[:] = (j, i)
        elif char == 'E':
            endpos[:] = (j, i)

dp = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Directions: right, down, left, up
dirch = ['>', 'v', '<', '^']  # Direction characters
def print_map(mapb,time,pos,path,npath,numpath=False):
    map_display = np.full((ly, lx), '.', dtype=str)
    map_display[stpos[1], stpos[0]] = 'S'
    map_display[endpos[1], endpos[0]] = 'E'
    map_display[pos[1], pos[0]] = '@'
    map_display[mapb < -1] = 'C'
    map_display[(mapb == -1) | (mapb == 1)] = '#'
    if npath > 0:
        path = path[:npath]
        for idx, (x, y) in enumerate(path):
            if numpath:
                map_display[y, x] = chr(ord('A') + int(idx / (npath / 58)))
            elif idx > 0:
                prev = path[idx - 1]
                diff = tuple(np.array([x, y]) - prev)
                direction_index = np.where((dp == diff).all(axis=1))[0]
                if len(direction_index) > 0:
                    map_display[y, x] = dirch[direction_index[0]]
                else:
                    print(f"Error in path: {path[idx-3:idx+3]}")
                    return
    print('\n'.join(''.join(row) for row in map_display),end='' )

def heuristic(a, b):
    """Manhattan distance as the heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(mapa, stpos, endpos):
    """Optimized pathfinding using A* algorithm."""
    open_set = []
    heappush(open_set, (stpos, []))  # (priority, current position, path)
    g_scores = np.full((ly, lx), np.inf)  # Cost to reach each cell
    g_scores[stpos[1], stpos[0]] = 0
    while open_set:
        current, path = heappop(open_set)
        path = path + [current]
        if np.array_equal(current, endpos):
            return path  # Return the found path
        for d in dp:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if not (0 <= neighbor[0] < lx and 0 <= neighbor[1] < ly):
                continue
            if mapa[neighbor[1], neighbor[0]] == 1:
                continue
            tentative_g_score = g_scores[current[1], current[0]] + 1
            if tentative_g_score < g_scores[neighbor[1], neighbor[0]]:
                g_scores[neighbor[1], neighbor[0]] = tentative_g_score
                heappush(open_set, (neighbor, path))
    return None  # No path found

path = np.array(a_star(mapa, stpos, endpos))
npath = len(path)
mapt = np.ones((ly,lx),dtype=int)*-1
mapt[mapa == 1] = -1
mapt[path[:npath, 1], path[:npath, 0]] = np.arange(npath)
ngoodcheats = 0
goodcheatval = 100
dse = np.meshgrid(range(-20,21),range(-20,21))
dist = np.abs(dse[0]) + np.abs(dse[1])
mask = dist <= 20
offs = np.column_stack((dse[0][mask], dse[1][mask]))
dists = dist[mask]
for cspos in path[0:npath]:
    cepos = cspos + offs
    bounds_mask = (1 <= cepos[:, 1]) & (cepos[:, 1] < ly) & \
                (1 <= cepos[:, 0]) & (cepos[:, 0] < lx)
    cepos = cepos[bounds_mask]
    fdists = dists[bounds_mask]
    mapt_mask = mapt[cepos[:, 1], cepos[:, 0]] != -1
    fcepos = cepos[mapt_mask]
    fdists = fdists[mapt_mask]
    mapt_values = mapt[fcepos[:, 1], fcepos[:, 0]]
    ngoodcheats += np.sum(mapt_values - mapt[cspos[1], cspos[0]] - fdists >= goodcheatval)
print(f'Cheats saving {goodcheatval} ps or more: {ngoodcheats}')