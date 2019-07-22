import sys
import matplotlib
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
import numpy as np

# from matplotlib.pyplot import figure
# figure(num=None, figsize=(64, 48), dpi=100, facecolor='w', edgecolor='k')

matplotlib.rcParams.update({'font.size': 22})

fig = plt.figure()
ax = plt.subplot(111)

graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "ca-coauthors", "coPapersCiteseer")
graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "coPapersDBLP", "coPapersCiteseer")

algoBPE = ("$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$AD$", "$WG_{a}$", "$WG_{s}$")

# markers = ("p", "H", "d", "h", ".", "*")
markers = {
    "$clique_{rr}$": "p",
    "$k2tree$": ".",
    "$k2tree_{BFS}$": "d",
    "$AD$": "*",
    "$WG_{a}$": "H",
    "$WG_{s}$": "h"
}

# colors = {
#     "$clique_{rr}$": "b",
#     "$k2tree$": "g",
#     "$k2tree_{BFS}$": "r",
#     "$AD$": "c",
#     "$WG_{a}$": "m",
#     "$WG_{s}$": "y"
# }
colors = {
    "$clique_{rr}$": "#377eb8",
    "$k2tree$": "#e41a1c",
    "$k2tree_{BFS}$": "#4daf4a",
    "$AD$": "#984ea3",
    "$WG_{a}$": "#ff7f00",
    "$WG_{s}$": "#ffff33"
}
# 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'

bpe = {
    "marknewman-astro": (4.45, 9.28, 8.05, 5.67, 8.10, 7.30),
    "marknewman-condmat": (6.20, 12.06, 10.43, 7.86, 11.78, 10.45),
    "dblp-2010": (6.27, 7.45, 8.00, 6.71, 8.67, 6.91),
    "dblp-2011": (6.87, 10.18, 11.37, 9.67, 10.13, 8.71),
    "snap-dblp": (7.19, 11.21, 9.92, 8.14, 11.80, 10.17),
    "snap-amazon": (10.49, 15.66, 12.33, 10.96, 14.50, 13.35),
    "coPapersDBLP": (0.80, 3.29, 1.83, 1.81, 2.71, 2.48),
    "coPapersCiteseer": (0.52, 2.35, 0.87, 0.85, 1.79 , 1.63)
}

algoSec = ("$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$WG_{s}$")

# tSec = {
#     "marknewman-astro": (0.16, 0.24, 0.14, 0.013),
#     "marknewman-condmat": (0.28, 0.24, 0.22, 0.022),
#     "dblp-2010": (1.36, 0.42, 0.41, 0.059),
#     "dblp-2011": (7.01, 1.76, 2.28, 0.254),
#     "snap-dblp": (2.05, 0.74, 0.66, 0.083),
#     "snap-amazon": (6.90, 2.57, 1.92, 0.183),
#     "ca-coauthors": (11.96, 2.50, 2.27, 0.401)
# }

tSec = {
    "marknewman-astro": (0.15, 0.07, 0.06, 0.28),
    "marknewman-condmat": (0.28, 0.14, 0.15, 0.52),
    "dblp-2010": (1.43, 0.29, 0.30, 1.09),
    "dblp-2011": (7.67, 1.57, 2.10, 2.41),
    "snap-dblp": (2.23, 0.64, 0.52, 1.20),
    "snap-amazon": (6.95, 2.37, 1.75, 1.30),
    "coPapersDBLP": (11.96, 2.02, 1.66, 1.59),
    "coPapersCiteseer": (11.69, 1.73, 1.10, 1.56)
}

algoAleat = ("$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$AD$", "$WG_{a}$")

tAleat = {
    "marknewman-astro": (4.80, 2.54, 1.31, 1.79, 0.052),
    "marknewman-condmat": (4.92, 5.46, 2.75, 2.32, 0.063),
    "dblp-2010": (4.75, 5.38, 4.74, 2.15, 0.097),
    "dblp-2011": (7.03, 11.63, 11.08, 2.36, 0.114),
    "snap-dblp": (6.01, 10.33, 7.15, 2.30, 0.125),
    "snap-amazon": (19.33, 14.53, 7.33, 2.47, 0.087),
    "coPapersDBLP": (1.69, 1.94, 1.17, 0.73, 0.045),
    "coPapersCiteseer": (1.57, 0.950, 0.480, 0.450, 0.037)
}

# fontP = FontProperties()
# fontP.set_size('small')


# For every graph, one plot
for graph in graphs:
    xS = []
    yS = []
    mS = []
    xA = []
    yA = []
    mA = []

    # # For every algorithm, one point
    # for iA, algo in enumerate(algoBPE):
    #     # If algorithm in secuencial, add point
    #     if algo in algoSec:
    #         plt.scatter(bpe[graph][iA], tSec[graph][algoSec.index(algo)], s=400, marker=markers[algo], color=colors[algo], linewidths=1, edgecolors="#000000", label=algo)

    # # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), fontsize='small',
    # #     ncol=4, fancybox=True, shadow=True)

    # # plt.title("BPE vs. Tiempo acceso secuencial para " + graph)
    # plt.title(graph, fontsize=20)
    # plt.grid(True)
    # # plt.figure(figsize=(3,4))
    # # plt.legend(fontsize=15)
    # plt.xlabel("BPE")
    # plt.ylabel("Tiempo [$s$]")
    # plt.minorticks_on()
    # plt.show()

    # continue


    # If algorithm in aleatory, add point
    for iA, algo in enumerate(algoBPE):
        if algo in algoAleat:
            plt.scatter(bpe[graph][iA], tAleat[graph][algoAleat.index(algo)], s=400, marker=markers[algo], color=colors[algo], linewidths=1, edgecolors="#000000", label=algo)

    # plt.title("BPE vs. Tiempo acceso aleatorio para " + graph)
    plt.title(graph, fontsize=20)
    plt.grid(True)
    # plt.legend(fontsize=15)
    plt.xlabel("BPE")
    plt.ylabel("Tiempo [$\mu s$]")
    plt.minorticks_on()
    plt.show()

    # sys.exit(1)

