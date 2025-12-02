i = 50
count = 0
print('Initial', i)
with open("d1.dat") as f:
    data = f.readlines()
for line in data:
    sign = +1 if line[0] == 'R' else -1
    val = int(line[1:])
    for j in range(val):
        i = (i + sign) % 100
        if (i==0):
            count = count + 1

    print(line[:-1],sign*val,i,count)
