import numpy as np
print(sum([(np.loadtxt('data.dat')[:,1]==d).sum()*d for d in np.loadtxt('data.dat')[:,0]]))