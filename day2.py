with open("d2.dat") as f:
    data = f.readlines()
ranges = data[0].split(',')
total = 0
for r in ranges:
    rs = r.split('-')
    lb = int(rs[0])
    ub = int(rs[1])
    print(r, lb, ub, ub-lb)
    for i in range(lb, ub + 1):
        s = str(i)
        ls = len(s)
        match = False
        for lrep in range(2,12):
            hs = int(ls/lrep)
            if (len(s)%lrep) == 0:
                lrepmatch = True
                for m in range(1,lrep):
                    if (s[0:hs]!=s[m*hs:(m+1)*hs]):
                        lrepmatch = False
                        break
                if lrepmatch:
                    match = True
                    break
        if match:
            total = total + i
            print("  ", s, " is a match")
print(total)