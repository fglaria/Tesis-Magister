# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys
from numpy import genfromtxt

matplotlib.rcParams.update({'font.size': 22})

from matplotlib.pyplot import figure
figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='k')

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " NORMALIZED(0|1)")
    sys.exit(1)

normalized = int(sys.argv[1])

extraTitle = " "

if(0 == normalized):
    ytitle = "Bits"
    textbottompaddingfactor = 5e5
else:
    ytitle = u"Proporción normalizada"
    textbottompaddingfactor = 0.01
    extraTitle = " normalizada "

csvFile = "sequences3.csv"
csvFile = "sequences3Profe.csv"
csvFile = "sequences32.csv"
sequencesData = genfromtxt(csvFile, delimiter=',',dtype=str)

gData = {}
graphsNames = []

xSeq = []
b1Seq = []
b2Seq = []
ySeq = []

# Each element of sequencesData is for each graph
for index, sData in enumerate(sequencesData):

    if(0 == normalized):
        divider = (1, 1, 1)
    else:
        divider = (float(sData[13]), float(sData[14]), float(sData[15]))

    f = [
        float(sData[1])/divider[0],
        float(sData[2])/divider[0],
        float(sData[3])/divider[0],
        float(sData[4])/divider[0]
    ]

    c = [
        float(sData[5])/divider[1],
        float(sData[6])/divider[1],
        float(sData[7])/divider[1],
        float(sData[8])/divider[1]
    ]

    r = [
        float(sData[9])/divider[2],
        float(sData[10])/divider[2],
        float(sData[11])/divider[2],
        float(sData[12])/divider[2]
    ]

    gData[sData[0]] = [f, c, r]

    graphsNames.append(sData[0])

    xSeq.append([f[0], c[0], r[0]])
    b1Seq.append([f[1], c[1], r[1]])
    b2Seq.append([f[2], c[2], r[2]])
    ySeq.append([f[3], c[3], r[3]])


# print(len(gData))

xSeq = np.array(xSeq)
b1Seq = np.array(b1Seq)
b2Seq = np.array(b2Seq)
ySeq = np.array(ySeq)

# print(xSeq[:,2])

# figure_size = (6, 4)
# fig = plt.figure(figsize=figure_size)
# ax = plt.gca()

w = 0.3
p = 0.0
x = np.arange(len(gData))
print(x)

#ticks = ["rf", "rc", "rr", "rf", "rc", "rr", "rf", "rc", "rr", "rf", "rc", "rr", "rf", "rc", "rr", "rf", "rc", "rr", "rf", "rc", "rr"]
ticks = ["rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf", "rr", "rc", "rf"]

x2 = np.zeros(len(ticks))
for indexX, xval in enumerate(x):
    x2[3*indexX + 0] = xval - (w + p)
    x2[3*indexX + 1] = xval
    x2[3*indexX + 2] = xval + (w + p)

# colors = ("#02818a", "#67a9cf", "#bdc9e1", "#f6eff7")
# colors = ("#2b8cbe", "#7bccc4", "#bae4bc", "#f0f9e8")
# colors = ("#d7301f", "#fc8d59", "#fdcc8a", "#fef0d9")
colors = ("#6a51a3", "#9e9ac8", "#cbc9e2", "#f2f0f7")
colors = ("#ff69b4", "#ffd700", "#ba55d3", "#DEDF9F")

edgecolor = "#000000"

# textbottompaddingfactor = 5e5
textcenteringfactor = 0.03

# rColors = ("#C75798", "#C48C4F", "#A5CD6A")
rColors = (edgecolor, edgecolor, edgecolor)

xb1 = xSeq + b1Seq
xb1b2 = xb1 + b2Seq
xb1b2y = xb1b2 + ySeq

xb1b2y += textbottompaddingfactor
x2 -= textcenteringfactor

linewidth = 1

# plt.rcParams.update({'font.size': 20})

#xSeq = xSeq.ravel()
#plt.bar(x2, xSeq, width=w, color=colors[0], edgecolor=edgecolor, label="X")
plt.bar(x-(w+p), xSeq[:, 2], width=w, color=colors[0], edgecolor=rColors[0], linewidth=linewidth, label="X")
plt.bar(x, xSeq[:, 1], width=w, color=colors[0], edgecolor=rColors[1], linewidth=linewidth)
plt.bar(x+(w+p), xSeq[:, 0], width=w, color=colors[0], edgecolor=rColors[2], linewidth=linewidth)

#b1Seq = b1Seq.ravel()
#plt.bar(x2, b1Seq, width=w, bottom=xSeq, color=colors[1], edgecolor=edgecolor, label="B")
plt.bar(x-(w+p), b1Seq[:, 2], width=w, bottom=xSeq[:, 2], color=colors[1], edgecolor=rColors[0], linewidth=linewidth, label="B")
plt.bar(x, b1Seq[:, 1], width=w, bottom=xSeq[:, 1], color=colors[1], edgecolor=rColors[1], linewidth=linewidth)
plt.bar(x+(w+p), b1Seq[:, 0], width=w, bottom=xSeq[:, 0], color=colors[1], edgecolor=rColors[2], linewidth=linewidth)

#b2Seq = b2Seq.ravel()
#plt.bar(x2, b2Seq, width=w, bottom=b1Seq+xSeq, color=colors[2], edgecolor=edgecolor, label="BB")
plt.bar(x-(w+p), b2Seq[:, 2], width=w, bottom=xb1[:, 2], color=colors[2], edgecolor=rColors[0], linewidth=linewidth, label="BB")
plt.bar(x, b2Seq[:, 1], width=w, bottom=xb1[:, 1], color=colors[2], edgecolor=rColors[1], linewidth=linewidth)
plt.bar(x+(w+p), b2Seq[:, 0], width=w, bottom=xb1[:, 0], color=colors[2], edgecolor=rColors[2], linewidth=linewidth)

#ySeq = ySeq.ravel()
#plt.bar(x2, ySeq, width=w, bottom=b2Seq+b1Seq+xSeq, color=colors[3], edgecolor=edgecolor, tick_label=ticks, label="Y")
plt.bar(x-(w+p), ySeq[:, 2], width=w, bottom=xb1b2[:, 2], color=colors[3], edgecolor=rColors[0], linewidth=linewidth, label="Y")
plt.bar(x, ySeq[:, 1], width=w, bottom=xb1b2[:, 1], color=colors[3], edgecolor=rColors[1], linewidth=linewidth)
plt.bar(x+(w+p), ySeq[:, 0], width=w, bottom=xb1b2[:, 0], color=colors[3], edgecolor=rColors[2], linewidth=linewidth)


for it, t in enumerate(ticks):
    plt.text(x2[it], xb1b2y[it//3, 2-it%3], t, color=rColors[it%3])

plt.xlabel("Grafos")
plt.xlabel("Datasets")
plt.ylabel(ytitle)
plt.legend()

fontsize = 20
# matplotlib.rcParams.update({'font.size': 14})
plt.title(u"Proporción" + extraTitle + u"de bits por cada secuencia en la estructura compacta para cada función de ranking.", fontsize=fontsize)
plt.title(u"Total bits for each sequence", fontsize=fontsize)
plt.xticks(x, graphsNames, rotation=20, fontsize=fontsize-4)

# plt.grid(True)
plt.gca().yaxis.grid(True)
plt.savefig('seqs_rankf.pdf', bbox_inches='tight')

plt.show()
