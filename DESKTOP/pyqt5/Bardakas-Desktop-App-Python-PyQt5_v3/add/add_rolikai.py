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


class AddRolikai(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(650 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Add5')
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
        self.pavadinimasCombo = QComboBox()
        self.pavadinimasCombo.setEditable(True)
        self.pavadinimasCombo.setPlaceholderText('Text')
        self.pavadinimasCombo.addItems(
            ["RM", "PAPRASTAS", "POSUKIS-RM", "POSUKIS"])
        self.pavadinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.ilgisEntry = QLineEdit()
        self.ilgisEntry.setPlaceholderText('Number')
        self.ilgisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.ilgisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText('Number')
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tvirtinimasCombo = QComboBox()
        self.tvirtinimasCombo.setEditable(True)
        self.tvirtinimasCombo.setPlaceholderText('Text')
        self.tvirtinimasCombo.addItems(
            ["SRIEGIS", "ASIS", "SESIAKAMPE ASIS"])
        self.tvirtinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tvirtinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tipasCombo = QComboBox()
        self.tipasCombo.setEditable(True)
        self.tipasCombo.setPlaceholderText('Text')
        self.tipasCombo.addItems(
            ["-", "2xD5", "1xD5", "PJ", "AT10", "TIMING BELT P=8 T18", "GUMUOTAS", "PVC", "2xD5 GUMUOTAS", "2xD5 PVC",
             "AT10 GUMUOTAS", "AT10 PVC", "2xZVAIGZDE", "1xD5 GALUOSE", "2xD5 TOLIAU", "D60 PRILAIKANTIS"])
        self.tipasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tipasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.aprasymasEntry = QLineEdit()
        self.aprasymasEntry.setPlaceholderText('Text')
        self.aprasymasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.aprasymasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasCombo = QComboBox()
        self.projektasCombo.setEditable(True)
        self.projektasCombo.setPlaceholderText('Text')
        self.projektasCombo.addItems(
            ["ATSARGOS"])
        self.projektasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.projektasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText('Text')
        self.sandelisCombo.addItems(
            ["BUTRIMONIU", "DRAUGYSTE", "MITUVOS"])
        self.sandelisCombo.setFont(QFont("Times", self.TEXT_PT))
        self.sandelisCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText('Text')
        self.vietaCombo.addItems(
            ["ZONA-1", "ZONA-2", "ZONA-3", "ZONA-4", "ZONA-5",
             "ZONA-6", "ZONA-7", "ZONA-8", "ZONA-9", "ZONA-10",
             "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
             "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4",
             "STELAZAS-5", "STELAZAS-6", "STELAZAS-7",
             "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11",
             "STELAZAS-12", "STELAZAS-13", "STELAZAS-14",
             "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addRolikai)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelAddRolikai)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

    def layouts(self):
        """add widgets to layouts"""
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasCombo)
        self.widgetLayout.addRow(QLabel("ILGIS: "), self.ilgisEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasCombo)
        self.widgetLayout.addRow(QLabel("TIPAS: "), self.tipasCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("APRAŠYMAS: "), self.aprasymasEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("SANDĖLIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout.addRow(self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        """add widgets to layouts"""
        self.mainLayout.addWidget(self.widgetFrame)
        self.setLayout(self.mainLayout)

    def addRolikai(self):
        pavadinimas1 = self.pavadinimasCombo.currentText().upper()
        ilgis1 = self.ilgisEntry.text()
        kiekis1 = self.kiekisEntry.text()
        tvirtinimas1 = self.tvirtinimasCombo.currentText().upper()
        tipas1 = self.tipasCombo.currentText()
        aprasymas1 = self.aprasymasEntry.text()
        projektas1 = self.projektasCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        vieta1 = self.vietaCombo.currentText().upper()
        sandelis1 = self.sandelisCombo.currentText().upper()
        update_date1 = self.update_date.text()

        try:
            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()

            cur.execute('''INSERT INTO rolikai (pavadinimas, ilgis, kiekis, vieta, tvirtinimas, tipas, 
            aprasymas, projektas, komentarai, sandelis, update_date)  VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', (pavadinimas1, ilgis1, kiekis1, vieta1,
                                                          tvirtinimas1, tipas1, aprasymas1, projektas1,
                                                          komentarai1, sandelis1, update_date1))

            conn.commit()

            conn.close()

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

    def cancelAddRolikai(self):
        self.close()

# def main():
#     import sys
#
#     App = QApplication(sys.argv)
#
#     window = AddRolikai()
#
#     sys.exit(App.exec_())
#
#
# if __name__ == '__main__':
#     main()