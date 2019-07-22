# -*- coding: utf-8 -*-
import sys
import os

if(2 > len(sys.argv)):
    print("ERROR: Modo de uso: " + sys.argv[0] + " ROUTE")
    sys.exit(1)

path = sys.argv[1]



filesNames = (
    "stats.c.out", 
    "stats.f.out",
    "stats.r.out"
)

for graph in os.listdir(path):
    # print(graph)
    for fileName in filesNames:
        route = path + graph + "/" + fileName

        f = open(route, "r")
        lines = f.readlines()
        f.close()

        f = open(route + ".csv", "w")

        first = lines.pop(0).split()

        firstLine = first[0] + " " + first[2] + " " + first[4] + "\n"
        f.write(firstLine)
        newLine = first[1] + " " + first[3] + " " + first[5] + "\n"
        f.write(newLine)

        for line in lines:
            line = line.split()
            if(1 == len(line)):
                break
            newLine = line[1] + " " + line[3] + " " + line[5] + "\n"
            f.write(newLine)

        # print(route)
        # print(first)

        f.close()
        # break
    # break
   # print(line[0])
