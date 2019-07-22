# -*- coding: utf-8 -*-

import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE")

route = sys.argv[1]
ending = route[-5:]

textRaw = open(route, 'r')

allData = {
    "data": [],
    "totalPartitions": 0,
    "totalN": [],
    "avgN": [],
    "total0": [],
    "avg0": 0
}

for lineRaw in textRaw:
    lineSplitted = lineRaw.split(' ')

    if("nodesPerPartition" == lineSplitted[0]):
        allData["data"].append([int(lineSplitted[1]), int(lineSplitted[3]), int(lineSplitted[5])])
    elif("TOTALParts" == lineSplitted[0]):
        allData["totalPartitions"] = int(lineSplitted[1])
    elif("TOTALN" == lineSplitted[0]):
        allData["totalN"] = [int(lineSplitted[2]), int(lineSplitted[4]), int(lineSplitted[6]), int(lineSplitted[8]), int(lineSplitted[10]), int(lineSplitted[12])]
    elif("AVG" == lineSplitted[0]):
        allData["avgN"] = [float(lineSplitted[2]), float(lineSplitted[4]), float(lineSplitted[6])]
    elif("TOTAL0" == lineSplitted[0]):
        allData["total0"] = [int(lineSplitted[5]), int(lineSplitted[7]), int(lineSplitted[9]), int(lineSplitted[11]), int(lineSplitted[13]), int(lineSplitted[15])]
    elif("AVG0" == lineSplitted[0]):
        allData["avg0"] = float(lineSplitted[8])
    else:
        continue

#print(allData["data"][1,:])
columns = ("nodesPerPartition", "bytesPerNode", "cliquesPerPartition")
df = pd.DataFrame(np.array(allData["data"]), columns=columns)
df.to_csv(route+".csv", sep=" ", columns=columns, index=False)

nodesPerPartition = df["nodesPerPartition"].value_counts()
bytesPerNode = df["bytesPerNode"].value_counts()
cliquesPerPartition = df["cliquesPerPartition"].value_counts()
# print(nodesPerPartition.sum())
#np.save(route, df)

if("s.out" == ending):
    title = "Razón: "
elif("f.out" == ending):
    title = "Frecuencia: "
elif("c.out" == ending):
    title = "Connectividad: "

figure(num=None, figsize=(10, 8), dpi=200)

# plt.bar(nodesPerPartition.axes[0], nodesPerPartition/nodesPerPartition.sum(), log=False)
# plt.xlim(0, nodesPerPartition.axes[0].max()+1)
# plt.title(title + "Nodos por partición")
# plt.xlabel("Nodos por partición")
# plt.ylabel("Particiones (normalizado)")
# plt.grid(True, linestyle='--')
# plt.savefig(route+".nodes.png", format="png", papertype="letter", orientation="landscape", bbox_inches='tight')
# #plt.show()
# plt.clf()

# plt.bar(bytesPerNode.axes[0], bytesPerNode/bytesPerNode.sum(), log=False)
# plt.xlim(-1, bytesPerNode.axes[0].max()+1)
# plt.title(title + "Bytes por partición")
# plt.xlabel("Bytes por partición")
# plt.ylabel("Particiones (normalizado)")
# plt.grid(True, linestyle='--')
# plt.savefig(route+".bytes.png", format="png", papertype="letter", orientation="landscape", bbox_inches='tight')
# #plt.show()
# plt.clf()

# plt.bar(cliquesPerPartition.axes[0], cliquesPerPartition/cliquesPerPartition.sum(), log=False)
# plt.xlim(0, cliquesPerPartition.axes[0].max()+1)
# plt.title(title + "Cliques por partición")
# plt.xlabel("Cliques por partición")
# plt.ylabel("Particiones (normalizado)")
# plt.grid(True, linestyle='--')
# plt.savefig(route+".cliques.png", format="png", papertype="letter", orientation="landscape", bbox_inches='tight')
# #plt.show()
# plt.clf()



# print(cliquesPerPartition.axes[0])
# np.savetxt("test.csv", cliquesPerPartition, delimiter=' ')





# nodesPerPartition.hist(cumulative=True, density=1, bins=100)
# plt.title(title + "CDF: Nodos por partición")
# plt.xlabel("Cliques por partición")
# plt.ylabel("Particiones (normalizado)")
# plt.grid(True, linestyle='--')
# plt.show()
