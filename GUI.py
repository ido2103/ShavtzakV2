from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from funcs import append_json
import json


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Shavtzak Maker")

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1000, 1000)

        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "Soldiers")

        # Setting up tab 2 (used for the list)
        self.tab2.layout = QVBoxLayout(self)
        self.table1 = Table()
        self.tab2.layout.addWidget(self.table1)
        self.tab2.setLayout(self.tab2.layout)

        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setText("Add")
        self.buttonAdd.clicked.connect(self.table1.addRow)
        self.tab2.layout.addWidget(self.buttonAdd)

        self.buttonRemove = QPushButton(self)
        self.buttonRemove.setText("Remove")
        self.buttonRemove.clicked.connect(self.table1.removeaRow)
        self.tab2.layout.addWidget(self.buttonRemove)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class Table(QTableWidget):
    def __init__(self):
        # saving the data to be used for building the table from a json file.
        with open("soldiers.json", "r") as f:
            self.data = json.load(f)
        self.keys = ["Name:", "S.G:", "Tapuz:", "Hamal:",
                "Siur:",
                "Mitbah:",
                "Resting Hours:",
                "Mitbah Cooldown:",
                "IsHamal",
                "IsPtorMitbah",
                "IsPtorShmira",
                "IsSevevMP",
                 "Division"]
        QTableWidget.__init__(self)  # super
        self.setColumnCount(len(self.keys))
        self.setRowCount(len(self.data))
        self.setHorizontalHeaderLabels(self.keys)
        # setting the items in the 2d table using doubled for loops.
        for r, dictionary in enumerate(self.data):
            for c, key in enumerate(dictionary):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(dictionary[key])))
        # every time you edit a section of the qtable it auto-saves.
        self.itemChanged.connect(self.updateJson)

    def updateJson(self):
        # this function gets called every time the qtable gets edited.
        list = []
        print("Updating...")
        # these 2 for's make a list to  be saved as the new json file.
        for r, name in enumerate(self.data):
            temp_dict = {"Name:": "", "S.G:": 0, "Tapuz:": 0, "Hamal:": 0,
                         "Siur:": 0,
                         "Mitbah:": 0,
                         "Resting Hours:": 0,
                         "Mitbah Cooldown:": 0,
                         "IsHamal": 0,
                         "IsPtorMitbah": 0,
                         "IsPtorShmira": 0,
                         "IsSevevMP": 0,
                         "Division": 0}
            for c, info in enumerate(name):
                if self.item(r, c) is None:
                    pass
                else:
                    temp_dict.update({self.keys[c]: self.item(r, c).text()})
            list.append(temp_dict)
        # updating the actual file
        with open("soldiers.json", "w") as f:
            f.seek(0)
            json.dump(list, f, indent=6)
        self.data = list
        print("updated json!")

    def addRow(self):
        # this function adds a new row to be edited from a template.
        print("addRow clicked.")
        # updating self.data to include the new row and updating the json
        self.data = append_json("Insert Name", 0, 0, 0, 0, 0, 0, 0, False, False, False, False, 0)
        self.insertRow(self.rowCount())
        # the dict that goes in the actual qtable (not in the file and program)
        temp_dict = {"Name:": "Insert Name", "S.G:": "0", "Tapuz:": "0", "Hamal:": "0", "Siur:": "0", "Mitbah:": "0",
                     "Resting Hours:": "0",
                     "Mitbah Cooldown:": "0",
                     "IsHamal": "False",
                     "IsPtorMitbah": "False",
                     "IsPtorShmira": "False",
                     "IsSevevMP": "False",
                     "Division": "0"}
        for c, key in enumerate(temp_dict):
            self.setItem(self.rowCount() - 1, c, QtWidgets.QTableWidgetItem(temp_dict[key]))  # setting up the new row
        print("Finished reprinting.")
        print("Added.")

    def removeaRow(self):
        # removes a row using a row number and a pop-up to ask the user which row to remove
        num = QtWidgets.QInputDialog.getInt(QtWidgets.QWidget(), "RemoveRow", "Which row do you want to remove?")
        if num[0] > self.rowCount():
            print("bigger num")
            try:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Invalid Number.")
                msg.exec_()
            except Exception as exc:
                print(exc)
            return
        if num[1]:  # num[1] is the boolean from the num enumerate. if it's true the user pressed ok.
            # if it's false the user pressed cancel
            self.removeRow(num[0]-1)  # removing the row from the qtable
        else:
            return
        d = self.data[num[0]-1]
        # updating the data to not include the dict in the removed row and updating the file to not include it.
        self.data.remove(d)
        self.updateJson()
        print("Removed row {0}".format(num[0]))
