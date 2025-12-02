import numpy as np
#np.set_printoptions()
#np.set_printoptions(formatter={'int': lambda x: f"{x:4d}"},threshold=np.inf,linewidth=np.inf)
with open('d10.dat') as f:
    data = f.read().splitlines()
lx = len(data[0])
ly = len(data)
data = np.array([list(x) for x in data],dtype=int)
nheads = np.count_nonzero(data == 0)
nends = np.count_nonzero(data == 9)
heads = np.zeros((nheads,2),dtype=int)
ends = np.zeros((nends,2),dtype=int)
ih = 0
ie = 0
for y in range(ly):
    for x in range(lx):
        if data[y,x] == 0:
            heads[ih,0] = x
            heads[ih,1] = y
            ih += 1
        if data[y,x] == 9:
            ends[ie,0] = x
            ends[ie,1] = y
            ie += 1
perms = 4**9
dirs = np.zeros(9,dtype=int)
deltas = np.array([[0,1],[1,0],[0,-1],[-1,0]],dtype=int)
nval = np.zeros((19,19),dtype=int)
cpos = np.zeros(2,dtype=int)
dpos_loc = np.zeros((9,2),dtype=int)
def eval_routes(dpos_final=None):
    nvalid = 0
    for perm in range(perms):
        valid = True
        cpos[:] = 0
        for d in range(0,9):
            dir = int(perm / 4**d) % 4
            cpos[:] = cpos[:] + deltas[dir,:]
            dpos_loc[d,:] = cpos[:]
            for k in range(0,d):
                if np.all(dpos_loc[d,:] == dpos_loc[k,:]):
                    valid = False
                    break
            if not valid:
                break
        if valid:
            nval[dpos_loc[d,0]+9,dpos_loc[d,1]+9] += 1
            if dpos_final is not None:
                icount = nval[dpos_loc[d,0]+9,dpos_loc[d,1]+9]-1
                ival[dpos_loc[d,0]+9,dpos_loc[d,1]+9,icount] = nvalid
                dpos_final[nvalid,:,:] = dpos_loc[:,:]
                if (dpos_final[nvalid,8,0] == -8) and (dpos_final[nvalid,8,1] == 0):
                    print(perm,dpos_final[nvalid].flat[:])
            nvalid += 1
    return nvalid
nvalid = eval_routes()
dpos = np.zeros((nvalid,9,2),dtype=int)
maxval = np.max(nval)
nval[:,:] = 0
ival = np.zeros((19,19,maxval),dtype=int)
nvalid_check = eval_routes(dpos)
routes = np.zeros((nheads,nends),dtype=int)
height = np.zeros(9,dtype=int)
steps = np.arange(1,10,dtype=int)
#np.set_printoptions(formatter={'int': lambda x: f"{x:2d}"},threshold=np.inf,linewidth=np.inf)
for ih in range(nheads):
    for ie in range(nends):
        dhe = ends[ie,:] - heads[ih,:]
        if np.abs(dhe[0]) > 9 or np.abs(dhe[1]) > 9:
            continue
        icount = nval[dhe[0]+9,dhe[1]+9]
        for i in range(icount):
            j = ival[dhe[0]+9,dhe[1]+9,i]
            route = dpos[j,:,:]
            for d in range(9):
                cpos = heads[ih,:] + route[d,:]
                if cpos[0] < 0 or cpos[0] >= lx or cpos[1] < 0 or cpos[1] >= ly:
                    height[d] = -1
                    break
                height[d] = data[cpos[1],cpos[0]]
            if np.all(height == steps):
                routes[ih,ie] += 1
            #if routes[ih,ie]:
            #    break
print(np.count_nonzero(routes[:,:]))
print(np.sum(routes[:,:]))