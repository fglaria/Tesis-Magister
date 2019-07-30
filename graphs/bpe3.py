import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 22})

graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "coPapersDBLP", "coPapersCiteseer")


# rf = (4.208, 5.826, 5.942, 6.499, 6.602, 9.996, 0.744, 0.476)
# rc = (4.246, 5.870, 6.182, 6.656, 6.702, 10.082, 0.770, 0.492)
# rr = (4.454, 6.207, 6.276, 6.878, 7.199, 10.500, 0.802, 0.529)
rf = (3.82, 5.44, 5.73, 6.48, 6.41, 10.46, 0.76, 0.48)
rc = (3.858, 5.470, 5.966, 6.633, 6.499, 10.526, 0.785, 0.499)
rr = (3.96, 5.74, 5.85, 6.58, 6.89, 10.44, 0.78, 0.52)

# colors = ("#2c7fb8", "#7fcdbb", "#edf8b1")
colors = ("#31a354", "#addd8e", "#f7fcb9")

labels = ("$r_r$", "$r_c$", "$r_f$")

x = np.arange(len(rf))
w = 0.3

plt.bar(x - w, rr, width=w, color=colors[0], edgecolor="black", label=labels[0])
plt.bar(x, rc, width=w, color=colors[1], edgecolor="black", label=labels[1])
plt.bar(x + w, rf, width=w, color=colors[2], edgecolor="black", label=labels[2])

plt.title("BPE de estructuras compactas para funciones de ranking.", fontsize=20)
plt.xticks(x, graphs, rotation=20, fontsize=20)
plt.xlabel("Grafos")
plt.ylabel("BPE")
plt.legend()
# plt.grid(True)
plt.gca().yaxis.grid(True)

plt.show()
