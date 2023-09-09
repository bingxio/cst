#!/bin/python3
from sys import argv as v
D = [[1,1,1],[1,1,0],[1,0,1],[1,0,0],[0,1,1],[0,1,0],[0,0,1],[0,0,0]]
x, y, m = int(v[1][0]), int(v[1][1]), int(v[1][2])
l, r = [*D[y - 1], *D[x - 1]], [*D[y - 1], *D[x - 1]]
r[m - 1] = (lambda p: 0 if p == 1 else 1)(l[m - 1])
c = [l[1], l[2], l[3], l[2], l[3], l[4]]
f = lambda p: "---" if p == 1 else "- -"
for i in range(5, -1, -1):
    print("  {}  {}  {}".format(f(l[i]), f(c[i]), f(r[i])))
