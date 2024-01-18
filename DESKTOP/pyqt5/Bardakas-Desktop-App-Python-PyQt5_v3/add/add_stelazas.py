import psycopg2
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


class AddStelazas(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(400 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Add4')
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
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.setPlaceholderText("Text")
        self.pavadiniamsEntry.addItems(["ROLIKAI", "VARIKLIAI", "DETALES IR KT.", "FESTO",
                                        "ATSARGOS", "EL. KOMPONENTAI"])
        self.pavadiniamsEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavadiniamsEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText("Text")
        self.sandelisCombo.addItems(["BUTRIMONIU", "DRAUGYSTE", "MITUVOS"])
        self.sandelisCombo.setFont(QFont("Times", self.TEXT_PT))
        self.sandelisCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText("Text")
        self.vietaCombo.addItems(
            ["KONTORA", "ZONA-1", "ZONA-2", "ZONA-3", "ZONA-4", "ZONA-5", "ZONA-6", "ZONA-7", "ZONA-8", "ZONA-9",
             "ZONA-10",
             "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
             "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4", "STELAZAS-5", "STELAZAS-6", "STELAZAS-7",
             "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11", "STELAZAS-12", "STELAZAS-13", "STELAZAS-14",
             "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addStelazas1)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddStelazas1)
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_PT))

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("SANDĖLIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.mainLayout.addWidget(self.widgetFrame)

        self.setLayout(self.mainLayout)

    def addStelazas1(self):
        pavadinimas1 = self.pavadiniamsEntry.currentText().upper()
        projektas1 = self.projektasEntry.text().upper()
        sandelis1 = self.sandelisCombo.currentText().upper()
        vieta1 = self.vietaCombo.currentText().upper()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        update_date1 = self.update_date.text()


        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute('''INSERT INTO stelazas (pavadinimas, projektas, sandelis, vieta, 
                    komentarai, update_date) VALUES
                    (%s, %s, %s, %s, %s, %s)''', (pavadinimas1, projektas1, sandelis1, vieta1, komentarai1, update_date1))

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

    def closeAddStelazas1(self):
        self.close()

def main():
    import sys

    App = QApplication(sys.argv)

    window = AddStelazas()

    sys.exit(App.exec_())


if __name__ == '__main__':
    main()