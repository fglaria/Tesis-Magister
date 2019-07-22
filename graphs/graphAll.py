# -*- coding: utf-8 -*-
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

matplotlib.rcParams.update({'font.size': 22})

if(3 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE TYPE(P|N|C|B)")
    sys.exit(1)

route = sys.argv[1]
inType = sys.argv[2]

possibleTypes = ("P", "N", "C", "B")


if(inType not in possibleTypes):
    print("ERROR: Invalid type(P|N|C): " + inType)
    sys.exit(1)

if("P" == inType):
    title = u"Número de particiones para cada función de ranking."
    ylabel = u"Número de particiones"
elif("N" == inType):
    title = u"Cantidad máxima de vertices en secuencia $X$ por partición para cada función de ranking."
    ylabel = u"Cantidad de vértices"
elif("C" == inType):
    title = u"Cantidad máxima de cliques por partición para cada función de ranking."
    ylabel = u"Cantidad de cliques"
elif("B" == inType):
    title = u"Cantidad máxima de bytes por vértice para cada función de ranking."
    ylabel = u"Cantidad de bytes"

# nodesPerPart = []
bytesPerNode = []
# cliquePerPart = []

filenames = (
    "stats.r.out.csv",
    "stats.c.out.csv",
    "stats.f.out.csv"
)

graphFolders = (
    "marknewman-astro",
    "marknewman-condmat",
    "dblp-2010",
    "dblp-2011",
    "snap-dblp",
    "snap-amazon",
    "coPapersDBLP",
    "coPapersCiteseer"
)

graphNames = (
    "marknewman-astro",
    "marknewman-condmat",
    "dblp-2010",
    "dblp-2011",
    "snap-dblp",
    "snapd-amazon",
    "coPapersDBLP",
    "coPapersCiteseer"
)

labels = ("$r_r$", "$r_c$", "$r_f$")

colors = ("#2c7fb8", "#7fcdbb", "#edf8b1")
colors = ("#31a354", "#addd8e", "#f7fcb9")

partitions = { i : [0, 0, 0] for i in graphFolders}
# print(partitions)

for i, folder in enumerate(graphFolders):
    for j, filename in enumerate(filenames):
        partitionsData = genfromtxt(route + folder + "/" + filename, delimiter=' ',dtype=str)

        for k, pData in enumerate(partitionsData):
            if(k != 0):
                if("P" == inType):
                    partitions[folder][j] += 1
                elif("N" == inType):
                    pData = int(pData[0])
                    if(partitions[folder][j] < pData):
                        partitions[folder][j] = pData
                elif("C" == inType):
                    pData = int(pData[2])
                    if(partitions[folder][j] < pData):
                        partitions[folder][j] = pData
                elif("B" == inType):
                    pData = int(pData[1])
                    if(partitions[folder][j] < pData):
                        partitions[folder][j] = pData


x = np.arange(len(graphFolders))
w = 0.3

for i, folder in enumerate(graphFolders):
    plt.bar(x[i] - w, partitions[folder][0], width=w, color=colors[0], edgecolor="black")
    plt.bar(x[i], partitions[folder][1], width=w, color=colors[1], edgecolor="black")
    plt.bar(x[i] + w, partitions[folder][2], width=w, color=colors[2], edgecolor="black")


plt.title(title, fontsize=20)
plt.ylabel(ylabel)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xticks(x, graphNames, rotation=20, fontsize=20)
plt.xlabel("Grafos")
# plt.grid(True)
plt.gca().yaxis.grid(True)
plt.legend(labels)
plt.show()
