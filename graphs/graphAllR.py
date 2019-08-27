# -*- coding: utf-8 -*-
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

matplotlib.rcParams.update({'font.size': 22})

if(3 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE TYPE(N|C|B)")
    sys.exit(1)

route = sys.argv[1]
inType = sys.argv[2]

possibleTypes = ("N", "C", "B")


if(inType not in possibleTypes):
    print("ERROR: Invalid type(P|N|C): " + inType)
    sys.exit(1)

if("N" == inType):
    xtitle = u"# de vértices"
    ylabel = u"# de particiones"
elif("C" == inType):
    xtitle = u"# de cliques"
    ylabel = u"# de particiones"
elif("B" == inType):
    xtitle = u"# de bytes por vértice"
    ylabel = u"# de particiones"

bytesPerNode = []

filename = "stats.r.out.csv"

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
    "snap-amazon",
    "coPapersDBLP",
    "coPapersCiteseer"
)

# labels = ("$r_r$", "$r_c$", "$r_f$")

# colors = ("#2c7fb8", "#7fcdbb", "#edf8b1")
# colors = ("#31a354", "#addd8e", "#f7fcb9")

partitions = { i : {} for i in graphFolders}
# print(partitions)

for i, folder in enumerate(graphFolders):
    partitionsData = genfromtxt(route + folder + "/" + filename, delimiter=' ',dtype=str)

    for k, pData in enumerate(partitionsData):
        if(k != 0):
            if("N" == inType):
                pData = int(pData[0])
                if(pData not in partitions[folder]):
                    partitions[folder][pData] = 0
                partitions[folder][pData] += 1
            elif("C" == inType):
                pData = int(pData[2])
                if(pData not in partitions[folder]):
                    partitions[folder][pData] = 0
                partitions[folder][pData] += 1
            elif("B" == inType):
                pData = int(pData[1])
                if(0 == pData):
                    continue
                if(pData not in partitions[folder]):
                    partitions[folder][pData] = 0
                partitions[folder][pData] += 1


# x = np.arange(len(graphFolders))
# w = 0.3

for i, folder in enumerate(graphFolders):
    x = partitions[folder].keys()
    y = partitions[folder].values()
    plt.bar(x, y)#, width=w, color=colors[0], edgecolor="black")


    plt.title(graphNames[i], fontsize=20)
    plt.ylabel(ylabel)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.xticks(x, graphNames, rotation=20, fontsize=20)
    plt.xlabel(xtitle)
    plt.xlim(left=-1)
    # plt.grid(True)
    plt.gca().yaxis.grid(True)
    # plt.legend(labels)
    plt.show()
