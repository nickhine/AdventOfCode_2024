import numpy as np

with open("d17.dat") as f:
    data = f.read().splitlines()

regAi = int(data[0].split()[2])
regBi = int(data[1].split()[2])
regCi = int(data[2].split()[2])
prog = np.array([int(x) for x in data[4].split()[1].split(",")])
progout = data[4].split()[1]

def tstr(i,width=2):
   t = np.base_repr(i,3)
   if len(t) < width:
        t = '0' * (width - len(t)) + t
   return t

def ostr(i,width=2):
   t = np.base_repr(i,8)
   if len(t) < width:
        t = '0' * (width - len(t)) + t
   return t

def bstr(i,width=2):
   t = np.base_repr(i,2)
   if len(t) < width:
        t = '0' * (width - len(t)) + t
   return t

def dstr(i,width=2):
   t = np.base_repr(i,10)
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
print(f'{bstr(0):36}: {progout}')
d = np.zeros(16,dtype=int)
digit = np.zeros(len(d),dtype=int)
l = 48
oldscore = 0
temp = 10
maxscore = 0
for m in range(len(prog)-1,-1,-1):
    maxscore += m**2
    #print(m,m*m,maxscore)
# empirical bounds for the solution based on trial and error
Amin = 109130730842522
Amax = 136904920099226
A = int((Amax + Amin)/2)
ratio = 10
while True:
    bit = np.random.randint(0,l)
    Atrial = A ^ (1<<bit)
    score = 0
    for m in range(len(prog)-1,-1,-1):
        Am = Atrial >> 3*m
        Bm0 = (Am&0b111)
        Bm1 = (Bm0^0b101)
        Bm2 = (Bm1^0b110)
        Cm = (Am>>Bm1)
        Bm = (Bm2^Cm)
        digit[m] = (Bm2^Cm)&0b111
        score += (digit[m]==prog[m])*m**2
    #score += int((Atrial/Amin-1)*ratio)
    if score==maxscore and Atrial<Amax:
        print('solution found:',Atrial,score)
        break
    if score>oldscore:
        print('m=',m,', check:',digit[m],prog[m],oldscore,score,"/",maxscore,Atrial)
    p = min(1.0,np.exp((score-oldscore)/temp))
    #print('score:',oldscore-score,p)
    if score>oldscore or np.random.rand()<p:
        A = Atrial
        oldscore = score
    temp *= 0.999999
    ratio *= 1.0000001
for override in range(A,A+1,1):
    regA = override
    output = ""
    for n in range(0,len(prog),2):
        An = regA >> 3*n
        Anp = (An>>3)
        if An==0 and n>0:
            break
        digit1 = ((((An&0b111)^0b101)^0b110)^(An>>((An&0b111)^0b101)))&0b111
        digit2 = (((((An>>3)&0b111)^0b101)^0b110)^((An>>3)>>(((An>>3)&0b111)^0b101)))&0b111
        output = output + tstr(digit1) + "," + tstr(digit2) + ","
    output = output[0:-1]
    ag = 0
    if output[0:ag]==progout[0:ag]:
        print(f'{dstr(override):36}: {output}')
        #print(f'{tstr(0):36}: {progout}')
