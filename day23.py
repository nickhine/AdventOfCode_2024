import numpy as np

data = []
with open('d23.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        data.append(line.split('-'))

cons = {}
for l in data:
    if l[0] not in cons:
        cons[l[0]] = []
    if l[1] not in cons:
        cons[l[1]] = []
    cons[l[0]].append(l[1])
    cons[l[1]].append(l[0])

threes = []
threes_with_t = []
for c1 in cons:
    if c1[0] != 't':
        continue
    for c2 in cons[c1]:
        for c3 in cons[c1]:
            if c2 in cons[c3]:
                set123 = set([c1,c2,c3])
                if set123 not in threes:
                    threes.append(set123)

import networkx as nx
G = nx.Graph()
for l in data:
    G.add_edge(l[0],l[1])
cliques = nx.find_cliques(G)
largest_clique = max(cliques, key=len)
largest_subgraph = G.subgraph(largest_clique)
complist = list(sorted(largest_clique))
password = ",".join([str(x) for x in complist])
print(password)