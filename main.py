from GUI import Window
import sys
from PyQt5.QtWidgets import QApplication


def app():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec_())


#computeList(1, 1, 1, 500, "מפ", ['Dolev', 'Ariel Ben Hamo', 'Ido', 'Adeel', 'Lidor', 'Mark', 'Sean'], "", 0)


if __name__ == '__main__':
    app()

