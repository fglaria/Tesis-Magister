import sys
import matplotlib.pyplot as plt
import numpy as np


colors = ("#55dde0", "#377eb8", "#e41a1c", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33")

# Markers
#markers = ("o", "s", "P", "D", "v", "^", ">", "<")
markers = ("X", "p", ".", "d", "*", "H", "h")

x = np.arange(len(markers))

for i, m in enumerate(markers):
    plt.scatter(x[i], 7, s=400, marker=markers[i], color=colors[i], linewidths=1, edgecolors="#000000")
    plt.scatter(x[i], 5, s=600, marker=markers[i], color=colors[i], linewidths=1, edgecolors="#000000")
    plt.scatter(x[i], 3, s=800, marker=markers[i], color=colors[i], linewidths=1, edgecolors="#000000")

    #plt.scatter(x[i], 7, s=400, marker=markers[i], color="k", linewidths=1, edgecolors="#000000")
    #plt.scatter(x[i], 5, s=600, marker=markers[i], color="k", linewidths=1, edgecolors="#000000")
    #plt.scatter(x[i], 3, s=800, marker=markers[i], color="k", linewidths=1, edgecolors="#000000")

# x1 = """
#     $XY_{wm}$ $B_{rrr}$  $BB_{hutu}$\n
#     $XY_{wt}$ $B_{rrr}$  $BB_{hutu}$\n
#     $XY_{wm}$ $B_{rrr}$  $BB_{huff}$\n
#     $XY_{wt}$ $B_{rrr}$  $BB_{huff}$\n
#     $XY_{wm}$ $B_{sdb}$  $BB_{hutu}$\n
#     $XY_{wt}$ $B_{sdb}$  $BB_{hutu}$\n
#     $XY_{wm}$ $B_{sdb}$  $BB_{huff}$\n
#     $XY_{wt}$ $B_{sdb}$  $BB_{huff}$\n
#     """
# x2 = """
#     $r_{f}$\n
#     $r_{c}$\n
#     $r_{r}$\n
# """

# plt.xlabel(x2)
plt.show()

