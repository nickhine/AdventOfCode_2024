import numpy as np

data = np.loadtxt('data.dat')
left = data[:,0]
right = data[:,1]
argleft = np.argsort(left)
argright = np.argsort(right)
left = left[argleft]
right = right[argright]
print(abs(left-right))
print(sum(abs(left-right)))