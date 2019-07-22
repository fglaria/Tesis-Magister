# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt
import operator

matplotlib.rcParams.update({'font.size': 22})

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " GRAPH")
    sys.exit(1)

graphsRoute = sys.argv[1]

f=open(graphsRoute, "r")

lines = f.readlines()

nodes = int(lines.pop(0))

howMany = {}

for adjacent in lines:
    adjacent = adjacent.split(" ")

    size = len(adjacent) - 1

    if(size not in howMany):
        howMany[size] = 0

    #node2 = pair[1]

    howMany[size] += 1

# howMany = {}

# for node, count in graphCount.items():
#     if count not in howMany:
#         howMany[count] = 0

#     howMany[count] += 1

sorted_x = sorted(howMany.items(), key=operator.itemgetter(0))

#print(howMany.items())
# print(sorted_x)

plt.plot([x[1] for x in sorted_x], 'o')
plt.title("coPapersCiteseer", fontsize=20)
plt.xlabel(u"Grado de vértice")
plt.ylabel("# de Nodos")
plt.yscale("log")
plt.xscale("log")
#plt.xlim((0,))
plt.grid(True)
# plt.savefig(graphFile + ".png")
plt.show()
