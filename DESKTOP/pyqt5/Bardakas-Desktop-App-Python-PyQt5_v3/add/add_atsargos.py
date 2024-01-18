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


class AddAtsargos(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(550 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Add2')
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

    def widgets(self):
        self.pavadinimasEntry = QComboBox()
        self.pavadinimasEntry.setEditable(True)
        self.pavadinimasEntry.setPlaceholderText("Text")
        self.pavadinimasEntry.addItems(["GUOLIS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ", "BELTAS",
                                        "GUOLIS+GUOLIAVIETE", "GUOLIAVIETE", "IVORE", "MOVA RCK", "GRANDINE",
                                        "VARZTAS", "ZVAIGZDE", "PNEUMO", "KAMSTIS"])
        self.pavadinimasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.konfigEntry = QLineEdit()
        self.konfigEntry.setPlaceholderText("Text")
        self.konfigEntry.setFont(QFont("Times", self.TEXT_PT))
        self.konfigEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText("Text")
        self.sandelisCombo.addItems(["BUTRIMONIU", "DRAUGYSTES", "MITUVOS"])
        self.sandelisCombo.setFont(QFont("Times", self.TEXT_PT))
        self.sandelisCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText("Text")
        self.vietaCombo.addItems(["ZONA-1", "ZONA-2", "ZONA-3", "ZONA-4", "ZONA-5",
                                  "ZONA-6", "ZONA-7", "ZONA-8", "ZONA-9", "ZONA-10",
                                  "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
                                  "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4",
                                  "STELAZAS-5", "STELAZAS-6", "STELAZAS-7",
                                  "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11",
                                  "STELAZAS-12", "STELAZAS-13", "STELAZAS-14",
                                  "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.kiekisEntry.setAlignment(Qt.AlignCenter)

        self.matvntCombo = QComboBox()
        self.matvntCombo.setEditable(True)
        self.matvntCombo.setPlaceholderText("Text")
        self.matvntCombo.addItems(["m.", "vnt."])
        self.matvntCombo.setFont(QFont("Times", self.TEXT_PT))
        self.matvntCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.matvntCombo.lineEdit().setAlignment(Qt.AlignCenter)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.photoName = QLineEdit()
        self.photoName.setReadOnly(True)
        self.photoName.setStyleSheet("QLineEdit{background: lightgrey;}")
        self.photoName.setPlaceholderText('')
        self.photoName.setFont(QFont("Times", self.TEXT_PT))
        self.photoName.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.nuotraukaBtn = QPushButton("ADD PICTURE")
        self.nuotraukaBtn.clicked.connect(self.getFileInfo)
        self.nuotraukaBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.nuotraukaBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addAtsargos1)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddAtsagors1)
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        self.kiekisBox = QHBoxLayout()
        self.kiekisBox.addWidget(self.kiekisEntry, 50)
        self.kiekisBox.addWidget(self.matvntCombo, 50)

        # self.nuotraukaBox = QHBoxLayout()
        # self.nuotraukaBox.addWidget(self.photoName)
        # self.nuotraukaBox.addWidget(self.nuotraukaBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasEntry)
        self.widgetLayout.addRow(QLabel("KONFIGURACIJA: "), self.konfigEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("SANDĖLIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisBox)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("NUOTRAUKA: "), self.photoName)
        self.widgetLayout.addRow(QLabel(""), self.nuotraukaBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.mainLayout.addWidget(self.widgetFrame)

        self.setLayout(self.mainLayout)

    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        except:
            pass

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.jpg;*.png;*.pdf)")
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

        self.photoName.setText(f"{justfilename}{filetype}")

    def addAtsargos1(self):
        pavadinimas1 = self.pavadinimasEntry.currentText().upper()
        konfig1 = self.konfigEntry.text()
        sandelis1 = self.sandelisCombo.currentText().upper()
        vieta1 = self.vietaCombo.currentText().upper()
        kiekis1 = self.kiekisEntry.text()
        vienetas1 = self.matvntCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        nuotrauka1 = self.photoName.text()
        update_date1 = self.update_date.text()

        filename = self.ListFileName.text()
        byteaPhoto = self.convertToBinaryData(self.ListDir.text())
        listfiletype = self.ListFileType.text()
        listentry = self.ListDir.text()

        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute('''INSERT INTO atsargos (pavadinimas, vieta, kiekis, mat_pav, komentaras, nuotrauka, update_date,
            filename, photo, filetype, filedir, konfig, sandelis) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                      (pavadinimas1, vieta1, kiekis1, vienetas1, komentarai1, nuotrauka1,
                       update_date1, filename, byteaPhoto, listfiletype, listentry,
                       konfig1, sandelis1))

            con.commit()

            con.close()

            self.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def closeAddAtsagors1(self):
        self.close()


# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = AddAtsargos()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()
