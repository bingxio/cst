from random import randint
from subprocess import run

x, y, m = randint(1, 8), randint(1, 8), randint(1, 6)
print("top=%d, bottom=%d, move=%d" % (x, y, m))
run(["python3", "mh.py", "%d%d%d" % (x, y, m)])
