import sys
import matplotlib.pyplot as plt
import numpy as np

graphs = ("marknewman-astro", "marknewman-condmat", "dblp-2010", "dblp-2011", "snap-dblp", "snap-amazon", "ca-coauthors")

functions = ("$r_{r}$", "$r_{c}$", "$r_{f}$")

sequences = ("$x_{wm}$", "$x_{wt}$", "$b_{rrr}$", "$b_{sdb}$", "$bb_{hutu}$", "$bb_{huff}$", "$y_{wm}$", "$y_{wt}$")

compact = (
    ("$x_{wm}$", "$b_{rrr}$", "$bb_{hutu}$", "$y_{wm}$"),
    ("$x_{wt}$", "$b_{rrr}$", "$bb_{hutu}$", "$y_{wt}$"),
    ("$x_{wm}$", "$b_{rrr}$", "$bb_{huff}$", "$y_{wm}$"),
    ("$x_{wt}$", "$b_{rrr}$", "$bb_{huff}$", "$y_{wt}$"),
    ("$x_{wm}$", "$b_{sdb}$", "$bb_{hutu}$", "$y_{wm}$"),
    ("$x_{wt}$", "$b_{sdb}$", "$bb_{hutu}$", "$y_{wt}$"),
    ("$x_{wm}$", "$b_{sdb}$", "$bb_{huff}$", "$y_{wm}$"),
    ("$x_{wt}$", "$b_{sdb}$", "$bb_{huff}$", "$y_{wt}$")
)

labels = (
    ("wm", "rrr", "hutu", "wm"),
    ("wt", "rrr", "hutu", "wt"),
    ("wm", "rrr", "huff", "wm"),
    ("wt", "rrr", "huff", "wt"),
    ("wm", "sdb", "hutu", "wm"),
    ("wt", "sdb", "hutu", "wt"),
    ("wm", "sdb", "huff", "wm"),
    ("wt", "sdb", "huff", "wt")
)

colors = ( "#005a32", "#238443", "#41ab5d", "#78c679", "#addd8e", "#d9f0a3", "#f7fcb9", "#ffffe5")

bits = {
    "marknewman-astro": {
        "$r_{r}$": (657528, 655032, 26200, 37568, 331912, 334920, 64568, 62904),
        "$r_{c}$": (520504, 517880, 17368, 29056, 443720, 446280, 48184, 45880),
        "$r_{f}$": (507512, 504568, 17240, 26416, 450888, 453128, 44856, 42744)
    },
    "marknewman-condmat": {
        "$r_{r}$": (1494392, 1492024, 61720, 85536, 466472, 470504, 158328, 156152),
        "$r_{c}$": (1225016, 1222584, 36504, 57048, 704520, 706760, 96696, 94904),
        "$r_{f}$": (1206392, 1203960, 36568, 53504, 710888, 712424, 93176, 91704)
    },
    "dblp-2010": {
        "$r_{r}$": (7412280, 7407480, 430424, 638616, 1088424, 1097128, 1207864, 1206520),
        "$r_{c}$": (6721336, 6715640, 264792, 455976, 2237544, 2243368, 762296, 762552),
        "$r_{f}$": (6376120, 6373560, 264536, 452072, 2233960, 2237288, 724664, 726200)
    },
    "dblp-2011": {
        "$r_{r}$": (32853944, 32828536, 1499800, 1963152, 7279144, 7397224, 4497976, 4508216),
        "$r_{c}$": (28130424, 28117304, 800664, 1172680, 13362280, 13419688, 2347192, 2359928),
        "$r_{f}$": (27129144, 27120312, 792408, 1155008, 13417192, 13468392, 2249848, 2262648)
    },
    "snap-dblp": {
        "$r_{r}$": (11034360, 11027576, 450520, 706304, 2321960, 2341736, 1308280, 1308728),
        "$r_{c}$": (9337976, 9329784, 267864, 398040, 3710120, 3712424, 756792, 760952),
        "$r_{f}$": (9157240, 9150200, 264152, 391248, 3717672, 3718760, 724024, 725560)
    },
    "snap-amazon": {
        "$r_{r}$": (32730680, 32719032, 1052056, 1402544, 14134568, 14330472, 3394104, 3410680),
        "$r_{c}$": (28092216, 28087160, 720600, 1074328, 18155816, 18265640, 2298040, 2316216),
        "$r_{f}$": (27688056, 27681592, 701272, 1045264, 18264104, 18376168, 2194616, 2211320)
    },
    "ca-coauthors": {
        "$r_{r}$": (21342328, 21329848, 573528, 788080, 1439880, 1453192, 1091192, 1089528),
        "$r_{c}$": (17791928, 17784056, 419992, 554488, 4341608, 4370536, 912184, 915448),
        "$r_{f}$": (16764152, 16753208, 388504, 518376, 4709416, 4757608, 810104, 813240)
    },
}


# x = np.arange(len(functions))
x = np.arange(1)
p = 0.2
b = len(compact)
w = (1 - p)/b
linewidth = 1

for graph in bits:

    wStart = -3.5

    for sequence in compact:
        values = {
            "$r_{r}$": 0,
            "$r_{c}$": 0,
            "$r_{f}$": 0
        }

        for seq in sequence:
            index = sequences.index(seq)

            for fr in functions:
                values[fr] += bits[graph][fr][index]
            
        val = [values["$r_{r}$"]]

        cIndex = compact.index(sequence)

        label = ' '.join(labels[cIndex])
        
        plt.bar((x-wStart*w),  val, width=w, color=colors[cIndex], linewidth=linewidth, edgecolor="black", label=label)

        wStart += 1

    plt.title("Espacio total de posibles estructuras compactas para " + graph + ", en bits.")
    plt.xticks(x, functions)
    plt.xlabel("Secuencias para estructura compacta")
    plt.ylabel("Espacio en bits")
    # plt.ylim(bottom=1000000)
    plt.grid(True, axis='y')
    plt.minorticks_on()
    plt.legend(loc=4)
    plt.show()

    # break

