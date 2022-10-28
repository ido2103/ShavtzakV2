from funcs import append_json
from GUI import Window
import sys
import json
from PyQt5.QtWidgets import *

#append_json("Nir",0,0,0,0,0,0,0, True, True, False, False)

def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())

app()
