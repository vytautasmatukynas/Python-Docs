import time
# import ctypes
import os
import sys
import webbrowser
from pathlib import Path

import pandas
import psycopg2
import requests
import xlsxwriter as xls
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UliPlot.XLSX import auto_adjust_xlsx_column_width
from xlsxwriter import utility

import Bardakas_style_gray
import config
import sheet_generator
from add import add_atsargos, add_combo_uzsakymai, add_stelazas, add_uzsakymai, add_rolikai, add_sanaudos, add_pavaros
from open import open_atkrovimai, open_rolikai_pvz
from scaling import pt_points

params = config.sql_db

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()

InnoSetupID = 'AppId={{DB4A3A4F-7520-4796-BD06-783C3BE4449C}'
__author__ = 'Vytautas Matukynas'
__copyright__ = f'Copyright (C) {year}, Vytautas Matukynas'
__credits__ = ['Vytautas Matukynas']
__license__ = 'Vytautas Matukynas'
__version__ = '4.4'
__maintainer__ = 'Vytautas Matukynas'
__email__ = 'vytautas.matukynas@gmail.com'
__status__ = 'No_End_to_This'
__AppName__ = 'Bardakas'

LINK_TO_VERSION = "https://drive.google.com/uc?export=download&id=11DkCAneKagXkkK8ItfaPyYn0JjnCoZG5"
LINK_TO_FILE = "https://drive.google.com/file/d/1r6hmP3FfwW31Iqwd55nhdqgH8PDYLNRM/view?usp=sharing"


# align for QTable class, DELEGATE ALIGNMENT
class AlignDelegate(QtWidgets.QStyledItemDelegate):

    def initStyleOption(self, option, index):
        """Delegate style to items"""
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


# takes everything from QMainWindow Class
class MainMenu(QMainWindow, pt_points):
    def __init__(self):
        """mainWindow"""
        # inheritance items from QMainWindow
        super().__init__()

        # self.shortcut_delete_uzsakymai = QShortcut(QKeySequence('Delete'), self)
        # self.shortcut_delete_uzsakymai.activated.connect(self.deleteUzsakymas_sh)

        # mainWindow
        self.setWindowTitle("BARDAKAS")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(100 / self.scale_factor), int(100 / self.scale_factor),
                         int(1200 * self.scale_factor), int(720 * self.scale_factor))

        # hide windows bar
        # self.setWindowFlag(Qt.FramelessWindowHint)

        # dont resize window
        # self.setFixedSize(self.size())
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showMaximized()

        self.option = True

        # MainClass functions
        self.show()
        self.UI()

    def UI(self):
        """Functions that starts at start"""
        Bardakas_style_gray.SheetStyle(self)
        self.menubar()
        self.searchWidgets()
        self.default_widgets()
        self.treeTableWidget()
        self.toolBarInside()
        self.tableWidgets()
        self.timeWidget()
        self.progressBar()
        self.layouts()
        self.toolbarTop()
        self.updateInfoOnStart()
        # self.clean_file_folder()

        # if style1.isChecked():
        #     Bardakas_style_blue.SheetStyle(self)
        # elif style2.isChecked():
        #     Bardakas_style_gray.SheetStyle(self)

    # def clean_file_folder(self):
    #     day = datetime.day()
    #     uzsk_dir = os.path.abspath(os.getcwd()) + "/" + 'bardakas_files/uzsakymai_list'
    #     atsrg_dir = os.path.abspath(os.getcwd()) + "/" + 'bardakas_files/uzsakymai_list'
    #     try:
    #         if int(day) == 1:
    #             # Delete dir with all files
    #             shutil.rmtree(uzsk_dir)
    #             shutil.rmtree(atsrg_dir)
    #
    #     except FileNotFoundError as error:
    #         print({error})
    #
    #     finally:
    #         if not os.path.isdir(uzsk_dir):
    #             os.makedirs(uzsk_dir)
    #         if not os.path.isdir(atsrg_dir):
    #             os.makedirs(atsrg_dir)

    def menubar(self):
        """Menu bar"""
        self.menuBarMain = self.menuBar()
        self.menuBarMain.isRightToLeft()

        # File bar
        file = self.menuBarMain.addMenu("File")
        # Submenu bar
        new = QAction("New", self)
        new.triggered.connect(self.addTables)
        new.setShortcut("Ctrl+N")
        file.addAction(new)

        file.addSeparator()
        save = QAction("Save", self)
        save.triggered.connect(self.save)
        save.setShortcut("Ctrl+S")
        save.setIcon(QIcon("icons/save.png"))
        file.addAction(save)
        saveAs = QAction("Save As", self)
        saveAs.triggered.connect(self.saveAs)
        saveAs.setShortcut("Alt+S")
        saveAs.setIcon(QIcon("icons/saveas.png"))
        file.addAction(saveAs)
        file.addSeparator()
        delete = QAction("Delete", self)
        delete.triggered.connect(self.deleteTables)
        delete.setIcon(QIcon("icons/delete.png"))
        file.addAction(delete)
        file.addSeparator()
        refresh = QAction("Refresh", self)
        refresh.triggered.connect(self.refreshTables)
        refresh.setShortcut("F5")
        refresh.setIcon(QIcon("icons/refresh.png"))
        file.addAction(refresh)
        file.addSeparator()
        print = QAction("Print", self)
        print.triggered.connect(self.handlePreview)
        print.setShortcut("Ctrl+P")
        print.setIcon(QIcon("icons/print.png"))
        file.addAction(print)
        file.addSeparator()
        exit = QAction("Exit", self)
        exit.triggered.connect(self.MainClose)
        exit.setShortcut("Ctrl+Q")
        exit.setIcon(QIcon("icons/exit.png"))
        file.addAction(exit)

        # Open bar
        Open = self.menuBarMain.addMenu("Open")
        StelazasMap = QAction("Butrimonių sandėlis", self)
        StelazasMap.triggered.connect(self.stelazas_map)
        StelazasMap.setShortcut("Ctrl+Alt+M")
        StelazasMap.setIcon(QIcon("icons/plan.png"))
        Open.addAction(StelazasMap)
        Open.addSeparator()
        openAtkrovimaiMmenu = QAction("Suruošti užsakymai", self)
        openAtkrovimaiMmenu.triggered.connect(self.openAtkrovimai)
        openAtkrovimaiMmenu.setIcon(QIcon("icons/truck.png"))
        openAtkrovimaiMmenu.setShortcut("Ctrl+Alt+A")
        Open.addAction(openAtkrovimaiMmenu)
        Open.addSeparator()
        openVazGen = QAction("Palečių generavimas", self)
        openVazGen.triggered.connect(self.openVaztarasciai)
        openVazGen.setIcon(QIcon("icons/paper.png"))
        openVazGen.setShortcut("Ctrl+Alt+P")
        Open.addAction(openVazGen)

        # Setting bar
        Settings = self.menuBarMain.addMenu("Settings")

        style = Settings.addMenu("Style")
        style.setIcon(QIcon("icons/design.png"))

        group_1 = QActionGroup(style)

        # style1 = QAction("Big BLUE... Whale", self)
        # style1.setCheckable(True)
        style2 = QAction("Gandalf the Grey", self)
        style2.setCheckable(True)
        style2.setChecked(True)
        # Style.addAction(style1)
        style.addAction(style2)

        # Group.addAction(style1)
        group_1.addAction(style2)

        # Check only one item in GroupBox
        group_1.setExclusive(True)

        Settings.addSeparator()

        combo_box = Settings.addMenu("Edit Combo-Box")
        group_2 = QActionGroup(combo_box)

        uzsakymai_combo = QAction("Uzsakymai", self)
        uzsakymai_combo.triggered.connect(self.add_combo_uzsakymai)

        combo_box.addAction(uzsakymai_combo)

        group_2.addAction(uzsakymai_combo)

        # Help bar
        help = self.menuBarMain.addMenu("Help")

        # Submenu bar
        UpdateApp = QAction("Check for Updates", self)
        UpdateApp.setIcon(QIcon("icons/update.png"))
        UpdateApp.triggered.connect(self.updateInfo)
        help.addAction(UpdateApp)
        help.addSeparator()
        Info = QAction("About", self)
        Info.setIcon(QIcon("icons/info.png"))
        Info.triggered.connect(self.helpinfo)
        help.addAction(Info)

    def updateInfoOnStart(self):
        """version check"""
        try:
            # Version file link
            response = requests.get(
                f'{LINK_TO_VERSION}')
            data = response.text

            if float(data) > float(__version__):
                # self.msg = QMessageBox.information(self, "UPDATE", "Bardakas 1.3.0")
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    # Donwload file link
                    webbrowser.open_new_tab(
                        f'{LINK_TO_FILE}')

                    self.MainClose()

                else:
                    pass

            else:
                pass

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def updateInfo(self):
        try:
            response = requests.get(
                f'{LINK_TO_VERSION}')
            data = response.text

            if float(data) > float(__version__):
                # self.msg = QMessageBox.information(self, "UPDATE", "Bardakas 1.3.0")
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    webbrowser.open_new_tab(
                        f'{LINK_TO_FILE}')

                    self.MainClose()

                else:
                    pass

            else:
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('No updates, version {}.'.format(__version__))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

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

    def tableWidgets(self):
        """Tables"""
        # UZSAKYMAI TABLE
        self.emptyTable = QTableWidget()
        self.emptyTable.setColumnCount(0)
        if self.emptyTable:
            self.treeitems()

        self.uzsakymuTable = QTableWidget()
        self.uzsakymuTable.setColumnCount(11)
        self.uzsakymuTable.setColumnHidden(0, True)
        self.uzsakymuTable.setColumnHidden(8, True)
        # self.uzsakymuTable.setColumnHidden(9, True)
        self.uzsakymuTable.setSortingEnabled(True)
        self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

        # for number in [1, 2, 3, 4, 5, 6, 9, 10]:
        #     self.uzsakymuTable.setColumnWidth(number, 150)

        headers_uzsk = ["ID", "ĮMONĖ", "KONSTRUKTORIUS", "PROJEKTAS", "PAVADINIMAS", "TERMINAS",
                        "STATUSAS", "KOMENTARAI", "APLANKAS", "KOMPONENTAI", "ATNAUJINTA"]

        for column_number in range(0, len(headers_uzsk)):
            while column_number < len(headers_uzsk):
                header_name = headers_uzsk[column_number]
                self.uzsakymuTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.uzsakymuTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.uzsakymuTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.uzsakymuTable.horizontalHeader().setHighlightSections(False)
        self.uzsakymuTable.horizontalHeader().setDisabled(True)
        self.uzsakymuTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.uzsakymuTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.uzsakymuTable.pressed.connect(self.uzsakymai_select)
        self.uzsakymuTable.doubleClicked.connect(self.updateUzsakymai)

        # ATSARGOS TABLE
        self.atsarguTable = QTableWidget()
        self.atsarguTable.setColumnCount(10)
        self.atsarguTable.setSortingEnabled(True)
        self.atsarguTable.setColumnHidden(0, True)
        # self.atsarguTable.setColumnHidden(6, True)
        self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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

        self.atsarguTable.pressed.connect(self.atsargos_select)
        self.atsarguTable.doubleClicked.connect(self.updateAtsargos)

        # ROLIKAI TABLE
        self.rolikaiTable = QTableWidget()
        self.rolikaiTable.setColumnCount(12)
        self.rolikaiTable.setColumnHidden(0, True)
        self.rolikaiTable.setSortingEnabled(True)
        self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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

        self.rolikaiTable.pressed.connect(self.rolikai_select)
        self.rolikaiTable.doubleClicked.connect(self.updateRolikai)

        # PAVAROS TABLE
        self.pavarosTable = QTableWidget()
        self.pavarosTable.setColumnCount(14)
        self.pavarosTable.setColumnHidden(0, True)
        self.pavarosTable.setSortingEnabled(True)
        self.pavarosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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

        self.pavarosTable.pressed.connect(self.pavaros_select)
        self.pavarosTable.doubleClicked.connect(self.updatePavaros)

        # STELAZAS TABLE
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(7)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        self.stelazasTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

        headers_stel = ["ID", "PAVADINIMAS", "PROJEKTAS", "SANDĖLIS", "VIETA", "KOMENTARAI", "ATNAUJINTA"]

        for column_number in range(0, len(headers_stel)):
            while column_number < len(headers_stel):
                header_name = headers_stel[column_number]
                self.stelazasTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setHighlightSections(False)
        self.stelazasTable.horizontalHeader().setDisabled(True)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.stelazasTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.stelazasTable.pressed.connect(self.stelazai_select)
        self.stelazasTable.doubleClicked.connect(self.updateStelazas)

        # SANAUNOS TABLE
        self.sanaudosTable = QTableWidget()
        self.sanaudosTable.setColumnCount(8)
        self.sanaudosTable.setSortingEnabled(True)
        self.sanaudosTable.setColumnHidden(0, True)
        self.sanaudosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

        headers_san = ["ID", "PAVADINIMAS", "PROJEKTAS", "KIEKIS", "VIENETAI", "KOMENTARAI", "METAI", "ATNAUJINTA"]

        for column_number in range(0, len(headers_san)):
            while column_number < len(headers_san):
                header_name = headers_san[column_number]
                self.sanaudosTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.sanaudosTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.sanaudosTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.sanaudosTable.horizontalHeader().setHighlightSections(False)
        self.sanaudosTable.horizontalHeader().setDisabled(True)
        self.sanaudosTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.sanaudosTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.sanaudosTable.pressed.connect(self.sanaudos_select)
        self.sanaudosTable.doubleClicked.connect(self.updateSanaudos)

        ########## Align delegate Class
        delegate = AlignDelegate()

        # for column
        for number in [1, 2, 3, 4, 5, 6, 9, 10]:
            self.uzsakymuTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 5, 6, 8, 9]:
            self.atsarguTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]:
            self.rolikaiTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13]:
            self.pavarosTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 6]:
            self.stelazasTable.setItemDelegateForColumn(number, delegate)

        for number in [1, 2, 3, 4, 6, 7]:
            self.sanaudosTable.setItemDelegateForColumn(number, delegate)

        # for all columns
        # self.uzsakymuTable.setItemDelegate(delegate)
        # self.atsarguTable.setItemDelegate(delegate)
        # self.sanaudosTable.setItemDelegate(delegate)
        # self.stelazasTable.setItemDelegate(delegate)
        # self.rolikaiTable.setItemDelegate(delegate)

    def searchWidgets(self):
        self.cancelButton1 = QPushButton("CANCEL")
        self.cancelButton1.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelButton1.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.cancelButton1.clicked.connect(self.clearSearchEntry)
        self.cancelButton1.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.searchButton1 = QPushButton("SEARCH")
        self.searchButton1.setFixedHeight(self.BUTTON_HEIGHT)
        self.searchButton1.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.searchButton1.clicked.connect(self.searchTables)
        self.searchButton1.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.searchEntry1 = QLineEdit()
        self.searchEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.searchEntry1.setPlaceholderText('Filter table...')

        self.cancelButton2 = QPushButton("CANCEL")
        self.cancelButton2.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelButton2.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.cancelButton2.clicked.connect(self.clearSearchEntry2)
        self.cancelButton2.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.searchEntry2 = QLineEdit()
        self.searchEntry2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.searchEntry2.setPlaceholderText('Select table items...')
        self.searchEntry2.textChanged.connect(self.searchTables2)

    def default_widgets(self):
        self.sort_check = QCheckBox("Enable Table Sorting")
        self.sort_check.clicked.connect(self.enable_sorting)

        self.expand_button = QPushButton()
        self.expand_button.setIcon(QIcon("icons/to_left.png"))
        self.expand_button.setIconSize(QSize(int(19 * self.scale_factor), int(19 * self.scale_factor)))
        self.expand_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.expand_button.setFixedWidth(int(20 * self.scale_factor))
        self.expand_button.clicked.connect(self.treeTableHideShow)

    def treeTableWidget(self):
        """Treeview table"""
        self.treeTable = QTreeWidget()
        self.treeTable.setAnimated(True)
        self.treeTable.setHeaderHidden(True)
        self.treeTable.setColumnCount(1)
        self.treeTable.setFixedWidth(self.TREE_TABLE_WIDTH)
        self.treeTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.treeTable.header().setStretchLastSection(False)
        # self.treeTable.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def treeitems(self):
        self.uzsakymaiSelect = QTreeWidgetItem(self.treeTable, ["Užsakymai"])
        self.uzsakymaiSelect.setExpanded(True)
        self.atsargosSelect = QTreeWidgetItem(self.treeTable, ["Atsargos"])
        self.atsargosSelect.setExpanded(True)
        self.rolikaiSelect = QTreeWidgetItem(self.treeTable, ["Rolikų atsargos"])
        self.rolikaiSelect.setExpanded(True)
        self.pavarosSelect = QTreeWidgetItem(self.treeTable, ["Pavarų atsargos"])
        self.pavarosSelect.setExpanded(True)
        self.stelazasSelect = QTreeWidgetItem(self.treeTable, ["Sandėliai"])
        self.sanaudosSelect = QTreeWidgetItem(self.treeTable, ["Sąnaudos"])

        self.uzsakymaiSelect1 = ["Pagaminta", "Gamina", "Brokuota"]
        for item1 in self.uzsakymaiSelect1:
            self.uzsakymaiSelect.addChild(QTreeWidgetItem([item1]))
        self.atsargosSelect1 = ["EQ", "Komponentai", "Pneumo"]
        for item2 in self.atsargosSelect1:
            self.atsargosSelect.addChild(QTreeWidgetItem([item2]))
        self.rolikaiSelect1 = ["Paprastas", "RM", "Posukis", "Posukis-RM"]
        for item3 in self.rolikaiSelect1:
            self.rolikaiSelect.addChild(QTreeWidgetItem([item3]))

        ######## pavarosTable child treeview headers ########
        con = psycopg2.connect(
            **params
        )
        cur = con.cursor()

        cur.execute("""SELECT galia FROM pavaros""")
        query = cur.fetchall()

        con.close()

        self.pavaros_get_headers = [i[0] + " kW" for i in query]
        self.pavaros_clean_get_header = set(self.pavaros_get_headers)
        self.pavaros_headers = list(self.pavaros_clean_get_header)
        self.pavaros_headers.sort()

        self.pavarosSelect1 = self.pavaros_headers
        for item4 in self.pavarosSelect1:
            self.pavarosSelect.addChild(QTreeWidgetItem([item4]))

        self.treeTable.clicked.connect(self.listTables)

    def toolBarInside(self):
        """Toolbar inside table"""
        self.tb2 = QtWidgets.QToolBar("Action tb")
        # self.addToolBar(QtCore.Qt.BottomToolBarArea, self.tb2)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        # self.tb2.setMovable(False)
        self.tb2.setIconSize(QtCore.QSize(self.IN_TB_ICON_HEIGHT, self.IN_TB_ICON_WIDTH))

        self.add_tb = QAction(QIcon("icons/add.png"), "Add", self)
        self.tb2.addAction(self.add_tb)
        self.add_tb.triggered.connect(self.addTables)

        self.delete_tb = QAction(QIcon("icons/delete.png"), "Delete", self)
        self.tb2.addAction(self.delete_tb)
        self.delete_tb.triggered.connect(self.deleteTables)

        self.tb2.addSeparator()

        self.refresh_tb = QAction(QIcon("icons/refresh.png"), "Refresh", self)
        self.tb2.addAction(self.refresh_tb)
        self.refresh_tb.triggered.connect(self.refreshTables)

        self.tb2.addSeparator()

        self.save_tb = QAction(QIcon("icons/save.png"), "Save", self)
        self.tb2.addAction(self.save_tb)
        self.save_tb.triggered.connect(self.save)

        self.saveAs_tb = QAction(QIcon("icons/saveas.png"), "Save As...", self)
        self.tb2.addAction(self.saveAs_tb)
        self.saveAs_tb.triggered.connect(self.saveAs)

    def toolbarTop(self):
        """toolbar buttons"""
        self.tb1 = self.addToolBar("Open tb")
        self.tb1.setMovable(False)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb1.setIconSize(QtCore.QSize(self.TOP_TB_ICON_HEIGHT, self.TOP_TB_ICON_WIDTH))

        self.openStelazai = QAction(QIcon("icons/plan.png"), "Butrimonių sandėlis", self)
        self.tb1.addAction(self.openStelazai)
        self.openStelazai.triggered.connect(self.stelazas_map)

        self.tb1.addSeparator()

        self.openAtkrovimaitb = QAction(QIcon("icons/truck.png"), "Suruošti užsakymai", self)
        self.tb1.addAction(self.openAtkrovimaitb)
        self.openAtkrovimaitb.triggered.connect(self.openAtkrovimai)

        self.tb1.addSeparator()

        self.openVazGen = QAction(QIcon("icons/paper.png"), "Excel Sheet Generator", self)
        self.tb1.addAction(self.openVazGen)
        self.openVazGen.triggered.connect(self.openVaztarasciai)

        self.tb1.addSeparator()

    def timeWidget(self):
        # Timer
        self.Timer = QLabel()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)  # update every second

        self.showTime()

    def showTime(self):
        self.currentTime = QTime.currentTime()
        self.displayTxt = self.currentTime.toString('hh:mm:ss')
        self.Timer.setText(self.displayTxt)

    def progressBar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(self.PROGRESS_WIDTH)
        self.progress_bar.setFixedHeight(self.PROGRESS_HEIGHT)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)

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

        # Right side tb
        self.tbLayout_table.addWidget(self.tb2)

        # Right side tables
        self.tableRightLayout.addWidget(self.uzsakymuTable)
        self.tableRightLayout.addWidget(self.atsarguTable)
        self.tableRightLayout.addWidget(self.rolikaiTable)
        self.tableRightLayout.addWidget(self.pavarosTable)
        self.tableRightLayout.addWidget(self.stelazasTable)
        self.tableRightLayout.addWidget(self.sanaudosTable)
        self.tableRightLayout.addWidget(self.emptyTable)
        self.tableRightLayout.setCurrentIndex(6)

        # Right layout with search
        self.mainRightLayout.addLayout(self.searchLayout_table, 1)
        self.mainRightLayout.addLayout(self.tbLayout_table, 1)
        self.mainRightLayout.addLayout(self.tableRightLayout, 97)

        # Bottom layout
        self.bottomLayout.addWidget(QLabel(f"Bardakas..."), 98, alignment=Qt.AlignLeft)
        # self.bottomLayout.addWidget(self.progress_bar, 12, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(QLabel(f"Current date/time: {datetime.toPyDate()}"), 1, alignment=Qt.AlignRight)
        self.bottomLayout.addWidget(self.Timer, 1, alignment=Qt.AlignRight)

        # Main layout
        self.middleLayout.addLayout(self.treeLeftLayout)
        self.middleLayout.addWidget(self.expand_button)
        self.middleLayout.addLayout(self.mainRightLayout)
        # self.middleLayout.addStretch()

        self.mainLayout.addLayout(self.searchLayout, 1)
        self.mainLayout.addLayout(self.middleLayout, 98)
        self.mainLayout.addLayout(self.bottomLayout, 1)

        # Central_widget to view widgets
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.central_widget)

    def enable_sorting(self):
        if self.sort_check.isChecked():
            self.uzsakymuTable.horizontalHeader().setDisabled(False)
            self.atsarguTable.horizontalHeader().setDisabled(False)
            self.sanaudosTable.horizontalHeader().setDisabled(False)
            self.stelazasTable.horizontalHeader().setDisabled(False)
            self.rolikaiTable.horizontalHeader().setDisabled(False)
            self.pavarosTable.horizontalHeader().setDisabled(False)

        else:
            self.uzsakymuTable.horizontalHeader().setDisabled(True)
            self.atsarguTable.horizontalHeader().setDisabled(True)
            self.sanaudosTable.horizontalHeader().setDisabled(True)
            self.stelazasTable.horizontalHeader().setDisabled(True)
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

    def uzsakymai_select(self):
        global uzsakymaiId

        self.listUzsakymai = []
        self.num = 0
        self.listUzsakymai.append(self.uzsakymuTable.item(self.uzsakymuTable.currentRow(), self.num).text())

        uzsakymaiId = self.listUzsakymai[0]

    def atsargos_select(self):
        global atsargosId

        self.listAtsargos = []
        self.num = 0
        self.listAtsargos.append(self.atsarguTable.item(self.atsarguTable.currentRow(), self.num).text())

        atsargosId = self.listAtsargos[0]

    def rolikai_select(self):
        global rolikaiId

        self.listRolikai = []
        self.num = 0
        self.listRolikai.append(self.rolikaiTable.item(self.rolikaiTable.currentRow(), self.num).text())

        rolikaiId = self.listRolikai[0]

    def pavaros_select(self):
        global pavarosId

        self.listPavaros = []
        self.num = 0
        self.listPavaros.append(self.pavarosTable.item(self.pavarosTable.currentRow(), self.num).text())

        pavarosId = self.listPavaros[0]

    def stelazai_select(self):
        global stelazasId

        self.listStelazai = []
        self.num = 0
        self.listStelazai.append(self.stelazasTable.item(self.stelazasTable.currentRow(), self.num).text())

        stelazasId = self.listStelazai[0]

    def sanaudos_select(self):
        global sanaudosId

        self.listSanaudos = []
        self.num = 0
        self.listSanaudos.append(self.sanaudosTable.item(self.sanaudosTable.currentRow(), self.num).text())

        sanaudosId = self.listSanaudos[0]

    def contextMenuEvent(self, event):
        """Right mouse button select"""
        if self.uzsakymuTable.underMouse():
            global uzsakymaiId

            # Left mouse button table
            contextMenu = QMenu(self)

            openBreziniai = contextMenu.addAction("Brėžiniai")
            openBreziniai.triggered.connect(self.openFolder)
            openBreziniai.setShortcut("Alt+D")
            openBreziniai.setIcon(QIcon("icons/drawings.png"))
            contextMenu.addSeparator()
            openSarasas = contextMenu.addAction("Komponentai")
            openSarasas.triggered.connect(self.openFile)
            openSarasas.setShortcut("Alt+L")
            openSarasas.setIcon(QIcon("icons/files.png"))
            contextMenu.addSeparator()
            openBrokas = contextMenu.addAction("Brokas/Trūkumas")
            openBrokas.triggered.connect(self.openBrokasEntry)
            openBrokas.setShortcut("Alt+B")
            openBrokas.setIcon(QIcon("icons/error.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_uzsakymai)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteBreziniai = contextMenu.addAction("Delete")
            deleteBreziniai.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.atsarguTable.underMouse():
            global atsargosId

            contextMenu = QMenu(self)
            openPicture = contextMenu.addAction("Nuotrauka")
            openPicture.triggered.connect(self.openPicture)
            openPicture.setShortcut("Alt+N")
            openPicture.setIcon(QIcon("icons/image.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_atsargos)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            Refresh2.setShortcut("F5")
            contextMenu.addSeparator()
            deleteAtsargos = contextMenu.addAction("Delete")
            deleteAtsargos.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.rolikaiTable.underMouse():
            global rolikaiId

            contextMenu = QMenu(self)

            roliku_pvz = contextMenu.addAction("Rolikų pvz.")
            roliku_pvz.triggered.connect(self.open_rolikai_pvz_)
            roliku_pvz.setIcon(QIcon("icons/rolikai.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_rolikai)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteRolikai = contextMenu.addAction("Delete")
            deleteRolikai.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.pavarosTable.underMouse():
            global pavarosId

            contextMenu = QMenu(self)

            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_pavaros)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteRolikai = contextMenu.addAction("Delete")
            deleteRolikai.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.stelazasTable.underMouse():
            global stelazasId

            contextMenu = QMenu(self)

            map2 = contextMenu.addAction("Butrimonių sandėlis")
            map2.triggered.connect(self.stelazas_map)
            map2.setShortcut("Alt+B")
            map2.setIcon(QIcon("icons/plan.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_stelazai)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteStelazas = contextMenu.addAction("Delete")
            deleteStelazas.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.sanaudosTable.underMouse():
            global sanaudosId

            contextMenu = QMenu(self)

            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_sanaudos)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refreshTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteSanaudos = contextMenu.addAction("Delete")
            deleteSanaudos.triggered.connect(self.deleteTables)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.treeTable.underMouse():
            contextMenu = QMenu(self)
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.refresh_tree_items)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def refresh_tree_pavaros_items(self):
        self.treeTable.clear()
        self.treeitems()
        self.treeTable.setCurrentItem(self.pavarosSelect)
        self.pavarosSelect.setExpanded(True)

    def refresh_tree_items(self):
        self.treeTable.clear()
        self.treeitems()
        self.pavarosSelect.setExpanded(True)

    def add_combo_uzsakymai(self):
        self.edit_combobox = add_combo_uzsakymai.AddCombo()
        self.edit_combobox.exec_()

    def add_uzsakymai(self):
        try:
            self.newUzsakymai = add_uzsakymai.AddUzsakymas()
            # Refresh table after executing QDialog .exec_
            self.newUzsakymai.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def add_atsargos(self):
        try:
            self.newStelazas = add_atsargos.AddAtsargos()
            self.newStelazas.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def add_rolikai(self):
        try:
            self.newRolikai = add_rolikai.AddRolikai()
            self.newRolikai.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def add_pavaros(self):
        try:
            self.newPavaros = add_pavaros.AddPavaros()
            self.newPavaros.exec_()
            self.displayPavaros()
            self.refresh_tree_pavaros_items()
        except Exception as error:
            print(f"{error}")

    def add_stelazai(self):
        try:
            self.newStelazas = add_stelazas.AddStelazas()
            self.newStelazas.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def add_sanaudos(self):
        try:
            self.newSanaudos = add_sanaudos.AddSanaudos()
            self.newSanaudos.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def addTables(self):
        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):

                self.add_uzsakymai()

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):

                self.add_atsargos()

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):

                self.add_rolikai()

            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.add_stelazai()

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.add_sanaudos()

            else:
                self.add_pavaros()
        except:
            pass

    def displayUzsakymai(self):
        """Shows SQL table in QTableWidget"""
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
            # Cleans table
            self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

            for i in reversed(range(self.uzsakymuTable.rowCount())):
                self.uzsakymuTable.removeRow(i)

            # Connect to SQL table
            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()

            cur.execute(
                """SELECT id, imone, konstruktorius, projektas, pav_uzsakymai,
                terminas, statusas, komentarai, breziniai, sarasas, update_date,
                filename, filetype, filedir FROM uzsakymai 
                ORDER BY statusas ASC, terminas ASC, projektas ASC, konstruktorius ASC, 
                pav_uzsakymai ASC, imone ASC""")
            query = cur.fetchall()

            # Sort table values and adds to table, change color of some values
            for row_date in query:
                row_number = self.uzsakymuTable.rowCount()
                self.uzsakymuTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    # print(row_number, column_number, data)

                    # check current date and table entry, if nor equal or bigger make it red
                    listdata = []

                    if column_number == 5:
                        listdata.append(str(data))
                        if listdata[0] == "+" or listdata[0] == "-":
                            listdata.pop()

                    for i in listdata:
                        if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                            None
                        elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                or int(i[0:4]) < int(date[0:4]):
                            setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                            # setitem.setForeground(QtGui.QColor(255, 255, 255))

                    projektas_query = [i[3] for i in query]
                    projektas_isvalymas = set(projektas_query)
                    projektas_list = list(projektas_isvalymas)
                    projektas_list.sort()

                    projektas_list_colors = [
                        (98, 184, 207, 110), (142, 162, 208, 110), (205, 125, 91, 110), (136, 175, 179, 110),
                        (119, 187, 165, 110), (119, 187, 165, 110), (142, 162, 208, 110), (142, 162, 208, 110),
                        (141, 176, 181, 110), (141, 176, 181, 110), (246, 202, 168, 110), (159, 159, 159, 110),
                        (203, 231, 240, 110), (160, 196, 201, 110), (224, 148, 120, 110), (165, 200, 203, 110),
                        (162, 212, 189, 110), (218, 187, 213, 110), (205, 216, 217, 110), (135, 184, 209, 110),
                        (149, 192, 216, 110), (131, 165, 202, 110), (99, 143, 172, 110), (74, 126, 160, 110),
                        (47, 90, 129, 110), (29, 65, 106, 110), (13, 42, 84, 110), (64, 135, 190, 110),
                        (81, 138, 165, 110), (166, 190, 208, 110)
                    ]

                    for count_num in range(0, len(projektas_list)):
                        while count_num < len(projektas_list):
                            if data == projektas_list[count_num] and data != None and data != "":
                                setitem.setBackground(QtGui.QColor(*projektas_list_colors[count_num]))
                            count_num += 1

                    list_names = ['PAGAMINTA', 'BROKUOTA', 'MODESTAS', 'JULIJUS', 'JULIUS', 'VAIDAS',
                                  'MINDAUGAS', 'HITECH']

                    list_colors = [(0, 204, 0, 110), (240, 128, 128, 110), (244, 193, 126, 110),
                                   (153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                   (86, 172, 186, 110), (50, 168, 84, 110)]

                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    list_lazeris = ["SRS", "METACO", "AUTOSABINA"]
                    for item in list_lazeris:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(255, 228, 181, 110))

                    list_komponentai = ['ALBASERVIS', 'DAGMITA', 'IGNERA', 'KRC RATUKAI', 'WURTH', 'DRUTSRAIGTIS',
                                        'JOLDITA', 'SERFAS', 'BL TECH', 'INTEROLL', 'TECHNOBALT', "HIDROBALT"]

                    for item in list_komponentai:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(176, 196, 222, 110))

                    list_tekinimas = ['M.J.', 'MITRONAS', 'KAVERA', 'KAGNETA']
                    for item in list_tekinimas:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(188, 143, 143, 110))

                    list_gumavimas = ['METGA', 'KASTAGA', 'BALTAS VEJAS']
                    for item in list_gumavimas:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(137, 175, 174, 110))

                    self.uzsakymuTable.setItem(row_number, column_number, setitem)

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            # Edit column cell disable
            self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def displayAtsargos(self):
        try:
            self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
            for i in reversed(range(self.atsarguTable.rowCount())):
                self.atsarguTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()
            cur.execute("""SELECT id, pavadinimas, konfig, sandelis, vieta, kiekis, mat_pav, komentaras,
            nuotrauka, update_date, filename, filetype, filedir FROM atsargos ORDER BY pavadinimas ASC,
            konfig ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.atsarguTable.rowCount()
                self.atsarguTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                  'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS', 'GUOLIAVIETE',
                                  'KAMSTIS']
                    list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                   (255, 153, 51, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                   (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                   (188, 143, 143, 110), (255, 229, 204, 110), (192, 192, 192, 110)]
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
            self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
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
            self.pavarosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
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

    def displayStelazas(self):
        try:
            self.stelazasTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
            for i in reversed(range(self.stelazasTable.rowCount())):
                self.stelazasTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()
            cur.execute("""SELECT * FROM stelazas ORDER BY vieta ASC, projektas ASC, sandelis ASC, pavadinimas ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.stelazasTable.rowCount()
                self.stelazasTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['ROLIKAI', 'VARIKLIAI', 'DETALES IR KT.', 'FESTO', 'ATSARGOS', 'BUTRIMONIU',
                                  'KONTORA']

                    list_colors = [(86, 172, 186, 110), (244, 193, 126, 110), (153, 204, 155, 110),
                                   (254, 253, 195, 110), (176, 196, 222, 110), (176, 196, 222, 110),
                                   (176, 196, 222, 110)]

                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    self.stelazasTable.setItem(row_number, column_number, setitem)

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

    def displaySanaudos(self):
        # Get current date
        datetime = QDate.currentDate()
        y = datetime.year()

        try:
            self.sanaudosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
            for i in reversed(range(self.sanaudosTable.rowCount())):
                self.sanaudosTable.removeRow(i)

            con = psycopg2.connect(
                **params
            )

            cur = con.cursor()
            cur.execute("""SELECT * FROM sanaudos ORDER BY metai DESC, projektas ASC, pavadinimas ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.sanaudosTable.rowCount()
                self.sanaudosTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    list_names = ['HABASIT', 'PROFILIAI', 'UZDENGIMAI']

                    list_colors = [(153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                   (176, 196, 222, 110)]

                    for count_num in range(0, len(list_names)):
                        while count_num < len(list_names):
                            if data == list_names[count_num]:
                                setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                            count_num += 1

                    list_standartiniai = ["PRILAIKANTIS", "GALINUKAS", "SKRIEMULYS",
                                          "SKRIEMULIO ASIS"]
                    for item in list_standartiniai:
                        if data == item:
                            setitem.setBackground(QtGui.QColor(244, 193, 126, 110))

                    if data == "ROLIKAI":
                        setitem.setBackground(QtGui.QColor(230, 230, 250, 110))

                    if data == 'VARIKLIAI':
                        setitem.setBackground(QtGui.QColor(86, 172, 186, 110))

                    if data == 'PLASTIKINES IVORES':
                        setitem.setBackground(QtGui.QColor(240, 128, 128, 110))

                    self.sanaudosTable.setItem(row_number, column_number, setitem)

                    # old date color
                    listdata = []
                    if column_number == 6:
                        listdata.append(str(data))
                        for i in listdata:
                            if int(i[0:4]) < int(y):
                                setitem.setBackground(QtGui.QColor(0, 204, 0, 110))

            row_count = cur.rowcount

            for i in range(0, row_count):
                value = 100

                self.progress_bar.setRange(0, value)

                if value > 50:
                    self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                progress_val = int(((i + 1) / row_count) * 100)
                self.progress_bar.setValue(progress_val)

            self.sanaudosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

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
            if self.treeTable.currentItem() == self.uzsakymaiSelect:
                self.tableRightLayout.setCurrentIndex(0)
                self.displayUzsakymai()

            elif self.treeTable.currentItem() == self.atsargosSelect:
                self.tableRightLayout.setCurrentIndex(1)
                self.displayAtsargos()

            elif self.treeTable.currentItem() == self.rolikaiSelect:
                self.tableRightLayout.setCurrentIndex(2)
                self.displayRolikai()

            elif self.treeTable.currentItem() == self.pavarosSelect:
                self.tableRightLayout.setCurrentIndex(3)
                self.displayPavaros()

            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.tableRightLayout.setCurrentIndex(4)
                self.displayStelazas()

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.tableRightLayout.setCurrentIndex(5)
                self.displaySanaudos()

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(0):
                self.tableRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT  id, imone, konstruktorius, projektas, pav_uzsakymai,
                    terminas, statusas, komentarai, breziniai, sarasas, update_date,
                    filename, filetype, filedir  FROM uzsakymai 
                    WHERE statusas = 'PAGAMINTA' 
                    ORDER BY terminas ASC, projektas ASC, konstruktorius ASC, pav_uzsakymai ASC, imone ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.uzsakymuTable.rowCount()
                    self.uzsakymuTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))
                        # check current date and table entry, if nor equal or more make it red
                        listdata = []

                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()

                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # projektas_query = [i[3] for i in query]
                        # projektas_isvalymas = set(projektas_query)
                        # projektas_list = list(projektas_isvalymas)
                        # projektas_list.sort()
                        #
                        # projektas_list_colors = [
                        #                          (176, 196, 222, 110), (244, 193, 126, 110), (188, 143, 143, 110),
                        #                          (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                        #                          (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                        #                          (230, 230, 250), (255, 250, 240), (122, 197, 205, 110)
                        #                         ]
                        #
                        # for count_num in range(0, len(projektas_list)):
                        #     while count_num < len(projektas_list):
                        #         if data == projektas_list[count_num] and data != None and data != "":
                        #             setitem.setBackground(QtGui.QColor(*projektas_list_colors[count_num]))
                        #         count_num += 1

                        list_names = ['PAGAMINTA', 'BROKUOTA', 'MODESTAS', 'JULIJUS', 'JULIUS', 'VAIDAS',
                                      'MINDAUGAS', 'HITECH']

                        list_colors = [(0, 204, 0, 110), (240, 128, 128, 110), (244, 193, 126, 110),
                                       (153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                       (86, 172, 186, 110), (50, 168, 84, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_lazeris = ["SRS", "METACO", "AUTOSABINA"]
                        for item in list_lazeris:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(255, 228, 181, 110))

                        list_komponentai = ['ALBASERVIS', 'DAGMITA', 'IGNERA', 'KRC RATUKAI', 'WURTH', 'DRUTSRAIGTIS',
                                            'JOLDITA', 'SERFAS', 'BL TECH', 'INTEROLL', 'TECHNOBALT', "HIDROBALT"]
                        for item in list_komponentai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(176, 196, 222, 110))

                        list_tekinimas = ['M.J.', 'MITRONAS', 'KAVERA', 'KAGNETA']
                        for item in list_tekinimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(188, 143, 143, 110))

                        list_gumavimas = ['METGA', 'KASTAGA', 'BALTAS VEJAS']
                        for item in list_gumavimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(137, 175, 174, 110))

                        if data == 'HITECH':
                            setitem.setBackground(QtGui.QColor(50, 168, 84, 110))

                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(1):
                self.tableRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT  id, imone, konstruktorius, projektas, pav_uzsakymai,
                    terminas, statusas, komentarai, breziniai, sarasas, update_date,
                    filename, filetype, filedir  FROM uzsakymai 
                    WHERE statusas = 'GAMINA' 
                    ORDER BY terminas ASC, projektas ASC, konstruktorius ASC, pav_uzsakymai ASC, imone ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.uzsakymuTable.rowCount()
                    self.uzsakymuTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))
                        # check current date and table entry, if nor equal or more make it red
                        listdata = []

                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()

                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # projektas_query = [i[3] for i in query]
                        # projektas_isvalymas = set(projektas_query)
                        # projektas_list = list(projektas_isvalymas)
                        # projektas_list.sort()
                        #
                        # projektas_list_colors = [
                        #                          (176, 196, 222, 110), (244, 193, 126, 110), (188, 143, 143, 110),
                        #                          (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                        #                          (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                        #                          (230, 230, 250), (255, 250, 240), (122, 197, 205, 110)
                        #                         ]
                        #
                        # for count_num in range(0, len(projektas_list)):
                        #     while count_num < len(projektas_list):
                        #         if data == projektas_list[count_num] and data != None and data != "":
                        #             setitem.setBackground(QtGui.QColor(*projektas_list_colors[count_num]))
                        #         count_num += 1

                        list_names = ['PAGAMINTA', 'BROKUOTA', 'MODESTAS', 'JULIJUS', 'JULIUS', 'VAIDAS',
                                      'MINDAUGAS', 'HITECH']

                        list_colors = [(0, 204, 0, 110), (240, 128, 128, 110), (244, 193, 126, 110),
                                       (153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                       (86, 172, 186, 110), (50, 168, 84, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_lazeris = ["SRS", "METACO", "AUTOSABINA"]
                        for item in list_lazeris:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(255, 228, 181, 110))

                        list_komponentai = ['ALBASERVIS', 'DAGMITA', 'IGNERA', 'KRC RATUKAI', 'WURTH', 'DRUTSRAIGTIS',
                                            'JOLDITA', 'SERFAS', 'BL TECH', 'INTEROLL', 'TECHNOBALT', "HIDROBALT"]
                        for item in list_komponentai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(176, 196, 222, 110))

                        list_tekinimas = ['M.J.', 'MITRONAS', 'KAVERA', 'KAGNETA']
                        for item in list_tekinimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(188, 143, 143, 110))

                        list_gumavimas = ['METGA', 'KASTAGA', 'BALTAS VEJAS']
                        for item in list_gumavimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(137, 175, 174, 110))

                        if data == 'HITECH':
                            setitem.setBackground(QtGui.QColor(50, 168, 84, 110))

                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):
                self.tableRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                con = psycopg2.connect(
                    **params
                )

                cur = con.cursor()

                cur.execute(
                    """SELECT  id, imone, konstruktorius, projektas, pav_uzsakymai,
                    terminas, statusas, komentarai, breziniai, sarasas, update_date,
                    filename, filetype, filedir  FROM uzsakymai 
                    WHERE statusas = 'BROKUOTA' 
                    ORDER BY terminas ASC, projektas ASC, konstruktorius ASC, pav_uzsakymai ASC, imone ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.uzsakymuTable.rowCount()
                    self.uzsakymuTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))
                        # check current date and table entry, if nor equal or more make it red
                        listdata = []

                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()

                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # projektas_query = [i[3] for i in query]
                        # projektas_isvalymas = set(projektas_query)
                        # projektas_list = list(projektas_isvalymas)
                        # projektas_list.sort()
                        #
                        # projektas_list_colors = [
                        #                          (176, 196, 222, 110), (244, 193, 126, 110), (188, 143, 143, 110),
                        #                          (244, 193, 126, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                        #                          (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                        #                          (230, 230, 250), (255, 250, 240), (122, 197, 205, 110)
                        #                         ]
                        #
                        # for count_num in range(0, len(projektas_list)):
                        #     while count_num < len(projektas_list):
                        #         if data == projektas_list[count_num] and data != None and data != "":
                        #             setitem.setBackground(QtGui.QColor(*projektas_list_colors[0]))
                        #         count_num += 1

                        list_names = ['PAGAMINTA', 'BROKUOTA', 'MODESTAS', 'JULIJUS', 'JULIUS', 'VAIDAS',
                                      'MINDAUGAS', 'HITECH']

                        list_colors = [(0, 204, 0, 110), (240, 128, 128, 110), (244, 193, 126, 110),
                                       (153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                       (86, 172, 186, 110), (50, 168, 84, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_lazeris = ["SRS", "METACO", "AUTOSABINA"]
                        for item in list_lazeris:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(255, 228, 181, 110))

                        list_komponentai = ['ALBASERVIS', 'DAGMITA', 'IGNERA', 'KRC RATUKAI', 'WURTH', 'DRUTSRAIGTIS',
                                            'JOLDITA', 'SERFAS', 'BL TECH', 'INTEROLL', 'TECHNOBALT', "HIDROBALT"]
                        for item in list_komponentai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(176, 196, 222, 110))

                        list_tekinimas = ['M.J.', 'MITRONAS', 'KAVERA', 'KAGNETA']
                        for item in list_tekinimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(188, 143, 143, 110))

                        list_gumavimas = ['METGA', 'KASTAGA', 'BALTAS VEJAS']
                        for item in list_gumavimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(137, 175, 174, 110))

                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                row_count = cur.rowcount

                for i in range(0, row_count):
                    value = 100

                    self.progress_bar.setRange(0, value)

                    if value > 50:
                        self.progress_bar.setStyleSheet("QProgressBar {color: white;}")

                    progress_val = int(((i + 1) / row_count) * 100)
                    self.progress_bar.setValue(progress_val)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

            elif self.treeTable.currentItem() == self.atsargosSelect.child(0):
                self.tableRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                    ORDER BY pavadinimas ASC, konfig ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS', 'GUOLIAVIETE',
                                      'KAMSTIS']

                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (255, 153, 51, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110), (255, 229, 204, 110), (192, 192, 192, 110)]
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
                self.tableRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                    ORDER BY pavadinimas ASC, konfig ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS', 'GUOLIAVIETE',
                                      'KAMSTIS']
                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (255, 153, 51, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110), (255, 229, 204, 110), (192, 192, 192, 110)]
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
                self.tableRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                    ORDER BY pavadinimas ASC, konfig ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['PNEUMO', 'BUTRIMONIU', 'GUOLIS', 'GUOLIS+GUOLIAVIETE', 'IVORE', 'MOVA RCK',
                                      'GRANDINE', 'ZVAIGZDE', 'FIKSACINIS ZIEDAS', 'VARZTAS', 'GUOLIAVIETE',
                                      'KAMSTIS']
                        list_colors = [(122, 197, 205, 110), (176, 196, 222, 110), (244, 193, 126, 110),
                                       (255, 153, 51, 110), (153, 204, 155, 110), (153, 204, 155, 110),
                                       (176, 196, 222, 110), (176, 196, 222, 110), (188, 143, 143, 110),
                                       (188, 143, 143, 110), (255, 229, 204, 110), (192, 192, 192, 110)]
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
                self.tableRightLayout.setCurrentIndex(2)
                self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                self.tableRightLayout.setCurrentIndex(2)
                self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                self.tableRightLayout.setCurrentIndex(2)
                self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                self.tableRightLayout.setCurrentIndex(2)
                self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
                        self.tableRightLayout.setCurrentIndex(3)
                        self.pavarosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def refreshTables(self):
        try:
            self.listTables()
        except Exception as error:
            print(f"{error}")

    def updateUzsakymai(self):
        """select row data and fill entry with current data"""
        global uzsakymaiId

        try:
            self.display = dipslayUzsakymaiUpdate()
            self.display.show()
            self.display.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def updateAtsargos(self):
        global atsargosId

        try:
            self.display = displayAtsargosUpdate()
            self.display.show()
            self.display.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def updateRolikai(self):
        global rolikaiId

        try:
            self.display = displayRolikaiUpdate()
            self.display.show()
            self.display.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def updatePavaros(self):
        global pavarosId

        try:
            self.display = displayPavarosUpdate()
            self.display.show()
            self.display.exec_()
            self.displayPavaros()
            self.refresh_tree_pavaros_items()

        except Exception as error:
            print(f"{error}")

    def updateStelazas(self):
        global stelazasId

        try:
            self.display = displayStelazasUpdate()
            self.display.show()
            self.display.exec_()
            self.refreshTables()
        except Exception as error:
            print(f"{error}")

    def updateSanaudos(self):
        global sanaudosId

        try:
            self.display = displaySanaudosUpdate()
            self.display.show()
            self.display.exec_()
            self.refreshTables()
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
            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):
                a = a1 = a2 = a3 = a4 = self.searchEntry1.text()

                self.uzsakymuTable.setFont(QFont("Times", self.TEXT_PT_TABLE))
                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM uzsakymai WHERE imone ILIKE '%{}%' OR projektas ILIKE '%{}%' OR 
                    konstruktorius ILIKE '%{}%' OR pav_uzsakymai ILIKE '%{}%' OR komentarai ILIKE '%{}%'
                    ORDER BY statusas ASC, terminas ASC, projektas ASC, konstruktorius ASC, 
                    pav_uzsakymai ASC, imone ASC""".format
                    (a, a1, a2, a3, a4))
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
                    row_number = self.uzsakymuTable.rowCount()
                    self.uzsakymuTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        # print(row_number, column_number, data)

                        # check current date and table entry, if nor equal or bigger make it red
                        listdata = []
                        if column_number == 5:
                            listdata.append(str(data))
                            if listdata[0] == "+" or listdata[0] == "-":
                                listdata.pop()

                        for i in listdata:
                            if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                                None
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        list_names = ['PAGAMINTA', 'BROKUOTA', 'MODESTAS', 'JULIJUS', 'JULIUS', 'VAIDAS',
                                      'MINDAUGAS', 'HITECH']

                        list_colors = [(0, 204, 0, 110), (240, 128, 128, 110), (244, 193, 126, 110),
                                       (153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                       (86, 172, 186, 110), (50, 168, 84, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_lazeris = ["SRS", "METACO", "AUTOSABINA"]
                        for item in list_lazeris:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(255, 228, 181, 110))

                        list_komponentai = ['ALBASERVIS', 'DAGMITA', 'IGNERA', 'KRC RATUKAI', 'WURTH', 'DRUTSRAIGTIS',
                                            'JOLDITA', 'SERFAS', 'BL TECH', 'INTEROLL', 'TECHNOBALT', "HIDROBALT"]
                        for item in list_komponentai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(176, 196, 222, 110))

                        list_tekinimas = ['M.J.', 'MITRONAS', 'KAVERA', 'KAGNETA']
                        for item in list_tekinimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(188, 143, 143, 110))

                        list_gumavimas = ['METGA', 'KASTAGA', 'BALTAS VEJAS']
                        for item in list_gumavimas:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(137, 175, 174, 110))

                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):
                a = a1 = a2 = a3 = a4 = a5 = self.searchEntry1.text()

                self.atsarguTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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

                self.rolikaiTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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

            elif self.treeTable.currentItem() == self.stelazasSelect:
                a = a1 = a2 = a3 = a4 = self.searchEntry1.text()

                self.stelazasTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

                for i in reversed(range(self.stelazasTable.rowCount())):
                    self.stelazasTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM stelazas WHERE pavadinimas ILIKE '%{}%' OR projektas ILIKE '%{}%' OR 
                    sandelis ILIKE '%{}%' OR vieta ILIKE '%{}%' OR komentarai ILIKE '%{}%'
                    ORDER BY vieta ASC, projektas ASC, sandelis ASC, pavadinimas ASC""".format
                    (a, a1, a2, a3, a4))
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
                    row_number = self.stelazasTable.rowCount()
                    self.stelazasTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['ROLIKAI', 'VARIKLIAI', 'DETALES IR KT.', 'FESTO', 'ATSARGOS', 'BUTRIMONIU',
                                      'KONTORA']

                        list_colors = [(86, 172, 186, 110), (244, 193, 126, 110), (153, 204, 155, 110),
                                       (254, 253, 195, 110), (176, 196, 222, 110), (176, 196, 222, 110),
                                       (176, 196, 222, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        self.stelazasTable.setItem(row_number, column_number, setitem)

                self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                a = a1 = a2 = a3 = a4 = self.searchEntry1.text()

                self.sanaudosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

                for i in reversed(range(self.sanaudosTable.rowCount())):
                    self.sanaudosTable.removeRow(i)

                conn = psycopg2.connect(
                    **params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM sanaudos WHERE pavadinimas ILIKE '%{}%' OR projektas ILIKE '%{}%' OR 
                    kiekis ILIKE '%{}%' OR mat_vnt ILIKE '%{}%' OR komentaras ILIKE '%{}%'
                    ORDER BY metai DESC, projektas ASC, pavadinimas ASC""".format
                    (a, a1, a2, a3, a4))
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
                    row_number = self.sanaudosTable.rowCount()
                    self.sanaudosTable.insertRow(row_number)

                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        list_names = ['HABASIT', 'PROFILIAI', 'UZDENGIMAI', 'VARIKLIAI']

                        list_colors = [(153, 204, 155, 110), (254, 253, 195, 110), (192, 192, 192, 110),
                                       (176, 196, 222, 110)]

                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        list_standartiniai = ["PRILAIKANTIS", "GALINUKAS", "SKRIEMULYS", "SKRIEMULIO ASIS"]
                        for item in list_standartiniai:
                            if data == item:
                                setitem.setBackground(QtGui.QColor(122, 197, 205, 110))

                        self.sanaudosTable.setItem(row_number, column_number, setitem)

                self.sanaudosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

            else:
                a = a1 = a2 = a3 = a4 = a5 = a6 = self.searchEntry1.text()

                self.pavarosTable.setFont(QFont("Times", self.TEXT_PT_TABLE))

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
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def clearSearchEntry(self):
        """search cancel"""
        self.searchEntry1.clear()
        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):
                self.refreshTables()

            elif self.treeTable.currentItem() == self.atsargosSelect or \
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

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.refreshTables()

            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.refreshTables()

            else:
                self.refreshTables()

        except Exception as error:
            print(f"{error}")

    def searchTables2(self, s):
        """search for items and select matched items"""
        if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):
            # Clear current selection
            self.uzsakymuTable.setCurrentItem(None)

            if not s:
                # Empty string, do not search
                return

            matching_items = self.uzsakymuTable.findItems(s, Qt.MatchContains)
            if matching_items:
                # if it finds something
                for item in matching_items:
                    item.setSelected(True)

        elif self.treeTable.currentItem() == self.atsargosSelect or \
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

        elif self.treeTable.currentItem() == self.stelazasSelect:
            if not s:
                return

            matching_items = self.stelazasTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

        elif self.treeTable.currentItem() == self.sanaudosSelect:
            self.sanaudosTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.sanaudosTable.findItems(s, Qt.MatchContains)
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

        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):

                global uzsakymaiId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )

                        cur = conn.cursor()
                        cur.execute("DELETE FROM uzsakymai WHERE id = %s", (uzsakymaiId,))
                        conn.commit()

                        self.refreshTables()

                        conn.close()

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

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):

                global atsargosId

                try:
                    if (x == QMessageBox.Yes):
                        con = psycopg2.connect(
                            **params
                        )

                        cur = con.cursor()
                        cur.execute("DELETE FROM atsargos WHERE id = %s", (atsargosId,))
                        con.commit()

                        self.refreshTables()

                        con.close()

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

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):

                global rolikaiId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )
                        cur = conn.cursor()
                        cur.execute("DELETE FROM rolikai WHERE id = %s", (rolikaiId,))
                        conn.commit()

                        self.refreshTables()

                        conn.close()

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

            elif self.treeTable.currentItem() == self.stelazasSelect:
                global stelazasId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )

                        cur = conn.cursor()
                        cur.execute("DELETE FROM stelazas WHERE id = %s", (stelazasId,))
                        conn.commit()

                        self.refreshTables()

                        conn.close()

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

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                global sanaudosId

                try:
                    if (x == QMessageBox.Yes):
                        con = psycopg2.connect(
                            **params
                        )

                        cur = con.cursor()
                        cur.execute("DELETE FROM sanaudos WHERE id = %s", (sanaudosId,))
                        con.commit()

                        self.refreshTables()

                        con.close()

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

            else:
                global pavarosId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )
                        cur = conn.cursor()
                        cur.execute("DELETE FROM pavaros WHERE id = %s", (pavarosId,))
                        conn.commit()

                        self.displayPavaros()

                        conn.close()

                        self.refresh_tree_pavaros_items()

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

        except Exception as error:
            print(f"{error}")

    def save(self):
        try:
            headers = ""
            table = ""
            table_name = ""

            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):

                headers = ["ĮMONĖ", "KONSTRUKTORIUS", "PROJEKTAS", "PAVADINIMAS", "TERMINAS",
                           "STATUSAS", "KOMENTARAI", "KOMPONENTAI", "ATNAUJINTA"]
                table = self.uzsakymuTable
                table_name = "uzsakymai"

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):

                headers = ["PAVADINIMAS", "KONFIGURACIJA", "SANDĖLIS", "VIETA", "KIEKIS", "VIENETAI", "KOMENTARAI",
                           "NUOTRAUKA", "ATNAUJINTA"]
                table = self.atsarguTable
                table_name = "atsargos"

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):

                headers = ["PAVADINIMAS", "ILGIS", "KIEKIS", "TVIRTINIMAS", "TIPAS", "APRAŠYMAS",
                           "PROJEKTAS", "KOMENTARAI", "SANDĖLIS", "VIETA", "ATNAUJINTA"]
                table = self.rolikaiTable
                table_name = "rolikai"

            elif self.treeTable.currentItem() == self.stelazasSelect:
                headers = ["PAVADINIMAS", "PROJEKTAS", "SANDĖLIS", "VIETA", "KOMENTARAI", "ATNAUJINTA"]
                table = self.stelazasTable
                table_name = "stelazas"

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                headers = ["PAVADINIMAS", "PROJEKTAS", "KIEKIS", "VIENETAI", "KOMENTARAI", "METAI", "ATNAUJINTA"]
                table = self.sanaudosTable
                table_name = "sanaudos"

            else:
                headers = ["PAVADINIMAS", "GAMINTOJAS", "TIPAS", "kW", "aps/min",
                           "Nm", "TVIRTINIMAS", "DIAMETRAS (mm)", "KIEKIS", "KOMENTARAI", "SANDĖLIS",
                           "VIETA", "ATNAUJINTA"]
                table = self.pavarosTable
                table_name = "pavaros"

            data = []
            # counts rows
            for row in range(table.rowCount()):
                row_data = []
                # counts columns
                for col in range(table.columnCount()):
                    if not table.isColumnHidden(col):
                        # prints table items, just have to add .text()
                        item = table.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                # print(row_data)
                data.append(row_data)
            df = pandas.DataFrame(data,
                                  columns=headers)

            path = "bardakas_files/save"
            # Check if the specified path exists or not
            if not os.path.isdir(path):
                os.makedirs(path)
            df.to_csv(f"{path}/{table_name}-{year}-{month}-{day}", index=False)

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def saveAs(self):
        """save table to .xlsx .csv .pdf"""
        try:
            # model = ""
            headers = ""
            table = ""
            table_name = ""

            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):

                headers = ["ĮMONĖ", "KONSTRUKTORIUS", "PROJEKTAS", "PAVADINIMAS", "TERMINAS",
                           "STATUSAS", "KOMENTARAI", "KOMPONENTAI", "ATNAUJINTA"]
                # model = self.uzsakymuTable.model()
                table = self.uzsakymuTable
                table_name = "uzsakymai"

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):

                headers = ["PAVADINIMAS", "KONFIGURACIJA", "SANDĖLIS", "VIETA", "KIEKIS", "VIENETAI", "KOMENTARAI",
                           "NUOTRAUKA", "ATNAUJINTA"]
                # model = self.atsarguTable.model()
                table = self.atsarguTable
                table_name = "atsargos"

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):

                headers = ["PAVADINIMAS", "ILGIS", "KIEKIS", "TVIRTINIMAS", "TIPAS", "APRAŠYMAS",
                           "PROJEKTAS", "KOMENTARAI", "SANDĖLIS", "VIETA", "ATNAUJINTA"]
                # model = self.rolikaiTable.model()
                table = self.rolikaiTable
                table_name = "rolikai"

            elif self.treeTable.currentItem() == self.stelazasSelect:
                headers = ["PAVADINIMAS", "PROJEKTAS", "SANDĖLIS", "VIETA", "KOMENTARAI", "ATNAUJINTA"]
                # model = self.stelazasTable.model()
                table = self.stelazasTable
                table_name = "stelazas"

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                headers = ["PAVADINIMAS", "PROJEKTAS", "KIEKIS", "VIENETAI", "KOMENTARAI", "METAI", "ATNAUJINTA"]
                # model = self.sanaudosTable.model()
                table = self.sanaudosTable
                table_name = "sanaudos"

            else:
                headers = ["PAVADINIMAS", "GAMINTOJAS", "TIPAS", "kW", "aps/min",
                           "Nm", "TVIRTINIMAS", "DIAMETRAS (mm)", "KIEKIS", "KOMENTARAI", "SANDĖLIS",
                           "VIETA", "ATNAUJINTA"]
                # model = self.pavarosTable.model()
                table = self.pavarosTable
                table_name = "pavaros"

            filename, file_end = QFileDialog.getSaveFileName(self, 'Save', '',
                                                             "(*.xlsx);; (*.csv)")

            dir_path = os.path.dirname(filename)
            # print(dir_path)
            file_name = os.path.basename(filename).split(".")[0]
            # print(file_name)

            if not filename:
                return

            if file_end == "(*.xlsx)":
                data = []
                # counts rows
                for row in range(table.rowCount()):
                    row_data = []
                    # counts columns
                    for col in range(table.columnCount()):
                        if not table.isColumnHidden(col):
                            # prints table items, just have to add .text()
                            item = table.item(row, col)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append('')
                    # print(row_data)
                    data.append(row_data)

                with pandas.ExcelWriter(f"{dir_path}\{file_name}.xlsx",
                                        engine='xlsxwriter') as writer:

                    data_table = pandas.DataFrame(data,
                                                  columns=headers)

                    data_table.index = range(1, len(data) + 1)

                    # Save to .xlsx
                    data_table.style.set_properties(**{'text-align': 'center'}). \
                        to_excel(writer,
                                 sheet_name=f'{table_name}', index=True,
                                 index_label="Nr.")

                    # # fit to cell
                    auto_adjust_xlsx_column_width(data_table, writer,
                                                  sheet_name=f'{table_name}',
                                                  margin=3)

                    # create workbook
                    workbook = writer.book
                    worksheet = writer.sheets[f'{table_name}']

                    # add border on cells
                    border_format = workbook.add_format({'border': True,
                                                         'align': 'center',
                                                         'valign': 'vcenter'})

                    # add style to headers
                    header_format = workbook.add_format({'font_name': 'Arial',
                                                         'font_size': 10,
                                                         'bold': True,
                                                         'bg_color': 'yellow'})

                    # "xl_range(0, 0, len(data_tables), len(data_tables.columns)"
                    # first int "0" and second "0" is start point first cell,
                    # third int is how much rows your need to apply
                    # and last one is for how many columns to apply
                    worksheet.conditional_format(xls.utility.xl_range(
                        0, 0, len(data_table), len(data_table.columns)),
                        {'type': 'no_errors',
                         'format': border_format})

                    worksheet.conditional_format(xls.utility.xl_range(
                        0, 0, 0, len(data_table.columns)),
                        {'type': 'no_errors',
                         'format': header_format})

            elif file_end == "(*.csv)":
                data = []
                # counts rows
                for row in range(table.rowCount()):
                    row_data = []
                    # counts columns
                    for col in range(table.columnCount()):
                        if not table.isColumnHidden(col):
                            # prints table items, just have to add .text()
                            item = table.item(row, col)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append('')
                    # print(row_data)
                    data.append(row_data)
                data_table = pandas.DataFrame(data,
                                              columns=headers)

                data_table.to_csv(f"{dir_path}/{file_name}", index=False)

            # elif file_end == ".pdf(*.pdf)":
            #     printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
            #     printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            #     printer.setPaperSize(QtPrintSupport.QPrinter.A4)
            #     printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
            #     printer.setOutputFileName(filename)
            #
            #     doc = QtGui.QTextDocument()
            #
            #     html = """<html>
            #     <head>
            #     <style>
            #     table, th, td {
            #       border: 1px solid black;
            #       border-collapse: collapse;
            #     }
            #     </style>
            #     </head>"""
            #     html += "<table><thead>"
            #     html += "<tr>"
            #     for c in range(model.columnCount()):
            #         if not table.isColumnHidden(c):
            #             html += "<th>{}</th>".format(model.headerData(c, QtCore.Qt.Horizontal))
            #
            #     html += "</tr></thead>"
            #     html += "<tbody>"
            #     for r in range(model.rowCount()):
            #         html += "<tr>"
            #         for c in range(model.columnCount()):
            #             if not table.isColumnHidden(c):
            #                 html += "<td>{}</td>".format(model.index(r, c).data() or "")
            #         html += "</tr>"
            #     html += "</tbody></table>"
            #     doc.setHtml(html)
            #     doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))
            #     doc.print_(printer)

        except Exception as error:
            print(f"{error}")

    def handlePrint(self):
        """send info to print and prints"""
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        """print preview"""
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        """paint print table"""

        table_name = ""

        try:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)

            if self.treeTable.currentItem() == self.uzsakymaiSelect or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):

                table_name = self.uzsakymuTable

            elif self.treeTable.currentItem() == self.atsargosSelect or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(0) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(1) or \
                    self.treeTable.currentItem() == self.atsargosSelect.child(2):

                table_name = self.atsarguTable

            elif self.treeTable.currentItem() == self.rolikaiSelect or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(0) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(1) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(2) or \
                    self.treeTable.currentItem() == self.rolikaiSelect.child(3):

                table_name = self.rolikaiTable

            elif self.treeTable.currentItem() == self.stelazasSelect:

                table_name = self.stelazasTable

            elif self.treeTable.currentItem() == self.sanaudosSelect:

                table_name = self.sanaudosTable

            else:
                table_name = self.pavarosTable

        except Exception as error:
            print(f"{error}")

        finally:
            visible_columns = [col for col in range(table_name.columnCount())
                               if not table_name.isColumnHidden(col)]

            # Get the number of visible columns
            num_visible_cols = len(visible_columns)

            # Insert a table with the number of visible columns and header rows
            table = cursor.insertTable(table_name.rowCount() + 1, num_visible_cols, tableFormat)

            # Set the background color of the header row to light gray and make it bold
            header_format = table.cellAt(0, 0).format()
            header_format.setBackground(QtGui.QColor(230, 230, 230))
            header_cursor = table.cellAt(0, 0).firstCursorPosition()
            header_cursor.insertText("")
            header_format.setFontWeight(QtGui.QFont.Bold)

            for col_index, col in enumerate(visible_columns):
                # Insert header text
                header_cursor = table.cellAt(0, col_index).firstCursorPosition()
                header_cursor.insertText(table_name.horizontalHeaderItem(col).text())
                header_format.setFontWeight(QtGui.QFont.Bold)
                header_format.setBackground(QtGui.QColor(230, 230, 230))
                # Insert data text
                for row in range(1, table.rows()):
                    cursor = table.cellAt(row, col_index).firstCursorPosition()
                    cursor.insertText(table_name.item(row - 1, col).text())

            # Set the border of the table
            frame_format = table.format()
            frame_format.setBorderStyle(QtGui.QTextFrameFormat.BorderStyle_Solid)
            frame_format.setBorder(0.5)
            frame_format.setBorderBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0)))
            document.print_(printer)

    def openFolder(self):
        """open selected folder"""
        try:
            global uzsakymaiId

            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()
            cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
            uzsakymas = cur.fetchone()

            uzsakymasBreziniai = uzsakymas[8]

            conn.close()

            isExist = os.path.exists(uzsakymasBreziniai)

            if isExist:
                webbrowser.open(os.path.realpath(uzsakymasBreziniai))

            else:
                if not isExist:
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR...")
                    msg.setText("NO FOLDER...")
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                    Bardakas_style_gray.msgsheetstyle(msg)

                    x = msg.exec_()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to open.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def uzsakymaiWriteToFile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def openFile(self):
        """open selected file"""
        global uzsakymaiId
        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute("""SELECT * FROM uzsakymai WHERE ID = %s""", (uzsakymaiId,))
            atsargos = c.fetchone()

            self.filename = atsargos[12]
            self.photo = atsargos[13]
            self.filetype = atsargos[14]

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
                path = "bardakas_files/uzsakymai_list"
                # Check if the specified path exists or not
                if not os.path.isdir(path):
                    os.makedirs(path)

                photoPath = "bardakas_files/uzsakymai_list/" + self.filename + self.filetype

                if not os.path.isfile(photoPath):
                    self.uzsakymaiWriteToFile(self.photo, photoPath)

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

                FILE_URL = os.path.abspath(os.getcwd()) + "/" + photoPath
                os.startfile(FILE_URL, 'open')

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

    def openBrokasEntry(self):
        try:
            self.brokasWindow = openBrokas()
        except Exception as error:
            print(f"{error}")

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

    def openAtkrovimai(self):
        try:
            self.open_atkrovimai_window = open_atkrovimai.MainMenu()
        except Exception as error:
            print(f"{error}")

    def openVaztarasciai(self):
        try:
            self.open_paletes_window = sheet_generator.main_window()
        except Exception as error:
            print(f"{error}")

    def MainClose(self):
        """exit app"""
        self.destroy()


class dipslayUzsakymaiUpdate(QDialog, pt_points):
    """double mouse click table"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(650 * self.scale_factor))
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
        self.uzsakymuDetails()
        self.widgets()
        self.layouts()

    def uzsakymuDetails(self):
        global uzsakymaiId

        conn = psycopg2.connect(
            **params
        )

        cur = conn.cursor()

        cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
        uzsakymas = cur.fetchone()

        conn.close()

        self.uzsakymasImone = uzsakymas[1]
        self.uzsakymasBraize = uzsakymas[2]
        self.uzsakymasProjektas = uzsakymas[3]
        self.uzsakymasPavadinimas = uzsakymas[4]
        self.uzsakymasTerminas = uzsakymas[5]
        self.uzsakymasStatusas = uzsakymas[6]
        self.uzsakymasKomentarai = uzsakymas[7]
        self.uzsakymasBreziniai = uzsakymas[8]
        self.uzsakymasList = uzsakymas[9]
        # self.uzsakymasUpdate_date = uzsakymas[10]
        self.filename = uzsakymas[12]
        self.photo = uzsakymas[13]
        self.filetype = uzsakymas[14]

    def widgets(self):
        conn = psycopg2.connect(
            **params
        )
        cur = conn.cursor()
        cur.execute("""SELECT * FROM combo_uzsakymai ORDER BY id ASC""")
        query = cur.fetchall()

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

        conn.close()

        self.imoneCombo1 = QComboBox()
        self.imoneCombo1.setEditable(True)
        self.imoneCombo1.addItems(
            list_imone)
        self.imoneCombo1.setCurrentText(self.uzsakymasImone)
        self.imoneCombo1.setFont(QFont("Times", self.TEXT_PT))
        self.imoneCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.braizeCombo1 = QComboBox()
        self.braizeCombo1.setEditable(True)
        self.braizeCombo1.addItems(list_konstruktorius)
        self.braizeCombo1.setCurrentText(self.uzsakymasBraize)
        self.braizeCombo1.setFont(QFont("Times", self.TEXT_PT))
        self.braizeCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasCombo1 = QComboBox()
        self.projektasCombo1.setEditable(True)
        self.projektasCombo1.setPlaceholderText('Text')
        self.projektasCombo1.addItems(list_projektas)
        self.projektasCombo1.setCurrentText(self.uzsakymasProjektas)
        self.projektasCombo1.setFont(QFont("Times", self.TEXT_PT))
        self.projektasCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.uzskpavCombo1 = QComboBox()
        self.uzskpavCombo1.setEditable(True)
        self.uzskpavCombo1.setPlaceholderText('Text')
        self.uzskpavCombo1.addItems(list_pavadinimas)
        self.uzskpavCombo1.setCurrentText(self.uzsakymasPavadinimas)
        self.uzskpavCombo1.setFont(QFont("Times", self.TEXT_PT))
        self.uzskpavCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.terminasEntry1 = QComboBox()
        self.terminasEntry1.addItems(["-", "+"])
        self.terminasEntry1.setEditable(True)
        self.terminasEntry1.setCurrentText(self.uzsakymasTerminas)
        self.terminasEntry1.setFont(QFont("Times", self.TEXT_PT))
        self.terminasEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.statusasCombo1 = QComboBox()
        self.statusasCombo1.addItems(['GAMINA', 'PAGAMINTA', 'BROKUOTA'])
        self.statusasCombo1.setEditable(True)
        self.statusasCombo1.setCurrentText(self.uzsakymasStatusas)
        self.statusasCombo1.setFont(QFont("Times", self.TEXT_PT))
        self.statusasCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry1 = QTextEdit()
        self.komentaraiEntry1.setText(self.uzsakymasKomentarai)
        self.komentaraiEntry1.setFont(QFont("Times", self.TEXT_PT))

        self.locEntry = QLineEdit()
        self.locEntry.setText(self.uzsakymasBreziniai)
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;}")
        self.locEntry.setFont(QFont("Times", self.TEXT_PT))
        self.locEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.breziniaiBtn = QPushButton("LINK TO FOLDER")
        self.breziniaiBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.breziniaiBtn.clicked.connect(self.OpenFolderDialog)
        self.breziniaiBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.ListEntry1 = QLineEdit()
        self.ListEntry1.setText(self.uzsakymasList)
        self.ListEntry1.setReadOnly(True)
        self.ListEntry1.setFont(QFont("Times", self.TEXT_PT))
        self.ListEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.ListEntry1.setStyleSheet("QLineEdit{background: darkgrey;}")

        self.fileBtn = QPushButton("CHANGE FILE")
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.dateBtn = QPushButton("CHANGE DATE")
        self.dateBtn.setFixedWidth(self.BUTTON_WIDTH)
        self.dateBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.clicked.connect(self.updateUzsakymas)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.clicked.connect(self.cancelUzsakymai)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        # self.qhbox1 = QHBoxLayout()
        # self.qhbox1.addWidget(self.locEntry)
        # self.qhbox1.addWidget(self.breziniaiBtn)
        #
        # self.qhbox2 = QHBoxLayout()
        # self.qhbox2.addWidget(self.ListEntry1)
        # self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.terminasEntry1)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("ĮMONĖ:"), self.imoneCombo1)
        self.widgetLayout.addRow(QLabel("BRAIŽĖ:"), self.braizeCombo1)
        self.widgetLayout.addRow(QLabel("PROJEKTAS:"), self.projektasCombo1)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS:"), self.uzskpavCombo1)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("TERMINAS:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("STATUSAS:"), self.statusasCombo1)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("BRĖŽINIAI:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.breziniaiBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("SĄRAŠAS:"), self.ListEntry1)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI:"))
        self.widgetLayout.addRow(self.komentaraiEntry1)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        """add widgets to layouts"""
        self.mainLayout1.addWidget(self.widgetFrame)

        self.mainLayout.addLayout(self.mainLayout1)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def terminasCalendar(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.calBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QWidget()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(int(780 / self.scale_factor), int(280 / self.scale_factor),
                                        int(350 / self.scale_factor), int(350 / self.scale_factor))
        self.calendarWindow.setWindowTitle('CHANGE DATE')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        Bardakas_style_gray.QCalendarstyle(self)
        self.calendarWindow.show()

        # @QtCore.pyqtSlot(QtCore.QDate)
        def get_date(qDate):
            if qDate.day() <= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.terminasEntry1.setCurrentText(date)

            elif qDate.day() <= 9 and qDate.month() >= 10:
                date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.terminasEntry1.setCurrentText(date)

            elif qDate.day() >= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.terminasEntry1.setCurrentText(date)

            else:
                date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.terminasEntry1.setCurrentText(date)

            self.calendarWindow.close()

        self.cal.clicked.connect(get_date)

    def cal_cancel(self):
        self.calendarWindow.close()

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

        self.ListEntry1.setText(f"{justfilename}{filetype}")

    def updateUzsakymas(self):
        global uzsakymaiId
        imone1 = self.imoneCombo1.currentText().upper()
        braize1 = self.braizeCombo1.currentText().upper()
        projektas1 = self.projektasCombo1.currentText().upper()
        pavadinimas1 = self.uzskpavCombo1.currentText()
        terminas1 = self.terminasEntry1.currentText()
        statusas1 = self.statusasCombo1.currentText().upper()
        komentarai1 = str(self.komentaraiEntry1.toPlainText())
        breziniai1 = self.locEntry.text()
        sarasas1 = self.ListEntry1.text()
        update_date1 = self.update_date.text()

        filename1 = self.ListFileName.text()
        blobPhoto1 = self.convertToBinaryDataFile(self.ListDir.text())
        filetype1 = self.ListFileType.text()
        filedir1 = self.ListDir.text()

        terminas_entry = ""

        if terminas1 != terminas_entry:
            try:
                if self.ListDir.text() != "":
                    conn = psycopg2.connect(
                        **params
                    )

                    cur = conn.cursor()

                    query = "UPDATE uzsakymai SET imone = %s, konstruktorius = %s, projektas = %s, pav_uzsakymai = %s, " \
                            "terminas = %s, statusas = %s, komentarai = %s, breziniai = %s, sarasas = %s, " \
                            "update_date = %s, filename = %s, photo = %s, filetype = %s, filedir = %s " \
                            "where id = %s"
                    cur.execute(query, (imone1, braize1, projektas1, pavadinimas1, terminas1, statusas1, komentarai1,
                                        breziniai1, sarasas1, update_date1, filename1, blobPhoto1, filetype1, filedir1,
                                        uzsakymaiId))
                    conn.commit()
                    conn.close()

                else:
                    conn = psycopg2.connect(
                        **params
                    )

                    cur = conn.cursor()

                    query = "UPDATE uzsakymai SET imone = %s, konstruktorius = %s, projektas = %s, pav_uzsakymai = %s, " \
                            "terminas = %s, statusas = %s, komentarai = %s, breziniai = %s, sarasas = %s, " \
                            "update_date = %s where id = %s"
                    cur.execute(query, (imone1, braize1, projektas1, pavadinimas1, terminas1, statusas1, komentarai1,
                                        breziniai1, sarasas1, update_date1, uzsakymaiId))
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


        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("TERMINAS can't be empty...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelUzsakymai(self):
        self.close()
        self.cal_cancel()


class displayAtsargosUpdate(QDialog, pt_points):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(600 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update2')
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
        self.atsargosDetails()
        self.widgets()
        self.layouts()

    def atsargosDetails(self):
        global atsargosId

        con = psycopg2.connect(
            **params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM atsargos WHERE ID = %s""", (atsargosId,))
        atsargos = c.fetchone()
        self.atsargosPavadinimas = atsargos[1]
        self.atsargosVieta = atsargos[2]
        self.atsargosKiekis = atsargos[3]
        self.atsargosMatmuo = atsargos[4]
        self.atsargosKomentarai = atsargos[5]
        self.atsargosNuotrauka = atsargos[6]
        # self.atsargosUpdate = atsargos[7]
        self.filename = atsargos[8]
        self.photo = atsargos[9]
        self.filetype = atsargos[10]
        self.konfiguracija = atsargos[12]
        self.sandelis = atsargos[13]

    def widgets(self):
        self.pavadinimasEntry2 = QComboBox()
        self.pavadinimasEntry2.setEditable(True)
        self.pavadinimasEntry2.setPlaceholderText("Text")
        self.pavadinimasEntry2.addItems([
            "GUOLIS", "DIRZAS", "DIRZELIS D5", "DIRZELIS PJ", "BELTAS", "GUOLIS+GUOLIAVIETE", "GUOLIAVIETE",
            "IVORE", "MOVA RCK", "GRANDINE", "VARZTAS", "ZVAIGZDE", "PNEUMO", "KAMSTIS"])
        self.pavadinimasEntry2.setCurrentText(self.atsargosPavadinimas)
        self.pavadinimasEntry2.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasEntry2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.konfigEntry = QLineEdit()
        self.konfigEntry.setPlaceholderText("Text")
        self.konfigEntry.setText(self.konfiguracija)
        self.konfigEntry.setFont(QFont("Times", self.TEXT_PT))
        self.konfigEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText("Text")
        self.sandelisCombo.addItems(["BUTRIMONIU", "DRAUGYSTES", "MITUVOS"])
        self.sandelisCombo.setCurrentText(self.sandelis)
        self.sandelisCombo.setFont(QFont("Times", self.TEXT_PT))
        self.sandelisCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vietaCombo2 = QComboBox()
        self.vietaCombo2.setEditable(True)
        self.vietaCombo2.addItems(["BUTRIMONIU", "MITUVOS", "KONTORA",
                                   "ZONA-1", "ZONA-2", "ZONA-3", "ZONA-4", "ZONA-5",
                                   "ZONA-6", "ZONA-7", "ZONA-8", "ZONA-9", "ZONA-10",
                                   "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
                                   "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4",
                                   "STELAZAS-5", "STELAZAS-6", "STELAZAS-7",
                                   "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11",
                                   "STELAZAS-12", "STELAZAS-13", "STELAZAS-14",
                                   "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo2.setCurrentText(self.atsargosVieta)
        self.vietaCombo2.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry2 = QLineEdit()
        self.kiekisEntry2.setText(self.atsargosKiekis)
        self.kiekisEntry2.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.kiekisEntry2.setAlignment(Qt.AlignCenter)

        self.matpavCombo2 = QComboBox()
        self.matpavCombo2.setEditable(True)
        self.matpavCombo2.addItems(["m.", "vnt."])
        self.matpavCombo2.setCurrentText(self.atsargosMatmuo)
        self.matpavCombo2.setFont(QFont("Times", self.TEXT_PT))
        self.matpavCombo2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.matpavCombo2.lineEdit().setAlignment(Qt.AlignCenter)

        self.kiekisChange = QLineEdit()
        self.kiekisChange.setPlaceholderText("Number")
        self.kiekisChange.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChange.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.kiekisChange.setAlignment(Qt.AlignCenter)

        self.kiekisChangeVnt = QLineEdit()
        self.kiekisChangeVnt.setReadOnly(False)
        self.kiekisChangeVnt.setStyleSheet("QLineEdit{background: darkgrey; color: black}")
        self.kiekisChangeVnt.setAlignment(Qt.AlignCenter)
        self.kiekisChangeVnt.setText(self.atsargosMatmuo)
        self.kiekisChangeVnt.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChangeVnt.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry2 = QTextEdit()
        self.komentaraiEntry2.setText(self.atsargosKomentarai)
        self.komentaraiEntry2.setFont(QFont("Times", self.TEXT_PT))

        # self.photoNameText = self.filename + self.filetype
        self.photoName = QLineEdit()
        self.photoName.setText(f"{self.filename}{self.filetype}")
        self.photoName.setReadOnly(True)
        self.photoName.setStyleSheet("QLineEdit{background: lightgrey;}")
        self.photoName.setFont(QFont("Times", self.TEXT_PT))
        self.photoName.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.nuotraukaBtn = QPushButton("CHANGE PICTURE")
        self.nuotraukaBtn.clicked.connect(self.getFileInfo)
        self.nuotraukaBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.nuotraukaBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.plusBtn = QPushButton()
        self.plusBtn.clicked.connect(self.plus)
        self.plusBtn.setIcon(QIcon("icons/plus.png"))
        self.plusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.plusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.minusBtn = QPushButton()
        self.minusBtn.clicked.connect(self.minus)
        self.minusBtn.setIcon(QIcon("icons/minus.png"))
        self.minusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.minusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateAtsargos)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelAtsargos)
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
        self.kiekisBox.addWidget(self.kiekisEntry2, 50)
        self.kiekisBox.addWidget(self.matpavCombo2, 50)

        self.kiekisBoxChange = QHBoxLayout()
        self.kiekisBoxChange.addWidget(self.kiekisChange, 50)
        self.kiekisBoxChange.addWidget(self.kiekisChangeVnt, 50)

        self.kiekisBtnChange = QHBoxLayout()
        self.kiekisBtnChange.addWidget(self.plusBtn)
        self.kiekisBtnChange.addWidget(self.minusBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasEntry2)
        self.widgetLayout.addRow(QLabel("KONFIGURACIJA: "), self.konfigEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("SANDĖLIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo2)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisBox)
        self.widgetLayout.addRow(QLabel("KIEKIS +/-: "), self.kiekisBoxChange)
        self.widgetLayout.addRow(QLabel(""), self.kiekisBtnChange)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("NUOTRAUKA: "), self.photoName)
        self.widgetLayout.addRow(QLabel(""), self.nuotraukaBtn)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout.addRow(self.komentaraiEntry2)
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
        except Exception as error:
            print(f"{error}")

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.jpg;*.png;*.pdf)")
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

        self.photoName.setText(f"{justfilename}{filetype}")

    def minus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry2.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data - get_kiekis_minus)
            kiekis_result = self.kiekisEntry2.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"-{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result

        except:
            pass

    def plus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry2.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data + get_kiekis_minus)
            kiekis_result = self.kiekisEntry2.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"+{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result

        except:
            pass

    def updateAtsargos(self):
        global atsargosId
        pavadinimas1 = self.pavadinimasEntry2.currentText().upper()
        konfig1 = self.konfigEntry.text()
        sandelis1 = self.sandelisCombo.currentText().upper()
        vieta1 = self.vietaCombo2.currentText().upper()
        kiekis1 = self.kiekisEntry2.text()
        matmuo1 = self.matpavCombo2.currentText()
        komentarai1 = str(self.komentaraiEntry2.toPlainText())
        nuotrauka1 = self.photoName.text()
        update_date1 = self.update_date.text()

        filename = self.ListFileName.text()
        blobPhoto = self.convertToBinaryData(self.ListDir.text())
        filetype = self.ListFileType.text()
        filedir = self.ListDir.text()

        try:
            if self.ListDir.text() != "":
                con = psycopg2.connect(
                    **params
                )

                c = con.cursor()

                c.execute(
                    "UPDATE atsargos SET pavadinimas = %s, vieta = %s, kiekis = %s, mat_pav = %s, komentaras = %s, "
                    "nuotrauka = %s, update_date = %s, filename = %s, photo = %s, filetype = %s, filedir = %s,"
                    "konfig = %s, sandelis = %s where id = %s",
                    (pavadinimas1, vieta1, kiekis1, matmuo1, komentarai1, nuotrauka1, update_date1, filename,
                     blobPhoto, filetype, filedir, konfig1, sandelis1, atsargosId))

                con.commit()

                con.close()

                self.close()

            else:
                con = psycopg2.connect(
                    **params
                )

                c = con.cursor()

                c.execute(
                    "UPDATE atsargos SET pavadinimas = %s, vieta = %s, kiekis = %s, mat_pav = %s, komentaras = %s, "
                    "nuotrauka = %s, update_date = %s, konfig = %s, sandelis = %s where id = %s",
                    (pavadinimas1, vieta1, kiekis1, matmuo1, komentarai1, nuotrauka1, update_date1,
                     konfig1, sandelis1, atsargosId))

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

    def cancelAtsargos(self):
        self.close()


class displayRolikaiUpdate(QDialog, pt_points):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(700 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update5')
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
        self.rolikuDetails()
        self.widgets()
        self.layouts()

    def rolikuDetails(self):
        global rolikaiId

        conn = psycopg2.connect(
            **params
        )
        cur = conn.cursor()

        cur.execute("""SELECT * FROM rolikai WHERE ID=%s""", (rolikaiId,))
        rolikai = cur.fetchone()

        self.pavadinimasRolikai = rolikai[1]
        self.ilgisRolikai = rolikai[2]
        self.kiekisRolikai = rolikai[3]
        self.vietaRolikai = rolikai[4]
        self.tvirtinimasRolikai = rolikai[5]
        self.tipasRolikai = rolikai[6]
        self.aprasymasRolikai = rolikai[7]
        self.projektasRolikai = rolikai[8]
        self.komentaraiRolikai = rolikai[9]
        # self.updateRolikai = rolikai[10]
        self.sandelisRolikai = rolikai[11]

    def widgets(self):
        self.pavadinimasCombo = QComboBox()
        self.pavadinimasCombo.setEditable(True)
        self.pavadinimasCombo.setPlaceholderText('Text')
        self.pavadinimasCombo.addItems(
            ["RM", "PAPRASTAS", "POSUKIS-RM", "POSUKIS"])
        self.pavadinimasCombo.setCurrentText(self.pavadinimasRolikai)
        self.pavadinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.pavadinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.ilgisEntry = QLineEdit(self.ilgisRolikai)
        self.ilgisEntry.setPlaceholderText('Number')
        self.ilgisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.ilgisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit(self.kiekisRolikai)
        self.kiekisEntry.setPlaceholderText('Number')
        self.kiekisEntry.setAlignment(Qt.AlignCenter)
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisChange = QLineEdit()
        self.kiekisChange.setPlaceholderText("Number")
        self.kiekisChange.setAlignment(Qt.AlignCenter)
        self.kiekisChange.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChange.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tvirtinimasCombo = QComboBox()
        self.tvirtinimasCombo.setEditable(True)
        self.tvirtinimasCombo.setPlaceholderText('Text')
        self.tvirtinimasCombo.addItems(
            ["SRIEGIS", "ASIS", "SESIAKAMPE ASIS"])
        self.tvirtinimasCombo.setCurrentText(self.tvirtinimasRolikai)
        self.tvirtinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tvirtinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tipasCombo = QComboBox()
        self.tipasCombo.setEditable(True)
        self.tipasCombo.setPlaceholderText('Text')
        self.tipasCombo.addItems(
            ["-", "2xD5", "1xD5", "PJ", "AT10", "TIMING BELT P=8 T18", "GUMUOTAS", "PVC", "2xD5 GUMUOTAS", "2xD5 PVC",
             "AT10 GUMUOTAS", "AT10 PVC", "2xZVAIGZDE", "1xD5 GALUOSE", "2xD5 TOLIAU", "D60 PRILAIKANTIS"])
        self.tipasCombo.setCurrentText(self.tipasRolikai)
        self.tipasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tipasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.aprasymasEntry = QLineEdit(self.aprasymasRolikai)
        self.aprasymasEntry.setPlaceholderText('Text')
        self.aprasymasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.aprasymasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasCombo = QComboBox()
        self.projektasCombo.setEditable(True)
        self.projektasCombo.addItems(
            ["ATSARGOS"])
        self.projektasCombo.setCurrentText(self.projektasRolikai)
        self.projektasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.projektasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText('Text')
        self.sandelisCombo.addItems(
            ["BUTRIMONIU", "DRAUGYSTE", "MITUVOS"])
        self.sandelisCombo.setCurrentText(self.sandelisRolikai)
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
        self.vietaCombo.setCurrentText(self.vietaRolikai)
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit(self.komentaraiRolikai)
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.plusBtn = QPushButton()
        self.plusBtn.clicked.connect(self.plus)
        self.plusBtn.setIcon(QIcon("icons/plus.png"))
        self.plusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.plusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.minusBtn = QPushButton()
        self.minusBtn.clicked.connect(self.minus)
        self.minusBtn.setIcon(QIcon("icons/minus.png"))
        self.minusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.minusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateRolikai)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelRolikai)
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

        self.kiekisBtnChange = QHBoxLayout()
        self.kiekisBtnChange.addWidget(self.plusBtn)
        self.kiekisBtnChange.addWidget(self.minusBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasCombo)
        self.widgetLayout.addRow(QLabel("ILGIS: "), self.ilgisEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS +/-: "), self.kiekisChange)
        self.widgetLayout.addRow(QLabel(""), self.kiekisBtnChange)
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

    def minus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data - get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"-{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result
        except:
            pass

    def plus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data + get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"+{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result
        except:
            pass

    def updateRolikai(self):
        global rolikaiId

        pavadinimas1 = self.pavadinimasCombo.currentText().upper()
        ilgis1 = self.ilgisEntry.text()
        kiekis1 = self.kiekisEntry.text()
        tvirtinimas1 = self.tvirtinimasCombo.currentText().upper()
        tipas1 = self.tipasCombo.currentText()
        aprasymas1 = self.aprasymasEntry.text()
        projektas1 = self.projektasCombo.currentText()
        vieta1 = self.vietaCombo.currentText().upper()
        sandelis1 = self.sandelisCombo.currentText().upper()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        update_date1 = self.update_date.text()

        try:
            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()

            query = "UPDATE rolikai SET pavadinimas = %s, ilgis = %s, kiekis = %s, vieta = %s, " \
                    "tvirtinimas = %s, tipas = %s, aprasymas = %s, projektas = %s, komentarai = %s," \
                    "update_date = %s, sandelis = %s where id = %s"
            cur.execute(query, (pavadinimas1, ilgis1, kiekis1, vieta1, tvirtinimas1, tipas1, aprasymas1, projektas1,
                                komentarai1, update_date1, sandelis1, rolikaiId))
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

    def cancelRolikai(self):
        self.close()


class displayPavarosUpdate(QDialog, pt_points):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(750 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update6')
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
        self.pavarosDetails()
        self.widgets()
        self.layouts()

    def pavarosDetails(self):
        global pavarosId

        conn = psycopg2.connect(
            **params
        )
        cur = conn.cursor()

        cur.execute("""SELECT * FROM pavaros WHERE ID=%s""", (pavarosId,))
        pavaros = cur.fetchone()

        self.pavadinimasP = pavaros[1]
        self.gamintojasP = pavaros[2]
        self.tipasP = pavaros[3]
        self.galiaP = pavaros[4]
        self.apsisukimaiP = pavaros[5]
        self.momentasP = pavaros[6]
        self.tvirtinimasP = pavaros[7]
        self.diametrasP = pavaros[8]
        self.kiekisP = pavaros[9]
        self.komentaraiP = pavaros[10]
        self.vietaP = pavaros[11]
        # self.updateP = pavaros[12]
        self.sandelisP = pavaros[13]

    def widgets(self):
        self.pavEntry = QLineEdit(self.pavadinimasP)
        self.pavEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.gamCombo = QComboBox()
        self.gamCombo.setEditable(True)
        self.gamCombo.setPlaceholderText('Text')
        self.gamCombo.addItems(
            ["TECHNOBALT", "HIDROBALT"])
        self.gamCombo.setCurrentText(self.gamintojasP)
        self.gamCombo.setFont(QFont("Times", self.TEXT_PT))
        self.gamCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tipasCombo = QComboBox()
        self.tipasCombo.setEditable(True)
        self.tipasCombo.setPlaceholderText('Text')
        self.tipasCombo.addItems(
            ["TIESINIS", "SLIEKINIS", "KUGINIS"])
        self.tipasCombo.setCurrentText(self.tipasP)
        self.tipasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tipasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.galiaEntry = QLineEdit(self.galiaP)
        self.galiaEntry.setPlaceholderText('Number')
        self.galiaEntry.setFont(QFont("Times", self.TEXT_PT))
        self.galiaEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.apsEntry = QLineEdit(self.apsisukimaiP)
        self.apsEntry.setPlaceholderText('Number')
        self.apsEntry.setFont(QFont("Times", self.TEXT_PT))
        self.apsEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.momEntry = QLineEdit(self.momentasP)
        self.momEntry.setPlaceholderText('Number')
        self.momEntry.setFont(QFont("Times", self.TEXT_PT))
        self.momEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.tvirtinimasCombo = QComboBox()
        self.tvirtinimasCombo.setEditable(True)
        self.tvirtinimasCombo.setPlaceholderText('Text')
        self.tvirtinimasCombo.addItems(
            ["ASIS", "KIAURYME", "KIAURYME+FLANSAS"])
        self.tvirtinimasCombo.setCurrentText(self.tvirtinimasP)
        self.tvirtinimasCombo.setFont(QFont("Times", self.TEXT_PT))
        self.tvirtinimasCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.diamEntry = QLineEdit(self.diametrasP)
        self.diamEntry.setPlaceholderText('Number')
        self.diamEntry.setFont(QFont("Times", self.TEXT_PT))
        self.diamEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit(self.kiekisP)
        self.kiekisEntry.setPlaceholderText('Number')
        self.kiekisEntry.setAlignment(Qt.AlignCenter)
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisChange = QLineEdit()
        self.kiekisChange.setPlaceholderText("Number")
        self.kiekisChange.setAlignment(Qt.AlignCenter)
        self.kiekisChange.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChange.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText('Text')
        self.sandelisCombo.addItems(
            ["BUTRIMONIU", "DRAUGYSTE", "MITUVOS"])
        self.sandelisCombo.setCurrentText(self.sandelisP)
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
        self.vietaCombo.setCurrentText(self.vietaP)
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit(self.komentaraiP)
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.plusBtn = QPushButton()
        self.plusBtn.clicked.connect(self.plus)
        self.plusBtn.setIcon(QIcon("icons/plus.png"))
        self.plusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.plusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.minusBtn = QPushButton()
        self.minusBtn.clicked.connect(self.minus)
        self.minusBtn.setIcon(QIcon("icons/minus.png"))
        self.minusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.minusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updatePavaros)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelPavaros)
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

        self.kiekisBtnChange = QHBoxLayout()
        self.kiekisBtnChange.addWidget(self.plusBtn)
        self.kiekisBtnChange.addWidget(self.minusBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavEntry)
        self.widgetLayout.addRow(QLabel("GAMINTOJAS: "), self.gamCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("TIPAS: "), self.tipasCombo)
        self.widgetLayout.addRow(QLabel("GALIA: "), self.galiaEntry)
        self.widgetLayout.addRow(QLabel("APSISUKIMAI: "), self.apsEntry)
        self.widgetLayout.addRow(QLabel("MOMENTAS: "), self.momEntry)
        self.widgetLayout.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasCombo)
        self.widgetLayout.addRow(QLabel("DIAMETRAS: "), self.diamEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS +/-: "), self.kiekisChange)
        self.widgetLayout.addRow(QLabel(""), self.kiekisBtnChange)
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

    def minus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data - get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"-{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result
        except:
            pass

    def plus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data + get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"+{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result
        except:
            pass

    def updatePavaros(self):
        global pavarosId

        pavadinimas1 = self.pavEntry.text().upper()
        gamintojas1 = self.gamCombo.currentText().upper()
        tipas1 = self.tipasCombo.currentText().upper()
        galia1 = self.galiaEntry.text()
        apsisukimai1 = self.apsEntry.text()
        momentas1 = self.momEntry.text()
        tvirtinimas1 = self.tvirtinimasCombo.currentText().upper()
        diametras1 = self.diamEntry.text()
        kiekis1 = self.kiekisEntry.text()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        sandelis1 = self.sandelisCombo.currentText()
        vieta1 = self.vietaCombo.currentText()
        update_date1 = self.update_date.text()

        try:
            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()

            query = "UPDATE pavaros SET pavadinimas = %s, gamintojas = %s, tipas = %s, galia = %s, " \
                    "apsisukimai = %s, momentas = %s, tvirtinimas = %s, diametras = %s, kiekis = %s, " \
                    "komentarai = %s, vieta = %s, update_date = %s , sandelis = %s where id = %s"
            cur.execute(query, (pavadinimas1, gamintojas1, tipas1, galia1, apsisukimai1, momentas1, tvirtinimas1,
                                diametras1, kiekis1, komentarai1, vieta1, update_date1, sandelis1, pavarosId))
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

    def cancelPavaros(self):
        self.close()


class displayStelazasUpdate(QDialog, pt_points):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(400 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update4')
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
        self.stelazasDetails()
        self.widgets()
        self.layouts()

    def stelazasDetails(self):
        global stelazasId

        con = psycopg2.connect(
            **params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM stelazas WHERE ID = %s""", (stelazasId,))
        stelazas = c.fetchone()
        self.stPavadinimas = stelazas[1]
        self.stProjektas = stelazas[2]
        self.stSandelis = stelazas[3]
        self.stVieta = stelazas[4]
        self.stKomentarai = stelazas[5]

    def widgets(self):
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.addItems(["ROLIKAI", "VARIKLIAI", "DETALES IR KT.", "FESTO",
                                        "ATSARGOS", "EL. KOMPONENTAI"])
        self.pavadiniamsEntry.setCurrentText(self.stPavadinimas)
        self.pavadiniamsEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavadiniamsEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setText(self.stProjektas)
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.addItems(["BUTRIMONIU", "DRAUGYSTE", "MITUVOS"])
        self.sandelisCombo.setCurrentText(self.stSandelis)
        self.sandelisCombo.setFont(QFont("Times", self.TEXT_PT))
        self.sandelisCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.addItems(
            ["KONTORA", "ZONA-1", "ZONA-2", "ZONA-3", "ZONA-4", "ZONA-5", "ZONA-6", "ZONA-7", "ZONA-8", "ZONA-9",
             "ZONA-10",
             "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
             "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4", "STELAZAS-5", "STELAZAS-6", "STELAZAS-7",
             "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11", "STELAZAS-12", "STELAZAS-13", "STELAZAS-14",
             "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setCurrentText(self.stVieta)
        self.vietaCombo.setFont(QFont("Times", self.TEXT_PT))
        self.vietaCombo.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setText(self.stKomentarai)
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateStelazas1)
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.setFont(QFont("Times", self.TEXT_PT))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeUpdateStelazas1)
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

    def updateStelazas1(self):
        global stelazasId
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

            c.execute(
                "UPDATE stelazas SET pavadinimas = %s, projektas = %s, sandelis = %s, "
                "vieta = %s, komentarai = %s, update_date = %s where id = %s",
                (pavadinimas1, projektas1, sandelis1, vieta1, komentarai1, update_date1, stelazasId))
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

    def closeUpdateStelazas1(self):
        self.close()


class displaySanaudosUpdate(QDialog, pt_points):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(400 * self.scale_factor), int(500 * self.scale_factor))
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update3')
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
        self.sanaudosDetails()
        self.widgets()
        self.layouts()

    def sanaudosDetails(self):
        global sanaudosId

        con = psycopg2.connect(
            **params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM sanaudos WHERE ID = %s""", (sanaudosId,))
        atsargos = c.fetchone()
        self.sanaudosPavadinimas = atsargos[1]
        self.sanaudosProjektas = atsargos[2]
        self.sanaudosKiekis = atsargos[3]
        self.sanaudosVnt = atsargos[4]
        self.sanaudosKomentarai = atsargos[5]
        self.sanaudosMetai = atsargos[6]

    def widgets(self):
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.addItems(["HABASIT", "PROFILIAI", "UZDENGIMAI", "GALINUKAS", "PRILAIKANTIS",
                                        "SKRIEMULYS", "SKRIEMULIO ASIS", "ROLIKAI", "VARIKLIAI", 'PLASTIKINES IVORES'])
        self.pavadiniamsEntry.setCurrentText(self.sanaudosPavadinimas)
        self.pavadiniamsEntry.setFont(QFont("Times", self.TEXT_PT))
        self.pavadiniamsEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.projektasEntry = QLineEdit(self.sanaudosProjektas)
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", self.TEXT_PT))
        self.projektasEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisEntry = QLineEdit(self.sanaudosKiekis)
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setAlignment(Qt.AlignCenter)
        self.kiekisEntry.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.vntEntry = QComboBox()
        self.vntEntry.setEditable(True)
        self.vntEntry.addItems(["m.", "vnt."])
        self.vntEntry.setCurrentText(self.sanaudosVnt)
        self.vntEntry.lineEdit().setAlignment(Qt.AlignCenter)
        self.vntEntry.setFont(QFont("Times", self.TEXT_PT))
        self.vntEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisChange = QLineEdit()
        self.kiekisChange.setPlaceholderText("Number")
        self.kiekisChange.setAlignment(Qt.AlignCenter)
        self.kiekisChange.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChange.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.kiekisChangeVnt = QLineEdit()
        self.kiekisChangeVnt.setReadOnly(False)
        self.kiekisChangeVnt.setStyleSheet("QLineEdit{background: darkgrey; color: black}")
        self.kiekisChangeVnt.setText(self.sanaudosVnt)
        self.kiekisChangeVnt.setAlignment(Qt.AlignCenter)
        self.kiekisChangeVnt.setFont(QFont("Times", self.TEXT_PT))
        self.kiekisChangeVnt.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.komentaraiEntry = QTextEdit(self.sanaudosKomentarai)
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.metaiEntry = QLineEdit(self.sanaudosMetai)
        self.metaiEntry.setPlaceholderText("Text")
        self.metaiEntry.setFont(QFont("Times", self.TEXT_PT))
        self.metaiEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.plusBtn = QPushButton()
        self.plusBtn.clicked.connect(self.plus)
        self.plusBtn.setIcon(QIcon("icons/plus.png"))
        self.plusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.plusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.minusBtn = QPushButton()
        self.minusBtn.clicked.connect(self.minus)
        self.minusBtn.setIcon(QIcon("icons/minus.png"))
        self.minusBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.minusBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateSanaudos)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelSanaudos)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame.setFont(QFont("Times", self.TEXT_PT))

        self.kiekisBox = QHBoxLayout()
        self.kiekisBox.addWidget(self.kiekisEntry, 50)
        self.kiekisBox.addWidget(self.vntEntry, 50)

        self.kiekisBoxChange = QHBoxLayout()
        self.kiekisBoxChange.addWidget(self.kiekisChange, 50)
        self.kiekisBoxChange.addWidget(self.kiekisChangeVnt, 50)

        self.kiekisBtnChange = QHBoxLayout()
        self.kiekisBtnChange.addWidget(self.plusBtn)
        self.kiekisBtnChange.addWidget(self.minusBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisBox)
        self.widgetLayout.addRow(QLabel("KIEKIS +/-: "), self.kiekisBoxChange)
        self.widgetLayout.addRow(QLabel(""), self.kiekisBtnChange)
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

    def minus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data - get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"-{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result

        except:
            pass

    def plus(self):
        try:
            get_kiekis_data = int(self.kiekisEntry.text())
            get_kiekis_minus = int(self.kiekisChange.text())
            kiekis_count = (get_kiekis_data + get_kiekis_minus)
            kiekis_result = self.kiekisEntry.setText(f"{kiekis_count}")
            self.kiekisChange.setPlaceholderText(f"+{self.kiekisChange.text()}")
            self.kiekisChange.clear()
            return kiekis_result

        except:
            pass

    def updateSanaudos(self):
        global sanaudosId
        pavadinimas1 = self.pavadiniamsEntry.currentText().upper()
        projektas1 = self.projektasEntry.text().upper()
        kiekis1 = self.kiekisEntry.text()
        vnt1 = self.vntEntry.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        metai1 = self.metaiEntry.text()
        update_date1 = self.update_date.text()

        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute(
                "UPDATE sanaudos SET pavadinimas = %s, projektas = %s, kiekis = %s, mat_vnt = %s, komentaras = %s, "
                "metai = %s, update_date = %s where id = %s",
                (pavadinimas1, projektas1, kiekis1, vnt1, komentarai1, metai1, update_date1, sanaudosId))
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

    def cancelSanaudos(self):
        self.close()


class openBrokas(QDialog, pt_points):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BROKAS/TRŪKUMAS")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(int(300 / self.scale_factor), int(200 / self.scale_factor),
                         int(600 * self.scale_factor), int(400 * self.scale_factor))
        self.setFixedSize(self.size())

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Picture1')

        # pozition and size
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except Exception as error:
            print(f"{error}")

        self.UI()

    def UI(self):
        self.brokasDetails()
        self.widgets()
        self.layouts()

    def brokasDetails(self):
        global uzsakymaiId

        try:

            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()

            cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
            uzsakymai = cur.fetchone()

            self.brokas = uzsakymai[11]

            conn.close()

            self.show()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please select ROW you want to open.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def widgets(self):
        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setText(self.brokas)
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", self.TEXT_PT))

        self.update_date = QLineEdit()
        self.update_date.setText(f"{datetime.toPyDate()}")

        self.okBtn = QPushButton("UPDATE")
        self.okBtn.clicked.connect(self.updateBrokas)
        self.okBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelBrokas)
        self.cancelBtn.setFont(QFont("Times", self.TEXT_BUTTON_PT))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

    def layouts(self):
        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.komentaraiEntry)
        self.mainLayout.addWidget(self.okBtn)
        self.mainLayout.addWidget(self.cancelBtn)

        self.setLayout(self.mainLayout)

    def updateBrokas(self):
        global uzsakymaiId

        komentarai1 = str(self.komentaraiEntry.toPlainText())
        update_date1 = self.update_date.text()

        try:
            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()

            query = "UPDATE uzsakymai SET brokas = %s, update_date = %s where id = %s"
            cur.execute(query, (komentarai1, update_date1, uzsakymaiId))
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

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def cancelBrokas(self):
        self.close()


# class openPic(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PICTURE")
#         self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
#         self.setGeometry(300, 200, 800, 600)
#         # self.setFixedSize(self.size())
#
#         # creates registry folder and subfolder
#         self.settings = QSettings('Bardakas', 'Picture1')
#         # pozition and size
#         try:
#             self.resize(self.settings.value('window size'))
#             self.move(self.settings.value('window position'))
#
#         except:
#             pass
#
#         global atsargosId
#
#         try:
#             con = psycopg2.connect(
#                 **params
#             )
#
#             c = con.cursor()
#
#             c.execute("""SELECT * FROM atsargos WHERE ID = %s""", (atsargosId,))
#             atsargos = c.fetchone()
#
#             self.atsargosNuotrauka = atsargos[6]
#
#             con.close()
#
#         except (Exception, psycopg2.Error) as error:
#             msg = QMessageBox()
#             msg.setWindowTitle("ERROR...")
#             msg.setText(f"Please select ROW you want to open picture.")
#             msg.setIcon(QMessageBox.Information)
#             msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
#
#             Bardakas_style_gray.msgsheetstyle(msg)
#
#             x = msg.exec_()
#
#         my_str = ""
#
#         if self.atsargosNuotrauka != my_str:
#             self.browser = QWebEngineView()
#             self.browser.setUrl(QUrl(self.atsargosNuotrauka))
#             self.mainLayout = QHBoxLayout()
#             self.mainLayout.addWidget(self.browser)
#             self.setLayout(self.mainLayout)
#
#             self.show()
#
#         else:
#             msg = QMessageBox()
#             msg.setWindowTitle("ERROR...")
#             msg.setText("NO FILE...")
#             msg.setIcon(QMessageBox.Information)
#             msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
#
#             Bardakas_style_gray.msgsheetstyle(msg)
#
#             x = msg.exec_()
#
#     def closeEvent(self, event):
#         self.settings.setValue('window size', self.size())
#         self.settings.setValue('window position', self.pos())
def main():
    # # SAME AS CHANGING ON python.exe DPI aware to Application ---->>> ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)

    App = QApplication(sys.argv)

    splash_pix = QtGui.QPixmap('icons/loadscreen.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    # Add fade to splashscreen
    currentOpacity = 0.0
    step = 0.01
    splash.setWindowOpacity(currentOpacity)
    splash.show()
    while currentOpacity < 1:
        splash.setWindowOpacity(currentOpacity)
        time.sleep(step)  # Gradually appears
        currentOpacity += step
    time.sleep(0.2)  # hold image on screen for a while
    splash.close()  # close the splash screen

    window = MainMenu()

    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
