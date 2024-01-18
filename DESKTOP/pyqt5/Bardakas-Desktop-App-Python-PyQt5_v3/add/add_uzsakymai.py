from pathlib import Path

import psycopg2
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Bardakas_style_gray
import config

from scaling import pt_points

params = config.sql_db

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()


class AddUzsakymas(QDialog, pt_points):
    """add new record class"""

    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(650 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        # self.setWindowFlags(Qt.FramelessWindowHint)

        self.UI()

        self.show()

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Add1')
        # print(self.settings.fileName())
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        conn = psycopg2.connect(
            **params
        )
        cur = conn.cursor()
        cur.execute("""SELECT * FROM combo_uzsakymai ORDER BY id ASC""")
        query = cur.fetchall()
        conn.close()

        list_imone_start = [item[1] for item in query]
        list_imone = []
        for a in list_imone_start:
            list_imone.append(a)
            if a == None or a == "":
                list_imone.remove(a)

        list_konstruktorius_start = [item[2] for item in query]
        list_konstruktorius = []
        for b in list_konstruktorius_start:
            list_konstruktorius.append(b)
            if b == None or b == "":
                list_konstruktorius.remove(b)

        list_projektas_start = [item[3] for item in query]
        list_projektas = []
        for c in list_projektas_start:
            list_projektas.append(c)
            if c == None or c == "":
                list_projektas.remove(c)

        list_pavadinimas_start = [item[4] for item in query]
        list_pavadinimas = []
        for d in list_pavadinimas_start:
            list_pavadinimas.append(d)
            if d == None or d == "":
                list_pavadinimas.remove(d)

        self.imoneCombo = QComboBox()
        self.imoneCombo.setEditable(True)
        self.imoneCombo.setPlaceholderText('Text')
        self.imoneCombo.addItems(list_imone)
        self.imoneCombo.setFont(QFont("Times", self.TEXT_PT))
        self.imoneCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.braizeCombo = QComboBox()
        self.braizeCombo.setEditable(True)
        self.braizeCombo.setPlaceholderText('Text')
        self.braizeCombo.addItems(list_konstruktorius)
        self.braizeCombo.setFont(QFont("Times", self.TEXT_PT))
        self.braizeCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasCombo = QComboBox()
        self.projektasCombo.setEditable(True)
        self.projektasCombo.setPlaceholderText('Text')
        self.projektasCombo.addItems(list_projektas)
        self.projektasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.projektasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.uzskpavCombo = QComboBox()
        self.uzskpavCombo.setEditable(True)
        self.uzskpavCombo.setPlaceholderText('Text')
        self.uzskpavCombo.addItems(list_pavadinimas)
        self.uzskpavCombo.setFont(QFont("Times", self.TEXT_PT))
        self.uzskpavCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.terminasEntry = QComboBox()
        self.terminasEntry.setEditable(True)
        self.terminasEntry.addItems(
            ["-", "+"])
        self.terminasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.terminasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.statusasEntry = QComboBox()
        self.statusasEntry.setEditable(True)
        self.statusasEntry.setPlaceholderText('Text')
        self.statusasEntry.addItems(
            ["GAMINA", "PAGAMINTA", "BROKUOTA"])
        self.statusasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.statusasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.locEntry = QLineEdit()
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                    "color:black;}")
        self.locEntry.setFont(QFont("Times", self.TEXT_PT))
        self.locEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.breziniaiBtn = QPushButton("ADD LINK TO FOLDER")
        self.breziniaiBtn.clicked.connect(self.OpenFolderDialog)
        self.breziniaiBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.breziniaiBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.ListEntry = QLineEdit()
        self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")
        self.ListEntry.setFont(QFont("Times", self.TEXT_PT))
        self.ListEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.dateBtn = QPushButton("ADD DATE")
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFixedWidth(self.BUTTON_WIDTH)
        self.dateBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.dateBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addUzsakymas)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        # self.okBtn.setMaximumWidth(200)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelUzsakymaiAdd)
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        # self.cancelBtn.setMaximumWidth(200)

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.topmainLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QVBoxLayout()
        self.mainLayout2 = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        # self.qhbox1 = QHBoxLayout()
        # self.qhbox1.addWidget(self.locEntry)
        # self.qhbox1.addWidget(self.breziniaiBtn)

        # self.qhbox2 = QHBoxLayout()
        # self.qhbox2.addWidget(self.ListEntry)
        # self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.terminasEntry)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("ĮMONĖ:"), self.imoneCombo)
        self.widgetLayout.addRow(QLabel("BRAIŽĖ:"), self.braizeCombo)
        self.widgetLayout.addRow(QLabel("PROJEKTAS:"), self.projektasCombo)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS:"), self.uzskpavCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("TERMINAS:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("STATUSAS:"), self.statusasEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("BRĖŽINIAI:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.breziniaiBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("SĄRAŠAS:"), self.ListEntry)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI:"))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        # """add widgets to layouts"""
        self.mainLayout1.addWidget(self.widgetFrame)

        self.mainLayout.addLayout(self.mainLayout1)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        """get folder dir"""
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def convertToBinaryDataFile(self, filename):
        # Convert digital data to binary format
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        except:
            pass

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.pdf;*.txt;*.xls)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name

        justfilename = getfullfilename[:-4]
        filetype = getfullfilename[-4:]

        print(directory)
        print(justfilename)
        print(filetype)

        self.ListDir.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetype))

        self.ListEntry.setText(f"{justfilename}{filetype}")

    def terminasCalendar(self):
        try:
            self.cal = QCalendarWidget(self)
            self.cal.setGridVisible(True)
            self.calBtn = QPushButton("CANCEL")
            self.calBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
            self.calBtn.setFixedHeight(self.BUTTON_HEIGHT)
            self.calBtn.clicked.connect(self.cal_cancel)

            self.calendarWindow = QDialog()
            self.hbox = QVBoxLayout()
            self.hbox.addWidget(self.cal)
            self.hbox.addWidget(self.calBtn)
            self.calendarWindow.setLayout(self.hbox)
            self.calendarWindow.setGeometry(int(780/self.scale_factor), int(280/self.scale_factor),
                                            int(350*self.scale_factor), int(350*self.scale_factor))
            self.calendarWindow.setWindowTitle('ADD DATE')
            self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
            Bardakas_style_gray.QCalendarstyle(self)
            self.calendarWindow.show()

            # @QtCore.pyqtSlot(QtCore.QDate)
            def get_date(qDate):
                if qDate.day() <= 9 and qDate.month() <= 9:
                    date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                    self.terminasEntry.setCurrentText(date)
                elif qDate.day() <= 9 and qDate.month() >= 10:
                    date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                    self.terminasEntry.setCurrentText(date)
                elif qDate.day() >= 9 and qDate.month() <= 9:
                    date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                    self.terminasEntry.setCurrentText(date)
                else:
                    date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                    self.terminasEntry.setCurrentText(date)
                self.calendarWindow.close()

            self.cal.clicked.connect(get_date)
        except:
            pass
        
    def cal_cancel(self):
        try:
            self.calendarWindow.close()
        except:
            pass

    def addUzsakymas(self):
        imone = self.imoneCombo.currentText().upper()
        braize = self.braizeCombo.currentText().upper()
        projektas = self.projektasCombo.currentText().upper()
        uzsakymo_pavadinimas = self.uzskpavCombo.currentText()
        terminas = self.terminasEntry.currentText()
        statusas = self.statusasEntry.currentText().upper()
        komentarai = str(self.komentaraiEntry.toPlainText())
        breziniai = self.locEntry.text()
        sarasas = self.ListEntry.text()
        update_date = self.update_date.text()

        filename = self.ListFileName.text()
        byteaPhoto = self.convertToBinaryDataFile(self.ListDir.text())
        listfiletype = self.ListFileType.text()
        listentry = self.ListDir.text()

        terminas_date = ""

        if terminas != terminas_date:
            try:
                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute('''INSERT INTO uzsakymai (imone, konstruktorius, projektas, pav_uzsakymai,
                terminas, statusas, komentarai, breziniai, sarasas, update_date,
                filename, photo, filetype, filedir) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (imone, braize, projektas, uzsakymo_pavadinimas,
                             terminas, statusas, komentarai, breziniai, sarasas, update_date,
                             filename, byteaPhoto, listfiletype, listentry))

                conn.commit()

                conn.close()


            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText(f"Error while fetching data from PostgreSQL: {error}")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("TERMINAS can't be empty...")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelUzsakymaiAdd(self):
        self.close()
        self.cal_cancel()


# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = AddUzsakymas()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()
