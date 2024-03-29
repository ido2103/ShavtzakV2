from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from funcs import append_json, computeList
import json


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Shavtzak Maker")
        with open("style.txt", "r") as f:
            style = f.read()
        self.setStyleSheet(style)
        self.soldiers = []
        self.sevev = "רגיל"
        self.inactive = []

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(1, 1)

        self.tabs.addTab(self.tab1, "שבצק")
        self.tabs.addTab(self.tab2, "רשומות חיילים")
        self.tabs.addTab(self.tab3, "הסרת חיילים")
        # setting up tab 1 (used for general control)
        self.tab1.layout = QGridLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.layout.setRowStretch(2, 1)


        self.shavtzak_table = ShavtzakTable()
        self.tab1.layout.addWidget(self.shavtzak_table, 0, 1)

        self.amount_of_siurim_label = QLabel()
        self.amount_of_siurim_label.setText("כמות הסיורים")
        self.tab1.layout.addWidget(self.amount_of_siurim_label, 1, 1)

        self.amount_of_siurim = QLineEdit()
        self.amount_of_siurim.setText("2")
        self.amount_of_siurim.setValidator(QIntValidator())
        self.tab1.layout.addWidget(self.amount_of_siurim, 2, 1)

        self.amount_of_soldiers_label = QLabel()
        self.amount_of_soldiers_label.setText("כמות חיילים בכל סיור")
        self.tab1.layout.addWidget(self.amount_of_soldiers_label, 3, 1)

        self.amount_of_soldiers = QLineEdit()
        self.amount_of_soldiers.setText("1")
        self.amount_of_soldiers.setValidator(QIntValidator())
        self.tab1.layout.addWidget(self.amount_of_soldiers, 4, 1)

        self.amount_of_kka_label = QLabel()
        self.amount_of_kka_label.setText("הכנס מספר חיילים לככ א")
        self.tab1.layout.addWidget(self.amount_of_kka_label, 5, 1)

        self.amount_of_kka = QLineEdit()
        self.amount_of_kka.setText("1")
        self.amount_of_kka.setValidator(QIntValidator())
        self.tab1.layout.addWidget(self.amount_of_kka, 6, 1)

        self.attempts_label = QLabel()
        self.attempts_label.setText("כמה נסיונות ליצירת שבצק? ממולץ 1000-2000")
        self.tab1.layout.addWidget(self.attempts_label, 7, 1)

        self.attempts = QLineEdit()
        self.attempts.setText("1000")
        self.attempts.setValidator(QIntValidator())
        self.tab1.layout.addWidget(self.attempts, 8, 1)

        self.sevev_label = QLabel()
        self.sevev_label.setText("בחר סבב")
        self.tab1.layout.addWidget(self.sevev_label, 9, 2)

        self.sevev_box = QComboBox()
        self.sevev_box.addItems(["רגיל", "מפ", "סמפ"])
        self.sevev_box.currentTextChanged.connect(self.combo_box)
        self.tab1.layout.addWidget(self.sevev_box, 9, 1)

        self.custom_name_label = QLabel()
        self.custom_name_label.setText("בחר שם להכנסת משימה. השאר ריק בשביל לא להוסיף עוד משימה.")
        self.tab1.layout.addWidget(self.custom_name_label, 10, 1)

        self.custom_name = QLineEdit()
        self.custom_name.setText("")
        self.tab1.layout.addWidget(self.custom_name, 11, 1)

        self.custom_num_label = QLabel()
        self.custom_num_label.setText("מספר אנשים למשימה החדשה.")
        self.tab1.layout.addWidget(self.custom_num_label, 12, 1)

        self.custom_num = QLineEdit()
        self.custom_num.setText("0")
        self.custom_num.setValidator(QIntValidator())
        self.tab1.layout.addWidget(self.custom_num, 13, 1)


        self.makeShavtzak = QPushButton(self)
        self.makeShavtzak.setText("צור שבצק")
        self.makeShavtzak.clicked.connect(lambda: self.shavtzak(int(self.amount_of_soldiers.text()),
                                    int(self.amount_of_siurim.text()), int(self.amount_of_kka.text()),
                                    int(self.attempts.text()), self.sevev, self.inactive, self.custom_name.text(),
                                    int(self.custom_num.text())))
        self.tab1.layout.addWidget(self.makeShavtzak, 14, 1)

        self.apply_button = QPushButton()
        self.apply_button.setText("שמור שבצק")
        self.apply_button.clicked.connect(self.shavtzak_table.apply_shavtzak)
        self.tab1.layout.addWidget(self.apply_button, 15, 1)

        # Setting up tab 2 (used for the list)
        self.tab2.layout = QVBoxLayout(self)
        self.table1 = Table()
        self.tab2.layout.addWidget(self.table1)
        self.tab2.setLayout(self.tab2.layout)

        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setText("הוסף")
        self.buttonAdd.clicked.connect(self.table1.addRow)
        self.tab2.layout.addWidget(self.buttonAdd)

        self.buttonRemove = QPushButton(self)
        self.buttonRemove.setText("הסר")
        self.buttonRemove.clicked.connect(self.table1.removeaRow)
        self.tab2.layout.addWidget(self.buttonRemove)

        self.buttonSave = QPushButton(self)
        self.buttonSave.setText("שמור")
        self.buttonSave.clicked.connect(self.table1.updateJson)
        self.tab2.layout.addWidget(self.buttonSave)

        self.buttonResetClmn = QPushButton(self)
        self.buttonResetClmn.setText("אפס רשומה")
        self.buttonResetClmn.clicked.connect(self.table1.removeclmn)
        self.tab2.layout.addWidget(self.buttonResetClmn)

        self.tab3.layout = QVBoxLayout()
        self.tab3.setLayout(self.tab3.layout)

        self.soldierList = QListWidget(self)
        with open("soldiers.json", "r") as f:
            data = json.load(f)
        for i in data:
            self.soldierList.addItem(i["Name:"])
        self.soldierList.clicked.connect(lambda: self.item_clicked(self.soldierList))
        self.tab3.layout.addWidget(self.soldierList)

        self.removed_list = QListWidget()
        for i in self.inactive:
            self.removed_list.addItem(i)
        self.removed_list.clicked.connect(lambda: self.item_clicked(self.removed_list))
        self.tab3.layout.addWidget(self.removed_list)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def shavtzak(self, amountOfSoldiers, amountOfSiurim, amountOfKKA, attempts, sevev, inactive, custom_name, custom_num):
        with open("soldiers.json", "r") as f:
            data = json.load(f)
            for i in data:
                for n in i:
                    try:
                        i[n] = int(i[n])
                    except ValueError:
                        pass
        try:
            self.soldiers, self.best, self.shavtzak_soldiers = computeList(amountOfSoldiers, amountOfSiurim, amountOfKKA, attempts
                                        , sevev, inactive, custom_name, custom_num)
            if custom_name != "":
                if custom_name not in self.shavtzak_table.keys:
                    self.shavtzak_table.keys.append(custom_name)
            self.shavtzak_table.set_items(self.soldiers, amountOfSoldiers, amountOfSiurim)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Question)
            msg.setText("האם אתה מרוצה מהשבצק שנוצר?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.exec_()
            if msg.standardButton(msg.clickedButton()) == QMessageBox.Yes:
                print("Yes")
                with open("soldiers.json", "w") as f:
                    json.dump(self.shavtzak_soldiers, f, indent=6)
                with open("shavtzak.json", "w") as f:
                    f.seek(0)
                    json.dump([self.soldiers, amountOfSoldiers, amountOfSiurim], f, indent=6)
            else:
                return
            self.table1.processDict(self.shavtzak_soldiers)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("שבצק נוצר!")
            msg.exec_()
        except Exception as exc:
            print(exc)
            exception = QMessageBox()
            exception.setIcon(QMessageBox.Critical)
            exception.setText(f"התוכנה לא הצליחה להכין שבצק. \n נסו שוב ואם הבעיה ממשיכה צריך להוסיף חיילים. \n Exception: IndexError {exc}")
            exception.exec_()

    def combo_box(self):
        self.sevev = self.sevev_box.currentText()
        print(self.sevev)

    def item_clicked(self, list):
        try:
            if list == self.soldierList:
                item = self.soldierList.currentItem()
                row = self.soldierList.currentRow()
                if item.text() not in self.inactive:
                    self.inactive.append(item.text())
                    self.removed_list.addItem(item.text())
                    self.soldierList.takeItem(row)

            if list == self.removed_list:
                item1 = self.removed_list.currentItem()
                row = self.removed_list.currentRow()
                self.inactive.remove(item1.text())
                self.removed_list.takeItem(row)
                self.soldierList.addItem(item1.text())
        except Exception as exc:
            print(exc)


class Table(QTableWidget):
    def __init__(self):
        # saving the data to be used for building the table from a json file.
        with open("soldiers.json", "r") as f:
            self.data = json.load(f)
        self.keys = ["Name:", "S.G:", "Tapuz:", "Hamal:",
                "Siur:",
                "Mitbah:",
                "Kaf Kaf A:",
                "Resting Hours:",
                "Mitbah Cooldown:",
                "IsHamal",
                "IsPtorMitbah",
                "IsPtorShmira",
                "Sevev",
                 "Division"]
        QTableWidget.__init__(self)  # super
        self.setColumnCount(len(self.keys))
        self.setRowCount(len(self.data))
        self.setHorizontalHeaderLabels(self.keys)
        self.resizeRowsToContents()
        # setting the items in the 2d table using doubled for loops.
        for r, dictionary in enumerate(self.data):
            for c, key in enumerate(dictionary):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(dictionary[key])))

    def updateJson(self):
        # whenever you call this function it saves the qtable in the json. it also gets
        # auto-called during things such as removing a row, adding a row, etc.
        list = []
        print("Updating...")
        # these 2 for's make a list to  be saved as the new json file.
        for r, name in enumerate(self.data):
            temp_dict = {"Name:": "", "S.G:": 0, "Tapuz:": 0, "Hamal:": 0,
                         "Siur:": 0,
                         "Mitbah:": 0,
                         "Kaf Kaf A:": 0,
                         "Resting Hours:": 0,
                         "Mitbah Cooldown:": 0,
                         "IsHamal": 0,
                         "IsPtorMitbah": 0,
                         "IsPtorShmira": 0,
                         "Sevev": 0,
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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("נשמר")
        msg.exec_()

    def addRow(self):
        # this function adds a new row to be edited from a template.
        print("addRow clicked.")
        # updating self.data to include the new row and updating the json
        self.data = append_json("Insert Name", 0, 0, 0, 0, 0, 0, 0, 0, False, False, False, False, 0)
        self.insertRow(self.rowCount())
        # the dict that goes in the actual qtable (not in the file and program)
        temp_dict = {"Name:": "Insert Name", "S.G:": "0", "Tapuz:": "0", "Hamal:": "0", "Siur:": "0", "Mitbah:": "0",
                     "KafKaf A:": "0",
                     "Resting Hours:": "0",
                     "Mitbah Cooldown:": "0",
                     "IsHamal": "No",
                     "IsPtorMitbah": "No",
                     "IsPtorShmira": "No",
                     "Sevev": "SMP",
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
        print(f"Removed row {num[0]}")

    def removeclmn(self): # rewrite using QComboBox
        num = QtWidgets.QInputDialog.getInt(QtWidgets.QWidget(), "Reset Column", "Which column do you want to reset?")
        if num[1]:
            if num[0] > 0:
                match num[0]:
                    case 1:
                        for i in self.data:
                            i["S.G:"] = 0
                    case 2:
                        for i in self.data:
                            i["Tapuz:"] = 0
                    case 3:
                        for i in self.data:
                            i["Hamal:"] = 0
                    case 4:
                        for i in self.data:
                            i["Siur:"] = 0
                    case 5:
                        for i in self.data:
                            i["Mitbah:"] = 0
                    case 6:
                        for i in self.data:
                            i["Kaf Kaf A:"] = 0
                    case 7:
                        for i in self.data:
                            i["Resting Hours:"] = 0
                    case 8:
                        for i in self.data:
                            i["Mitbah Cooldown:"] = 0
                    case _:
                        return
                for r, dictionary in enumerate(self.data):
                    for c, key in enumerate(dictionary):
                        self.setItem(r, c, QtWidgets.QTableWidgetItem(str(dictionary[key])))
        else:
            return

    def processDict(self, data):
        for r, dictionary in enumerate(data):
            for c, key in enumerate(dictionary):
                self.setItem(r, c, QtWidgets.QTableWidgetItem(str(dictionary[key])))


class ShavtzakTable(QTableWidget):
    def __init__(self):
        self.keys = ["ש.ג", "תפוז", "חמל", "סיור", "ככ א", "מטבח"]
        self.hours = ["6:00-10:00", "10:00-14:00", "14:00-18:00", "18:00-22:00",
                      "22:00-2:00", "2:00-6:00"]
        QTableWidget.__init__(self)
        self.setRowCount(6)
        self.setColumnCount(len(self.keys))
        self.setHorizontalHeaderLabels(self.keys)
        self.setVerticalHeaderLabels(self.hours)
        #self.setMaximumSize(677, 205)
        with open("shavtzak.json", "r") as f:
            self.json_data = json.load(f)
        self.set_items(self.json_data[0], self.json_data[1], self.json_data[2])

    def apply_shavtzak(self):
        try:
            with open("shavtzak.json", "r") as f:
                data = json.load(f)
                amount_of_siurim = data[2]
            soldiers = [[],[],[],[],[],[]]
            for i in range(self.columnCount()):
                for j in range(self.rowCount()):
                    try:
                        soldiers[i].append(self.item(j, i).text())
                    except Exception:
                        pass
            mitbah = [soldiers[5][0]]
            kka = [soldiers[4][0]]
            siur = [i for num, i in enumerate(soldiers[3]) if num % 2 == 0] # this worked 1st try
            for i in siur:
                if i == "": siur.remove(i)
            hamal = [i for num, i in enumerate(soldiers[2]) if num % 2 == 0]
            tapuz = soldiers[1]
            sg = soldiers[0]
            template = []
            mitbah = mitbah[0].split(", ")
            kka = kka[0].split(", ")
            tempsiur = []
            for i in range(len(siur)):
                tempsiur += siur[i].split(", ")
            siur = tempsiur
            for i in mitbah:
                template.append([i, "Mitbah"])
            for i in kka:
                template.append([i, "Kaf Kaf A"])
            for i in siur:
                template.append([i, "Siur"])
            for i in hamal:
                template.append([i, "Hamal"])
            for i in tapuz:
                template.append([i, "Tapuz"])
            for i in sg:
                template.append([i, "SG"])
            final_template = []
            final_template.append(template[0])
            final_template.append(template[1])
            template.remove(template[0])
            template.remove(template[0])
            list_kka = []
            list_siur = []
            list_hamal = []
            list_sg = []
            list_tapuz = []
            for i in template:
                if i[1] == "Kaf Kaf A":
                    list_kka.append(i)
                elif i[1] == "Siur":
                    list_siur.append(i)
                elif i[1] == "Hamal":
                    for j in range(2):
                        list_hamal.append(i)
                elif i[1] == "SG":
                    list_sg.append(i)
                elif i[1] == "Tapuz":
                    list_tapuz.append(i)

            for i in list_siur:
                template.remove(i)
                if i[0] == "":
                    list_siur.remove(i)
            for i in list_kka:
                final_template.append(i)
                template.remove(i)
            match amount_of_siurim:
                case 0:
                    for i in range(6):
                        if i % 2 == 0:
                            final_template.append(list_hamal[i])
                        final_template.append(list_tapuz[i])
                        final_template.append(list_sg[i])
                case 1:
                    for i in range(6):
                        if i % 2 == 0:
                            final_template.append(list_hamal[i])
                        if i == 0:
                            for s in list_siur:
                                final_template.append(s)
                        final_template.append(list_tapuz[i])
                        final_template.append(list_sg[i])
                case 2:
                    for i in range(6):
                        if i % 2 == 0:
                            final_template.append(list_hamal[i])
                        if i == 0 or i == 2:
                            if len(list_siur) == 2:
                                if i == 0:
                                    final_template.append(list_siur[0])
                                elif i == 2:
                                    final_template.append(list_siur[1])
                            elif len(list_siur) == 4:
                                if i == 0:
                                    final_template.append(list_siur[0])
                                    final_template.append(list_siur[1])
                                elif i == 2:
                                    final_template.append(list_siur[2])
                                    final_template.append(list_siur[3])
                        final_template.append(list_tapuz[i])
                        final_template.append(list_sg[i])
                case 3:
                    for i in range(6):
                        if i % 2 == 0:
                            final_template.append(list_hamal[i])
                            if len(list_siur) == 3:
                                if i > 0:
                                    final_template.append(list_siur[int(i/2)])
                                elif i == 0:
                                    final_template.append(list_siur[0])
                            elif len(list_siur) == 6:
                                final_template.append(list_siur[i])
                                final_template.append(list_siur[i+1])
                        final_template.append(list_tapuz[i])
                        final_template.append(list_sg[i])

            with open("shavtzak.json", "r+") as f:
                data = json.load(f)
                data[0] = final_template
                f.seek(0)
                json.dump(data, f, indent=6)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("שבצק נשמר!")
            msg.exec_()
        except Exception as exc:
            print(exc)

    def set_items(self, soldiers, amount_of_soldiers, amount_of_siurim):
        self.setColumnCount(len(self.keys))
        self.setHorizontalHeaderLabels(self.keys)
        self.mitbah = []
        self.kka = []
        self.siur = []
        self.hamal = []
        self.tapuz = []
        self.sg = []
        self.custom = []
        if self.mitbah or self.siur or self.hamal or self.sg or self.tapuz or self.kka:
            exception = QMessageBox()
            exception.setIcon(QMessageBox.Critical)
            exception.setText(
                "התוכנה לא הצליחה להכין שבצק. \n נסו שוב ואם הבעיה ממשיכה צריך להוסיף חיילים. \n Exception: IndexError }")
            exception.exec_()
            raise Exception
        try:
            for i in soldiers:
                match i[1]:
                    case "Mitbah":
                        self.mitbah.append(i[0])
                    case "Kaf Kaf A":
                        self.kka.append(i[0])
                    case "Siur":
                        self.siur.append(i[0])
                    case "Hamal":
                        self.hamal.append(i[0])
                        self.hamal.append(i[0])
                    case "Tapuz":
                        self.tapuz.append(i[0])
                    case "SG":
                        self.sg.append(i[0])
                    case "Custom":
                        self.custom.append(i[0])
                    case _:
                        print(i, "case_")
            for i, name in enumerate(self.sg):
                self.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            for i, name in enumerate(self.tapuz):
                self.setItem(i, 1, QtWidgets.QTableWidgetItem(name))
            for i, name in enumerate(self.hamal):
                self.setItem(i, 2, QtWidgets.QTableWidgetItem(name))
            match amount_of_soldiers:
                case 1:
                    match amount_of_siurim:
                        case 0:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(""))
                        case 1:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(""))
                        case 2:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(self.siur[1]))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(self.siur[1]))
                        case 3:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(self.siur[1]))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(self.siur[1]))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(self.siur[2]))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(self.siur[2]))
                case 2:
                    match amount_of_siurim:
                        case 0:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(""))
                        case 1:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0] + ", " + self.siur[1]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0] + ", " + self.siur[1]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(""))
                        case 2:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0] + ", " + self.siur[1]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0] + ", " + self.siur[1]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(""))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(self.siur[2]+ ", "+ self.siur[3]))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(self.siur[2]+ ", "+ self.siur[3]))
                        case 3:
                            self.setItem(0, 3, QtWidgets.QTableWidgetItem(self.siur[0]+ ", "+ self.siur[1]))
                            self.setItem(1, 3, QtWidgets.QTableWidgetItem(self.siur[0]+ ", "+ self.siur[1]))
                            self.setItem(2, 3, QtWidgets.QTableWidgetItem(self.siur[2]+ ", "+ self.siur[3]))
                            self.setItem(3, 3, QtWidgets.QTableWidgetItem(self.siur[2]+ ", "+ self.siur[3]))
                            self.setItem(4, 3, QtWidgets.QTableWidgetItem(self.siur[4]+ ", "+ self.siur[5]))
                            self.setItem(5, 3, QtWidgets.QTableWidgetItem(self.siur[4]+ ", "+ self.siur[5]))
            self.kka = ", ".join(self.kka)
            for i in range(5):
                self.setItem(i, 4, QtWidgets.QTableWidgetItem(self.kka))
            self.mitbah = ", ".join(self.mitbah)
            for i in range(4):
                self.setItem(i, 5, QtWidgets.QTableWidgetItem(self.mitbah))
            if len(self.keys) > 6:
                self.custom = ", ".join(self.custom)
                for i in range(6):
                    self.setItem(i, 6, QtWidgets.QTableWidgetItem(self.custom))
        except Exception as exc:
            print(exc, 1)
