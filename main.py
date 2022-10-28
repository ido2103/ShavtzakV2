from GUI import Window
import sys
from funcs import seperate_to_divisions
from PyQt5.QtWidgets import *


def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())


app()
