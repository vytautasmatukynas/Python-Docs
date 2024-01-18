import psycopg2
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config

stelazas_db_table = config.sql_db


class MainWindowStelazas(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Butrimoniu Sandelis")
        MainWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        MainWindow.resize(1190, 410)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.s1 = QtWidgets.QPushButton(self.centralwidget)
        self.s1.setGeometry(QtCore.QRect(20, 20, 90, 30))
        self.s1.setObjectName("s1")
        self.s1.clicked.connect(self.stelazas1)

        self.s13 = QtWidgets.QPushButton(self.centralwidget)
        self.s13.setGeometry(QtCore.QRect(140, 290, 30, 90))
        self.s13.setObjectName("s13")
        self.s13.clicked.connect(self.stelazas13)

        self.s2 = QtWidgets.QPushButton(self.centralwidget)
        self.s2.setGeometry(QtCore.QRect(180, 20, 90, 30))
        self.s2.setObjectName("s2")
        self.s2.clicked.connect(self.stelazas2)

        self.s7 = QtWidgets.QPushButton(self.centralwidget)
        self.s7.setGeometry(QtCore.QRect(630, 20, 90, 30))
        self.s7.setObjectName("s7")
        self.s7.clicked.connect(self.stelazas7)

        self.s5 = QtWidgets.QPushButton(self.centralwidget)
        self.s5.setGeometry(QtCore.QRect(450, 20, 90, 30))
        self.s5.setObjectName("s5")
        self.s5.clicked.connect(self.stelazas5)

        self.s4 = QtWidgets.QPushButton(self.centralwidget)
        self.s4.setGeometry(QtCore.QRect(360, 20, 90, 30))
        self.s4.setObjectName("s4")
        self.s4.clicked.connect(self.stelazas4)

        self.s3 = QtWidgets.QPushButton(self.centralwidget)
        self.s3.setGeometry(QtCore.QRect(270, 20, 90, 30))
        self.s3.setObjectName("s3")
        self.s3.clicked.connect(self.stelazas3)

        self.s6 = QtWidgets.QPushButton(self.centralwidget)
        self.s6.setGeometry(QtCore.QRect(540, 20, 90, 30))
        self.s6.setObjectName("s6")
        self.s6.clicked.connect(self.stelazas6)

        self.s12 = QtWidgets.QPushButton(self.centralwidget)
        self.s12.setGeometry(QtCore.QRect(140, 200, 30, 90))
        self.s12.setObjectName("s12")
        self.s12.clicked.connect(self.stelazas12)

        self.s14 = QtWidgets.QPushButton(self.centralwidget)
        self.s14.setGeometry(QtCore.QRect(170, 200, 30, 90))
        self.s14.setObjectName("s14")
        self.s14.clicked.connect(self.stelazas14)

        self.s15 = QtWidgets.QPushButton(self.centralwidget)
        self.s15.setGeometry(QtCore.QRect(170, 290, 30, 90))
        self.s15.setObjectName("s15")
        self.s15.clicked.connect(self.stelazas15)

        self.s16 = QtWidgets.QPushButton(self.centralwidget)
        self.s16.setGeometry(QtCore.QRect(350, 290, 30, 90))
        self.s16.setObjectName("s16")
        self.s16.clicked.connect(self.stelazas16)

        self.s17 = QtWidgets.QPushButton(self.centralwidget)
        self.s17.setGeometry(QtCore.QRect(1080, 160, 30, 90))
        self.s17.setObjectName("s17")
        self.s17.clicked.connect(self.stelazas17)

        self.s8 = QtWidgets.QPushButton(self.centralwidget)
        self.s8.setGeometry(QtCore.QRect(720, 20, 90, 30))
        self.s8.setObjectName("s8")
        self.s8.clicked.connect(self.stelazas8)

        self.s10 = QtWidgets.QPushButton(self.centralwidget)
        self.s10.setGeometry(QtCore.QRect(900, 20, 90, 30))
        self.s10.setObjectName("s10")
        self.s10.clicked.connect(self.stelazas10)

        self.s9 = QtWidgets.QPushButton(self.centralwidget)
        self.s9.setGeometry(QtCore.QRect(810, 20, 90, 30))
        self.s9.setObjectName("s9")
        self.s9.clicked.connect(self.stelazas9)

        self.s11 = QtWidgets.QPushButton(self.centralwidget)
        self.s11.setGeometry(QtCore.QRect(990, 20, 90, 30))
        self.s11.setObjectName("s11")
        self.s11.clicked.connect(self.stelazas11)

        self.v10 = QtWidgets.QPushButton(self.centralwidget)
        self.v10.setGeometry(QtCore.QRect(10, 60, 111, 321))
        self.v10.setObjectName("v10")
        self.v10.clicked.connect(self.vartai10)

        self.v11 = QtWidgets.QPushButton(self.centralwidget)
        self.v11.setGeometry(QtCore.QRect(220, 60, 111, 321))
        self.v11.setObjectName("v11")
        self.v11.clicked.connect(self.vartai11)

        self.v12 = QtWidgets.QPushButton(self.centralwidget)
        self.v12.setGeometry(QtCore.QRect(400, 60, 111, 321))
        self.v12.setObjectName("v12")
        self.v12.clicked.connect(self.vartai12)

        self.v14 = QtWidgets.QPushButton(self.centralwidget)
        self.v14.setGeometry(QtCore.QRect(950, 60, 111, 321))
        self.v14.setObjectName("v14")
        self.v14.clicked.connect(self.vartai14)

        self.z1 = QtWidgets.QPushButton(self.centralwidget)
        self.z1.setGeometry(QtCore.QRect(660, 60, 271, 321))
        self.z1.setObjectName("z1")
        self.z1.clicked.connect(self.zona1)

        self.z2 = QtWidgets.QPushButton(self.centralwidget)
        self.z2.setGeometry(QtCore.QRect(1120, 20, 60, 180))
        self.z2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.z2.setFlat(False)
        self.z2.setObjectName("z2")
        self.z2.clicked.connect(self.zona2)

        self.kontora = QtWidgets.QPushButton(self.centralwidget)
        self.kontora.setGeometry(QtCore.QRect(1120, 210, 60, 180))
        self.kontora.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.kontora.setFlat(False)
        self.kontora.setObjectName("kontora")
        self.kontora.clicked.connect(self.kontora1)

        self.v13 = QtWidgets.QPushButton(self.centralwidget)
        self.v13.setGeometry(QtCore.QRect(530, 60, 111, 321))
        self.v13.setObjectName("v13")
        self.v13.clicked.connect(self.vartai13)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1193, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Butrimoniu Sandelis", "Butrimoniu Sandelis"))
        self.s1.setText(_translate("MainWindow", "1"))
        self.s13.setText(_translate("MainWindow", "13"))
        self.s2.setText(_translate("MainWindow", "2"))
        self.s7.setText(_translate("MainWindow", "7"))
        self.s5.setText(_translate("MainWindow", "5"))
        self.s4.setText(_translate("MainWindow", "4"))
        self.s3.setText(_translate("MainWindow", "3"))
        self.s6.setText(_translate("MainWindow", "6"))
        self.s12.setText(_translate("MainWindow", "12"))
        self.s14.setText(_translate("MainWindow", "14"))
        self.s15.setText(_translate("MainWindow", "15"))
        self.s16.setText(_translate("MainWindow", "16"))
        self.s17.setText(_translate("MainWindow", "17"))
        self.s8.setText(_translate("MainWindow", "8"))
        self.s10.setText(_translate("MainWindow", "10"))
        self.s9.setText(_translate("MainWindow", "9"))
        self.s11.setText(_translate("MainWindow", "11"))
        self.v10.setText(_translate("MainWindow", "Vartai 10"))
        self.v11.setText(_translate("MainWindow", "Vartai 11"))
        self.v12.setText(_translate("MainWindow", "Vartai 12"))
        self.v14.setText(_translate("MainWindow", "Vartai 14"))
        self.z1.setText(_translate("MainWindow", "Zona 1"))
        self.z2.setText(_translate("MainWindow", "Zona 2"))
        self.kontora.setText(_translate("MainWindow", "Kontora"))
        self.v13.setText(_translate("MainWindow", "Vartai 13"))

    def stelazas1(self):
        self.stel1 = mainStelazas1()

    def stelazas2(self):
        self.stel1 = mainStelazas2()

    def stelazas3(self):
        self.stel1 = mainStelazas3()

    def stelazas4(self):
        self.stel1 = mainStelazas4()

    def stelazas5(self):
        self.stel1 = mainStelazas5()

    def stelazas6(self):
        self.stel1 = mainStelazas6()

    def stelazas7(self):
        self.stel1 = mainStelazas7()

    def stelazas8(self):
        self.stel1 = mainStelazas8()

    def stelazas9(self):
        self.stel1 = mainStelazas9()

    def stelazas10(self):
        self.stel1 = mainStelazas10()

    def stelazas11(self):
        self.stel1 = mainStelazas11()

    def stelazas12(self):
        self.stel1 = mainStelazas12()

    def stelazas13(self):
        self.stel1 = mainStelazas13()

    def stelazas14(self):
        self.stel1 = mainStelazas14()

    def stelazas15(self):
        self.stel1 = mainStelazas15()

    def stelazas16(self):
        self.stel1 = mainStelazas16()

    def stelazas17(self):
        self.stel1 = mainStelazas17()

    def vartai10(self):
        self.stel1 = mainVartai10()

    def vartai11(self):
        self.stel1 = mainVartai11()

    def vartai12(self):
        self.stel1 = mainVartai12()

    def vartai13(self):
        self.stel1 = mainVartai13()

    def vartai14(self):
        self.stel1 = mainVartai14()

    def zona1(self):
        self.stel1 = mainZona1()

    def zona2(self):
        self.stel1 = mainZona2()

    def kontora1(self):
        self.stel1 = mainKontora1()


class mainStelazas1(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-1")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-1' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas2(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-2")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-2' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas3(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-3")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-3' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas4(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-4")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-4' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas5(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-5")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-5' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas6(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-6")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-6' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas7(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-7")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-7' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas8(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-8")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-8' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas9(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-9")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-9' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas10(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-10")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-10' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas11(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-11")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-11' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas12(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-12")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-12' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas13(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-13")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-13' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas14(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-14")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-14' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas15(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-15")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-15' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas16(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-16")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-16' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainStelazas17(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("STELAZAS-17")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'STELAZAS-17' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainVartai10(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("VARTAI-10")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'VARTAI-10' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainVartai11(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("VARTAI-11")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'VARTAI-11' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainVartai12(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("VARTAI-12")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'VARTAI-12' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainVartai13(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("VARTAI-13")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'VARTAI-13' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainVartai14(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("VARTAI-14")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'VARTAI-14' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainZona1(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("ZONA-1")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'ZONA-1' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainZona2(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("ZONA-2")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'ZONA-2' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


class mainKontora1(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        self.setWindowTitle("KONTORA")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(200, 200, 800, 400)
        # self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
        self.displayStelazas()

    def widgets(self):
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setColumnWidth(2, 50)
        self.stelazasTable.setColumnWidth(3, 50)
        self.stelazasTable.setColumnWidth(4, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.stelazasTable)
        central_widget = QWidget()
        central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(central_widget)

    def displayStelazas(self):
        self.stelazasTable.setFont(QFont("Times", 10))
        for i in reversed(range(self.stelazasTable.rowCount())):
            self.stelazasTable.removeRow(i)

        conn = psycopg2.connect(
            **stelazas_db_table
        )

        cur = conn.cursor()

        cur.execute(
            """SELECT * FROM stelazas WHERE vieta = 'KONTORA' ORDER BY sandelis ASC, vieta ASC, pavadinimas ASC""")

        query = cur.fetchall()

        for row_date in query:
            row_number = self.stelazasTable.rowCount()
            self.stelazasTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                self.stelazasTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        """neleidzia editint column"""
        self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""QWidget{
                            background-color:lightgrey;
                            padding: -2px;
                            }

                            QScrollBar::vertical{
                            background-color:dimgray;
                            width:10px;
                            padding-top:24px;
                            }

                            QScrollBar::sub-page:vertical{
                            background: lightgray;
                            }

                            QScrollBar::add-page:vertical{
                            background: lightgray;
                            }

                            QScrollBar::handle{
                            background-color: dimgray;
                            }

                            QScrollBar::sub-line:vertical {
                            height: 23px;
                            background-color: dimgray;
                            border-bottom:1px solid black;
                            }

                            QTableWidget{
                            background:floralwhite;
                            gridline-color:black;
                            border:1px solid black;
                            }

                            QTableWidget::item:hover{
                            background:steelblue;
                            color: white;
                            }

                            QTableWidget::item:selected{
                            background:slategray;
                            color:white;
                            }

                            QHeaderView{
                            background-color:gray;
                            }

                            QHeaderView::section{
                            background:dimgray;
                            color:white;
                            }

                            QHeaderView::section:selected{
                            background:dimgray;
                            color:white;
                            }

                            QHeaderView::section:checked{
                            background-color: dimgray;
                            font: normal;
                            }

                            QTableCornerButton::section{
                            background:gray;
                            border:0.5px solid black;
                            }


                            QPushButton{
                            background-color:dimgray;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            }

                            QPushButton::hover{
                            background-color:steelblue;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:slategray;
                            color:white;
                            }
                            """)

    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowStelazas()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
