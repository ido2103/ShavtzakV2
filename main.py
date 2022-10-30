import pstats

from GUI import Window
import sys
import json
from funcs import doMitbah, doShmira, doHamal, doSiur, printAllFuncs
from PyQt5.QtWidgets import *
import cProfile


def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())


with open("soldiers.json", "r") as f:
        data = json.load(f)
        for i in data:
            for n in i:
                try:
                    i[n] = int(i[n])
                except ValueError as exc:
                    pass

with cProfile.Profile() as pr:
    for i in range(10000):
        print(cycle(data, 2, 2, debug=True))

stats = pstats.Stats(pr)
stats.sort_stats(pstats.SortKey.TIME)
stats.print_stats()

app()
