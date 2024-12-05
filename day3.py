import numpy as np
tot=0
enabled = True
with open('d3.dat') as f:
    d=f.read()
    #d=d[450:1000]
    dp = d.split('don\'t()')
    print('\n\n\n\nd=',d)
    print('\n\ndp=',dp)
    dpp=[dp[0]]
    for s in dp[1:]:
        r = s.split('do()')
        #print('r=',r)
        for q in r[1:]:
            dpp.append(q)
    print('\n\ndpp=',dpp)
    dppp="".join(s for s in dpp)
    print('dppp=',dppp)
    with open('d3p.dat','w') as f:
        f.write(dppp)
    dmul=dppp.split('mul')
    for op in dmul[1:]:
        a=0
        b=0
        if op[0]=='(':
            if op[2]==',':
                a=int(op[1])
                rop=op[3:]
            elif op[3]==',':
                a=int(op[1:3])
                rop=op[4:]
            elif op[4]==',':
                a=int(op[1:4])
                rop=op[5:]
            if rop[1]==')':
                b=int(rop[0])
            elif rop[2]==')':
                b=int(rop[0:2])
            elif rop[3]==')':
                b=int(rop[0:3])
        print(a,b,a*b)
        tot = tot+a*b
    #print(dmul[1:])
print(tot)
