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

class AddAtkrovimai(QDialog, pt_points):
    """add new record class"""

    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400/self.scale_factor), int(300/self.scale_factor),
                         int(400*self.scale_factor), int(400*self.scale_factor))
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

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.pavadinimasCombo = QComboBox()
        self.pavadinimasCombo.setEditable(True)
        self.pavadinimasCombo.setPlaceholderText("Text")
        self.pavadinimasCombo.addItems(
            ["Palečių turinys", "Palečių sąrašas", "Sandėlio turinys"])
        self.pavadinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.ListEntry = QLineEdit()
        self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")
        self.ListEntry.setFont(QFont("Times", self.TEXT_PT))
        self.ListEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.setFixedHeight(25)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addAtkrovimai)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelAdd)
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

    def OpenFolderDialog(self):
        """get folder dir"""
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.ListEntry.setText('{}'.format(directory))

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

    def addAtkrovimai(self):
        projektas1 = self.projektasEntry.text().upper()
        pavadinimas1 = self.pavadinimasCombo.currentText()
        sarasas = self.ListEntry.text()
        komentarai1 = str(self.komentaraiEntry.toPlainText())

        filename = self.ListFileName.text()
        byteaPhoto = self.convertToBinaryDataFile(self.ListDir.text())
        listfiletype = self.ListFileType.text()
        listentry = self.ListDir.text()

        try:
            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()

            cur.execute('''INSERT INTO atkrovimai 
            (projektas, pavadinimas, sarasas, komentarai,
            filename, photo, filetype, filedir) 
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)''',
                        (projektas1, pavadinimas1, sarasas, komentarai1,
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

        self.close()

    def cancelAdd(self):
        self.close()


# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = AddAtkrovimai()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()