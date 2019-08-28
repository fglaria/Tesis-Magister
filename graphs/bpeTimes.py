import sys
import matplotlib
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
import numpy as np

# from matplotlib.pyplot import figure
# figure(num=None, figsize=(64, 48), dpi=100, facecolor='w', edgecolor='k')

# matplotlib.rcParams.update({'font.size': 22})
matplotlib.rcParams.update({'font.size': 28})

fig = plt.figure()
ax = plt.subplot(111)

graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "ca-coauthors", "coPapersCiteseer")
graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "coPapersDBLP", "coPapersCiteseer")

algoBPE = ("$clique_{rf}$", "$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$AD$", "$WG_{a}$", "$WG_{s}$")

# markers = ("p", "H", "d", "h", ".", "*")
markers = {
    "$clique_{rf}$": "X",
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
    "$clique_{rf}$": "#55DDE0",
    "$clique_{rr}$": "#377eb8",
    "$k2tree$": "#e41a1c",
    "$k2tree_{BFS}$": "#4daf4a",
    "$AD$": "#984ea3",
    "$WG_{a}$": "#ff7f00",
    "$WG_{s}$": "#ffff33"
}
# 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'

# bpe = {
#     "marknewman-astro": (4.45, 9.28, 8.05, 5.67, 8.10, 7.30),
#     "marknewman-condmat": (6.20, 12.06, 10.43, 7.86, 11.78, 10.45),
#     "dblp-2010": (6.27, 7.45, 8.00, 6.71, 8.67, 6.91),
#     "dblp-2011": (6.87, 10.18, 11.37, 9.67, 10.13, 8.71),
#     "snap-dblp": (7.19, 11.21, 9.92, 8.14, 11.80, 10.17),
#     "snap-amazon": (10.49, 15.66, 12.33, 10.96, 14.50, 13.35),
#     "coPapersDBLP": (0.80, 3.29, 1.83, 1.81, 2.71, 2.48),
#     "coPapersCiteseer": (0.52, 2.35, 0.87, 0.85, 1.79 , 1.63)
# }
bpe = {
    "marknewman-astro": (3.82, 3.96, 4.89, 4.34, 5.67, 8.10, 7.30),
    "marknewman-condmat": (5.44, 5.74, 6.28, 5.60, 7.86, 11.78, 10.45),
    "dblp-2010": (6.41, 5.84, 4.23, 4.30, 6.71, 8.67, 6.91),
    "dblp-2011": (10.46, 6.58, 5.48, 5.89, 9.67, 10.13, 8.71),
    "snap-dblp": (5.73, 6.89, 5.88, 5.23, 8.14, 11.80, 10.17),
    "snap-amazon": (6.48, 10.44, 8.02, 6.38, 10.96, 14.50, 13.35),
    "coPapersDBLP": (0.76, 0.78, 1.67, 0.94, 1.81, 2.71, 2.48),
    "coPapersCiteseer": (0.48, 0.52, 1.21, 0.45, 0.85, 1.79 , 1.63)
}



algoSec = ("$clique_{rf}$", "$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$WG_{s}$")

# tSec = {
#     "marknewman-astro": (0.15, 0.07, 0.06, 0.28),
#     "marknewman-condmat": (0.28, 0.14, 0.15, 0.52),
#     "dblp-2010": (1.43, 0.29, 0.30, 1.09),
#     "dblp-2011": (7.67, 1.57, 2.10, 2.41),
#     "snap-dblp": (2.23, 0.64, 0.52, 1.20),
#     "snap-amazon": (6.95, 2.37, 1.75, 1.30),
#     "coPapersDBLP": (11.96, 2.02, 1.66, 1.59),
#     "coPapersCiteseer": (11.69, 1.73, 1.10, 1.56)
# }
tSec = {
    "marknewman-astro": (0.09, 0.09, 0.03, 0.02, 0.28),
    "marknewman-condmat": (0.16, 0.16, 0.07, 0.04, 0.52),
    "dblp-2010": (0.79, 0.82, 0.18, 0.16, 1.09),
    "dblp-2011": (4.61, 4.45, 1.10, 1.31, 2.41),
    "snap-dblp": (1.16, 1.26, 0.58, 0.35, 1.20),
    "snap-amazon": (7.09, 4.53, 1.36, 1.13, 1.30),
    "coPapersDBLP": (5.68, 5.81, 1.45, 1.01, 1.59),
    "coPapersCiteseer": (4.62, 5.46, 1.33, 0.65, 1.56)
}

algoAleat = ("$clique_{rf}$", "$clique_{rr}$", "$k2tree$", "$k2tree_{BFS}$", "$AD$", "$WG_{a}$")

# tAleat = {
#     "marknewman-astro": (4.80, 2.54, 1.31, 1.79, 0.052),
#     "marknewman-condmat": (4.92, 5.46, 2.75, 2.32, 0.063),
#     "dblp-2010": (4.75, 5.38, 4.74, 2.15, 0.097),
#     "dblp-2011": (7.03, 11.63, 11.08, 2.36, 0.114),
#     "snap-dblp": (6.01, 10.33, 7.15, 2.30, 0.125),
#     "snap-amazon": (19.33, 14.53, 7.33, 2.47, 0.087),
#     "coPapersDBLP": (1.69, 1.94, 1.17, 0.73, 0.045),
#     "coPapersCiteseer": (1.57, 0.950, 0.480, 0.450, 0.037)
# }
tAleat = {
    "marknewman-astro": (2.97, 2.67, 2.58, 1.33, 1.79, 0.052),
    "marknewman-condmat": (3.32, 3.16, 5.53, 2.81, 2.32, 0.063),
    "dblp-2010": (3.80, 3.70, 5.55, 4.84, 2.15, 0.097),
    "dblp-2011": (5.21, 4.66, 11.43, 10.69, 2.36, 0.114),
    "snap-dblp": (4.06, 4.07, 10.35, 6.93, 2.30, 0.125),
    "snap-amazon": (12.17, 6.99, 13.97, 7.13, 2.47, 0.087),
    "coPapersDBLP": (1.69, 1.51, 1.89, 1.16, 0.73, 0.045),
    "coPapersCiteseer": (1.25, 1.30, 0.95, 0.50, 0.45, 0.037)
}

s=1400

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

    # For every algorithm, one point
    for iA, algo in enumerate(algoBPE):
        # If algorithm in secuencial, add point
        if algo in algoSec:
            plt.scatter(bpe[graph][iA], tSec[graph][algoSec.index(algo)], s=s, marker=markers[algo], color=colors[algo], linewidths=1, edgecolors="#000000", label=algo)

    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), fontsize='small',
    #     ncol=4, fancybox=True, shadow=True)

    # plt.title("BPE vs. Tiempo acceso secuencial para " + graph)
    # plt.title(graph, fontsize=20)
    plt.title(graph, fontsize=28)
    plt.grid(True)
    # plt.figure(figsize=(3,4))
    # plt.legend(fontsize=15)
    plt.xlabel("BPE")
    plt.ylabel("Tiempo [$s$]")
    plt.minorticks_on()
    plt.subplots_adjust(left=0.07, bottom=0.10, right=0.98, top=0.96)
    plt.show()

    #continue


    # If algorithm in aleatory, add point
    for iA, algo in enumerate(algoBPE):
        if algo in algoAleat:
            plt.scatter(bpe[graph][iA], tAleat[graph][algoAleat.index(algo)], s=s, marker=markers[algo], color=colors[algo], linewidths=1, edgecolors="#000000", label=algo)

    # plt.title("BPE vs. Tiempo acceso aleatorio para " + graph)
    # plt.title(graph, fontsize=20)
    plt.title(graph, fontsize=28)
    plt.grid(True)
    # plt.legend(fontsize=15)
    plt.xlabel("BPE")
    plt.ylabel("Tiempo [$\mu s$]")
    plt.minorticks_on()
    plt.subplots_adjust(left=0.07, bottom=0.10, right=0.98, top=0.96)
    plt.show()

    # sys.exit(1)

