# -*- coding: utf-8 -*-
from __future__ import division
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 22})

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE")
    sys.exit(1)

route = sys.argv[1]

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

# colors = (
#     "#FF0000",
#     "#FF7F00",
#     "#FFFF00",
#     "#00FF00",
#     "#0000FF",
#     "#4B0082",
#     "#8B00FF"
# )

cliqueSizes = {}

boxes = []
exes = []

# fig, axs = plt.subplots(7, 1)

for index, graph in enumerate(graphNames):
    if graph not in cliqueSizes:
        cliqueSizes[graph] = {}
        cliqueSizes[graph][0] = 0

    # Load files
    cliqueFile = open(route + graph + ".cliques", "r")
    cliqueLines = cliqueFile.readlines()
    cliqueFile.close()

    for line in cliqueLines:
        line = line.split(" ")
        size = len(line)

        if size not in cliqueSizes[graph]:
            cliqueSizes[graph][size] = 0

        cliqueSizes[graph][size] += 1

    # print(cliqueSizes[graph])
    average = 0
    total = 0
    for size, count in cliqueSizes[graph].items():
        average += size*count
        total += count

    average /= total
    print(max(cliqueSizes[graph].keys()))

    boxes.append(cliqueSizes[graph].values())
    exes.append(cliqueSizes[graph].keys())



    # axs[index].plot(cliqueSizes[graph].keys(), cliqueSizes[graph].values())
    plt.bar(cliqueSizes[graph].keys(), cliqueSizes[graph].values(), label=graph)
    # plt.axhline(y=average, color='r', linestyle='-')
    # plt.text(max(cliqueSizes[graph].keys())*.94, average+1, "{:.2f}".format(average), fontsize=14, color='r')
    plt.title(graph, fontsize=20)
    # plt.xlabel(u"Tamaño de cliques")
    # plt.xlim(left=0, right=max(cliqueSizes[graph].keys()) + 1)
    plt.xlim(left=0, right=338)
    # plt.xlim(left=0)
    # plt.ylabel("# de cliques")
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.yscale("log")
    # plt.legend()
    plt.grid()
    plt.ylabel("# de cliques")
    plt.xlabel(u"Tamaño de cliques")
    plt.show()

# sys.exit(1)

x = np.arange(len(graphNames))

plt.violinplot(boxes, showmeans=True)
plt.boxplot(boxes)
plt.xlabel("Grafos")
plt.xticks(x+1, graphNames, rotation=20, fontsize=20)
plt.ylabel("# de cliques")
plt.yscale("log")
plt.grid()
plt.show()

# plt.violinplot(exes)
# plt.boxplot(exes)
# plt.xlabel("Grafos")
# plt.xticks(x+1, graphNames, rotation=20, fontsize=20)
# plt.ylabel("# de cliques")
# plt.yscale("log")
# plt.grid()
# plt.show()

# plt.boxplot(boxes)
# plt.xlabel("Grafos")
# plt.xticks(x+1, graphNames, rotation=20, fontsize=20)
# plt.ylabel("# de cliques")
# plt.yscale("log")
# plt.grid()
# plt.show()