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


class AddSanaudos(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(420 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Add3')
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
        self.pavadiniamsEntry.addItems(["HABASIT", "PROFILIAI", "UZDENGIMAI", "GALINUKAS", "PRILAIKANTIS",
                                        "SKRIEMULYS", "SKRIEMULIO ASIS", "ROLIKAI", "VARIKLIAI", 'PLASTIKINES IVORES'])
        self.pavadiniamsEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavadiniamsEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.matvntEntry = QComboBox()
        self.matvntEntry.setEditable(True)
        self.matvntEntry.setPlaceholderText("Text")
        self.matvntEntry.addItems(["m.", "vnt."])
        self.matvntEntry.lineEdit().setAlignment(Qt.AlignCenter)
        self.matvntEntry.setFont(QFont("Times", self.TEXT_PT))
        self.matvntEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.metaiEntry = QLineEdit()
        self.metaiEntry.setText(str(year))
        self.metaiEntry.setFont(QFont("Times", self.TEXT_PT))
        self.metaiEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addSanaudos1)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddSanaudos1)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.kiekisBox = QHBoxLayout()
        self.kiekisBox.addWidget(self.kiekisEntry, 50)
        self.kiekisBox.addWidget(self.matvntEntry, 50)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisBox)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("METAI: "), self.metaiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.mainLayout.addWidget(self.widgetFrame)

        self.setLayout(self.mainLayout)

    def addSanaudos1(self):
        pavadinimas1 = self.pavadiniamsEntry.currentText().upper()
        projektas1 = self.projektasEntry.text().upper()
        kiekis1 = self.kiekisEntry.text()
        vienetai1 = self.matvntEntry.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        metai1 = self.metaiEntry.text()
        update_date1 = self.update_date.text()


        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute('''INSERT INTO sanaudos (pavadinimas, projektas, kiekis, mat_vnt, komentaras, 
                    metai, update_date) VALUES
                    (%s, %s, %s, %s, %s, %s, %s)''', (pavadinimas1, projektas1, kiekis1, vienetai1, komentarai1,
                                                      metai1, update_date1))

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

    def closeAddSanaudos1(self):
        self.close()


# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = AddSanaudos()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()