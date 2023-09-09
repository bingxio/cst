#!/bin/python3
from sys import argv as v; del(v[0])
D = [[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]]
i = v[0]; x, y, m = int(i[0]) - 1, int(i[1]) - 1, int(i[2]) - 1
F,l,r=lambda a:"  ---"if a==1 else"  - -",[*D[y],*D[x]],[*D[y],*D[x]]
r[m], c = 1 if F(l[m])[3]!="-"else 0, [l[1],l[2],l[3],l[2],l[3],l[4]]
for i in range(5,-1,-1): print("%s%s%s" %(F(l[i]), F(c[i]), F(r[i])))
