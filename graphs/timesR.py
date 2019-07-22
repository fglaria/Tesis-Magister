import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 22})

graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "coPapersDBLP", "coPapersCiteseer")

rf = (12.93, 10.56, 7.04, 19.49, 10.23, 64.98, 50.49, 2.52)
rc = (12.57, 10.20, 7.06, 19.44, 9.76, 64.48, 48.52, 2.61)
rr = (4.80, 4.92, 4.75, 7.03, 6.01, 19.33, 1.69, 1.57)

colors = ("#2c7fb8", "#7fcdbb", "#edf8b1")
colors = ("#31a354", "#addd8e", "#f7fcb9")
labels = ("$r_r$", "$r_c$", "$r_f$")

x = np.arange(len(rf))
w = 0.3

plt.bar(x - w, rr, width=w, color=colors[0], edgecolor="black", label=labels[0])
plt.bar(x, rc, width=w, color=colors[1], edgecolor="black", label=labels[1])
plt.bar(x + w, rf, width=w, color=colors[2], edgecolor="black", label=labels[2])

plt.title("Tiempos de acceso aleatorio para funciones de ranking.", fontsize=20)
plt.xticks(x, graphs, rotation=20, fontsize=20)
plt.xlabel("Grafos")
plt.ylabel("Tiempo [s]")
plt.legend()
# plt.grid(True)
plt.gca().yaxis.grid(True)

plt.show()
