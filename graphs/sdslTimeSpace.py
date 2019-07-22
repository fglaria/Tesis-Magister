# -*- coding: utf-8 -*-
from __future__ import division
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 28})

if(3 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " SPACE_FILE TIME_FILE SECUENCIAL/ALEATORIO(S|A)")
    sys.exit(1)

spaceFile = sys.argv[1]
timeFile = sys.argv[2]
# secAle = sys.argv[3]

# if "S" == secAle:
#     secAle = u"de reconstrucción secuencial"
# elif "A" == secAle:
#     secAle = u"de acceso aleatorio"
# else:
#     print(u"ERROR: Tipo inválido (S|A): " + secAle)
#     sys.exit(1)

# Load files
fSpace = open(spaceFile, "r")
linesSpace = fSpace.readlines()
fSpace.close()
fTime = open(timeFile, "r")
linesTime = fTime.readlines()
fTime.close()

# print(linesSpace, linesTime)

# Read lines
graph = ""
function = ""

space = {}
for line in linesSpace:
    if "G" == line[0]:
        line = line.split(" ")
        graph = line[1]
        if graph not in space:
            space[graph] = {}
        function = line[2].strip()
        space[graph][function] = []
    else:
        space[graph][function].append(float(line))

del linesSpace

time = {}
for line in linesTime:
    if "G" == line[0]:
        line = line.split(" ")
        graph = line[1]
        if graph not in time:
            time[graph] = {}
        function = line[2].strip()
        time[graph][function] = []
    else:
        line = line.split(" ")
        milisecs = int(line[0])
        edges = int(line[1])
        microsec = 1000*milisecs/edges
        time[graph][function].append(microsec)

del linesTime


# PLOTTING
# Colors for graphs
# colors = ("#f7fcb9", "#addd8e", "#31a354")
# colors = ("#FF0000", "#00FF00", "#0000FF")
# colors = ("#31a354", "#addd8e", "#f7fcb9")
colors = {
    "F": "#f7fcb9",
    "C": "#addd8e",
    "R": "#31a354"
}

# colors = ("#996633", "#b933ad", "#808183")
# colors = ("#0039a6", "#ff6319", "#6cbe45", "#996633", "#ee352e", "#fccc0a", "#b933ad", "#808183")
# Markers
markers = ("o", "s", "P", "D", "v", "^", ">", "<")
# markers = ("+", "x", "1", "2", ".", "*")

functions = {
    "F": "$r_{f}$",
    "C": "$r_{c}$",
    "R": "$r_{r}$"
}


for graph in space:
    for fIndex, f in enumerate(space[graph]):

        for sIndex, sData in enumerate(space[graph][f]):
            tData = time[graph][f][sIndex]
            plt.scatter(sData, tData, s=400, c=colors[f], marker=markers[sIndex], linewidths=1, edgecolors="#000000", label=f)

        # print (f)
        # break

        # plt.title("BPE vs Tiempo, para " + graph + " y funcion " + functions[f])
    # plt.title("BPE vs Tiempo " + secAle + " medio, para " + graph, fontsize=20)
    # plt.savefig.format = 'pdf'
    plt.title(graph, fontsize=28)
    # plt.legend()
    plt.xlabel("BPE")
    plt.ylabel("Tiempo [$\mu s$]")
    plt.grid()
    # plt.minorticks_on()
    plt.show()

