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
# input is output of monte carlo search favouring high digits
seed = 136904920099226
for override in range(seed-2**18,seed+2**18,1):
    regA = override
    regB = regBi
    regC = regCi
    output = ""
    ip = 0
    lp = len(prog)
    progstr = ""
    while(ip<lp):
        opcode = prog[ip]
        operand = prog[ip+1]
        if operand <= 3:
            combo = operand
            combstr = tstr(operand,4)
        elif operand == 4:
            combo = regA
            combstr = "regA"
        elif operand == 5:
            combo = regB
            combstr = "regB"
        elif operand == 6:
            combo = regC
            combstr = "regC"

        #print(ip,opcode,operand)
        os = tstr(ip,4) + " " + opstr[opcode]
        if opcode==0: #'adv'
            newregA = int(regA / 2**combo)
            progstr += os + f": regA = regA / 2**{combstr} = " + tstr(regA) + " / 2**" + tstr(combo) + " = " + tstr(newregA) + "\n"
            regA = newregA
        elif opcode==1: # 'bxl'
            newregB = regB ^ operand
            progstr += os + ": regB = regB ^ operand = " + tstr(regB) + " ^ " + tstr(operand) + " = " + tstr(newregB) + "\n"
            regB = newregB
        elif opcode==2: #'bst'
            regB = combo % 8
            progstr += os + f": regB = {combstr} % 8       = " + tstr(combo) + " % " + tstr(8) + " = " + tstr(regB) + "\n"
        elif opcode==3: #'jnz'
            if regA>0:
                ip = operand - 2
                progstr += os + ": " + tstr(regA) + " > 0, ip = " + tstr(operand) + " - " + tstr(2) + "\n"
            else:
                progstr += "end\n"
        elif opcode==4: #'bxc'
            newregB = regB ^ regC
            progstr += os + ": regB = regB ^ regC    = " + tstr(regB) + " ^ " + tstr(regC) + " = " + tstr(newregB) + "\n"
            regB = newregB
        elif opcode==5: #'out'
            output += str(tstr(combo % 8))+","
            progstr += os + f": output({combstr}%8)        = (" + tstr(combo) + " % " + tstr(8) + ") = " + tstr(combo % 8) + "\n"
        elif opcode==6: #'bdv'
            regB = int(regA / 2**combo)
            progstr += os + f": regB = regA / 2**{combstr} = " + tstr(regA) + " / 2**" + tstr(combo) + " = " + tstr(regB) + "\n"
        elif opcode==7: #'cdv'
            regC = int(regA / 2**combo)
            progstr += os + f": regC = regA / 2**{combstr} = " + tstr(regA) + " / 2**" + tstr(combo) + " = " + tstr(regC) + "\n"
        ip += 2
        #print(progstr,end="")
    #print(progstr,end="")
    output = output[0:-1]
    ag = 21
    if output==progout:
        print('BINGO: ',override)
    if output[0:ag]==progout[0:ag]:
        print(f'{dstr(override):36}: {output}')
        print(f'{dstr(0):36}: {progout}')
