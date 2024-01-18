import psycopg2
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Bardakas_style_gray
import config
from add import add_atkrovimai
from scaling import pt_points

params = config.sql_db


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        """Delegate style to items"""
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class MainMenu(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle('Suruošti užsakymai')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400/self.scale_factor), int(300/self.scale_factor),
                         int(1000*self.scale_factor), int(600*self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.SheetStyle(self)

        self.settings = QSettings('Bardakas', 'atkrovimai')
        # print(self.settings.fileName())
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

        self.UI()
        self.show()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayAtkrovimai()

    def widgets(self):
        # ATKROVIMAI TABLE
        self.atkrovimaiTable = QTableWidget()
        self.atkrovimaiTable.setColumnCount(5)
        self.atkrovimaiTable.setColumnHidden(0, True)
        self.atkrovimaiTable.setSortingEnabled(True)

        headers_atkr = ["ID", "PROJEKTAS", "PAVADINIMAS", "SĄRAŠAS",
                        "KOMENTARAI"]

        for column_number in range(0, len(headers_atkr)):
            while column_number < len(headers_atkr):
                header_name = headers_atkr[column_number]
                self.atkrovimaiTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.atkrovimaiTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atkrovimaiTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atkrovimaiTable.horizontalHeader().setHighlightSections(False)
        self.atkrovimaiTable.horizontalHeader().setDisabled(True)
        self.atkrovimaiTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.atkrovimaiTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.atkrovimaiTable.clicked.connect(self.atkrovimai_select)
        self.atkrovimaiTable.doubleClicked.connect(self.updateAtkrovimai)

        delegate = AlignDelegate()

        for number in [1, 2, 3]:
            self.atkrovimaiTable.setItemDelegateForColumn(number, delegate)

    def layouts(self):
        """App layouts"""
        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.atkrovimaiTable)
        self.setLayout(self.mainLayout)

    def atkrovimai_select(self):
        global atkrovimaiId

        self.listAtkrovimai = []
        self.num = 0
        self.listAtkrovimai.append(self.atkrovimaiTable.item(self.atkrovimaiTable.currentRow(), self.num).text())

        atkrovimaiId = self.listAtkrovimai[0]

    def contextMenuEvent(self, event):
        """Right mouse button select"""
        if self.atkrovimaiTable.underMouse():
            global atkrovimaiId

            # Left mouse button table
            contextMenu = QMenu(self)

            openSarasas = contextMenu.addAction("Sąrašas")
            openSarasas.triggered.connect(self.openFile)
            openSarasas.setShortcut("Alt+L")
            openSarasas.setIcon(QIcon("icons/files.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_atkrovimai)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh = contextMenu.addAction("Refresh")
            Refresh.triggered.connect(self.displayAtkrovimai)
            Refresh.setShortcut("F5")
            Refresh.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteAtkrovimai = contextMenu.addAction("Delete")
            deleteAtkrovimai.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def add_atkrovimai(self):
        try:
            self.new_atkrovimai = add_atkrovimai.AddAtkrovimai()
            # Refresh table after executing QDialog .exec_
            self.new_atkrovimai.exec_()
            self.displayAtkrovimai()
        except Exception as error:
            print(f"{error}")

    def updateAtkrovimai(self):
        """select row data and fill entry with current data"""
        global atkrovimaiId

        try:
            self.display = dipslayAtkrovimaiUpdate()
            self.display.show()
            self.display.exec_()
            self.displayAtkrovimai()
        except Exception as error:
            print(f"{error}")

    def displayAtkrovimai(self):
        """Shows SQL table in QTableWidget"""
        try:
            # Cleans table
            self.atkrovimaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

            for i in reversed(range(self.atkrovimaiTable.rowCount())):
                self.atkrovimaiTable.removeRow(i)

            # Connect to SQL table
            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()

            cur.execute(
                """SELECT id, projektas, pavadinimas, sarasas, komentarai,
                filename, filetype, filedir 
                FROM atkrovimai 
                ORDER BY projektas ASC""")
            query = cur.fetchall()

            # Sort table values and adds to table, change color of some values
            for row_date in query:
                row_number = self.atkrovimaiTable.rowCount()
                self.atkrovimaiTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))
                    self.atkrovimaiTable.setItem(row_number, column_number, setitem)

            # Edit column cell disable
            self.atkrovimaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def deleteTables(self):
        """deletes item and refresh list"""
        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        global atkrovimaiId

        try:
            if (x == QMessageBox.Yes):
                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()
                cur.execute("DELETE FROM atkrovimai WHERE id = %s", (atkrovimaiId,))
                conn.commit()
                conn.close()

                self.displayAtkrovimai()

            elif (x == QMessageBox.No):
                pass

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to delete.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def atkrovimaiWriteToFile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def openFile(self):
        """open selected file"""
        global atkrovimaiId
        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute("""SELECT * FROM atkrovimai WHERE ID = %s""", (atkrovimaiId,))
            atkrovimai = c.fetchone()

            self.filename = atkrovimai[5]
            self.photo = atkrovimai[6]
            self.filetype = atkrovimai[7]

            str_none = ""

            if self.filetype == None or self.filetype == str_none \
                    or self.photo == None or self.photo == str_none \
                    or self.filename == None or self.filename == str_none:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText("NO FILE...")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

            else:
                path = "bardakas_files/atkrovimai_list"
                # Check whether the specified path exists or not
                if not os.path.isdir(path):
                    os.makedirs(path)

                photoPath = "bardakas_files/atkrovimai_list/" + self.filename + self.filetype

                if not os.path.isfile(photoPath):
                    self.atkrovimaiWriteToFile(self.photo, photoPath)

                os.startfile(os.path.abspath(os.getcwd()) + "/" + photoPath, 'open')

                con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to open.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

class dipslayAtkrovimaiUpdate(QDialog, pt_points):
    """double mouse click table"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400/self.scale_factor), int(300/self.scale_factor),
                         int(400*self.scale_factor), int(400*self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update1')
        # pozition and size
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except Exception as error:
            print(f"{error}")

        self.UI()
        self.show()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.atkrovimaiDetails()
        self.widgets()
        self.layouts()

    def atkrovimaiDetails(self):
        global atkrovimaiId

        conn = psycopg2.connect(
            **params
        )

        cur = conn.cursor()

        cur.execute("""SELECT * FROM atkrovimai WHERE ID=%s""", (atkrovimaiId,))
        atkrovimai = cur.fetchone()

        conn.close()


        self.atkrovimaiProjektas = atkrovimai[1]
        self.atkrovimaiPavadinimas = atkrovimai[2]
        self.atkrovimaiList = atkrovimai[3]
        self.atkrovimaiKomentarai = atkrovimai[4]
        self.filename = atkrovimai[5]
        self.photo = atkrovimai[6]
        self.filetype = atkrovimai[7]

    def widgets(self):
        self.projektasEntry = QLineEdit()
        self.projektasEntry.setText(self.atkrovimaiProjektas)
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.pavadinimasCombo = QComboBox()
        self.pavadinimasCombo.setCurrentText(self.atkrovimaiPavadinimas)
        self.pavadinimasCombo.setEditable(True)
        self.pavadinimasCombo.addItems(
            ["Palečių turinys", "Palečių sąrašas", "Sandėlio turinys"])
        self.pavadinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.ListEntry = QLineEdit()
        self.ListEntry.setText(self.atkrovimaiList)
        self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")
        self.ListEntry.setFont(QFont("Times", self.TEXT_PT))
        self.ListEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setText(self.atkrovimaiKomentarai)
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateAtkrovimai)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelUpdate)
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        self.widgetLayout.addRow(QLabel("PROJEKTAS:"), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS:"), self.pavadinimasCombo)
        self.widgetLayout.addRow(QLabel("SĄRAŠAS:"), self.ListEntry)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI:"))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.mainLayout.addWidget(self.widgetFrame)

        self.setLayout(self.mainLayout)

    def convertToBinaryDataFile(self, filename):
        # Convert digital data to binary format
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        except Exception as error:
            print(f"{error}")

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.pdf;*.txt;*.xls)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name

        justfilename = getfullfilename[:-4]
        filetype = getfullfilename[-4:]

        # print(directory)
        # print(justfilename)
        # print(filetype)

        self.ListDir.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetype))

        self.ListEntry.setText(f"{justfilename}{filetype}")

    def updateAtkrovimai(self):
        global atkrovimaiId

        projektas1 = self.projektasEntry.text().upper()
        pavadinimas1 = self.pavadinimasCombo.currentText()
        sarasas1 = self.ListEntry.text()
        komentarai1 = str(self.komentaraiEntry.toPlainText())

        filename1 = self.ListFileName.text()
        byteaPhoto1 = self.convertToBinaryDataFile(self.ListDir.text())
        listfiletype1 = self.ListFileType.text()
        listentry1 = self.ListDir.text()

        try:
            if self.ListDir.text() != "":
                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                query = "UPDATE atkrovimai SET projektas = %s, pavadinimas = %s, sarasas = %s, komentarai = %s," \
                        "filename = %s, photo = %s, filetype = %s, filedir = %s " \
                        "where id = %s"
                cur.execute(query, (projektas1, pavadinimas1, sarasas1, komentarai1,
                                    filename1, byteaPhoto1, listfiletype1, listentry1,
                                    atkrovimaiId))
                conn.commit()
                conn.close()

            else:
                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                query = "UPDATE atkrovimai SET projektas = %s, pavadinimas = %s, sarasas = %s, komentarai = %s " \
                        "where id = %s"
                cur.execute(query, (projektas1, pavadinimas1, sarasas1, komentarai1, atkrovimaiId))
                conn.commit()
                conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelUpdate(self):
        self.close()
#
# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = MainMenu()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()
