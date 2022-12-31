from GUI import Window
import sys
from funcs import computeList
from PyQt5.QtWidgets import QApplication
import pstats
import cProfile


def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())
"""
pr = cProfile.Profile()
pr.enable()
# mostly used for bug testing without the GUI since the GUI doesn't show exceptions, it just crashes.
computeList(1, 1, 3, 1000, "רגיל", [], "", 0)
pr.disable()
stats = pstats.Stats(pr)
stats.sort_stats("tottime")
stats.print_stats()
"""

if __name__ == '__main__':
    app()
