import numpy as np
import re
tol = 0.00001
tot = 0
offset = 10000000000000
with open("d13.dat") as f:
    while True:
        Aline = f.readline()
        if not Aline:
            break
        Bline = f.readline()
        Cline = f.readline()
        blank = f.readline()
        Aproc = re.split(r'[ |+|,]', Aline.strip())
        Bproc = re.split(r'[ |+|,]', Bline.strip())
        Cproc = re.split(r'[ |=|,]', Cline.strip())
        A = np.array((int(Aproc[3]),int(Aproc[6])))
        B = np.array((int(Bproc[3]),int(Bproc[6])))
        C = np.array((int(Cproc[2])+offset,int(Cproc[5])+offset))
        P = np.zeros(2)
        Q = np.zeros(2)
        #print(A,B,C)
        D = A[0]*B[1] - A[1]*B[0]
        if D == 0:
            print(A,B,C,"DET ZERO no solution")
            continue
        P[0] = B[1]/D
        P[1] = -B[0]/D
        Q[0] = -A[1]/D
        Q[1] = A[0]/D
        m = np.dot(P,C)
        n = np.dot(Q,C)
        if abs(m-round(m)) > tol or abs(n-round(n)) > tol:
            #print(A,B,C,m,n,abs(m-round(m,3))>tol,abs(n-round(n,3))>tol,"No integer solution")
            continue
        #if (n>100) or (m>100):
        #    print(A,B,C,"Too large")
        #    continue
        #if (n<0) or (m<0):
        #    print(A,B,C,"Too small")
        #    continue
        i = int(m)
        j = int(n)
        #print(np.dot(P,A),np.dot(P,B))
        #print(np.dot(Q,A),np.dot(Q,B))
        #print(np.dot(P,C),np.dot(Q,C))
        tot = tot + 3*m + n
        #print(A,B,C,m,n,i,j,m*A+n*B-C,3*m+n,tot)

print(tot)
