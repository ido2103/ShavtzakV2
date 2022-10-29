from GUI import Window
import sys
import json
from funcs import doMitbah, doShmira, doHamal
from PyQt5.QtWidgets import *


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


print(doMitbah(data)[0])
print(doShmira(data, "Tapuz:"))
print(doShmira(data, "S.G:"))
print(doHamal(data))
# TODO ADD SIUR
app()
