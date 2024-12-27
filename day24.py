import numpy as np

wires = {}
gates = {}
with open('d24m.dat') as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        wire = line.split(' ')
        wires[wire[0][0:-1]] = int(wire[1])
    while True:
        line = f.readline().strip()
        if not line:
            break
        gate = line.split(' ')
        gates[gate[0],gate[2],gate[4]] = (gate[1],False)

# pass to ensure all wires are defined
for key in gates:
    wire0 = key[0]
    wire1 = key[1]
    wire2 = key[2]
    if wire0 not in wires:
        wires[wire0] = None
    if wire1 not in wires:
        wires[wire1] = None
    if wire2 not in wires:
        wires[wire2] = None

def wirestr(wire):
    return f'{wire:4d}' if wire is not None else 'None'

def run_code(wires,gates):
    while True:
        #print('new iteration')
        alldone = True
        for key in gates:
            wire0 = key[0]
            wire0str = wirestr(wires[wire0])
            wire1 = key[1]
            wire1str = wirestr(wires[wire1])
            wire2 = key[2]
            wire2str = wirestr(wires[wire2])
            op = gates[key][0]
            done = gates[key][1]
            doable = wires[wire0] is not None and wires[wire1] is not None
            if doable and not done:
                alldone = False
                if op == 'AND':
                    wires[wire2] = wires[wire0] & wires[wire1]
                elif op == 'OR':
                    wires[wire2] = wires[wire0] | wires[wire1]
                elif op == 'XOR':
                    wires[wire2] = wires[wire0] ^ wires[wire1]
                else:
                    raise ValueError(f'Unknown operation {op}')
                gates[key] = (op,True)
                newwire2str = wirestr(wires[wire2])
                #print(f'{wire0}({wire0str}) {op:3s} {wire1}({wire1str}) -> {wire2}({wire2str}->{newwire2str}) {doable}')
        if alldone:
            #print('all done, breaking')
            break

def read_from_wires(wires,char):
    outputs = sorted([w for w in wires if w[0]==char])
    bits = [wires[w] for w in outputs]
    output = sum([2**(i)*bits[i] for i in range(len(bits))])
    return output

def set_wires(wires,char,value):
    for key in wires:
        if key[0] == char:
            i = int(key[1:])
            wires[key] = value >> i & 1

rename = {}
reverse = {}
wires_ren = {}
gates_ren = {}

def add_rename(key,key2):
    if key not in rename:
        rename[key] = [key2]
    else:
        rename[key].append(key2)
    if key2 not in reverse:
        reverse[key2] = [key]
    else:
        reverse[key2].append(key)

def check_rename_first(key,char):
    if key in rename:
        if len(rename[key])>1:
            print(f'key {key} has multiple values {rename[key]}')
        return rename[key][0][0]==char
    return False

alldone = False
it = 0
while not alldone:
    alldone = True
    for key in wires:
        if (key[0]=='x' or key[0]=='y' or key[0]=='z') and key not in rename:
            key2 = key
            add_rename(key,key2)
            alldone = False
        for gate in gates:
            op = gates[gate][0]
            # GATE0
            if (key==gate[2] and op=='XOR' and key not in rename and 
                ((gate[0][0]=='x' and gate[1][0]=='y') or (gate[0][0]=='y' and gate[1][0]=='x'))):
                key2 = 'j'+gate[0][1:]
                add_rename(key,key2)
                alldone = False
            # GATE1
            if (key==gate[0] and op=='XOR' and key not in rename and
                check_rename_first(gate[1],'j') and gate[2][0]=='z'):
                    key2 = 'c'+gate[2][1:]
                    add_rename(key,key2)
                    alldone = False
            if (key==gate[1] and op=='XOR' and key not in rename and
                check_rename_first(gate[0],'j') and gate[2][0]=='z'):
                    key2 = 'c'+gate[2][1:]
                    add_rename(key,key2)
                    alldone = False
            # GATE2
            if (key==gate[2] and op=='AND' and key not in rename and
                check_rename_first(gate[0],'j') and 
                check_rename_first(gate[1],'c')):
                    key2 = 'k'+rename[gate[1]][0][1:]
                    add_rename(key,key2)
                    alldone = False
            if (key==gate[2] and op=='AND' and key not in rename and
                check_rename_first(gate[0],'c') and 
                check_rename_first(gate[1],'j')):
                    key2 = 'k'+rename[gate[1]][0][1:]
                    add_rename(key,key2)
                    alldone = False
            # GATE3
            if (key==gate[2] and op=='AND' and key not in rename and 
                ((gate[0][0]=='x' and gate[1][0]=='y') or 
                 (gate[0][0]=='y' and gate[1][0]=='x'))):
                bit = int(gate[0][1:])
                if bit>0:
                    key2 = 'l'+f'{bit:02d}'
                else:
                    key2 = 'c'+f'{bit+1:02d}'
                add_rename(key,key2)
                alldone = False
            # GATE4
            if (key==gate[2] and op=='OR' and key not in rename and
                check_rename_first(gate[0],'k') and 
                check_rename_first(gate[1],'l')):
                    key2 = 'c'+str(f'{int(rename[gate[1]][0][1:])+1:02d}')
                    add_rename(key,key2)
                    alldone = False
            if (key==gate[2] and op=='OR' and key not in rename and
                check_rename_first(gate[0],'l') and 
                check_rename_first(gate[1],'k')):
                    key2 = 'c'+str(f'{int(rename[gate[1]][0][1:])+1:02d}')
                    add_rename(key,key2)
                    alldone = False
    it += 1

# check for duplicate values in rename:
for key in rename:
    if len(rename[key])>1:
        print(f'key {key} has multiple values {rename[key]}')
        quit()
for key in reverse:
    if len(reverse[key])>1:
        print(f'key {key} has multiple values {reverse[key]}')
        quit()

def rename_wires(wires,wires_ren,rename):
    for key in wires:
        if key in rename:
            wires_ren[rename[key][0]] = wires[key]
        else:
            wires_ren[key] = wires[key]

def rename_gates(gates,gates_ren,rename):
    for key in gates:
        gate = gates[key]
        if key[0] in rename:
            key0 = rename[key[0]][0]
        else:
            key0 = key[0]
        if key[1] in rename:
            key1 = rename[key[1]][0]
        else:
            key1 = key[1]
        if key[2] in rename:
            key2 = rename[key[2]][0]
        else:
            key2 = key[2]
        gates_ren[key0,key1,key2] = gate
#print(len(wires),wires)
#print(len(wires_ren),wires_ren)

#run_code(wires,gates)
#run_code(wires_ren,gates_ren)

rename_wires(wires,wires_ren,rename)
rename_gates(gates,gates_ren,rename)

for bit in range(0,46):
    #print()
    for op in ['XOR','AND','OR']:
        bitstr = f'{bit:02d}'
        for gate in gates_ren:
            isdig = [gate[i][1:].isdigit() for i in range(3)]
            if gates_ren[gate][0]==op and any(isdig) and any(int(gate[i][1:])==bit if isdig[i] else False for i in range(2)):
                if gate[0] in reverse:
                    revgate0 = reverse[gate[0]][0]
                else:
                    revgate0 = gate[0]
                if gate[1] in reverse:
                    revgate1 = reverse[gate[1]][0]
                else:
                    revgate1 = gate[1]
                if gate[2] in reverse:
                    revgate2 = reverse[gate[2]][0]
                else:
                    revgate2 = gate[2]
                #print(f'{gate[0]} {gate[1]} {gate[2]} {gates_ren[gate]} {revgate0} {revgate1} {revgate2}')

if False:
    x = read_from_wires(wires,'x')
    y = read_from_wires(wires,'y')
    z = read_from_wires(wires,'z')
    x_r = read_from_wires(wires_ren,'x')
    y_r = read_from_wires(wires_ren,'y')
    z_r = read_from_wires(wires_ren,'z')
    z1 = x+y
def compare_bits(za,zb):
    diffbits = []
    for i in range(46):
        if za >> i & 1 != zb >> i & 1:
            diffbits.append(i)
    return diffbits
#print(x,y)
#print(x_r,y_r)
#print(x+y)
#print(z)
#print(compare_bits(z,z1))
#print(compare_bits(z_r,z1))

xs = np.arange(0,1000000000,100000000)
ys = np.arange(0,1000000000,100000000)
for x in xs:
    for y in ys:
        rename_wires(wires,wires_ren,rename)
        rename_gates(gates,gates_ren,rename)
        set_wires(wires_ren,'x',x)
        set_wires(wires_ren,'y',y)
        run_code(wires_ren,gates_ren)
        z = read_from_wires(wires_ren,'z')
        z1 = x+y
        diffits = compare_bits(z,x+y)
        if len(diffits)>0:
            #pass
            print(x,y,z,z1)
            print(diffits)

# identified swaps from examining the outputs above
swaps = ['z12','vdc','tvb','khg','gst','z33','nhn','z21']
print(",".join(sorted(swaps)))