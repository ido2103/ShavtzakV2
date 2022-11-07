import pstats
from GUI import Window
import sys
import json
from funcs import computeList
from PyQt5.QtWidgets import *
import cProfile

def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())

# TODO LIST
"""
RETURN SCORE +
SEVEV MP
TRANSLATE UI
GIMELIM
UPGRADE UI
KAF KAF A +
export shavtzak +
"""
# TO IMPROVE
"""
dont use deepcopy use json instead
improve score +
improve kafkafa +
"""

with open("soldiers.json", "r") as f:
        data = json.load(f)
        for i in data:
            for n in i:
                try:
                    i[n] = int(i[n])
                except ValueError as exc:
                    pass

#soldiers = computeList(data, 2, 2, 2, 200, False)
#print(soldiers)
"""
p = cProfile.Profile()
p.run("computeList(data, 2, 2, 1, 5000, False)")
s = pstats.Stats(p)
s.sort_stats("cumtime").print_stats()
#app()
"""
app()
