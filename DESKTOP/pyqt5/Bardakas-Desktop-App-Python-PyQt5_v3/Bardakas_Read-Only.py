import os
import sys

import psycopg2
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import config

import Bardakas_style_gray
from open import open_rolikai_pvz

params = config.sql_db

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()

__author__ = 'Vytautas Matukynas'
__copyright__ = f'Copyright (C) {year}, Vytautas Matukynas'
__credits__ = ['Vytautas Matukynas']
__license__ = 'Vytautas Matukynas'
__version__ = 'Read-Only'
__maintainer__ = 'Vytautas Matukynas'
__email__ = 'vytautas.matukynas@gmail.com'
__status__ = 'Read-Only'
_AppName_ = 'Bardakas'


# align for QTable class, DELEGATE ALIGNMENT
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class MainMenu(QMainWindow):
    def __init__(self):
        """mainWindow"""
        super().__init__()

        # self.shortcut_delete_uzsakymai = QShortcut(QKeySequence('Delete'), self)
        # self.shortcut_delete_uzsakymai.activated.connect(self.deleteUzsakymas_sh)

        # mainWindow
        self.setWindowTitle("BARDAKAS")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(100, 100, 1200, 720)
        # dont resize window
        # self.setFixedSize(self.size())
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

        self.option = True

        # MainClass functions
        self.UI()
        self.show()

    def UI(self):
        """Main Menu bar"""
        # Function that starts at starts
        self.menubar()
        self.widgets()
        self.default_widgets()
        self.progressBar()
        self.layouts()
        self.toolbarTop()
        Bardakas_style_gray.SheetStyle(self)

    def menubar(self):
        menuBar = self.menuBar()
        menuBar.isRightToLeft()

        # File bar
        file = menuBar.addMenu("File")
        # Submenu bar
        Info = QAction("About", self)
        Info.setIcon(QIcon("icons/info.png"))
        Info.triggered.connect(self.helpinfo)
        file.addAction(Info)
        file.addSeparator()
        exit = QAction("Exit", self)
        exit.triggered.connect(self.MainClose)
        exit.setShortcut("Ctrl+Q")
        exit.setIcon(QIcon("icons/exit.png"))
        file.addAction(exit)

    def helpinfo(self):
        # QMessageBox.information(self, "ABOUT", "If you want to find a needle in a haystack,\n"
        #                                        "burn the haystack.")
        msg = QMessageBox()
        msg.setWindowTitle("ABOUT")
        msg.setText("If you want to find a needle in a haystack,\n"
                    "burn the haystack.\n"
                    "\n"
                    "BARDAKAS version {}\n"
                    "\n"
                    "{}".format(__version__, __copyright__))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

        Bardakas_style_gray.msgsheetstyle(msg)

        x = msg.exec_()

    def widgets(self):
        """Tables"""
        self.emptyTable = QTableWidget()
        self.emptyTable.setColumnCount(0)

        # ATSARGOS TABLE
        self.atsarguTable = QTableWidget()
        self.atsarguTable.setColumnCount(10)
        self.atsarguTable.setSortingEnabled(True)
        self.atsarguTable.setColumnHidden(0, True)
        # self.atsarguTable.setColumnHidden(6, True)

        headers_atsr = ["ID", "PAVADINIMAS", "KONFIGURACIJA", "SANDĖLIS", "VIETA", "KIEKIS", "VIENETAI", "KOMENTARAI",
                        "NUOTRAUKA", "ATNAUJINTA"]

        for column_number in range(0, len(headers_atsr)):
            while column_number < len(headers_atsr):
                header_name = headers_atsr[column_number]
                self.atsarguTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.atsarguTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atsarguTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atsarguTable.horizontalHeader().setHighlightSections(False)
        self.atsarguTable.horizontalHeader().setDisabled(True)
        self.atsarguTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.atsarguTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.atsarguTable.clicked.connect(self.atsargostable_select)
        self.atsarguTable.doubleClicked.connect(self.openPicture)

        # ROLIKAI TABLE
        self.rolikaiTable = QTableWidget()
        self.rolikaiTable.setColumnCount(12)
        self.rolikaiTable.setColumnHidden(0, True)
        self.rolikaiTable.setSortingEnabled(True)

        headers_rolik = ["ID", "PAVADINIMAS", "ILGIS", "KIEKIS", "TVIRTINIMAS", "TIPAS", "APRAŠYMAS",
                         "PROJEKTAS", "KOMENTARAI", "SANDĖLIS", "VIETA", "ATNAUJINTA"]

        for column_number in range(0, len(headers_rolik)):
            while column_number < len(headers_rolik):
                header_name = headers_rolik[column_number]
                self.rolikaiTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.rolikaiTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rolikaiTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rolikaiTable.horizontalHeader().setHighlightSections(False)
        self.rolikaiTable.horizontalHeader().setDisabled(True)
        self.rolikaiTable.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)
        self.rolikaiTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        # PAVAROS TABLE
        self.pavarosTable = QTableWidget()
        self.pavarosTable.setColumnCount(14)
        self.pavarosTable.setColumnHidden(0, True)
        self.pavarosTable.setSortingEnabled(True)

        headers_pavar = ["ID", "PAVADINIMAS", "GAMINTOJAS", "TIPAS", "kW", "aps/min",
                         "Nm", "TVIRTINIMAS", "DIAMETRAS (mm)", "KIEKIS", "KOMENTARAI", "SANDĖLIS",
                         "VIETA", "ATNAUJINTA"]

        for column_number in range(0, len(headers_pavar)):
            while column_number < len(headers_pavar):
                header_name = headers_pavar[column_number]
                self.pavarosTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.pavarosTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.pavarosTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.pavarosTable.horizontalHeader().setHighlightSections(False)
        self.pavarosTable.horizontalHeader().setDisabled(True)
        self.pavarosTable.horizontalHeader().setSectionResizeMode(10, QHeaderView.Stretch)
        self.pavarosTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Align delegate Class
        delegate = AlignDelegate()

        # for column
        for number in [1, 2, 3, 4, 5, 6, 8, 9]:
            self.atsarguTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]:
            self.rolikaiTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13]:
            self.pavarosTable.setItemDelegateForColumn(number, delegate)

        # Search widget
        self.cancelButton1 = QPushButton("CANCEL")
        self.cancelButton1.setFixedHeight(25)
        self.cancelButton1.setFixedWidth(90)
        self.cancelButton1.clicked.connect(self.clearSearchEntry)
        self.cancelButton1.setFont(QFont("Times", 10))

        self.searchButton1 = QPushButton("SEARCH")
        self.searchButton1.setFixedHeight(25)
        self.searchButton1.setFixedWidth(90)
        self.searchButton1.clicked.connect(self.searchTables)
        self.searchButton1.setFont(QFont("Times", 10))

        self.searchEntry1 = QLineEdit()
        self.searchEntry1.setFixedHeight(25)
        self.searchEntry1.setPlaceholderText('Filter table...')

        self.cancelButton2 = QPushButton("CANCEL")
        self.cancelButton2.setFixedHeight(25)
        self.cancelButton2.setFixedWidth(90)
        self.cancelButton2.clicked.connect(self.clearSearchEntry2)
        self.cancelButton2.setFont(QFont("Times", 10))

        self.searchEntry2 = QLineEdit()
        self.searchEntry2.setFixedHeight(25)
        self.searchEntry2.setPlaceholderText('Select table items...')
        self.searchEntry2.textChanged.connect(self.searchTables2)

        # Treeview table
        self.treeTable = QTreeWidget()
        self.treeTable.setAnimated(True)
        self.treeTable.setHeaderHidden(True)
        self.treeTable.setColumnCount(1)
        self.treeTable.setFixedWidth(150)

        self.atsargosSelect = QTreeWidgetItem(self.treeTable, ["Atsargos"])
        self.atsargosSelect.setExpanded(True)
        self.rolikaiSelect = QTreeWidgetItem(self.treeTable, ["Rolikų atsargos"])
        self.rolikaiSelect.setExpanded(True)
        self.pavarosSelect = QTreeWidgetItem(self.treeTable, ["Pavarų atsargos"])
        self.pavarosSelect.setExpanded(True)

        atsargosSelect1 = ["EQ", "Komponentai", "Pneumo"]
        for item2 in atsargosSelect1:
            self.atsargosSelect.addChild(QTreeWidgetItem([item2]))
        rolikaiSelect1 = ["Paprastas", "RM", "Posukis", "Posukis-RM"]
        for item3 in rolikaiSelect1:
            self.rolikaiSelect.addChild(QTreeWidgetItem([item3]))

        # PAVAROS child treeview headers
        con = psycopg2.connect(
            **params
        )
        cur = con.cursor()

        cur.execute("""SELECT galia FROM pavaros""")
        query = cur.fetchall()

        con.close()

        pavaros_default_headers = [i[0] + " (kW)" for i in query]
        pavaros_clean_headers = set(pavaros_default_headers)
        pavaros_child_header = list(pavaros_clean_headers)
        pavaros_child_header.sort()

        self.pavarosSelect1 = pavaros_child_header
        for item4 in self.pavarosSelect1:
            self.pavarosSelect.addChild(QTreeWidgetItem([item4]))

        self.treeTable.clicked.connect(self.listTables)

        # Timer
        self.Timer = QLabel()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)  # update every second

        self.showTime()

    def showTime(self):
        currentTime = QTime.currentTime()
        displayTxt = currentTime.toString('hh:mm:ss')
        self.Timer.setText(displayTxt)

    def progressBar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)

    def default_widgets(self):
        self.sort_check = QCheckBox("Enable Table Sorting")
        self.sort_check.clicked.connect(self.enable_sorting)

        self.expand_button = QPushButton()
        self.expand_button.setIcon(QIcon("icons/to_left.png"))
        self.expand_button.setIconSize(QSize(19, 19))
        self.expand_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.expand_button.setFixedWidth(20)
        self.expand_button.clicked.connect(self.treeTableHideShow)

    def enable_sorting(self):
        if self.sort_check.isChecked():
            self.atsarguTable.horizontalHeader().setDisabled(False)
            self.rolikaiTable.horizontalHeader().setDisabled(False)
            self.pavarosTable.horizontalHeader().setDisabled(False)

        else:
            self.atsarguTable.horizontalHeader().setDisabled(True)
            self.rolikaiTable.horizontalHeader().setDisabled(True)
            self.pavarosTable.horizontalHeader().setDisabled(True)

    def treeTableHideShow(self):
        if self.option:
            self.treeTable.hide()
            self.sort_check.hide()
            self.expand_button.setIcon(QIcon("icons/to_right.png"))

            self.option = False

        else:
            self.treeTable.show()
            self.sort_check.show()
            self.expand_button.setIcon(QIcon("icons/to_left.png"))

            self.option = True

    def layouts(self):
        """App layouts"""
        self.mainLayout = QVBoxLayout()

        self.searchLayout = QHBoxLayout()
        self.middleLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.LeftLayoutTop = QVBoxLayout()
        self.treeLeftLayout = QVBoxLayout()

        self.searchLayout_table = QHBoxLayout()
        self.tbLayout_table = QHBoxLayout()
        self.tableRightLayout = QStackedLayout()
        self.mainRightLayout = QVBoxLayout()

        # Search layout
        self.searchLayout.addWidget(self.cancelButton1)
        self.searchLayout.addWidget(self.searchButton1)
        self.searchLayout.addWidget(self.searchEntry1)

        # Middle layout
        # Left side
        self.LeftLayoutTop.addWidget(self.treeTable)
        self.LeftLayoutTop.addWidget(self.sort_check)
        self.treeLeftLayout.addLayout(self.LeftLayoutTop)

        # Right side search
        self.searchLayout_table.addWidget(self.cancelButton2)
        self.searchLayout_table.addWidget(self.searchEntry2)

        # Right side tables
        self.tableRightLayout.addWidget(self.atsarguTable)
        self.tableRightLayout.addWidget(self.rolikaiTable)
        self.tableRightLayout.addWidget(self.pavarosTable)
        self.tableRightLayout.addWidget(self.emptyTable)
        self.tableRightLayout.setCurrentIndex(3)

        # Right layout with search
        self.mainRightLayout.addLayout(self.searchLayout_table, 1)
        self.mainRightLayout.addLayout(self.tableRightLayout, 98)

        # Bottom layout
        self.bottomLayout.addWidget(QLabel(f"Bardakas (Read-Only)"), 86, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(self.progress_bar, 12, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(QLabel(f"Current date/time: {datetime.toPyDate()}"), 1, alignment=Qt.AlignRight)
        self.bottomLayout.addWidget(self.Timer, 1, alignment=Qt.AlignRight)

        # Main layout
        self.middleLayout.addLayout(self.treeLeftLayout)
        self.middleLayout.addWidget(self.expand_button)
        self.middleLayout.addLayout(self.mainRightLayout)

        self.mainLayout.addLayout(self.searchLayout, 1)
        self.mainLayout.addLayout(self.middleLayout, 98)
        self.mainLayout.addLayout(self.bottomLayout, 1)

        # Central_widget to view widgets
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.central_widget)

        self.atsarguTable.horizontalHeader().setDisabled(True)
        self.rolikaiTable.horizontalHeader().setDisabled(True)
        self.pavarosTable.horizontalHeader().setDisabled(True)

    def atsargostable_select(self):
        global atsargosId

        listAtsargos = []
        for i in range(0, 8):
            listAtsargos.append(self.atsarguTable.item(self.atsarguTable.currentRow(), i).text())

        atsargosId = listAtsargos[0]

    def toolbarTop(self):
        """toolbar buttons"""
        self.tb1 = self.addToolBar("Open tb")
        self.tb1.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb1.setIconSize(QtCore.QSize(30, 30))

        self.openStelazai = QAction(QIcon("icons/plan.png"), "Butrimonių sandėlis", self)
        self.tb1.addAction(self.openStelazai)
        self.openStelazai.triggered.connect(self.stelazas_map)

        self.tb1.addSeparator()

        self.openRolikuPvz = QAction(QIcon("icons/rolikai.png"), "Roliku Pavyzdys", self)
        self.tb1.addAction(self.openRolikuPvz)
        self.openRolikuPvz.triggered.connect(self.open_rolikai_pvz_)

        self.tb1.addSeparator()

    def displayAtsargos(self):
        try:
            self.atsarguTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.atsarguTable.rowCount())):
                self.atsarguTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()
            cur.execute("""SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
            nuotrauka, update_date, filename, filetype, filedir FROM atsargos ORDER BY pavadinimas ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.atsarguTable.rowCount()
                self.atsarguTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                  'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS']
                    list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                   (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                   (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                   (188, 143, 143, 110)]
                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    list_dirz = ["BELTAS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ"]
                    for item in list_dirz:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(254, 253, 195, 110))

                    list_EQ = ["EQ-GALINUKAS", "EQ-PRILAIKANTIS", "EQ-03-01-00-003 NORD", "EQ-03-01-00-002", "EQ-IVORE"]
                    for item in list_EQ:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                    list_standartiniai = ["HABASIT", "PLASTIKINE IVORE", "UZDENGIMAS", "ALIUMINIS PROFILIS"]
                    for item in list_standartiniai:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                    if data == "0":
                        setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                    for i in range(1, 31):
                        if data == str(i):
                            setitem.setBackground(QtGui.QColor(242, 172, 10, 110))

                    #   if column_number == 3 and 20 < int(data):
                    #     setitem.setBackground(QtGui.QColor(0, 204, 0))

                    self.atsarguTable.setItem(row_number, column_number, setitem)

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def displayRolikai(self):
        try:
            self.rolikaiTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.rolikaiTable.rowCount())):
                self.rolikaiTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )
            cur = con.cursor()

            cur.execute("""SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
            aprasymas, projektas, komentarai, sandelis, vieta, update_date
            FROM rolikai 
            ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.rolikaiTable.rowCount()
                self.rolikaiTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                  'AT10', 'PVC', 'GUMUOTAS', 'BUTRIMONIU']
                    list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                   (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                   (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                   (205, 200, 177, 110), (250, 235, 215, 110), (176, 196, 222, 110)]
                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                    for item in list_proj:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                    if data == "0":
                        setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                    self.rolikaiTable.setItem(row_number, column_number, setitem)

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def displayPavaros(self):
        try:
            self.pavarosTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.pavarosTable.rowCount())):
                self.pavarosTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )
            cur = con.cursor()

            cur.execute("""SELECT id, pavadinimas, gamintojas, tipas, galia, apsisukimai,
            momentas, tvirtinimas, diametras, kiekis, komentarai, sandelis, vieta, update_date
            FROM pavaros 
            ORDER BY tipas ASC, galia ASC, apsisukimai ASC, momentas ASC,
            tvirtinimas ASC, diametras ASC""")

            query = cur.fetchall()

            for row_date in query:
                row_number = self.pavarosTable.rowCount()
                self.pavarosTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['TIESINIS', 'SLIEKINIS', 'ASIS', 'KIAURYME', 'KIAURYME+FLANSAS', 'TECHNOBALT',
                                  'HIDROBALT', 'BUTRIMONIU']

                    list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                   (137, 175, 174, 110), (244, 193, 126, 110), (122, 197, 205, 110),
                                   (250, 235, 215, 110), (176, 196, 222, 110)]

                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    if data == "0":
                        setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                    self.pavarosTable.setItem(row_number, column_number, setitem)

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            self.pavarosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def listTables(self):
        """sort"""
        # Get current date
        if datetime.day() <= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-0{2}".format(year, month, day))
        elif datetime.day() <= 9 and datetime.month() >= 10:
            date = ("{0}-{1}-0{2}".format(year, month, day))
        elif datetime.day() >= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-{2}".format(year, month, day))
        else:
            date = ("{0}-{1}-{2}".format(year, month, day))

        try:
            if self.treeTable.currentItem() == self.atsargosSelect:
                self.tableRightLayout.setCurrentIndex(0)
                self.displayAtsargos()

            elif self.treeTable.currentItem() == self.rolikaiSelect:
                self.tableRightLayout.setCurrentIndex(1)
                self.displayRolikai()

            elif self.treeTable.currentItem() == self.pavarosSelect:
                self.tableRightLayout.setCurrentIndex(2)
                self.displayPavaros()

            elif self.treeTable.currentItem() == self.atsargosSelect.child(0):

                self.tableRightLayout.setCurrentIndex(0)

                self.atsarguTable.setFont(QFont("Times", 10))

                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(

                    **params

                )

                cur = con.cursor()

                cur.execute(

                    """SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
                
                    nuotrauka, update_date, filename, filetype, filedir 
                
                    FROM atsargos 
                
                    WHERE pavadinimas LIKE 'EQ%' 
                
                    ORDER BY pavadinimas ASC""")

                query = cur.fetchall()

                for row_date in query:

                    row_number = self.atsarguTable.rowCount()

                    self.atsarguTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):

                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',

                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS']

                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),

                                       (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),

                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),

                                       (188, 143, 143, 110)]

                        for count_num in range(0, len(list_names)):

                            while count_num < len(list_names):

                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))

                                count_num += 1

                        list_dirz = ["BELTAS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ"]

                        for item in list_dirz:

                            if data == item:
                                setitem.setBackground(QtGui.QColor(254, 253, 195, 110))

                        list_EQ = ["EQ-GALINUKAS", "EQ-PRILAIKANTIS", "EQ-03-01-00-003 NORD", "EQ-03-01-00-002",

                                   "EQ-IVORE"]

                        for item in list_EQ:

                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        list_standartiniai = ["HABASIT", "PLASTIKINE IVORE", "UZDENGIMAS", "ALIUMINIS PROFILIS"]

                        for item in list_standartiniai:

                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        for i in range(1, 31):

                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10, 110))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):

                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)

                    self.progress_bar.setValue(progress_val)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.atsargosSelect.child(1):
                self.tableRightLayout.setCurrentIndex(0)
                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
                    nuotrauka, update_date, filename, filetype, filedir 
                    FROM atsargos 
                    WHERE pavadinimas NOT LIKE 'EQ%' AND pavadinimas NOT LIKE 'PNEUMO'
                    ORDER BY pavadinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS']
                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_dirz = ["BELTAS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ"]
                        for item in list_dirz:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(254, 253, 195, 110))

                        list_EQ = ["EQ-GALINUKAS", "EQ-PRILAIKANTIS", "EQ-03-01-00-003 NORD", "EQ-03-01-00-002",
                                   "EQ-IVORE"]
                        for item in list_EQ:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        list_standartiniai = ["HABASIT", "PLASTIKINE IVORE", "UZDENGIMAS", "ALIUMINIS PROFILIS"]
                        for item in list_standartiniai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10, 110))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.atsargosSelect.child(2):
                self.tableRightLayout.setCurrentIndex(0)
                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
                    nuotrauka, update_date, filename, filetype, filedir 
                    FROM atsargos 
                    WHERE pavadinimas LIKE 'PNEUMO' 
                    ORDER BY pavadinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS']
                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_dirz = ["BELTAS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ"]
                        for item in list_dirz:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(254, 253, 195, 110))

                        list_EQ = ["EQ-GALINUKAS", "EQ-PRILAIKANTIS", "EQ-03-01-00-003 NORD", "EQ-03-01-00-002",
                                   "EQ-IVORE"]
                        for item in list_EQ:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        list_standartiniai = ["HABASIT", "PLASTIKINE IVORE", "UZDENGIMAS", "ALIUMINIS PROFILIS"]
                        for item in list_standartiniai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10, 110))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(0):
                self.tableRightLayout.setCurrentIndex(1)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )
                cur = con.cursor()

                cur.execute("""SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
                aprasymas, projektas, komentarai, sandelis, vieta, update_date
                FROM rolikai WHERE pavadinimas = 'PAPRASTAS'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                      'AT10', 'PVC', 'GUMUOTAS', 'BUTRIMONIU']
                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                       (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                       (205, 200, 177, 110), (250, 235, 215, 110), (176, 196, 222, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                        for item in list_proj:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(1):
                self.tableRightLayout.setCurrentIndex(1)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )
                cur = con.cursor()

                cur.execute("""SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
                aprasymas, projektas, komentarai, sandelis, vieta, update_date
                FROM rolikai WHERE pavadinimas = 'RM'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                      'AT10', 'PVC', 'GUMUOTAS', 'BUTRIMONIU']
                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                       (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                       (205, 200, 177, 110), (250, 235, 215, 110), (176, 196, 222, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                        for item in list_proj:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(2):
                self.tableRightLayout.setCurrentIndex(1)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )
                cur = con.cursor()

                cur.execute("""SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
                aprasymas, projektas, komentarai, sandelis, vieta, update_date
                FROM rolikai WHERE pavadinimas = 'POSUKIS'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                      'AT10', 'PVC', 'GUMUOTAS', 'BUTRIMONIU']
                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                       (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                       (205, 200, 177, 110), (250, 235, 215, 110), (176, 196, 222, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                        for item in list_proj:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(3):
                self.tableRightLayout.setCurrentIndex(1)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )
                cur = con.cursor()

                cur.execute("""SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
                aprasymas, projektas, komentarai, sandelis, vieta, update_date
                FROM rolikai WHERE pavadinimas = 'POSUKIS-RM'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                      'AT10', 'PVC', 'GUMUOTAS', 'BUTRIMONIU']
                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                       (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                       (205, 200, 177, 110), (250, 235, 215, 110), (176, 196, 222, 110)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                        for item in list_proj:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            else:
                ######### sort pavarostable by selecting items in SQL table, same as TreeTable child headers ######
                con = psycopg2.connect(
                    **params
                )
                cur = con.cursor()

                cur.execute("""SELECT galia FROM pavaros""")
                query = cur.fetchall()

                self.pavaros_get_header = [i[0] for i in query]
                self.pavaros_clean_get_header = set(self.pavaros_get_header)
                self.pavaros_headers = list(self.pavaros_clean_get_header)
                self.pavaros_headers.sort()

                for index_number in range(0, len(self.pavaros_headers)):
                    if self.treeTable.currentItem() == self.pavarosSelect.child(index_number):
                        self.tableRightLayout.setCurrentIndex(2)
                        self.pavarosTable.setFont(QFont("Times", 10))
                        for i in reversed(range(self.pavarosTable.rowCount())):
                            self.pavarosTable.removeRow(i)

                        con = psycopg2.connect(
                            **params
                        )
                        cur = con.cursor()

                        cur.execute(f"""SELECT id, pavadinimas, gamintojas, tipas, galia, apsisukimai,
                        momentas, tvirtinimas, diametras, kiekis, komentarai, sandelis, vieta, update_date 
                        FROM pavaros WHERE galia = '{self.pavaros_headers[index_number]}'
                        ORDER BY tipas ASC, galia ASC, apsisukimai ASC, momentas ASC, tvirtinimas ASC, 
                        diametras ASC""")
                        query = cur.fetchall()

                        for row_date in query:
                            row_number = self.pavarosTable.rowCount()
                            self.pavarosTable.insertRow(row_number)
                            for column_number, data in enumerate(row_date):
                                setitem = QTableWidgetItem(str(data))

                                list_names = ['TIESINIS', 'SLIEKINIS', 'ASIS', 'KIAURYME', 'KIAURYME+FLANSAS',
                                              'TECHNOBALT', 'HIDROBALT', 'BUTRIMONIU']

                                list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                               (137, 175, 174, 110), (244, 193, 126, 110), (122, 197, 205, 110),
                                               (250, 235, 215, 110), (176, 196, 222, 110)]

                                for count_num in range(0, len(list_names)):
                                    while count_num < len(list_names):
                                        if data == list_names[count_num]:
                                            setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                        count_num += 1

                                if data == "0":
                                    setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                                self.pavarosTable.setItem(row_number, column_number, setitem)

                        row_count = cur.rowcount

                        for i in range(0, row_count):
                            value = 100

                            self.progress_bar.setRange(0, value)

                            if value > 50:
                                self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                            progress_val = int(((i + 1) / row_count) * 100)
                            self.progress_bar.setValue(progress_val)

                        self.pavarosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                    con.close()

                    index_number += 1


        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def refreshTables(self):
        try:
            self.listTables()
        except Exception as error:
            print(f"{error}")

    def searchTables(self):
        """SEARCH FROM SQL TABLE AND REFRESH QTABLE TO VIEW JUST SEARCHED ITEMS"""
        # Get current date
        if datetime.day() <= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-0{2}".format(year, month, day))
        elif datetime.day() <= 9 and datetime.month() >= 10:
            date = ("{0}-{1}-0{2}".format(year, month, day))
        elif datetime.day() >= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-{2}".format(year, month, day))
        else:
            date = ("{0}-{1}-{2}".format(year, month, day))

        try:
            if self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):
                a = a1 = a2 = a3 = a4 = a5 = self.searchEntry1.text()

                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
                    nuotrauka, update_date, filename, filetype, filedir
                    FROM atsargos WHERE pavadinimas ILIKE '%{}%' OR konfig ILIKE '%{}%' OR vieta ILIKE '%{}%' OR 
                    kiekis ILIKE '%{}%' OR mat_pav ILIKE '%{}%' OR komentaras ILIKE '%{}%'
                    ORDER BY pavadinimas ASC, konfig ASC""".format
                    (a, a1, a2, a3, a4, a5))
                query = cur.fetchall()

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS']

                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_dirz = ["BELTAS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ"]
                        for item in list_dirz:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(254, 253, 195, 110))

                        list_EQ = ["EQ-GALINUKAS", "EQ-PRILAIKANTIS", "EQ-03-01-00-003 NORD", "EQ-03-01-00-002",
                                   "EQ-IVORE"]
                        for item in list_EQ:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        list_standartiniai = ["HABASIT", "PLASTIKINE IVORE", "UZDENGIMAS", "ALIUMINIS PROFILIS"]
                        for item in list_standartiniai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10, 110))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):
                a = a1 = a2 = a3 = a4 = a5 = a6 = self.searchEntry1.text()

                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT id, pavadinimas, ilgis, kiekis, tvirtinimas, tipas,
                    aprasymas, projektas, komentarai, sandelis, vieta, update_date
                    FROM rolikai WHERE pavadinimas ILIKE '%{}%' OR ilgis ILIKE '%{}%' OR 
                    tvirtinimas ILIKE '%{}%' OR tipas ILIKE '%{}%' OR aprasymas ILIKE '%{}%' 
                    OR aprasymas ILIKE '%{}%' OR projektas ILIKE '%{}%'
                    ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""".format
                    (a, a1, a2, a3, a4, a5, a6))
                query = cur.fetchall()

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['POSUKIS', 'POSUKIS-RM', 'PAPRASTAS', 'RM', 'ASIS', 'SRIEGIS', '2xD5', 'PJ',
                                      'AT10', 'PVC', 'GUMUOTAS']

                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (192, 192, 192, 110), (205, 186, 150, 110), (122, 197, 205, 110),
                                       (155, 205, 155, 110), (122, 197, 205, 110), (219, 219, 219, 110),
                                       (205, 200, 177, 110), (250, 235, 215, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_proj = ["atsargos", "ATSARGOS", "Atsargos"]
                        for item in list_proj:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            else:
                a = a1 = a2 = a3 = a4 = a5 = a6 = self.searchEntry1.text()

                self.pavarosTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.pavarosTable.rowCount())):
                    self.pavarosTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )
                cur = conn.cursor()

                cur.execute(
                    """SELECT id, pavadinimas, gamintojas, tipas, galia, apsisukimai,
                        momentas, tvirtinimas, diametras, kiekis, komentarai, sandelis, vieta, update_date 
                        FROM pavaros WHERE pavadinimas ILIKE '%{}%' OR gamintojas ILIKE '%{}%' 
                        OR tipas ILIKE '%{}%' OR galia ILIKE '%{}%'
                        OR apsisukimai ILIKE '%{}%' OR momentas ILIKE '%{}%'
                        OR tvirtinimas ILIKE '%{}%'
                        ORDER BY tipas ASC, galia ASC, apsisukimai ASC, momentas ASC, tvirtinimas ASC, 
                        diametras ASC""".format
                    (a, a1, a2, a3, a4, a5, a6))
                query = cur.fetchall()

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                for row_date in query:
                    row_number = self.pavarosTable.rowCount()
                    self.pavarosTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['TIESINIS', 'SLIEKINIS', 'ASIS', 'KIAURYME', 'KIAURYME+FLANSAS',
                                      'TECHNOBALT', 'HIDROBALT']

                        list_colors = [(244, 193, 126, 110), (153, 204, 155, 110), (254, 253, 195, 110),
                                       (137, 175, 174, 110), (244, 193, 126, 110), (122, 197, 205, 110),
                                       (250, 235, 215, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                        self.pavarosTable.setItem(row_number, column_number, setitem)

                self.pavarosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def clearSearchEntry(self):
        """search cancel"""
        self.searchEntry1.clear()
        try:
            if self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):
                self.refreshTables()

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):
                self.refreshTables()

            else:
                self.refreshTables()

        except Exception as error:
            print(f"{error}")

    def searchTables2(self, s):
        """search for items and select matched items"""
        if self.treeTable.currentItem() == self.atsargosSelect or \
                self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                self.treeTable.currentItem() == self.atsargosSelect.child(2):

            self.atsarguTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.atsarguTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

        elif self.treeTable.currentItem() == self.rolikaiSelect or \
                self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                self.treeTable.currentItem() == self.rolikaiSelect.child(3):

            self.rolikaiTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.rolikaiTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

        else:
            self.pavarosTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.pavarosTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

    def clearSearchEntry2(self):
        """search cancel"""
        self.searchEntry2.clear()

    def atsargosWriteToFile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def openPicture(self):
        global atsargosId
        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute("""SELECT * FROM atsargos WHERE ID = %s""", (atsargosId,))
            atsargos = c.fetchone()

            self.filename = atsargos[8]
            self.photo = atsargos[9]
            self.filetype = atsargos[10]

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
                path = "bardakas_files/images"
                # Check whether the specified path exists or not
                if not os.path.isdir(path):
                    os.makedirs(path)

                photoPath = "bardakas_files/images/" + self.filename + self.filetype

                if not os.path.isfile(photoPath):
                    self.atsargosWriteToFile(self.photo, photoPath)

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

    def open_rolikai_pvz_(self):
        try:
            self.open_rolikai_pvz_window = open_rolikai_pvz.ImgRolikuPvz()
        except Exception as error:
            print(f"{error}")

    def stelazas_map(self):
        try:
            path = "sandelis_butrimoniu/Map.exe"
            os.startfile(os.path.abspath(os.getcwd()) + "/" + path, 'open')
        except Exception as error:
            print(f"{error}")

    def MainClose(self):
        """exit app"""
        self.destroy()


def main():
    App = QApplication(sys.argv)
    window = MainMenu()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
