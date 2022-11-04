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
RETURN SCORE
SEVEV MP
TRANSLATE UI
GIMELIM
UPGRADE UI
--KAF KAF A--
"""

with open("soldiers.json", "r") as f:
        data = json.load(f)
        for i in data:
            for n in i:
                try:
                    i[n] = int(i[n])
                except ValueError as exc:
                    pass
#computeList(data, 1, 2, 1, False)
app()
