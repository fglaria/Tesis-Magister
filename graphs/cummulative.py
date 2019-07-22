# -*- coding: utf-8 -*-
import sys
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt

matplotlib.rcParams.update({'font.size': 22})

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE")
    sys.exit(1)

route = sys.argv[1]

# def numfmt(x, pos): # your custom formatter function: divide by 100.0
#     s = '{}'.format(x / 100000)
#     return s

# import matplotlib.ticker as tkr     # has classes for tick-locating and -formatting
# yfmt = tkr.FuncFormatter(numfmt)    # create your custom formatter function

for graph in os.listdir(route):

    nodesPerPart = []
    bytesPerNode = []
    cliquePerPart = []

    filenames = (
        "stats.out.csv",
        "stats.c.out.csv",
        "stats.f.out.csv"
    )

    labels = ("$r_r$", "$r_c$", "$r_f$")
    # colors = ((237/255, 248/255, 177/255, 0.5), (127/255, 205/255, 187/255, 0.5), (44/255, 127/255, 184/255, 0.5))
    # colors = ("#008DD5", "#9CFC97", "#F64740")
    colors = ("#2c7fb8", "#7fcdbb", "#edf8b1")
    colors = ("#31a354", "#addd8e", "#f7fcb9")

    for fIndex, filename in enumerate(filenames):
        partitionsData = genfromtxt(route + "/" + graph + "/" + filename, delimiter=' ',dtype=str)

        nodesPerPart.append([])
        bytesPerNode.append([])
        cliquePerPart.append([])

        for index, pData in enumerate(partitionsData):
            if(index != 0):
                nodesPerPart[fIndex].append(int(pData[0]))
                bytesPerNode[fIndex].append(int(pData[1]))
                cliquePerPart[fIndex].append(int(pData[2]))
            else:
                continue

        # num_bins = len(set(bytesPerNode[fIndex]))
        # print(num_bins)
        bytesPerNode[fIndex].sort()
        # print(bytesPerNode)
        x = np.array(bytesPerNode[fIndex])
        unique, counts = np.unique(x, return_counts=True)
        # print(graph, fIndex)
        # print(unique, counts)

        plt.hist(bytesPerNode[fIndex], bins=unique, cumulative=True, label=labels[fIndex], color=colors[fIndex], alpha=0.6, edgecolor='black', histtype="stepfilled")

    # plt.title(u"CDF número de bytes por vértice para " + graph)
    plt.title(graph, fontsize=20)
    plt.xlabel(u"# bytes por vértice")
    plt.ylabel(u"# particiones")
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    # plt.gca().yaxis.set_major_formatter(yfmt)
    plt.grid(True)
    plt.legend(loc=4, prop={'size': 16})
    plt.show()
