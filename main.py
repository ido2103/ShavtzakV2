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


#computeList(1, 1, 1, 500, "סמפ", False)


app()

with open("soldiers.json", "r") as f:
        data = json.load(f)
        for i in data:
            for n in i:
                try:
                    i[n] = int(i[n])
                except ValueError as exc:
                    pass

with cProfile.Profile() as pr:
        computeList(1, 1, 1, 500, False)

s = pstats.Stats(pr)
s.sort_stats("cumtime").print_stats()
s.print_stats()

app()
