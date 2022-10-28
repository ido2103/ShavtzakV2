from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import json


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "Soldiers")

        self.tab2.layout = QVBoxLayout(self)
        self.table1 = Table()
        self.tab2.layout.addWidget(self.table1)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Table(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.setColumnCount(len(keys))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(keys)
        for r, name in enumerate(data):
            for c, info in enumerate(name):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(name[info])))
        self.itemChanged.connect(lambda: self.updateJson(data))

    def updateJson(self, data):
        list = []
        for r, name in enumerate(data):
            temp_dict = {"Name:": "", "S.G:": 0, "Tapuz:": 0, "Hamal:": 0,
            "Siur:": 0,
            "Mitbah:": 0,
            "Resting Hours:": 0,
            "Mitbah Cooldown:": 0,
            "IsHamal": 0,
            "IsPtorMitbah": 0,
            "IsPtorShmira": 0,
            "IsSevevMP": 0}
            for c, info in enumerate(name):
                temp_dict.update({keys[c]: self.item(r, c).text()})
            list.append(temp_dict)
        with open("soldiers.json", "w") as f:
            f.seek(0)
            json.dump(list, f, indent=6)
        print("updated json!")


keys = ["Name:", "S.G:", "Tapuz:", "Hamal:",
            "Siur:",
            "Mitbah:",
            "Resting Hours:",
            "Mitbah Cooldown:",
            "IsHamal",
            "IsPtorMitbah",
            "IsPtorShmira",
            "IsSevevMP"]
with open("soldiers.json", "r") as f:
    data = json.load(f)

