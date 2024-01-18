import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import Bardakas_style_gray
import config
from scaling import pt_points

params = config.sql_db


class AddCombo(QDialog, pt_points):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle('ADD ComboBox ITEMS')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(270 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        self.settings = QSettings('Bardakas', 'Combo')
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

        # uzsakymai ########################
        self.imoneE = QLineEdit()
        self.imoneE.setFont(QFont("Times", self.TEXT_PT))
        self.imoneE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.braizeE = QLineEdit()
        self.braizeE.setFont(QFont("Times", self.TEXT_PT))
        self.braizeE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasE = QLineEdit()
        self.projektasE.setFont(QFont("Times", self.TEXT_PT))
        self.projektasE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.pavadinimasE = QLineEdit()
        self.pavadinimasE.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.okBtn = QPushButton("UPDATE")
        self.okBtn.clicked.connect(self.addCombo)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CLOSE")
        self.cancelBtn.clicked.connect(self.closeAddCombo)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

        # # atsargos #######################
        # self.pavadinimasA = QLineEdit()
        # self.pavadinimasA.setFont(QFont("Times", self.TEXT_PT))
        # self.pavadinimasA.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.sandelisA = QLineEdit()
        # self.sandelisA.setFont(QFont("Times", self.TEXT_PT))
        # self.sandelisA.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.vietaA = QLineEdit()
        # self.vietaA.setFont(QFont("Times", self.TEXT_PT))
        # self.vietaA.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # # rolikai ##################################
        # self.pavadinimasR = QLineEdit()
        # self.pavadinimasR.setFont(QFont("Times", self.TEXT_PT))
        # self.pavadinimasR.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.tvirtinimasR = QLineEdit()
        # self.tvirtinimasR.setFont(QFont("Times", self.TEXT_PT))
        # self.tvirtinimasR.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.tipasR = QLineEdit()
        # self.tipasR.setFont(QFont("Times", self.TEXT_PT))
        # self.tipasR.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.sandelisR = QLineEdit()
        # self.sandelisR.setFont(QFont("Times", self.TEXT_PT))
        # self.sandelisR.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.vietaR = QLineEdit()
        # self.vietaR.setFont(QFont("Times", self.TEXT_PT))
        # self.vietaR.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # # pavaros ##################################
        # self.gamintojasP = QLineEdit()
        # self.gamintojasP.setFont(QFont("Times", self.TEXT_PT))
        # self.gamintojasP.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.tipasP = QLineEdit()
        # self.tipasP.setFont(QFont("Times", self.TEXT_PT))
        # self.tipasP.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.tvirtinimasP = QLineEdit()
        # self.tvirtinimasP.setFont(QFont("Times", self.TEXT_PT))
        # self.tvirtinimasP.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.sandelisP = QLineEdit()
        # self.sandelisP.setFont(QFont("Times", self.TEXT_PT))
        # self.sandelisP.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.vietaP = QLineEdit()
        # self.vietaP.setFont(QFont("Times", self.TEXT_PT))
        # self.vietaP.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # # stelazas ##################################
        # self.pavadinimasS = QLineEdit()
        # self.pavadinimasS.setFont(QFont("Times", self.TEXT_PT))
        # self.pavadinimasS.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.projektasS = QLineEdit()
        # self.projektasS.setFont(QFont("Times", self.TEXT_PT))
        # self.projektasS.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.sandelisS = QLineEdit()
        # self.sandelisS.setFont(QFont("Times", self.TEXT_PT))
        # self.sandelisS.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.vietaS = QLineEdit()
        # self.vietaS.setFont(QFont("Times", self.TEXT_PT))
        # self.vietaS.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # # sanaudos ##################################
        # self.pavadinimasSA = QLineEdit()
        # self.pavadinimasSA.setFont(QFont("Times", self.TEXT_PT))
        # self.pavadinimasSA.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        #
        # self.projektasSA = QLineEdit()
        # self.projektasSA.setFont(QFont("Times", self.TEXT_PT))
        # self.projektasSA.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

    def layouts(self):
        self.mainLayout = QGridLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QGroupBox("Užsakymai:")
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        # self.widgetLayout1 = QFormLayout()
        # self.widgetFrame1 = QGroupBox("Atsargos (neveikia):")
        # self.widgetFrame1.setFont(QFont("Times", self.TEXT_PT))
        #
        # self.widgetLayout2 = QFormLayout()
        # self.widgetFrame2 = QGroupBox("Rolikai (neveikia):")
        # self.widgetFrame2.setFont(QFont("Times", self.TEXT_PT))
        #
        # self.widgetLayout3 = QFormLayout()
        # self.widgetFrame3 = QGroupBox("Pavaros (neveikia):")
        # self.widgetFrame3.setFont(QFont("Times", self.TEXT_PT))
        #
        # self.widgetLayout4 = QFormLayout()
        # self.widgetFrame4 = QGroupBox("Sandėlis (neveikia):")
        # self.widgetFrame4.setFont(QFont("Times", self.TEXT_PT))
        #
        # self.widgetLayout5 = QFormLayout()
        # self.widgetFrame5 = QGroupBox("Sąnaudos (neveikia):")
        # self.widgetFrame5.setFont(QFont("Times", self.TEXT_PT))

        # self.widgetFrame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        # self.widgetFrame1.setFrameStyle(QFrame.Panel | QFrame.Plain)
        # self.widgetFrame2.setFrameStyle(QFrame.Panel | QFrame.Plain)
        # self.widgetFrame3.setFrameStyle(QFrame.Panel | QFrame.Plain)
        # self.widgetFrame4.setFrameStyle(QFrame.Panel | QFrame.Plain)
        # self.widgetFrame5.setFrameStyle(QFrame.Panel | QFrame.Plain)

        ############################## UZSAKYMAI
        self.widgetLayout.addRow(QLabel("ĮMONĖ: "), self.imoneE)
        self.widgetLayout.addRow(QLabel("BRAIŽĖ: "), self.braizeE)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasE)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasE)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetFrame.setLayout(self.widgetLayout)

        # ############################ ATSARGOS
        # self.widgetLayout1.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasA)
        # self.widgetLayout1.addRow(QLabel("SANDĖLIS: "), self.sandelisA)
        # self.widgetLayout1.addRow(QLabel("VIETA: "), self.vietaA)
        # self.widgetLayout1.addRow(QLabel(""))
        # self.widgetFrame1.setLayout(self.widgetLayout1)
        #
        #
        # ############################### ROLIKAI
        # self.widgetLayout2.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasR)
        # self.widgetLayout2.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasR)
        # self.widgetLayout2.addRow(QLabel("TIPAS: "), self.tipasR)
        # self.widgetLayout2.addRow(QLabel("SANDĖLIS: "), self.sandelisR)
        # self.widgetLayout2.addRow(QLabel("VIETA: "), self.vietaR)
        # self.widgetLayout2.addRow(QLabel(""))
        # self.widgetFrame2.setLayout(self.widgetLayout2)
        #
        # ################################# PAVAROS
        # self.widgetLayout3.addRow(QLabel("GAMINTOJAS: "), self.gamintojasP)
        # self.widgetLayout3.addRow(QLabel("TIPAS: "), self.tipasP)
        # self.widgetLayout3.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasP)
        # self.widgetLayout3.addRow(QLabel("SANDĖLIS: "), self.sandelisP)
        # self.widgetLayout3.addRow(QLabel("VIETA: "), self.vietaP)
        # self.widgetLayout3.addRow(QLabel(""))
        # self.widgetFrame3.setLayout(self.widgetLayout3)
        #
        # ############################## SANDELIAI
        # self.widgetLayout4.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasS)
        # self.widgetLayout4.addRow(QLabel("PROJEKTAS: "), self.projektasS)
        # self.widgetLayout4.addRow(QLabel("SANDĖLIS: "), self.sandelisS)
        # self.widgetLayout4.addRow(QLabel("VIETA: "), self.vietaS)
        # self.widgetLayout4.addRow(QLabel(""))
        # self.widgetFrame4.setLayout(self.widgetLayout4)
        #
        # ################################# SANAUDOS
        # self.widgetLayout5.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasSA)
        # self.widgetLayout5.addRow(QLabel("PROJEKTAS: "), self.projektasSA)
        # self.widgetLayout5.addRow(QLabel(""))
        # self.widgetFrame5.setLayout(self.widgetLayout5)

        ####################################
        self.mainLayout.addWidget(self.widgetFrame, 0, 0)
        # self.mainLayout.addWidget(self.widgetFrame1, 0, 1)
        # self.mainLayout.addWidget(self.widgetFrame2, 0, 2)
        # self.mainLayout.addWidget(self.widgetFrame3, 1, 0)
        # self.mainLayout.addWidget(self.widgetFrame4, 1, 1)
        # self.mainLayout.addWidget(self.widgetFrame5, 1, 2)
        self.mainLayout.addWidget(self.okBtn, 1, 0)
        self.mainLayout.addWidget(self.cancelBtn, 2, 0)

        #################################
        self.setLayout(self.mainLayout)

    def addCombo(self):
        imone = self.imoneE.text().upper()
        braize = self.braizeE.text().upper()
        projektas = self.projektasE.text().upper()
        pavadinimas = self.pavadinimasE.text()

        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute('''INSERT INTO combo_uzsakymai (uzsakymai_imone, uzsakymai_konstruktorius, uzsakymai_projektas, 
                        uzsakymai_pavadinimas) VALUES (%s, %s, %s, %s)''',
                      (imone, braize, projektas, pavadinimas))

            con.commit()

            con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        finally:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Has been successfully added.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def closeAddCombo(self):
        self.close()
