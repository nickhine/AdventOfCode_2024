import numpy as np

with open("d17.dat") as f:
    data = f.read().splitlines()

regAi = int(data[0].split()[2])
regBi = int(data[1].split()[2])
regCi = int(data[2].split()[2])
prog = [int(x) for x in data[4].split()[1].split(",")]
progout = data[4].split()[1]

def tstr(i,width=2):
   t = np.base_repr(i,3)
   if len(t) < width:
        t = '0' * (width - len(t)) + t
   return t

progtern = [tstr(x) for x in prog]
progout = ",".join(progtern)
#print(regA,regB,regC)
#print(prog)

opstr = {0:'adv',
         1:'bxl',
         2:'bst',
         3:'jnz',
         4:'bxc',
         5:'out',
         6:'bdv',
         7:'cdv'}

regAi = 5
for override in range(0,3000000,1):
    regA = override
    output = ""
    for n in range(len(prog)):
        An = int(regA / 2**(3*n))
        if An==0 and n>0:
            break
        digit = ((((An%8)^5)^6)^(int(An/2**((An%8)^5))))%8
        output = output + tstr(digit) + ","
    output = output[0:-1]
    ag = 12
    if output[0:ag]==progout[0:ag]:
        print(f'{tstr(override):36}: {output}')
        print(f'{tstr(0):36}: {progout}')
