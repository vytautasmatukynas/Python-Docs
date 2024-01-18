import os
import sys
import webbrowser
import time
import subprocess

import psycopg2
import requests
import xlwt
from PyQt5 import QtWidgets, QtCore, QtPrintSupport, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

import Bardakas_style_gray

import db_conn

uzsakymai_db_params = db_conn.uzsakymai_db
komponentai_db_params = db_conn.komponentai_db
rolikai_db_params = db_conn.rolikai_db
sanaudos_db_params = db_conn.sanaudos_db
stelazas_db_params = db_conn.stelazas_db

InnoSetupID = 'AppId={{DB4A3A4F-7520-4796-BD06-783C3BE4449C}'
__author__ = 'Vytautas Matukynas'
__copyright__ = 'Copyright (C) 2022, Vytautas Matukynas'
__credits__ = ['Vytautas Matukynas']
__license__ = 'Vytautas Matukynas'
__version__ = '3.42'
__maintainer__ = 'Vytautas Matukynas'
__email__ = 'vytautas.matukynas@gmail.com'
__status__ = 'Alpha'
_AppName_ = 'Bardakas'

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()


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

        # MainClass functions
        self.UI()
        self.show()

    # Close widnow and open selected window
    # @pyqtSlot()
    # def Switch_Atsargos(self):
    #     self.Switch_Atsargos1 = Bardakas_atsargos.MainMenuAtsargos()
    #     self.Switch_Atsargos1.show()
    #     self.close()
    #
    # @pyqtSlot()
    # def Switch_Rolikai(self):
    #     self.Switch_Rolikai1 = Bardakas_rolikai.MainMenu()
    #     self.Switch_Rolikai1.show()
    #     self.close()
    #
    # @pyqtSlot()
    # def Switch_Sanaudos(self):
    #     self.Switch_Sanaudos1 = Bardakas_sanaudos.MainMenuSanaudos()
    #     self.Switch_Sanaudos1.show()
    #     self.close()
    #
    # @pyqtSlot()
    # def Switch_Stelazas(self):
    #     self.Switch_Stelazas1 = Bardakas_stelazas.MainMenu()
    #     self.Switch_Stelazas1.show()
    #     self.close()

    def UI(self):
        """Main Menu bar"""
        menuBar = self.menuBar()

        # File bar
        file = menuBar.addMenu("File")
        # Submenu bar
        new = QAction("New", self)
        new.triggered.connect(self.add_selected)
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
        refresh = QAction("Refresh", self)
        refresh.triggered.connect(self.refresh_selected)
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
        Open = menuBar.addMenu("Open")
        StelazasMap = QAction("Sandelio Zonos", self)
        StelazasMap.triggered.connect(self.stelazas_map)
        StelazasMap.setShortcut("Alt+P")
        StelazasMap.setIcon(QIcon("icons/plan.png"))
        Open.addAction(StelazasMap)

        # Setting bar
        Settings = menuBar.addMenu("Settings")

        Style = Settings.addMenu("Style")
        Style.setIcon(QIcon("icons/design.png"))

        Group = QActionGroup(Style)

        style2 = QAction("Gandalf the Grey", self)
        style2.setCheckable(True)
        style2.setChecked(True)
        Style.addAction(style2)

        Group.addAction(style2)

        # Check only one item in GroupBox
        Group.setExclusive(True)

        # Calculators bar
        Calculators = menuBar.addMenu("Calculators")
        normavimas = QAction("Machining Time", self)
        normavimas.setIcon(QIcon("icons/Machining.png"))
        Calculators.addAction(normavimas)
        guoliu_tolerancijos = QAction("Press Fit Tolerance", self)
        guoliu_tolerancijos.setIcon(QIcon("icons/Tolerance.png"))
        Calculators.addAction(guoliu_tolerancijos)
        conveyor_design = QAction("Conveyor Design", self)
        conveyor_design.setIcon(QIcon("icons/conveyor.png"))
        Calculators.addAction(conveyor_design)

        # Help bar
        help = menuBar.addMenu("Help")

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
        SQL = QAction("Edit SQL", self)
        SQL.triggered.connect(self.edit_sql)
        help.addAction(Info)

        # Function that starts at starts
        self.widgets()
        self.layouts()
        self.toolbar()
        self.displayUzsakymai()
        Bardakas_style_gray.SheetStyle(self)
        self.updateInfoOnStart()

    def edit_sql(self):
        """edit sql table in TERMINAL"""
        pass

    def updateInfoOnStart(self):
        """version check"""
        try:
            # Version file link
            response = requests.get(
                'https://gist.githubusercontent.com/heroik9/9b0f8d1efa983a66eb021602314e1928/raw/version')
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
                        'https://drive.google.com/file/d/1r6hmP3FfwW31Iqwd55nhdqgH8PDYLNRM/view?usp=sharing')
                    self.close()

                else:
                    pass

            else:
                pass

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

    def updateInfo(self):
        try:
            response = requests.get(
                'https://gist.githubusercontent.com/heroik9/9b0f8d1efa983a66eb021602314e1928/raw/version')
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
                        'https://drive.google.com/file/d/1r6hmP3FfwW31Iqwd55nhdqgH8PDYLNRM/view?usp=sharing')
                    self.close()
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
            msg.setIcon(QMessageBox.Information)
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
                    "BARDAKAS version 3.0")
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

        Bardakas_style_gray.msgsheetstyle(msg)

        x = msg.exec_()

    def widgets(self):
        """Tables"""
        # UZSAKYMAI TABLE
        self.uzsakymuTable = QTableWidget()
        self.uzsakymuTable.setColumnCount(8)
        self.uzsakymuTable.setColumnHidden(0, True)
        self.uzsakymuTable.setSortingEnabled(True)
        # self.uzsakymuTable.setColumnWidth(1, 100)
        self.uzsakymuTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.uzsakymuTable.setHorizontalHeaderItem(1, QTableWidgetItem("IMONE"))
        self.uzsakymuTable.setHorizontalHeaderItem(2, QTableWidgetItem("BRAIZE"))
        self.uzsakymuTable.setHorizontalHeaderItem(3, QTableWidgetItem("PROJEKTAS"))
        self.uzsakymuTable.setHorizontalHeaderItem(4, QTableWidgetItem("UZSAKYMO\nPAVADINIMAS"))
        self.uzsakymuTable.setHorizontalHeaderItem(5, QTableWidgetItem("TERMINAS"))
        self.uzsakymuTable.setHorizontalHeaderItem(6, QTableWidgetItem("STATUSAS"))
        self.uzsakymuTable.setHorizontalHeaderItem(7, QTableWidgetItem("KOMENTARAI"))
        self.uzsakymuTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.uzsakymuTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.uzsakymuTable.horizontalHeader().setHighlightSections(False)
        self.uzsakymuTable.horizontalHeader().setDisabled(True)
        self.uzsakymuTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.uzsakymuTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.uzsakymuTable.doubleClicked.connect(self.selectUzsakymai)
        self.uzsakymuTable.clicked.connect(self.uzsakymusdetales_delete)

        # ATSARGOS TABLE
        self.atsarguTable = QTableWidget()
        self.atsarguTable.setColumnCount(7)
        self.atsarguTable.setSortingEnabled(True)
        self.atsarguTable.setColumnHidden(0, True)
        self.atsarguTable.setColumnHidden(6, True)
        self.atsarguTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.atsarguTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.atsarguTable.setHorizontalHeaderItem(2, QTableWidgetItem("VIETA"))
        self.atsarguTable.setHorizontalHeaderItem(3, QTableWidgetItem("KIEKIS"))
        self.atsarguTable.setHorizontalHeaderItem(4, QTableWidgetItem("MATAVIMO\nVIENETAI"))
        self.atsarguTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.atsarguTable.setHorizontalHeaderItem(6, QTableWidgetItem("NUOTRAUKA"))
        self.atsarguTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atsarguTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.atsarguTable.horizontalHeader().setHighlightSections(False)
        self.atsarguTable.horizontalHeader().setDisabled(True)
        self.atsarguTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.atsarguTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.atsarguTable.clicked.connect(self.atsargostable_delete)
        self.atsarguTable.doubleClicked.connect(self.selectAtsargos)

        # SANAUNOS TABLE
        self.sanaudosTable = QTableWidget()
        self.sanaudosTable.setColumnCount(7)
        self.sanaudosTable.setSortingEnabled(True)
        self.sanaudosTable.setColumnHidden(0, True)
        self.sanaudosTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.sanaudosTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.sanaudosTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.sanaudosTable.setHorizontalHeaderItem(3, QTableWidgetItem("KIEKIS"))
        self.sanaudosTable.setHorizontalHeaderItem(4, QTableWidgetItem("MATAVIMO\nVIENETAI"))
        self.sanaudosTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.sanaudosTable.setHorizontalHeaderItem(6, QTableWidgetItem("METAI"))
        self.sanaudosTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.sanaudosTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.sanaudosTable.horizontalHeader().setHighlightSections(False)
        self.sanaudosTable.horizontalHeader().setDisabled(True)
        self.sanaudosTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.uzsakymuTable.setColumnWidth(6, 100)
        self.sanaudosTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.sanaudosTable.clicked.connect(self.sanaudostable_delete)
        self.sanaudosTable.doubleClicked.connect(self.selectSanaudos)

        # STELAZAS TABLE
        self.stelazasTable = QTableWidget()
        self.stelazasTable.setColumnCount(6)
        self.stelazasTable.setColumnHidden(0, True)
        self.stelazasTable.setSortingEnabled(True)
        # self.stelazasTable.setColumnWidth(1, 50)
        self.stelazasTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.stelazasTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.stelazasTable.setHorizontalHeaderItem(2, QTableWidgetItem("PROJEKTAS"))
        self.stelazasTable.setHorizontalHeaderItem(3, QTableWidgetItem("SANDELIS"))
        self.stelazasTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.stelazasTable.setHorizontalHeaderItem(5, QTableWidgetItem("KOMENTARAI"))
        self.stelazasTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.stelazasTable.horizontalHeader().setHighlightSections(False)
        self.stelazasTable.horizontalHeader().setDisabled(True)
        self.stelazasTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.stelazasTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.stelazasTable.doubleClicked.connect(self.selectStelazas)
        self.stelazasTable.clicked.connect(self.stelazastable_delete)

        # ROLIKAI TABLE
        self.rolikaiTable = QTableWidget()
        self.rolikaiTable.setColumnCount(8)
        self.rolikaiTable.setColumnHidden(0, True)
        self.rolikaiTable.setSortingEnabled(True)
        self.rolikaiTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.rolikaiTable.setHorizontalHeaderItem(1, QTableWidgetItem("PAVADINIMAS"))
        self.rolikaiTable.setHorizontalHeaderItem(2, QTableWidgetItem("ILGIS"))
        self.rolikaiTable.setHorizontalHeaderItem(3, QTableWidgetItem("KIEKIS"))
        self.rolikaiTable.setHorizontalHeaderItem(4, QTableWidgetItem("VIETA"))
        self.rolikaiTable.setHorizontalHeaderItem(5, QTableWidgetItem("TVIRTINIMAS"))
        self.rolikaiTable.setHorizontalHeaderItem(6, QTableWidgetItem("TIPAS"))
        self.rolikaiTable.setHorizontalHeaderItem(7, QTableWidgetItem("KOMENTARAI"))
        self.rolikaiTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rolikaiTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.rolikaiTable.horizontalHeader().setHighlightSections(False)
        self.rolikaiTable.horizontalHeader().setDisabled(True)
        self.rolikaiTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.rolikaiTable.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.rolikaiTable.doubleClicked.connect(self.selectRolikai)
        self.rolikaiTable.clicked.connect(self.deleteRolikai_Select)

        # Align data in table
        delegate = AlignDelegate()

        # for column
        self.uzsakymuTable.setItemDelegateForColumn(1, delegate)
        self.uzsakymuTable.setItemDelegateForColumn(2, delegate)
        self.uzsakymuTable.setItemDelegateForColumn(3, delegate)
        self.uzsakymuTable.setItemDelegateForColumn(4, delegate)
        self.uzsakymuTable.setItemDelegateForColumn(5, delegate)
        self.uzsakymuTable.setItemDelegateForColumn(6, delegate)

        self.atsarguTable.setItemDelegateForColumn(1, delegate)
        self.atsarguTable.setItemDelegateForColumn(2, delegate)
        self.atsarguTable.setItemDelegateForColumn(3, delegate)
        self.atsarguTable.setItemDelegateForColumn(4, delegate)
        self.atsarguTable.setItemDelegateForColumn(6, delegate)

        self.sanaudosTable.setItemDelegateForColumn(1, delegate)
        self.sanaudosTable.setItemDelegateForColumn(2, delegate)
        self.sanaudosTable.setItemDelegateForColumn(3, delegate)
        self.sanaudosTable.setItemDelegateForColumn(4, delegate)
        self.sanaudosTable.setItemDelegateForColumn(6, delegate)

        self.stelazasTable.setItemDelegateForColumn(1, delegate)
        self.stelazasTable.setItemDelegateForColumn(2, delegate)
        self.stelazasTable.setItemDelegateForColumn(3, delegate)
        self.stelazasTable.setItemDelegateForColumn(4, delegate)

        self.rolikaiTable.setItemDelegateForColumn(1, delegate)
        self.rolikaiTable.setItemDelegateForColumn(2, delegate)
        self.rolikaiTable.setItemDelegateForColumn(3, delegate)
        self.rolikaiTable.setItemDelegateForColumn(4, delegate)
        self.rolikaiTable.setItemDelegateForColumn(5, delegate)
        self.rolikaiTable.setItemDelegateForColumn(6, delegate)

        # for all columns
        # self.uzsakymuTable.setItemDelegate(delegate)
        # self.atsarguTable.setItemDelegate(delegate)
        # self.sanaudosTable.setItemDelegate(delegate)
        # self.stelazasTable.setItemDelegate(delegate)
        # self.rolikaiTable.setItemDelegate(delegate)

        # Search widget
        self.searchEntry1 = QLineEdit()
        self.searchEntry1.setFixedHeight(25)
        self.searchEntry1.setPlaceholderText('SEARCH...')
        self.searchEntry1.textChanged.connect(self.searchTables)

        self.searchButton1 = QPushButton("CANCEL")
        self.searchButton1.setFixedWidth(90)
        self.searchButton1.setFixedHeight(25)
        self.searchButton1.clicked.connect(self.clearSearchEntry1)
        self.searchButton1.setFont(QFont("Times", 10))

        # Treeview table
        self.treeTable = QTreeWidget()
        self.treeTable.setAnimated(True)
        self.treeTable.setHeaderHidden(True)
        self.treeTable.setColumnCount(1)
        self.treeTable.setFixedWidth(150)

        self.uzsakymaiSelect = QTreeWidgetItem(self.treeTable, ["UZSAKYMAI"])
        # self.uzsakymaiSelect.setExpanded(True)
        self.uzsakymaiSelect.setSelected(True)
        self.atsargosSelect = QTreeWidgetItem(self.treeTable, ["ATSARGOS"])
        # self.atsargosSelect.setExpanded(True)
        self.sanaudosSelect = QTreeWidgetItem(self.treeTable, ["SANAUDOS"])
        self.stelazasSelect = QTreeWidgetItem(self.treeTable, ["SANDELIS"])
        self.rolikaiSelect = QTreeWidgetItem(self.treeTable, ["ROLIKAI"])
        # self.rolikaiSelect.setExpanded(True)

        self.uzsakymaiSelect1 = ["PAGAMINTA", "GAMINA", "BROKUOTA"]
        for item1 in self.uzsakymaiSelect1:
            self.uzsakymaiSelect.addChild(QTreeWidgetItem([item1]))
        atsargosSelect1 = ["EQ", "KOMPONENTAI", "PAVAROS"]
        for item2 in atsargosSelect1:
            self.atsargosSelect.addChild(QTreeWidgetItem([item2]))
        rolikaiSelect1 = ["RM", "PAPRASTAS", "POSUKIS", "RM-POSUKIS"]
        for item3 in rolikaiSelect1:
            self.rolikaiSelect.addChild(QTreeWidgetItem([item3]))

        self.treeTable.clicked.connect(self.listTables)

        # Check box for sorting
        self.sortCheck = QCheckBox("Enable header", self)
        self.sortCheck.stateChanged.connect(self.enable_sorting)

    def enable_sorting(self):
        if self.sortCheck.isChecked():
            self.uzsakymuTable.horizontalHeader().setDisabled(False)
            self.atsarguTable.horizontalHeader().setDisabled(False)
            self.sanaudosTable.horizontalHeader().setDisabled(False)
            self.stelazasTable.horizontalHeader().setDisabled(False)
            self.rolikaiTable.horizontalHeader().setDisabled(False)

        else:
            self.uzsakymuTable.horizontalHeader().setDisabled(True)
            self.atsarguTable.horizontalHeader().setDisabled(True)
            self.sanaudosTable.horizontalHeader().setDisabled(True)
            self.stelazasTable.horizontalHeader().setDisabled(True)
            self.rolikaiTable.horizontalHeader().setDisabled(True)

    def contextMenuEvent(self, event):
        """Right mouse button select"""
        if self.uzsakymuTable.underMouse():
            try:
                global uzsakymaiId
                listUzsakymai = []
                for i in range(0, 7):
                    listUzsakymai.append(self.uzsakymuTable.item(self.uzsakymuTable.currentRow(), i).text())

                uzsakymaiId = listUzsakymai[0]
            except:
                pass

            # Left mouse button table
            contextMenu = QMenu(self)

            openBreziniai = contextMenu.addAction("Drawings")
            openBreziniai.triggered.connect(self.openFolder)
            openBreziniai.setShortcut("Alt+B")
            openBreziniai.setIcon(QIcon("icons/drawings.png"))
            contextMenu.addSeparator()
            openSarasas = contextMenu.addAction("List")
            openSarasas.triggered.connect(self.openFile)
            openSarasas.setShortcut("Alt+L")
            openSarasas.setIcon(QIcon("icons/files.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.funcAddUzsakymas)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.displayUzsakymai)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteBreziniai = contextMenu.addAction("Delete")
            deleteBreziniai.triggered.connect(self.deleteUzsakymas_sh)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.atsarguTable.underMouse():
            try:
                global atsargosId
                listAtsargos = []
                for i in range(0, 6):
                    listAtsargos.append(self.atsarguTable.item(self.atsarguTable.currentRow(), i).text())

                atsargosId = listAtsargos[0]
            except:
                pass

            contextMenu = QMenu(self)
            openPicture = contextMenu.addAction("Picture")
            openPicture.triggered.connect(self.openPicture)
            openPicture.setShortcut("Alt+N")
            openPicture.setIcon(QIcon("icons/image.png"))
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.funcAddAtsargos)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.displayAtsargos)
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            Refresh2.setShortcut("F5")
            contextMenu.addSeparator()
            deleteAtsargos = contextMenu.addAction("Delete")
            deleteAtsargos.triggered.connect(self.deleteAtsargos_sh)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.sanaudosTable.underMouse():
            try:
                global sanaudosId
                listSanaudos = []
                for i in range(0, 6):
                    listSanaudos.append(self.sanaudosTable.item(self.sanaudosTable.currentRow(), i).text())

                sanaudosId = listSanaudos[0]
            except:
                pass

            contextMenu = QMenu(self)

            bendros_sanaudos = contextMenu.addAction("Sanaudos")
            bendros_sanaudos.triggered.connect(self.sanaudos_chart)
            bendros_sanaudos.setIcon(QIcon("icons/chart.png"))
            bendros_sanaudos.setShortcut("Ctrl+L")
            contextMenu.addSeparator()
            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.funcAddSanaudos)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.displaySanaudos)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteSanaudos = contextMenu.addAction("Delete")
            deleteSanaudos.triggered.connect(self.deletesanaudos_sh)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.stelazasTable.underMouse():
            try:
                global stelazasId
                listStelazas = []
                for i in range(0, 5):
                    listStelazas.append(self.stelazasTable.item(self.stelazasTable.currentRow(), i).text())

                stelazasId = listStelazas[0]
            except:
                pass

            contextMenu = QMenu(self)

            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.funcAddStelazas)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.displayStelazas)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteStelazas = contextMenu.addAction("Delete")
            deleteStelazas.triggered.connect(self.deletestelazas_sh)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        elif self.rolikaiTable.underMouse():
            try:
                global rolikaiId
                listRolikai = []
                for i in range(0, 7):
                    listRolikai.append(self.rolikaiTable.item(self.rolikaiTable.currentRow(), i).text())

                rolikaiId = listRolikai[0]
            except:
                pass

            contextMenu = QMenu(self)

            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.funcAddRolikai)
            new2.setShortcut("Ctrl+N")
            contextMenu.addSeparator()
            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.displayRolikai)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("icons/refresh.png"))
            contextMenu.addSeparator()
            deleteRolikai = contextMenu.addAction("Delete")
            deleteRolikai.triggered.connect(self.deleteRolikai_Combo)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def layouts(self):
        """App layouts"""
        self.mainLayout = QVBoxLayout()

        self.searchLayout = QHBoxLayout()

        self.bottomLayout = QHBoxLayout()

        self.mainLeftLayout = QVBoxLayout()
        self.LeftLayoutTop = QVBoxLayout()
        self.LeftLayoutBottom = QVBoxLayout()

        self.mainRightLayout = QStackedLayout()

        # Right side
        self.mainRightLayout.addWidget(self.uzsakymuTable)
        self.mainRightLayout.addWidget(self.atsarguTable)
        self.mainRightLayout.addWidget(self.sanaudosTable)
        self.mainRightLayout.addWidget(self.stelazasTable)
        self.mainRightLayout.addWidget(self.rolikaiTable)
        self.mainRightLayout.setCurrentIndex(0)

        # Left side
        self.LeftLayoutTop.addWidget(self.treeTable)
        self.LeftLayoutBottom.addWidget(self.sortCheck)
        self.mainLeftLayout.addLayout(self.LeftLayoutTop, 90)
        self.mainLeftLayout.addLayout(self.LeftLayoutBottom, 10)

        # Search layout
        self.searchLayout.addWidget(self.searchButton1)
        self.searchLayout.addWidget(self.searchEntry1)

        self.bottomLayout.addLayout(self.mainLeftLayout)
        self.bottomLayout.addLayout(self.mainRightLayout)

        self.mainLayout.addLayout(self.searchLayout, 10)
        self.mainLayout.addLayout(self.bottomLayout, 90)

        # Central_widget to view widgets
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.central_widget)

    def toolbar(self):
        """toolbar buttons"""
        self.tb = self.addToolBar("Open tb")
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb.setIconSize(QtCore.QSize(17, 17))

        self.add_tb = QAction(QIcon("icons/add.png"), "Add", self)
        self.tb.addAction(self.add_tb)
        self.add_tb.triggered.connect(self.addTables)

        self.delete_tb = QAction(QIcon("icons/delete.png"), "Delete", self)
        self.tb.addAction(self.delete_tb)
        self.delete_tb.triggered.connect(self.deleteTables)

        self.tb.addSeparator()

        self.refresh_tb = QAction(QIcon("icons/refresh.png"), "Refresh", self)
        self.tb.addAction(self.refresh_tb)
        self.refresh_tb.triggered.connect(self.refreshTables)

        self.tb.addSeparator()

        self.save_tb = QAction(QIcon("icons/save.png"), "Save", self)
        self.tb.addAction(self.save_tb)
        self.save_tb.triggered.connect(self.save)

        self.saveAs_tb = QAction(QIcon("icons/saveas.png"), "Save As...", self)
        self.tb.addAction(self.saveAs_tb)
        self.saveAs_tb.triggered.connect(self.saveAs)

        self.tb.addSeparator()

        self.openStelazai = QAction(QIcon("icons/plan.png"), "Sandelio Zonos", self)
        self.tb.addAction(self.openStelazai)
        self.openStelazai.triggered.connect(self.stelazas_map)

    def stelazas_map(self):
        try:
            exePath = "Map\Stelazas_map.exe"
            subprocess.Popen(exePath)
        # try:
        #     os.system("map\Stelazas_map.exe")
        except:
            pass

    def funcAddUzsakymas(self):
        self.window = AddUzsakymas1()
        # Refresh table after executing QDialog .exec_
        self.window.exec_()
        self.displayUzsakymai()

    def funcAddAtsargos(self):
        self.newAtsargos = AddAtsargos2()
        self.newAtsargos.exec_()
        self.displayAtsargos()

    def funcAddSanaudos(self):
        self.newSanaudos = AddSanaudos2()
        self.newSanaudos.exec_()
        self.displaySanaudos()

    def funcAddStelazas(self):
        self.newAtsargos = AddStelazas()
        self.newAtsargos.exec_()
        self.displayStelazas()

    def funcAddRolikai(self):
        self.newRolikai = AddRolikai()
        self.newRolikai.exec_()
        self.displayRolikai()

    def add_selected(self):
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
            self.funcAddUzsakymas()
        elif self.treeTable.currentItem() == self.atsargosSelect:
            self.funcAddAtsargos()
        elif self.treeTable.currentItem() == self.sanaudosSelect:
            self.funcAddSanaudos()
        elif self.treeTable.currentItem() == self.stelazasSelect:
            self.funcAddStelazas()
        elif self.treeTable.currentItem() == self.rolikaiSelect:
            self.funcAddRolikai()

    def displayUzsakymai(self):
        """Shows SQL table ir QTableWidget"""
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
            self.uzsakymuTable.setFont(QFont("Times", 10))

            for i in reversed(range(self.uzsakymuTable.rowCount())):
                self.uzsakymuTable.removeRow(i)

            # Connect to SQL table
            conn = psycopg2.connect(
                **uzsakymai_db_params
            )

            cur = conn.cursor()

            cur.execute(
                """SELECT * FROM uzsakymai ORDER BY projektas ASC, konstruktorius ASC, terminas ASC,  imone ASC""")
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
                            setitem.setBackground(QtGui.QColor(255, 0, 0))
                            # setitem.setForeground(QtGui.QColor(255, 255, 255))

                    if data == 'PAGAMINTA':
                        setitem.setBackground(QtGui.QColor(0, 204, 0))
                    elif data == 'BROKUOTA':
                        setitem.setBackground(QtGui.QColor(242, 172, 10))

                    elif data == 'MODESTAS':
                        setitem.setBackground(QtGui.QColor(244, 193, 126))
                    elif data == 'JULIJUS':
                        setitem.setBackground(QtGui.QColor(153, 204, 155))
                    elif data == 'JULIUS':
                        setitem.setBackground(QtGui.QColor(254, 253, 195))
                    elif data == 'VAIDAS':
                        setitem.setBackground(QtGui.QColor(192, 192, 192))
                    elif data == 'MINDAUGAS':
                        setitem.setBackground(QtGui.QColor(86, 172, 186))

                    elif data == 'SRS':
                        setitem.setBackground(QtGui.QColor(255, 228, 181))
                    elif data == 'METACO':
                        setitem.setBackground(QtGui.QColor(255, 228, 181))
                    elif data == 'AUTOSABINA':
                        setitem.setBackground(QtGui.QColor(255, 228, 181))
                    elif data == 'ALBASERVIS':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'DAGMITA':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'IGNERA':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'KRC RATUKAI':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'WURTH':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'DRUTSRAIGTIS':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'JOLDITA':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'SERFAS':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'BITECH':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == 'HITECH':
                        setitem.setBackground(QtGui.QColor(50, 168, 84))
                    elif data == 'M.J.':
                        setitem.setBackground(QtGui.QColor(188, 143, 143))
                    elif data == 'MITRONAS':
                        setitem.setBackground(QtGui.QColor(188, 143, 143))
                    elif data == 'KAVERA':
                        setitem.setBackground(QtGui.QColor(188, 143, 143))
                    elif data == 'KAGNETA':
                        setitem.setBackground(QtGui.QColor(188, 143, 143))
                    elif data == 'METGA':
                        setitem.setBackground(QtGui.QColor(137, 175, 174))
                    elif data == 'KASTAGA':
                        setitem.setBackground(QtGui.QColor(137, 175, 174))
                    elif data == 'BALTAS VEJAS':
                        setitem.setBackground(QtGui.QColor(137, 175, 174))
                    self.uzsakymuTable.setItem(row_number, column_number, setitem)

            # Edit column cell disable
            self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            # makes error messagebox on start from update on start
            pass

    def displayAtsargos(self):
        try:
            self.atsarguTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.atsarguTable.rowCount())):
                self.atsarguTable.removeRow(i)

            con = psycopg2.connect(
                **komponentai_db_params
            )

            c = con.cursor()
            c.execute("""SELECT * FROM komponentai ORDER BY pavadinimas ASC""")
            query = c.fetchall()
            for row_date in query:
                row_number = self.atsarguTable.rowCount()
                self.atsarguTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    if data == 'GUOLIS' or data == 'GUOLIS+GUOLIAVIETE':
                        setitem.setBackground(QtGui.QColor(244, 193, 126))
                    elif data == 'IVORE' or data == 'MOVA RCK':
                        setitem.setBackground(QtGui.QColor(153, 204, 155))
                    elif data == 'BELTAS' or data == 'DIRZAS' \
                            or data == 'DIRZELIS':
                        setitem.setBackground(QtGui.QColor(254, 253, 195))
                    elif data == "GRANDINE" or data == 'ZVAIGZDE':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == "FIKSACINIS ZIEDAS" or data == 'VARZTAS':
                        setitem.setBackground(QtGui.QColor(188, 143, 143))
                    elif data == "EQ-GALINUKAS" or data == "EQ-PRILAIKANTIS" or data == "EQ-03-01-00-003 NORD" \
                            or data == "EQ-03-01-00-002" or data == "EQ-IVORE":
                        setitem.setBackground(QtGui.QColor(0, 204, 0))
                    elif data == 'HABASIT' or data == 'PLASTIKINE IVORE' \
                            or data == 'UZDENGIMAS' or data == 'ALIUMINIS PROFILIS':
                        setitem.setBackground(QtGui.QColor(0, 204, 0))

                    if data == "0":
                        setitem.setBackground(QtGui.QColor(255, 0, 0))

                    for i in range(1, 31):
                        if data == str(i):
                            setitem.setBackground(QtGui.QColor(242, 172, 10))

                    #   if column_number == 3 and 20 < int(data):
                    #     setitem.setBackground(QtGui.QColor(0, 204, 0))

                    self.atsarguTable.setItem(row_number, column_number, setitem)

            self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass

    def displaySanaudos(self):
        # Get current date
        datetime = QDate.currentDate()
        y = datetime.year()

        try:
            self.sanaudosTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.sanaudosTable.rowCount())):
                self.sanaudosTable.removeRow(i)

            con = psycopg2.connect(
                **sanaudos_db_params
            )

            c = con.cursor()
            c.execute("""SELECT * FROM sanaudos ORDER BY projektas ASC, pavadinimas ASC""")
            query = c.fetchall()

            for row_date in query:
                row_number = self.sanaudosTable.rowCount()
                self.sanaudosTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))
                    if data == 'HABASIT':
                        setitem.setBackground(QtGui.QColor(153, 204, 155))
                    elif data == 'PROFILIAI':
                        setitem.setBackground(QtGui.QColor(254, 253, 195))
                    elif data == 'UZDENGIMAI':
                        setitem.setBackground(QtGui.QColor(192, 192, 192))
                    elif data == 'PRILAIKANTIS' or data == 'GALINUKAS' or data == 'SKRIEMULYS' \
                            or data == 'SKRIEMULIO ASIS':
                        setitem.setBackground(QtGui.QColor(193, 205, 205))
                    self.sanaudosTable.setItem(row_number, column_number, setitem)

                    # old date color
                    listdata = []
                    if column_number == 6:
                        listdata.append(str(data))
                        for i in listdata:
                            if int(i[0:4]) < int(y):
                                setitem.setBackground(QtGui.QColor(0, 204, 0))

            self.sanaudosTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass

    def displayStelazas(self):
        try:
            self.stelazasTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.stelazasTable.rowCount())):
                self.stelazasTable.removeRow(i)

            con = psycopg2.connect(
                **stelazas_db_params
            )

            c = con.cursor()
            c.execute("""SELECT * FROM stelazas ORDER BY vieta ASC, projektas ASC, sandelis ASC, pavadinimas ASC""")
            query = c.fetchall()
            for row_date in query:
                row_number = self.stelazasTable.rowCount()
                self.stelazasTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))
                    if data == 'ROLIKAI':
                        setitem.setBackground(QtGui.QColor(86, 172, 186))
                    elif data == 'VARIKLIAI':
                        setitem.setBackground(QtGui.QColor(244, 193, 126))
                    elif data == 'DETALES IR KT.':
                        setitem.setBackground(QtGui.QColor(153, 204, 155))
                    elif data == 'FESTO':
                        setitem.setBackground(QtGui.QColor(254, 253, 195))
                    elif data == 'ATSARGOS':
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    elif data == "BUTRIMONIU" or data == "BUTRIMONIU KAMB.":
                        setitem.setBackground(QtGui.QColor(176, 196, 222))
                    self.stelazasTable.setItem(row_number, column_number, setitem)

            self.stelazasTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass

    def displayRolikai(self):
        try:
            self.rolikaiTable.setFont(QFont("Times", 10))
            for i in reversed(range(self.rolikaiTable.rowCount())):
                self.rolikaiTable.removeRow(i)

            conn = psycopg2.connect(
                **rolikai_db_params
            )
            cur = conn.cursor()

            cur.execute("""SELECT * FROM rolikai ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
            query = cur.fetchall()

            for row_date in query:
                row_number = self.rolikaiTable.rowCount()
                self.rolikaiTable.insertRow(row_number)
                for column_number, data in enumerate(row_date):
                    setitem = QTableWidgetItem(str(data))

                    if data == 'POSUKIS':
                        setitem.setBackground(QtGui.QColor(244, 193, 126))
                    elif data == 'POSUKIS-RM':
                        setitem.setBackground(QtGui.QColor(153, 204, 155))
                    elif data == 'PAPRASTAS':
                        setitem.setBackground(QtGui.QColor(254, 253, 195))
                    elif data == 'RM':
                        setitem.setBackground(QtGui.QColor(192, 192, 192))
                    elif data == 'ASIS':
                        setitem.setBackground(QtGui.QColor(205, 186, 150))
                    elif data == 'SRIEGIS':
                        setitem.setBackground(QtGui.QColor(255, 228, 196))
                    elif data == '2xD5':
                        setitem.setBackground(QtGui.QColor(155, 205, 155))
                    elif data == 'PJ':
                        setitem.setBackground(QtGui.QColor(122, 197, 205))
                    elif data == 'AT10':
                        setitem.setBackground(QtGui.QColor(219, 219, 219))
                    elif data == 'PVC':
                        setitem.setBackground(QtGui.QColor(205, 200, 177))
                    elif data == 'GUMUOTAS':
                        setitem.setBackground(QtGui.QColor(250, 235, 215))

                    self.rolikaiTable.setItem(row_number, column_number, setitem)

            self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        except:
            pass

    def refresh_selected(self):
        """refresh selected listTable QTable"""
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
            self.displayUzsakymai()

        if self.treeTable.currentItem() == self.atsargosSelect:
            self.displayAtsargos()

        if self.treeTable.currentItem() == self.sanaudosSelect:
            self.displaySanaudos()

        if self.treeTable.currentItem() == self.stelazasSelect:
            self.displayStelazas()

        if self.treeTable.currentItem() == self.rolikaiSelect:
            self.displayRolikai()

    def selectUzsakymai(self):
        """select row data and fill entry with current data"""
        global uzsakymaiId
        listUzsakymai = []
        for i in range(0, 7):
            listUzsakymai.append(self.uzsakymuTable.item(self.uzsakymuTable.currentRow(), i).text())

        uzsakymaiId = listUzsakymai[0]
        self.display = dipslayUzsakymaiUpdate1()
        self.display.show()
        self.display.exec_()
        self.displayUzsakymai()

    def selectAtsargos(self):
        global atsargosId
        listAtsargos = []
        for i in range(0, 6):
            listAtsargos.append(self.atsarguTable.item(self.atsarguTable.currentRow(), i).text())

        atsargosId = listAtsargos[0]
        self.display = displayAtsargosUpdate2()
        self.display.show()
        self.display.exec_()
        self.displayAtsargos()

    def selectSanaudos(self):
        global sanaudosId
        listSanaudos = []
        for i in range(0, 6):
            listSanaudos.append(self.sanaudosTable.item(self.sanaudosTable.currentRow(), i).text())

        sanaudosId = listSanaudos[0]
        self.display = displaySanaudosUpdate2()
        self.display.show()
        self.display.exec_()
        self.displaySanaudos()

    def selectStelazas(self):
        global stelazasId
        listStelazas = []
        for i in range(0, 5):
            listStelazas.append(self.stelazasTable.item(self.stelazasTable.currentRow(), i).text())

        stelazasId = listStelazas[0]
        self.display = displayStelazasUpdate()
        self.display.show()
        self.display.exec_()
        self.displayStelazas()

    def selectRolikai(self):
        global rolikaiId
        listRolikai = []
        for i in range(0, 7):
            listRolikai.append(self.rolikaiTable.item(self.rolikaiTable.currentRow(), i).text())

        rolikaiId = listRolikai[0]
        self.display = updateRolikai()
        self.display.show()
        self.display.exec_()
        self.displayRolikai()

    def searchTables(self, s):
        """search for items and select matched items"""
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
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

            # # SEARCH FROM SQL TABLE AND REFRESH QTABLE TO VIEW JUST SEARCHED ITEMS
            # a, a1, a2, a3, a4 = self.searchEntry1.text()
            #
            # self.uzsakymuTable.setFont(QFont("Times", 10))
            # for i in reversed(range(self.uzsakymuTable.rowCount())):
            #     self.uzsakymuTable.removeRow(i)
            #
            # conn = psycopg2.connect(
            #     **uzsakymai_db_params
            # )
            #
            # cur = conn.cursor()
            #
            # cur.execute(
            #     """SELECT * FROM uzsakymai WHERE imone ILIKE '%{}%' OR projektas ILIKE '%{}%' OR konstruktorius ILIKE '%{}%'
            #     OR pav_uzsakymai ILIKE '%{}%' OR komentarai ILIKE '%{}%'""".format
            #     (a, a1, a2, a3, a4))
            # query = cur.fetchall()
            #
            # for row_date in query:
            #     row_number = self.uzsakymuTable.rowCount()
            #     self.uzsakymuTable.insertRow(row_number)
            #     for column_number, data in enumerate(row_date):
            #         self.uzsakymuTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            # # neleidzia editint column
            # self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        elif self.treeTable.currentItem() == self.atsargosSelect:
            self.atsarguTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.atsarguTable.findItems(s, Qt.MatchContains)
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

        elif self.treeTable.currentItem() == self.stelazasSelect:
            if not s:
                return

            matching_items = self.stelazasTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

        elif self.treeTable.currentItem() == self.rolikaiSelect:
            self.rolikaiTable.setCurrentItem(None)

            if not s:
                return

            matching_items = self.rolikaiTable.findItems(s, Qt.MatchContains)
            if matching_items:
                for item in matching_items:
                    item.setSelected(True)

    def clearSearchEntry1(self):
        """search cancel"""
        self.searchEntry1.clear()

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
                self.mainRightLayout.setCurrentIndex(0)
                self.displayUzsakymai()

            elif self.treeTable.currentItem() == self.atsargosSelect:
                self.mainRightLayout.setCurrentIndex(1)
                self.displayAtsargos()

            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.mainRightLayout.setCurrentIndex(2)
                self.displaySanaudos()

            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.mainRightLayout.setCurrentIndex(3)
                self.displayStelazas()

            elif self.treeTable.currentItem() == self.rolikaiSelect:
                self.mainRightLayout.setCurrentIndex(4)
                self.displayRolikai()

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(0):
                self.mainRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                conn = psycopg2.connect(
                    **uzsakymai_db_params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM uzsakymai WHERE statusas = 'PAGAMINTA' ORDER BY projektas ASC, konstruktorius ASC, 
                    terminas ASC,  imone DESC""")
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
                            if int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0))

                        if data == 'PAGAMINTA':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'BROKUOTA':
                            setitem.setBackground(QtGui.QColor(242, 172, 10))

                        elif data == 'MODESTAS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'JULIJUS':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'JULIUS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'VAIDAS':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'MINDAUGAS':
                            setitem.setBackground(QtGui.QColor(86, 172, 186))

                        elif data == 'SRS':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'METACO':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'AUTOSABINA':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'ALBASERVIS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'DAGMITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'IGNERA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'KRC RATUKAI':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'JOLDITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'SERFAS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'BITECH':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'HITECH':
                            setitem.setBackground(QtGui.QColor(50, 168, 84))
                        elif data == 'M.J.':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'MITRONAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAVERA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAGNETA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'METGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'KASTAGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'BALTAS VEJAS':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(1):
                self.mainRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                conn = psycopg2.connect(
                    **uzsakymai_db_params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM uzsakymai WHERE statusas = 'GAMINA' ORDER BY projektas ASC, konstruktorius ASC, 
                    terminas ASC,  imone DESC""")
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
                            if int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0))

                        if data == 'PAGAMINTA':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'BROKUOTA':
                            setitem.setBackground(QtGui.QColor(242, 172, 10))

                        elif data == 'MODESTAS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'JULIJUS':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'JULIUS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'VAIDAS':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'MINDAUGAS':
                            setitem.setBackground(QtGui.QColor(86, 172, 186))

                        elif data == 'SRS':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'METACO':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'AUTOSABINA':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'ALBASERVIS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'DAGMITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'IGNERA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'KRC RATUKAI':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'JOLDITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'SERFAS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'BITECH':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'HITECH':
                            setitem.setBackground(QtGui.QColor(50, 168, 84))
                        elif data == 'M.J.':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'MITRONAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAVERA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAGNETA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'METGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'KASTAGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'BALTAS VEJAS':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.uzsakymaiSelect.child(2):
                self.mainRightLayout.setCurrentIndex(0)
                self.uzsakymuTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.uzsakymuTable.rowCount())):
                    self.uzsakymuTable.removeRow(i)

                conn = psycopg2.connect(
                    **uzsakymai_db_params
                )

                cur = conn.cursor()

                cur.execute(
                    """SELECT * FROM uzsakymai WHERE statusas = 'BROKUOTA' ORDER BY projektas ASC, konstruktorius ASC, 
                    terminas ASC,  imone DESC""")
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
                            if int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0))

                        if data == 'PAGAMINTA':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'BROKUOTA':
                            setitem.setBackground(QtGui.QColor(242, 172, 10))

                        elif data == 'MODESTAS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'JULIJUS':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'JULIUS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'VAIDAS':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'MINDAUGAS':
                            setitem.setBackground(QtGui.QColor(86, 172, 186))

                        elif data == 'SRS':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'METACO':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'AUTOSABINA':
                            setitem.setBackground(QtGui.QColor(255, 228, 181))
                        elif data == 'ALBASERVIS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'DAGMITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'IGNERA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'KRC RATUKAI':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'JOLDITA':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'SERFAS':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'BITECH':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == 'HITECH':
                            setitem.setBackground(QtGui.QColor(50, 168, 84))
                        elif data == 'M.J.':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'MITRONAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAVERA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'KAGNETA':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == 'METGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'KASTAGA':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        elif data == 'BALTAS VEJAS':
                            setitem.setBackground(QtGui.QColor(137, 175, 174))
                        self.uzsakymuTable.setItem(row_number, column_number, setitem)

                self.uzsakymuTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.atsargosSelect.child(0):
                self.mainRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(
                    **komponentai_db_params
                )

                c = con.cursor()

                c.execute("""SELECT * FROM komponentai WHERE pavadinimas LIKE 'EQ%' ORDER BY pavadinimas ASC""")
                query = c.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'GUOLIS' or data == 'GUOLIS+GUOLIAVIETE':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'IVORE' or data == 'MOVA RCK':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'BELTAS' or data == 'DIRZAS' \
                                or data == 'DIRZELIS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == "GRANDINE" or data == 'ZVAIGZDE':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == "FIKSACINIS ZIEDAS" or data == 'VARZTAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == "EQ-GALINUKAS" or data == "EQ-PRILAIKANTIS" or data == "EQ-03-01-00-003 NORD" \
                                or data == "EQ-03-01-00-002" or data == "EQ-IVORE":
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'HABASIT' or data == 'PLASTIKINE IVORE' \
                                or data == 'UZDENGIMAS' or data == 'ALIUMINIS PROFILIS':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(255, 0, 0))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


            elif self.treeTable.currentItem() == self.atsargosSelect.child(1):
                self.mainRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(
                    **komponentai_db_params
                )

                c = con.cursor()

                c.execute("""SELECT * FROM komponentai WHERE pavadinimas NOT LIKE 'EQ%' ORDER BY pavadinimas ASC""")
                query = c.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'GUOLIS' or data == 'GUOLIS+GUOLIAVIETE':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'IVORE' or data == 'MOVA RCK':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'BELTAS' or data == 'DIRZAS' \
                                or data == 'DIRZELIS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == "GRANDINE" or data == 'ZVAIGZDE':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == "FIKSACINIS ZIEDAS" or data == 'VARZTAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == "EQ-GALINUKAS" or data == "EQ-PRILAIKANTIS" or data == "EQ-03-01-00-003 NORD" \
                                or data == "EQ-03-01-00-002" or data == "EQ-IVORE":
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'HABASIT' or data == 'PLASTIKINE IVORE' \
                                or data == 'UZDENGIMAS' or data == 'ALIUMINIS PROFILIS':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(255, 0, 0))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.atsargosSelect.child(2):
                self.mainRightLayout.setCurrentIndex(1)
                self.atsarguTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.atsarguTable.rowCount())):
                    self.atsarguTable.removeRow(i)

                con = psycopg2.connect(
                    **komponentai_db_params
                )

                c = con.cursor()

                c.execute("""SELECT * FROM komponentai WHERE pavadinimas = 'PAVARA' ORDER BY pavadinimas ASC""")
                query = c.fetchall()

                for row_date in query:
                    row_number = self.atsarguTable.rowCount()
                    self.atsarguTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'GUOLIS' or data == 'GUOLIS+GUOLIAVIETE':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'IVORE' or data == 'MOVA RCK':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'BELTAS' or data == 'DIRZAS' \
                                or data == 'DIRZELIS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == "GRANDINE" or data == 'ZVAIGZDE':
                            setitem.setBackground(QtGui.QColor(176, 196, 222))
                        elif data == "FIKSACINIS ZIEDAS" or data == 'VARZTAS':
                            setitem.setBackground(QtGui.QColor(188, 143, 143))
                        elif data == "EQ-GALINUKAS" or data == "EQ-PRILAIKANTIS" or data == "EQ-03-01-00-003 NORD" \
                                or data == "EQ-03-01-00-002" or data == "EQ-IVORE":
                            setitem.setBackground(QtGui.QColor(0, 204, 0))
                        elif data == 'HABASIT' or data == 'PLASTIKINE IVORE' \
                                or data == 'UZDENGIMAS' or data == 'ALIUMINIS PROFILIS':
                            setitem.setBackground(QtGui.QColor(0, 204, 0))

                        if data == "0":
                            setitem.setBackground(QtGui.QColor(255, 0, 0))

                        for i in range(1, 31):
                            if data == str(i):
                                setitem.setBackground(QtGui.QColor(242, 172, 10))

                        self.atsarguTable.setItem(row_number, column_number, setitem)

                self.atsarguTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(0):
                self.mainRightLayout.setCurrentIndex(4)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                conn = psycopg2.connect(
                    **rolikai_db_params
                )
                cur = conn.cursor()

                cur.execute("""SELECT * FROM rolikai WHERE pavadinimas = 'RM'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'POSUKIS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'POSUKIS-RM':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'PAPRASTAS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'RM':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'ASIS':
                            setitem.setBackground(QtGui.QColor(205, 186, 150))
                        elif data == 'SRIEGIS':
                            setitem.setBackground(QtGui.QColor(255, 228, 196))
                        elif data == '2xD5':
                            setitem.setBackground(QtGui.QColor(155, 205, 155))
                        elif data == 'PJ':
                            setitem.setBackground(QtGui.QColor(122, 197, 205))
                        elif data == 'AT10':
                            setitem.setBackground(QtGui.QColor(219, 219, 219))
                        elif data == 'PVC':
                            setitem.setBackground(QtGui.QColor(205, 200, 177))
                        elif data == 'GUMUOTAS':
                            setitem.setBackground(QtGui.QColor(250, 235, 215))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(1):
                self.mainRightLayout.setCurrentIndex(4)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                conn = psycopg2.connect(
                    **rolikai_db_params
                )
                cur = conn.cursor()

                cur.execute("""SELECT * FROM rolikai WHERE pavadinimas = 'PAPRASTAS'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'POSUKIS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'POSUKIS-RM':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'PAPRASTAS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'RM':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'ASIS':
                            setitem.setBackground(QtGui.QColor(205, 186, 150))
                        elif data == 'SRIEGIS':
                            setitem.setBackground(QtGui.QColor(255, 228, 196))
                        elif data == '2xD5':
                            setitem.setBackground(QtGui.QColor(155, 205, 155))
                        elif data == 'PJ':
                            setitem.setBackground(QtGui.QColor(122, 197, 205))
                        elif data == 'AT10':
                            setitem.setBackground(QtGui.QColor(219, 219, 219))
                        elif data == 'PVC':
                            setitem.setBackground(QtGui.QColor(205, 200, 177))
                        elif data == 'GUMUOTAS':
                            setitem.setBackground(QtGui.QColor(250, 235, 215))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(2):
                self.mainRightLayout.setCurrentIndex(4)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                conn = psycopg2.connect(
                    **rolikai_db_params
                )
                cur = conn.cursor()

                cur.execute("""SELECT * FROM rolikai WHERE pavadinimas = 'POSUKIS'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'POSUKIS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'POSUKIS-RM':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'PAPRASTAS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'RM':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'ASIS':
                            setitem.setBackground(QtGui.QColor(205, 186, 150))
                        elif data == 'SRIEGIS':
                            setitem.setBackground(QtGui.QColor(255, 228, 196))
                        elif data == '2xD5':
                            setitem.setBackground(QtGui.QColor(155, 205, 155))
                        elif data == 'PJ':
                            setitem.setBackground(QtGui.QColor(122, 197, 205))
                        elif data == 'AT10':
                            setitem.setBackground(QtGui.QColor(219, 219, 219))
                        elif data == 'PVC':
                            setitem.setBackground(QtGui.QColor(205, 200, 177))
                        elif data == 'GUMUOTAS':
                            setitem.setBackground(QtGui.QColor(250, 235, 215))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

            elif self.treeTable.currentItem() == self.rolikaiSelect.child(3):
                self.mainRightLayout.setCurrentIndex(4)
                self.rolikaiTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.rolikaiTable.rowCount())):
                    self.rolikaiTable.removeRow(i)

                conn = psycopg2.connect(
                    **rolikai_db_params
                )
                cur = conn.cursor()

                cur.execute("""SELECT * FROM rolikai WHERE pavadinimas = 'POSUKIS-RM'
                ORDER BY pavadinimas ASC, ilgis ASC, tipas ASC, tvirtinimas ASC""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.rolikaiTable.rowCount()
                    self.rolikaiTable.insertRow(row_number)
                    for column_number, data in enumerate(row_date):
                        setitem = QTableWidgetItem(str(data))

                        if data == 'POSUKIS':
                            setitem.setBackground(QtGui.QColor(244, 193, 126))
                        elif data == 'POSUKIS-RM':
                            setitem.setBackground(QtGui.QColor(153, 204, 155))
                        elif data == 'PAPRASTAS':
                            setitem.setBackground(QtGui.QColor(254, 253, 195))
                        elif data == 'RM':
                            setitem.setBackground(QtGui.QColor(192, 192, 192))
                        elif data == 'ASIS':
                            setitem.setBackground(QtGui.QColor(205, 186, 150))
                        elif data == 'SRIEGIS':
                            setitem.setBackground(QtGui.QColor(255, 228, 196))
                        elif data == '2xD5':
                            setitem.setBackground(QtGui.QColor(155, 205, 155))
                        elif data == 'PJ':
                            setitem.setBackground(QtGui.QColor(122, 197, 205))
                        elif data == 'AT10':
                            setitem.setBackground(QtGui.QColor(219, 219, 219))
                        elif data == 'PVC':
                            setitem.setBackground(QtGui.QColor(205, 200, 177))
                        elif data == 'GUMUOTAS':
                            setitem.setBackground(QtGui.QColor(250, 235, 215))

                        self.rolikaiTable.setItem(row_number, column_number, setitem)

                self.rolikaiTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        except:
            pass

    def MainClose(self):
        """exit app.py"""
        self.destroy()

    def uzsakymusdetales_delete(self):
        """selects what you want to delete"""
        global uzsakymaiId

        listUzsakymai = []
        for i in range(0, 7):
            listUzsakymai.append(self.uzsakymuTable.item(self.uzsakymuTable.currentRow(), i).text())

        uzsakymaiId = listUzsakymai[0]

    def deleteUzsakymas_sh(self):
        """deletes item and refresh list"""
        global uzsakymaiId

        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        if (x == QMessageBox.Yes):
            conn = psycopg2.connect(
                **uzsakymai_db_params
            )

            cur = conn.cursor()
            cur.execute("DELETE FROM uzsakymai WHERE id = %s", (uzsakymaiId,))
            conn.commit()
            conn.close()

            self.displayUzsakymai()

        elif (x == QMessageBox.No):
            self.displayUzsakymai()

    def atsargostable_delete(self):
        global atsargosId

        atsargosId = []
        for i in range(0, 6):
            atsargosId.append(self.atsarguTable.item(self.atsarguTable.currentRow(), i).text())

        atsargosId = atsargosId[0]

    def deleteAtsargos_sh(self):
        global atsargosId

        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        if (x == QMessageBox.Yes):
            con = psycopg2.connect(
                **komponentai_db_params
            )

            c = con.cursor()
            c.execute("DELETE FROM komponentai WHERE id = %s", (atsargosId,))
            con.commit()
            con.close()

            self.displayAtsargos()

        elif (x == QMessageBox.No):
            self.displayAtsargos()

    def sanaudostable_delete(self):
        global sanaudosId

        sanaudosId = []
        for i in range(0, 6):
            sanaudosId.append(self.sanaudosTable.item(self.sanaudosTable.currentRow(), i).text())

        sanaudosId = sanaudosId[0]

    def deletesanaudos_sh(self):
        global sanaudosId

        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        if (x == QMessageBox.Yes):
            con = psycopg2.connect(
                **sanaudos_db_params
            )

            c = con.cursor()
            c.execute("DELETE FROM sanaudos WHERE id = %s", (sanaudosId,))
            con.commit()
            con.close()

            self.displaySanaudos()

        elif (x == QMessageBox.No):
            self.displaySanaudos()

    def stelazastable_delete(self):
        global stelazasId

        listStelazai = []
        for i in range(0, 5):
            listStelazai.append(self.stelazasTable.item(self.stelazasTable.currentRow(), i).text())

        stelazasId = listStelazai[0]

    def deletestelazas_sh(self):
        global stelazasId

        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()
        if (x == QMessageBox.Yes):
            conn = psycopg2.connect(
                **stelazas_db_params
            )

            cur = conn.cursor()
            cur.execute("DELETE FROM stelazas WHERE id = %s", (stelazasId,))
            conn.commit()
            conn.close()

            self.displayStelazas()

        elif (x == QMessageBox.No):
            self.displayStelazas()

    def deleteRolikai_Select(self):
        global rolikaiId
        listRolikai = []
        for i in range(0, 7):
            listRolikai.append(self.rolikaiTable.item(self.rolikaiTable.currentRow(), i).text())

        rolikaiId = listRolikai[0]

    def deleteRolikai_Combo(self):
        global rolikaiId

        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        Bardakas_style_gray.mboxsheetstyle(mbox)

        x = mbox.exec_()

        if (x == QMessageBox.Yes):
            conn = psycopg2.connect(
                **rolikai_db_params
            )
            cur = conn.cursor()
            cur.execute("DELETE FROM rolikai WHERE id = %s", (rolikaiId,))
            conn.commit()
            conn.close()

            self.displayRolikai()

        elif (x == QMessageBox.No):
            self.displayRolikai()

    def save(self):
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
            pass

        elif self.treeTable.currentItem() == self.atsargosSelect:
            pass

        elif self.treeTable.currentItem() == self.sanaudosSelect:
            pass

        elif self.treeTable.currentItem() == self.stelazasSelect:
            pass

        elif self.treeTable.currentItem() == self.rolikaiSelect:
            pass

    def saveAs(self):
        """save table to .xls .csv .txt"""
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save', '', ".xls(*.xls);; .csv(*.csv)")
            if not filename:
                return
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.uzsakymuTable.model()
            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)
            wbk.save(filename)

        elif self.treeTable.currentItem() == self.atsargosSelect:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save', '', ".xls(*.xls);; .csv(*.csv)")
            if not filename:
                return
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.atsarguTable.model()
            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)
            wbk.save(filename)

        elif self.treeTable.currentItem() == self.sanaudosSelect:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save', '', ".xls(*.xls);; .csv(*.csv)")
            if not filename:
                return
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.sanaudosTable.model()
            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)
            wbk.save(filename)

        elif self.treeTable.currentItem() == self.stelazasSelect:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save', '', ".xls(*.xls);; .csv(*.csv)")
            if not filename:
                return
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.stelazasTable.model()
            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)
            wbk.save(filename)

        elif self.treeTable.currentItem() == self.rolikaiSelect:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save', '', ".xls(*.xls);; .csv(*.csv)")
            if not filename:
                return
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
            style = xlwt.XFStyle()
            font = xlwt.Font()
            font.bold = True
            style.font = font
            model = self.rolikaiTable.model()
            for c in range(model.columnCount()):
                text = model.headerData(c, QtCore.Qt.Horizontal)
                sheet.write(0, c + 1, text, style=style)

            for r in range(model.rowCount()):
                text = model.headerData(r, QtCore.Qt.Vertical)
                sheet.write(r + 1, 0, text, style=style)

            for c in range(model.columnCount()):
                for r in range(model.rowCount()):
                    text = model.data(model.index(r, c))
                    sheet.write(r + 1, c + 1, text)
            wbk.save(filename)

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
        if self.treeTable.currentItem() == self.uzsakymaiSelect:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(3)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            table = cursor.insertTable(
                self.uzsakymuTable.rowCount(), self.uzsakymuTable.columnCount(), tableFormat)
            for row in range(table.rows()):
                for col in range(table.columns()):
                    cursor.insertText(self.uzsakymuTable.item(row, col).text())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

        elif self.treeTable.currentItem() == self.atsargosSelect:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(3)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            table = cursor.insertTable(
                self.atsarguTable.rowCount(), self.atsarguTable.columnCount(), tableFormat)
            for row in range(table.rows()):
                for col in range(table.columns()):
                    cursor.insertText(self.atsarguTable.item(row, col).text())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

        elif self.treeTable.currentItem() == self.sanaudosSelect:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(3)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            table = cursor.insertTable(
                self.sanaudosTable.rowCount(), self.sanaudosTable.columnCount(), tableFormat)
            for row in range(table.rows()):
                for col in range(table.columns()):
                    cursor.insertText(self.sanaudosTable.item(row, col).text())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

        elif self.treeTable.currentItem() == self.stelazasSelect:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(3)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            table = cursor.insertTable(
                self.stelazasTable.rowCount(), self.stelazasTable.columnCount(), tableFormat)
            for row in range(table.rows()):
                for col in range(table.columns()):
                    cursor.insertText(self.stelazasTable.item(row, col).text())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

        elif self.treeTable.currentItem() == self.rolikaiSelect:
            tableFormat = QtGui.QTextTableFormat()
            tableFormat.setBorder(0.5)
            tableFormat.setBorderStyle(3)
            tableFormat.setCellSpacing(0)
            tableFormat.setTopMargin(0)
            tableFormat.setCellPadding(4)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            table = cursor.insertTable(
                self.rolikaiTable.rowCount(), self.rolikaiTable.columnCount(), tableFormat)
            for row in range(table.rows()):
                for col in range(table.columns()):
                    cursor.insertText(self.rolikaiTable.item(row, col).text())
                    cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

    def openFolder(self):
        """open selected folder"""
        try:
            global uzsakymaiId

            conn = psycopg2.connect(
                **uzsakymai_db_params
            )

            cur = conn.cursor()
            cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
            uzsakymas = cur.fetchone()

            uzsakymasBreziniai = uzsakymas[8]

            conn.close()

            my_str = ""

            if uzsakymasBreziniai != my_str:
                webbrowser.open(os.path.realpath(uzsakymasBreziniai))

            else:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText("NO FOLDER...")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()


        except:
            pass

    def openFile(self):
        """open selected file"""
        try:
            global uzsakymaiId

            conn = psycopg2.connect(
                **uzsakymai_db_params
            )

            cur = conn.cursor()
            cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
            uzsakymas = cur.fetchone()

            uzsakymasList = uzsakymas[9]

            conn.close()

            my_str = ""

            if uzsakymasList != my_str:
                webbrowser.open(os.path.realpath(uzsakymasList))

            else:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText("NO FILE...")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

                Bardakas_style_gray.msgsheetstyle(msg)

                x = msg.exec_()

        except:
            pass

    def openPicture(self):
        try:
            self.pictureWindow = openPic()
        except:
            pass

    def sanaudos_chart(self):
        try:
            self.sanaudos_chart_window = openSanaudosChart()
        except:
            pass

    def refreshTables(self):
        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect:
                self.displayUzsakymai()
            elif self.treeTable.currentItem() == self.atsargosSelect:
                self.displayAtsargos()
            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.displaySanaudos()
            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.displayStelazas()
        except:
            pass

    def deleteTables(self):
        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect:
                self.deleteUzsakymas_sh()
            elif self.treeTable.currentItem() == self.atsargosSelect:
                self.deleteAtsargos_sh()
            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.deletesanaudos_sh()
            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.deletestelazas_sh()
        except:
            pass

    def addTables(self):
        try:
            if self.treeTable.currentItem() == self.uzsakymaiSelect:
                self.funcAddUzsakymas()
            elif self.treeTable.currentItem() == self.atsargosSelect:
                self.funcAddAtsargos()
            elif self.treeTable.currentItem() == self.sanaudosSelect:
                self.funcAddSanaudos()
            elif self.treeTable.currentItem() == self.stelazasSelect:
                self.funcAddStelazas()
        except:
            pass


class AddUzsakymas1(QDialog):
    """add new record class"""

    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 1000, 345)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

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
        self.imoneCombo = QComboBox()
        self.imoneCombo.setEditable(True)
        self.imoneCombo.setPlaceholderText('Text')
        self.imoneCombo.addItems(
            ["EQ", "METACO", "SRS", "AUTOSABINA", "M.J.", "KAVERA", "MITRONAS", "MK KOMPONENTAI", "KAGNETA",
             "HITECH", "PLASTME", "KASTAGA", "METGA", "BALTAS VEJAS", "MILTECHA", "TRUKME", "DAGMITA", "ALBASERVIS",
             "IGNERA", "SERFAS", "BITECH", "KRC RATUKAI", "JOLDITA", "WURTH", "DRUTSRAIGTIS", "MILTECHA", "ULMAS"])
        self.imoneCombo.setFont(QFont("Times", 12))

        self.braizeCombo = QComboBox()
        self.braizeCombo.setEditable(True)
        self.braizeCombo.setPlaceholderText('Text')
        self.braizeCombo.addItems(["MODESTAS", "VAIDAS", "JULIJUS", "JULIUS", "MINDAUGAS", "VYTAUTAS"])
        self.braizeCombo.setFont(QFont("Times", 12))

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setFont(QFont("Times", 12))
        self.projektasEntry.setPlaceholderText('Text')

        self.uzskpavEntry = QLineEdit()
        self.uzskpavEntry.setFont(QFont("Times", 12))
        self.uzskpavEntry.setPlaceholderText('Text')

        self.terminasEntry = QComboBox()
        self.terminasEntry.setEditable(True)
        self.terminasEntry.addItems(
            ["-", "+"])
        self.terminasEntry.setFont(QFont("Times", 12))

        self.statusasEntry = QComboBox()
        self.statusasEntry.setEditable(True)
        self.statusasEntry.setPlaceholderText('Text')
        self.statusasEntry.addItems(
            ["GAMINA", "PAGAMINTA", "BROKUOTA"])
        self.statusasEntry.setFont(QFont("Times", 12))

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setFont(QFont("Times", 12))
        self.komentaraiEntry.setPlaceholderText('Text')

        self.locEntry = QLineEdit()
        # self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                    "color:black;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.breziniaiBtn = QPushButton("ADD FOLDER")
        self.breziniaiBtn.setFixedWidth(110)
        self.breziniaiBtn.setFixedHeight(25)
        self.breziniaiBtn.clicked.connect(self.OpenFolderDialog)
        self.breziniaiBtn.setFont(QFont("Times", 10))

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.setFixedWidth(110)
        self.fileBtn.setFixedHeight(25)
        self.fileBtn.clicked.connect(self.OpenFileDialog)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("ADD DATE")
        self.dateBtn.setFixedWidth(110)
        self.dateBtn.setFixedHeight(25)
        self.dateBtn.clicked.connect(self.myCal)
        self.dateBtn.setFont(QFont("Times", 10))

        self.ListEntry = QLineEdit()
        # self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")
        self.ListEntry.setFont(QFont("Times", 12))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(25)
        self.okBtn.clicked.connect(self.addUzsakymas)
        self.okBtn.setFont(QFont("Times", 10))
        # self.okBtn.setMaximumWidth(200)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(25)
        self.cancelBtn.clicked.connect(self.cancelUzsakymaiAdd)
        self.cancelBtn.setFont(QFont("Times", 10))
        # self.cancelBtn.setMaximumWidth(200)

    def layouts(self):
        self.topmainLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QVBoxLayout()
        self.mainLayout2 = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()

        self.qhbox1 = QHBoxLayout()
        self.qhbox1.addWidget(self.locEntry)
        self.qhbox1.addWidget(self.breziniaiBtn)

        self.qhbox2 = QHBoxLayout()
        self.qhbox2.addWidget(self.ListEntry)
        self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.terminasEntry)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("IMONE:"), self.imoneCombo)
        self.widgetLayout.addRow(QLabel("BRAIZE:"), self.braizeCombo)
        self.widgetLayout.addRow(QLabel("PROJEKTAS:"), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS:"), self.uzskpavEntry)
        self.widgetLayout.addRow(QLabel("TERMINAS:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("STATUSAS:"), self.statusasEntry)

        self.widgetLayout.addRow(QLabel("BREZINIAI:"), self.qhbox1)
        self.widgetLayout.addRow(QLabel("SARASAS:"), self.qhbox2)

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("KOMENTARAI:"))
        self.widgetLayout2.addRow(self.komentaraiEntry)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        # """add widgets to layouts"""
        self.mainLayout1.addWidget(self.widgetFrame)
        self.mainLayout2.addWidget(self.widgetFrame2)

        self.mainLayout.addLayout(self.mainLayout1, 37)
        self.mainLayout.addLayout(self.mainLayout2, 63)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        """get folder dir"""
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def OpenFileDialog(self):
        """getOpenFileName creates tuples and we need just dir, get file dir"""
        (directory, fileType) = QtWidgets.QFileDialog.getOpenFileName()
        self.ListEntry.setText('{}'.format(directory))

    def myCal(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(25)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QDialog()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(780, 280, 350, 350)
        self.calendarWindow.setWindowTitle('TERMINAS')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        Bardakas_style_gray.QCalendarstyle(self)
        self.calendarWindow.show()

        @QtCore.pyqtSlot(QtCore.QDate)
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

    def cal_cancel(self):
        self.calendarWindow.close()

    def save(self):
        query = """SELECT * FROM uzsakymai"""

        conn = psycopg2.connect(
            **uzsakymai_db_params
        )

        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('uzsakymai_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def addUzsakymas(self):
        imone = self.imoneCombo.currentText()
        braize = self.braizeCombo.currentText()
        projektas = self.projektasEntry.text()
        uzsakymo_pavadinimas = self.uzskpavEntry.text()
        terminas = self.terminasEntry.currentText()
        statusas = self.statusasEntry.currentText()
        komentarai = str(self.komentaraiEntry.toPlainText())
        breziniai = self.locEntry.text()
        sarasas = self.ListEntry.text()

        terminas_date = ""

        if terminas != terminas_date:
            try:
                conn = psycopg2.connect(
                    **uzsakymai_db_params
                )

                cur = conn.cursor()

                cur.execute('''INSERT INTO uzsakymai (imone, konstruktorius, projektas, pav_uzsakymai,
                terminas, statusas, komentarai, breziniai, sarasas) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (imone, braize, projektas, uzsakymo_pavadinimas,
                             terminas, statusas, komentarai, breziniai, sarasas))

                conn.commit()

                conn.close()

                self.save()

            except:
                pass

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("TERMINAS can't be empty...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelUzsakymaiAdd(self):
        self.close()


class AddAtsargos2(QDialog):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 800, 253)
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

    def save(self):
        query = """SELECT * FROM komponentai"""

        conn = psycopg2.connect(
            **komponentai_db_params
        )

        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('komponentai_bakcup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def widgets(self):
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.setPlaceholderText("Text")
        self.pavadiniamsEntry.addItems(["GUOLIS", "DIRZAS", "DIRZELIS", "BELTAS", "GUOLIS+GUOLIAVIETE",
                                        "IVORE", "MOVA RCK", "GRANDINE", "VARZTAS", "ZVAIGZDE"])
        self.pavadiniamsEntry.setFont(QFont("Times", 12))

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText("Text")
        self.vietaCombo.addItems(["BUTRIMONIU", "MITUVOS", "BUTRIMONIU KAMB."])
        self.vietaCombo.setFont(QFont("Times", 12))

        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setFont(QFont("Times", 12))

        self.matvntCombo = QComboBox()
        self.matvntCombo.setEditable(True)
        self.matvntCombo.setPlaceholderText("Text")
        self.matvntCombo.addItems(["m.", "vnt."])
        self.matvntCombo.setFont(QFont("Times", 12))

        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", 12))

        self.locEntry = QLineEdit()
        # self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: lightgrey;}")
        # self.locEntry.setPlaceholderText('')
        self.locEntry.setFont(QFont("Times", 12))

        self.nuotraukaBtn = QPushButton("ADD PICTURE")
        # self.nuotraukaBtn.clicked.connect(self._open_file_dialog)
        self.nuotraukaBtn.setFont(QFont("Times", 10))
        self.nuotraukaBtn.setFixedWidth(120)
        self.nuotraukaBtn.setFixedHeight(25)

        self.locEntry1 = QLineEdit()
        # self.locEntry.setReadOnly(True)
        self.locEntry1.setStyleSheet("QLineEdit{background: lightgrey;}")
        # self.locEntry.setPlaceholderText('')
        self.locEntry1.setFont(QFont("Times", 12))

        self.brezinysBtn = QPushButton("ADD DRAWING")
        # self.brezinysBtn.clicked.connect(self._open_file_dialog)
        self.brezinysBtn.setFont(QFont("Times", 10))
        self.brezinysBtn.setFixedWidth(120)
        self.brezinysBtn.setFixedHeight(25)

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addAtsargos1)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddAtsagors1)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.qhbox1 = QHBoxLayout()
        self.qhbox1.addWidget(self.locEntry)
        self.qhbox1.addWidget(self.nuotraukaBtn)

        self.qhbox2 = QHBoxLayout()
        self.qhbox2.addWidget(self.locEntry1)
        self.qhbox2.addWidget(self.brezinysBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("MATAVIMO vnt.: "), self.matvntCombo)
        self.widgetLayout.addRow(QLabel("NUOTRAUKA: "), self.qhbox1)
        # self.widgetLayout.addRow(QLabel("BREZINYS: "), self.qhbox2)
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def _open_file_dialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def addAtsargos1(self):
        pavadinimas1 = self.pavadiniamsEntry.currentText()
        vieta1 = self.vietaCombo.currentText()
        kiekis1 = self.kiekisEntry.text()
        vienetas1 = self.matvntCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        nuotrauka1 = self.locEntry.text()

        try:
            con = psycopg2.connect(
                **komponentai_db_params
            )

            c = con.cursor()

            c.execute('''INSERT INTO komponentai (pavadinimas, vieta, kiekis, mat_pav, komentaras, nuotrauka) VALUES
                    (%s, %s, %s, %s, %s, %s)''', (pavadinimas1, vieta1, kiekis1, vienetas1, komentarai1, nuotrauka1))

            con.commit()

            con.close()

            self.save()

            self.close()
        except:
            self.close()

    def closeAddAtsagors1(self):
        self.close()


class AddSanaudos2(QDialog):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

        self.setGeometry(400, 300, 800, 253)
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

    def save(self):
        query = """SELECT * FROM sanaudos"""

        conn = psycopg2.connect(
            **sanaudos_db_params
        )

        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('sanaudos_bakcup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def widgets(self):
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.setPlaceholderText("Text")
        self.pavadiniamsEntry.addItems(["HABASIT", "PROFILIAI", "UZDENGIMAI", "GALINUKAS", "PRILAIKANTIS",
                                        "SKRIEMULYS", "SKRIEMULIO ASIS"])
        self.pavadiniamsEntry.setFont(QFont("Times", 12))
        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", 12))
        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setFont(QFont("Times", 12))
        self.matvntEntry = QComboBox()
        self.matvntEntry.setEditable(True)
        self.matvntEntry.setPlaceholderText("Text")
        self.matvntEntry.addItems(["m.", "vnt."])
        self.matvntEntry.setFont(QFont("Times", 12))
        self.metaiSpinEntry = QSpinBox()
        self.metaiSpinEntry.setValue(year)
        self.metaiSpinEntry.setMinimum(2022)
        self.metaiSpinEntry.setMaximum(3000)
        self.metaiSpinEntry.setFont(QFont("Times", 12))
        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", 12))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addSanaudos1)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)
        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddSanaudos1)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("MATAVIMO vnt.: "), self.matvntEntry)
        self.widgetLayout.addRow(QLabel("METAI: "), self.metaiSpinEntry)

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def addSanaudos1(self):
        pavadinimas1 = self.pavadiniamsEntry.currentText()
        projektas1 = self.projektasEntry.text()
        kiekis1 = self.kiekisEntry.text()
        vienetai1 = self.matvntEntry.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        metai1 = str(self.metaiSpinEntry.text())

        try:
            con = psycopg2.connect(
                **sanaudos_db_params
            )

            c = con.cursor()

            c.execute('''INSERT INTO sanaudos (pavadinimas, projektas, kiekis, mat_vnt, komentaras, metai) VALUES
                    (%s, %s, %s, %s, %s, %s)''', (pavadinimas1, projektas1, kiekis1, vienetai1, komentarai1, metai1))

            con.commit()

            con.close()

            self.save()

            self.close()

        except:
            self.close()

    def closeAddSanaudos1(self):
        self.close()


class AddStelazas(QDialog):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 800, 270)
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
        self.pavadiniamsEntry.addItems(["ROLIKAI", "VARIKLIAI", "DETALES IR KT.", "FESTO", "ATSARGOS"])
        self.pavadiniamsEntry.setFont(QFont("Times", 12))
        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", 12))
        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.setPlaceholderText("Text")
        self.sandelisCombo.addItems(["BUTRIMONIU", "MITUVOS", "BUTRIMONIU KAMB."])
        self.sandelisCombo.setFont(QFont("Times", 12))
        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText("Text")
        self.vietaCombo.addItems(
            ["KONTORA", "ZONA-1", "ZONA-2", "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
             "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4", "STELAZAS-5", "STELAZAS-6", "STELAZAS-7"
                , "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11", "STELAZAS-12", "STELAZAS-13", "STELAZAS-14"
                , "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setFont(QFont("Times", 12))
        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", 12))
        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addStelazas1)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)
        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeAddStelazas1)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("SANDELIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT * FROM stelazas"""

        conn = psycopg2.connect(
            **stelazas_db_params
        )
        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('stelazas_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def addStelazas1(self):
        pavadinimas1 = self.pavadiniamsEntry.currentText()
        projektas1 = self.projektasEntry.text()
        sandelis1 = self.sandelisCombo.currentText()
        vieta1 = self.vietaCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())

        try:
            con = psycopg2.connect(
                **stelazas_db_params
            )

            c = con.cursor()

            c.execute('''INSERT INTO stelazas (pavadinimas, projektas, sandelis, vieta, komentarai) VALUES
                    (%s, %s, %s, %s, %s)''', (pavadinimas1, projektas1, sandelis1, vieta1, komentarai1))

            con.commit()

            con.close()

            self.close()

            self.save()
        except:
            self.close()

    def closeAddStelazas1(self):
        self.close()


class AddRolikai(QDialog):
    def __init__(self):
        """mainWindow"""
        super().__init__()
        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(300, 200, 500, 400)
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
        self.pavadinimasCombo.setFont(QFont("Times", 12))
        self.ilgisEntry = QLineEdit()
        self.ilgisEntry.setPlaceholderText('Number')
        self.ilgisEntry.setFont(QFont("Times", 12))
        self.kiekisEntry = QLineEdit()
        self.kiekisEntry.setPlaceholderText('Number')
        self.kiekisEntry.setFont(QFont("Times", 12))
        self.vietaCombo = QComboBox()
        self.vietaCombo.setPlaceholderText('Text')
        self.vietaCombo.setEditable(True)
        self.vietaCombo.addItems(
            ["BUTRIMONIU", "MITUVOS", "DRAUGYSTE"])
        self.vietaCombo.setFont(QFont("Times", 12))
        self.tvirtinimasCombo = QComboBox()
        self.tvirtinimasCombo.setPlaceholderText('Text')
        self.tvirtinimasCombo.setEditable(True)
        self.tvirtinimasCombo.addItems(
            ["SRIEGIS", "ASIS", "SESIAKAMPE ASIS"])
        self.tvirtinimasCombo.setFont(QFont("Times", 12))
        self.tipasCombo = QComboBox()
        self.tipasCombo.setPlaceholderText('Text')
        self.tipasCombo.setEditable(True)
        self.tipasCombo.addItems(
            ["-", "2xD5", "1xD5", "PJ", "AT10", "GUMUOTAS", "PVC", "2xD5 GUMUOTAS", "2xD5 PVC",
             "AT10 GUMUOTAS", "AT10 PVC"])
        self.tipasCombo.setFont(QFont("Times", 12))
        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", 12))
        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.addRolikai)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)
        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelAddRolikai)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasCombo)
        self.widgetLayout.addRow(QLabel("ILGIS: "), self.ilgisEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasCombo)
        self.widgetLayout.addRow(QLabel("TIPAS: "), self.tipasCombo)
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "), self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""), self.okBtn)
        self.widgetLayout.addRow(QLabel(""), self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        """add widgets to layouts"""
        self.mainLayout.addWidget(self.widgetFrame)
        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT pavadinimas, ilgis, kiekis, vieta, tvirtinimas, tipas, komentarai FROM rolikai"""

        conn = psycopg2.connect(
            **rolikai_db_params
        )
        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('rolikai_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def addRolikai(self):
        pavadinimas = self.pavadinimasCombo.currentText()
        ilgis = self.ilgisEntry.text()
        kiekis = self.kiekisEntry.text()
        vieta = self.vietaCombo.currentText()
        tvirtinimas = self.tvirtinimasCombo.currentText()
        tipas = self.tipasCombo.currentText()
        komentarai = str(self.komentaraiEntry.toPlainText())

        try:
            conn = psycopg2.connect(
                **rolikai_db_params
            )
            cur = conn.cursor()

            cur.execute('''INSERT INTO rolikai (pavadinimas, ilgis, kiekis, vieta, tvirtinimas, tipas, komentarai) VALUES
            (%s, %s, %s, %s, %s, %s, %s)''', (pavadinimas, ilgis, kiekis, vieta, tvirtinimas, tipas, komentarai))

            conn.commit()

            conn.close()

            self.save()

            self.close()
        except:
            self.close()

    def cancelAddRolikai(self):
        self.close()


class dipslayUzsakymaiUpdate1(QDialog):
    """double mouse click table"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 1000, 345)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update1')
        # pozition and size
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
        self.uzsakymuDetails()
        self.widgets()
        self.layouts()

    def uzsakymuDetails(self):
        global uzsakymaiId

        conn = psycopg2.connect(
            **uzsakymai_db_params
        )

        cur = conn.cursor()

        cur.execute("""SELECT * FROM uzsakymai WHERE ID=%s""", (uzsakymaiId,))
        uzsakymas = cur.fetchone()

        self.uzsakymasImone = uzsakymas[1]
        self.uzsakymasBraize = uzsakymas[2]
        self.uzsakymasProjektas = uzsakymas[3]
        self.uzsakymasPavadinimas = uzsakymas[4]
        self.uzsakymasTerminas = uzsakymas[5]
        self.uzsakymasStatusas = uzsakymas[6]
        self.uzsakymasKomentarai = uzsakymas[7]
        self.uzsakymasBreziniai = uzsakymas[8]
        self.uzsakymasList = uzsakymas[9]

    def widgets(self):
        self.imoneCombo1 = QComboBox()
        self.imoneCombo1.setEditable(True)
        self.imoneCombo1.addItems(
            ["EQ", "METACO", "SRS", "AUTOSABINA", "M.J.", "KAVERA", "MITRONAS", "MK KOMPONENTAI", "KAGNETA",
             "HITECH", "PLASTME", "KASTAGA", "METGA", "BALTAS VEJAS", "MILTECHA", "TRUKME", "DAGMITA", "ALBASERVIS",
             "IGNERA", "SERFAS", "HIDROBALT", "TECHNOBALT", "BITECH", "KRC RATUKAI", "WURTH", "DRUTSRAIGTIS", "ULMAS",
             "MILTECHA"])
        self.imoneCombo1.setCurrentText(self.uzsakymasImone)
        self.imoneCombo1.setFont(QFont("Times", 12))

        self.braizeCombo1 = QComboBox()
        self.braizeCombo1.setEditable(True)
        self.braizeCombo1.addItems(["MODESTAS", "VAIDAS", "JULIJUS", "JULIUS", "MINDAUGAS", "VYTAUTAS"])
        self.braizeCombo1.setCurrentText(self.uzsakymasBraize)
        self.braizeCombo1.setFont(QFont("Times", 12))

        self.projektasEntry1 = QLineEdit()
        self.projektasEntry1.setText(self.uzsakymasProjektas)
        self.projektasEntry1.setFont(QFont("Times", 12))

        self.uzskpavEntry1 = QLineEdit()
        self.uzskpavEntry1.setText(self.uzsakymasPavadinimas)
        self.uzskpavEntry1.setFont(QFont("Times", 12))

        self.terminasEntry1 = QComboBox()
        self.terminasEntry1.addItems(["-", "+"])
        self.terminasEntry1.setEditable(True)
        self.terminasEntry1.setCurrentText(self.uzsakymasTerminas)
        self.terminasEntry1.setFont(QFont("Times", 12))

        self.statusasCombo1 = QComboBox()
        self.statusasCombo1.addItems(['GAMINA', 'PAGAMINTA', 'BROKUOTA'])
        self.statusasCombo1.setEditable(True)
        self.statusasCombo1.setCurrentText(self.uzsakymasStatusas)
        self.statusasCombo1.setFont(QFont("Times", 12))

        self.komentaraiEntry1 = QTextEdit()
        self.komentaraiEntry1.setText(self.uzsakymasKomentarai)
        self.komentaraiEntry1.setFont(QFont("Times", 12))

        self.locEntry = QLineEdit()
        self.locEntry.setText(self.uzsakymasBreziniai)
        # self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.breziniaiBtn = QPushButton("CHANGE FOLDER")
        self.breziniaiBtn.setFixedWidth(110)
        self.breziniaiBtn.setFixedHeight(25)
        self.breziniaiBtn.clicked.connect(self.OpenFolderDialog)
        self.breziniaiBtn.setFont(QFont("Times", 10))

        self.fileBtn = QPushButton("CHANGE FILE")
        self.fileBtn.setFixedWidth(110)
        self.fileBtn.setFixedHeight(25)
        self.fileBtn.clicked.connect(self.OpenFileDialog)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("CHANGE DATE")
        self.dateBtn.setFixedWidth(110)
        self.dateBtn.setFixedHeight(25)
        self.dateBtn.clicked.connect(self.myCal)
        self.dateBtn.setFont(QFont("Times", 10))

        self.ListEntry1 = QLineEdit()
        self.ListEntry1.setText(self.uzsakymasList)
        self.ListEntry1.setFont(QFont("Times", 12))
        self.ListEntry1.setStyleSheet("QLineEdit{background: darkgrey;}")

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(25)
        self.okBtn.clicked.connect(self.updateUzsakymas)
        self.okBtn.setFont(QFont("Times", 10))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(25)
        self.cancelBtn.clicked.connect(self.cancelUzsakymai)
        self.cancelBtn.setFont(QFont("Times", 10))

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()

        self.qhbox1 = QHBoxLayout()
        self.qhbox1.addWidget(self.locEntry)
        self.qhbox1.addWidget(self.breziniaiBtn)

        self.qhbox2 = QHBoxLayout()
        self.qhbox2.addWidget(self.ListEntry1)
        self.qhbox2.addWidget(self.fileBtn)

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.terminasEntry1)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("IMONE:"), self.imoneCombo1)
        self.widgetLayout.addRow(QLabel("BRAIZE:"), self.braizeCombo1)
        self.widgetLayout.addRow(QLabel("PROJEKTAS:"), self.projektasEntry1)
        self.widgetLayout.addRow(QLabel("PAVADINIMAS:"), self.uzskpavEntry1)
        self.widgetLayout.addRow(QLabel("TERMINAS:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("STATUSAS:"), self.statusasCombo1)
        self.widgetLayout.addRow(QLabel("BREZINIAI:"), self.qhbox1)
        self.widgetLayout.addRow(QLabel("SARASAS:"), self.qhbox2)
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("KOMENTARAI:"))
        self.widgetLayout2.addRow(self.komentaraiEntry1)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        """add widgets to layouts"""
        self.mainLayout1.addWidget(self.widgetFrame, 37)
        self.mainLayout1.addWidget(self.widgetFrame2, 63)

        self.mainLayout.addLayout(self.mainLayout1)

        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT * FROM uzsakymai"""

        conn = psycopg2.connect(
            **uzsakymai_db_params
        )

        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('uzsakymai_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def OpenFolderDialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def OpenFileDialog(self):
        (directory, fileType) = QtWidgets.QFileDialog.getOpenFileName()
        self.ListEntry1.setText('{}'.format(directory))

    def myCal(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(25)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QWidget()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(780, 280, 350, 350)
        self.calendarWindow.setWindowTitle('TERMINAS')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        Bardakas_style_gray.QCalendarstyle(self)
        self.calendarWindow.show()

        @QtCore.pyqtSlot(QtCore.QDate)
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

    def updateUzsakymas(self):
        global uzsakymaiId
        imone1 = self.imoneCombo1.currentText()
        braize1 = self.braizeCombo1.currentText()
        projektas1 = self.projektasEntry1.text()
        pavadinimas1 = self.uzskpavEntry1.text()
        terminas1 = self.terminasEntry1.currentText()
        statusas1 = self.statusasCombo1.currentText()
        komentarai1 = str(self.komentaraiEntry1.toPlainText())
        breziniai1 = self.locEntry.text()
        sarasas1 = self.ListEntry1.text()

        terminas_entry = ""

        if terminas1 != terminas_entry:
            try:
                conn = psycopg2.connect(
                    **uzsakymai_db_params
                )

                cur = conn.cursor()

                query = "UPDATE uzsakymai SET imone = %s, konstruktorius = %s, projektas = %s, pav_uzsakymai = %s, " \
                        "terminas = %s, statusas = %s, komentarai = %s, breziniai = %s, sarasas = %s where id = %s"
                cur.execute(query, (imone1, braize1, projektas1, pavadinimas1, terminas1, statusas1, komentarai1,
                                    breziniai1, sarasas1, uzsakymaiId))
                conn.commit()
                conn.close()

                self.save()

            except:
                pass


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


class displayAtsargosUpdate2(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 800, 255)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update2')
        # pozition and size
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
        self.atsargosDetails()
        self.widgets()
        self.layouts()

    def atsargosDetails(self):
        global atsargosId

        con = psycopg2.connect(
            **komponentai_db_params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM komponentai WHERE ID = %s""", (atsargosId,))
        atsargos = c.fetchone()
        self.atsargosPavadinimas = atsargos[1]
        self.atsargosVieta = atsargos[2]
        self.atsargosKiekis = atsargos[3]
        self.atsargosMatmuo = atsargos[4]
        self.atsargosKomentarai = atsargos[5]
        self.atsargosNuotrauka = atsargos[6]

    def widgets(self):
        self.pavadinimasEntry2 = QComboBox()
        self.pavadinimasEntry2.setEditable(True)
        self.pavadinimasEntry2.setPlaceholderText("Text")
        self.pavadinimasEntry2.addItems(["GUOLIS", "DIRZAS", "DIRZELIS", "BELTAS", "GUOLIS+GUOLIAVIETE",
                                         "IVORE", "MOVA RCK", "GRANDINE", "VARZTAS", "ZVAIGZDE"])
        self.pavadinimasEntry2.setCurrentText(self.atsargosPavadinimas)
        self.pavadinimasEntry2.setFont(QFont("Times", 12))

        self.vietaCombo2 = QComboBox()
        self.vietaCombo2.setEditable(True)
        self.vietaCombo2.addItems(["BUTRIMONIU", "MITUVOS", "BUTRIMONIU KAMB."])
        self.vietaCombo2.setCurrentText(self.atsargosVieta)
        self.vietaCombo2.setFont(QFont("Times", 12))

        self.kiekisEntry2 = QLineEdit()
        self.kiekisEntry2.setText(self.atsargosKiekis)
        self.kiekisEntry2.setFont(QFont("Times", 12))

        self.matpavCombo2 = QComboBox()
        self.matpavCombo2.setEditable(True)
        self.matpavCombo2.addItems(["m.", "vnt."])
        self.matpavCombo2.setCurrentText(self.atsargosMatmuo)
        self.matpavCombo2.setFont(QFont("Times", 12))

        self.komentaraiEntry2 = QTextEdit()
        self.komentaraiEntry2.setText(self.atsargosKomentarai)
        self.komentaraiEntry2.setFont(QFont("Times", 12))

        self.locEntry = QLineEdit()
        self.locEntry.setText(self.atsargosNuotrauka)
        # self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: lightgrey;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.nuotraukaBtn = QPushButton("CHANGE PICTURE")
        # self.nuotraukaBtn.clicked.connect(self._open_file_dialog)
        self.nuotraukaBtn.setFont(QFont("Times", 10))
        self.nuotraukaBtn.setFixedWidth(120)
        self.nuotraukaBtn.setFixedHeight(25)

        self.locEntry1 = QLineEdit()
        # self.locEntry.setReadOnly(True)
        self.locEntry1.setStyleSheet("QLineEdit{background: lightgrey;}")
        # self.locEntry.setPlaceholderText('')
        self.locEntry1.setFont(QFont("Times", 12))

        self.brezinysBtn = QPushButton("CHANGE DRAWING")
        # self.brezinysBtn.clicked.connect(self._open_file_dialog)
        self.brezinysBtn.setFont(QFont("Times", 10))
        self.brezinysBtn.setFixedWidth(120)
        self.brezinysBtn.setFixedHeight(25)

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(25)
        self.okBtn.clicked.connect(self.updateAtsargos)
        self.okBtn.setFont(QFont("Times", 10))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(25)
        self.cancelBtn.clicked.connect(self.cancelAtsargos)
        self.cancelBtn.setFont(QFont("Times", 10))

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.qhbox1 = QHBoxLayout()
        self.qhbox1.addWidget(self.locEntry)
        self.qhbox1.addWidget(self.nuotraukaBtn)

        self.qhbox2 = QHBoxLayout()
        self.qhbox2.addWidget(self.locEntry1)
        self.qhbox2.addWidget(self.brezinysBtn)

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasEntry2)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo2)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry2)
        self.widgetLayout.addRow(QLabel("MATAVIMO vnt.: "), self.matpavCombo2)
        self.widgetLayout.addRow(QLabel("NUOTRAUKA: "), self.qhbox1)
        # self.widgetLayout.addRow(QLabel("BREZINYS: "), self.qhbox2)
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry2)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def _open_file_dialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def updateAtsargos(self):
        global atsargosId
        pavadinimas1 = self.pavadinimasEntry2.currentText()
        vieta1 = self.vietaCombo2.currentText()
        kiekis1 = self.kiekisEntry2.text()
        matmuo1 = self.matpavCombo2.currentText()
        komentarai1 = str(self.komentaraiEntry2.toPlainText())
        nuotrauka1 = self.locEntry.text()

        try:
            con = psycopg2.connect(
                **komponentai_db_params
            )

            c = con.cursor()

            c.execute(
                "UPDATE komponentai SET pavadinimas = %s, vieta = %s, kiekis = %s, mat_pav = %s, komentaras = %s, "
                "nuotrauka = %s where id = %s",
                (pavadinimas1, vieta1, kiekis1, matmuo1, komentarai1, nuotrauka1, atsargosId))

            con.commit()

            con.close()

            self.close()

        except:
            pass

    def cancelAtsargos(self):
        self.close()


class displaySanaudosUpdate2(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 800, 253)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update3')
        # pozition and size
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
        self.sanaudosDetails()
        self.widgets()
        self.layouts()

    def sanaudosDetails(self):
        global sanaudosId

        con = psycopg2.connect(
            **sanaudos_db_params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM sanaudos WHERE ID = %s""", (sanaudosId,))
        atsargos = c.fetchone()
        self.atsargosPavadinimas = atsargos[1]
        self.atsargosProjektas = atsargos[2]
        self.atsargosKiekis = atsargos[3]
        self.atsargosVnt = atsargos[4]
        self.atsargosKomentarai = atsargos[5]
        self.atsargosMetai = atsargos[6]

    def widgets(self):
        self.pavadiniamsEntry = QComboBox()
        self.pavadiniamsEntry.setEditable(True)
        self.pavadiniamsEntry.addItems(["HABASIT", "PROFILIAI", "UZDENGIMAI", "GALINUKAS", "PRILAIKANTIS",
                                        "SKRIEMULYS", "SKRIEMULIO ASIS"])
        self.pavadiniamsEntry.setFont(QFont("Times", 12))
        self.pavadiniamsEntry.setCurrentText(self.atsargosPavadinimas)
        self.projektasEntry = QLineEdit(self.atsargosProjektas)
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setFont(QFont("Times", 12))
        self.kiekisEntry = QLineEdit(self.atsargosKiekis)
        self.kiekisEntry.setPlaceholderText("Number")
        self.kiekisEntry.setFont(QFont("Times", 12))
        self.vntEntry = QComboBox()
        self.vntEntry.setEditable(True)
        self.vntEntry.addItems(["m.", "vnt."])
        self.vntEntry.setFont(QFont("Times", 12))
        self.vntEntry.setCurrentText(self.atsargosVnt)
        self.komentaraiEntry = QTextEdit(self.atsargosKomentarai)
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setFont(QFont("Times", 12))
        self.metaiEntry = QLineEdit(self.atsargosMetai)
        self.metaiEntry.setPlaceholderText("Text")
        self.metaiEntry.setFont(QFont("Times", 12))
        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateSanaudos)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)
        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelSanaudos)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("MATAVIMO vnt.: "), self.vntEntry)
        self.widgetLayout.addRow(QLabel("METAI: "), self.metaiEntry)

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT * FROM sanaudos"""

        conn = psycopg2.connect(
            **sanaudos_db_params
        )

        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('sanaudos_bakcup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def updateSanaudos(self):
        global sanaudosId
        pavadinimas1 = self.pavadiniamsEntry.currentText()
        projektas1 = self.projektasEntry.text()
        kiekis1 = self.kiekisEntry.text()
        vnt1 = self.vntEntry.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())
        metai1 = self.metaiEntry.text()

        try:
            con = psycopg2.connect(
                **sanaudos_db_params
            )

            c = con.cursor()

            c.execute(
                "UPDATE sanaudos SET pavadinimas = %s, projektas = %s, kiekis = %s, mat_vnt = %s, komentaras = %s, "
                "metai = %s where id = %s",
                (pavadinimas1, projektas1, kiekis1, vnt1, komentarai1, metai1, sanaudosId))
            con.commit()
            con.close()

            self.close()

            self.save()


        except:
            pass

    def cancelSanaudos(self):
        self.close()


class displayStelazasUpdate(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(400, 300, 800, 270)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update4')
        # pozition and size
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
        self.stelazasDetails()
        self.widgets()
        self.layouts()

    def stelazasDetails(self):
        global stelazasId

        con = psycopg2.connect(
            **stelazas_db_params
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
        self.pavadiniamsEntry.addItems(["ROLIKAI", "VARIKLIAI", "DETALES IR KT.", "FESTO", "ATSARGOS"])
        self.pavadiniamsEntry.setCurrentText(self.stPavadinimas)
        self.pavadiniamsEntry.setFont(QFont("Times", 12))

        self.projektasEntry = QLineEdit()
        self.projektasEntry.setPlaceholderText("Text")
        self.projektasEntry.setText(self.stProjektas)
        self.projektasEntry.setFont(QFont("Times", 12))
        self.sandelisCombo = QComboBox()
        self.sandelisCombo.setEditable(True)
        self.sandelisCombo.addItems(["BUTRIMONIU", "MITUVOS", "BUTRIMONIU KAMB."])
        self.sandelisCombo.setCurrentText(self.stSandelis)
        self.sandelisCombo.setFont(QFont("Times", 12))
        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.addItems(
            ["KONTORA", "ZONA-1", "ZONA-2", "VARTAI-10", "VARTAI-11", "VARTAI-12", "VARTAI-13", "VARTAI-14",
             "STELAZAS-1", "STELAZAS-2", "STELAZAS-3", "STELAZAS-4", "STELAZAS-5", "STELAZAS-6", "STELAZAS-7"
                , "STELAZAS-8", "STELAZAS-9", "STELAZAS-10", "STELAZAS-11", "STELAZAS-12", "STELAZAS-13", "STELAZAS-14"
                , "STELAZAS-15", "STELAZAS-16", "STELAZAS-17"])
        self.vietaCombo.setCurrentText(self.stVieta)
        self.vietaCombo.setFont(QFont("Times", 12))
        self.komentaraiEntry = QTextEdit()
        self.komentaraiEntry.setPlaceholderText("Text")
        self.komentaraiEntry.setText(self.stKomentarai)
        self.komentaraiEntry.setFont(QFont("Times", 12))
        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateStelazas1)
        self.okBtn.setFixedHeight(25)
        self.okBtn.setFont(QFont("Times", 10))
        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.closeUpdateStelazas1)
        self.cancelBtn.setFixedHeight(25)
        self.cancelBtn.setFont(QFont("Times", 10))

    def layouts(self):
        self.mainLayout = QHBoxLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()

        self.widgetLayout1 = QFormLayout()
        self.widgetFrame1 = QFrame()

        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadiniamsEntry)
        self.widgetLayout.addRow(QLabel("PROJEKTAS: "), self.projektasEntry)
        self.widgetLayout.addRow(QLabel("SANDELIS: "), self.sandelisCombo)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(QLabel(""))
        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout1.addRow(QLabel("KOMENTARAI: "))
        self.widgetLayout1.addRow(self.komentaraiEntry)
        self.widgetFrame1.setLayout(self.widgetLayout1)

        self.mainLayout.addWidget(self.widgetFrame, 37)
        self.mainLayout.addWidget(self.widgetFrame1, 63)

        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT * FROM stelazas"""

        conn = psycopg2.connect(
            **stelazas_db_params
        )
        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('stelazas_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def updateStelazas1(self):
        global stelazasId
        pavadinimas1 = self.pavadiniamsEntry.currentText()
        projektas1 = self.projektasEntry.text()
        sandelis1 = self.sandelisCombo.currentText()
        vieta1 = self.vietaCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())

        try:
            con = psycopg2.connect(
                **stelazas_db_params
            )

            c = con.cursor()

            c.execute(
                "UPDATE stelazas SET pavadinimas = %s, projektas = %s, sandelis = %s, vieta = %s, komentarai = %s where id = %s",
                (pavadinimas1, projektas1, sandelis1, vieta1, komentarai1, stelazasId))
            con.commit()
            con.close()

            self.close()

            self.save()

        except:
            pass

    def closeUpdateStelazas1(self):
        self.close()


class updateRolikai(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(300, 200, 500, 400)
        self.setFixedSize(self.size())

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        Bardakas_style_gray.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Update5')
        # pozition and size
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
        self.rolikuDetails()
        self.widgets()
        self.layouts()

    def rolikuDetails(self):
        global rolikaiId

        conn = psycopg2.connect(
            **rolikai_db_params
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
        self.komentaraiRolikai = rolikai[7]

    def widgets(self):
        self.pavadinimasCombo = QComboBox()
        self.pavadinimasCombo.setEditable(True)
        self.pavadinimasCombo.setPlaceholderText('Text')
        self.pavadinimasCombo.addItems(
            ["RM", "PAPRASTAS", "POSUKIS-RM", "POSUKIS"])
        self.pavadinimasCombo.setCurrentText(self.pavadinimasRolikai)
        self.pavadinimasCombo.setFont(QFont("Times", 12))

        self.ilgisEntry = QLineEdit(self.ilgisRolikai)
        self.ilgisEntry.setPlaceholderText('Number')
        self.ilgisEntry.setFont(QFont("Times", 12))

        self.kiekisEntry = QLineEdit(self.kiekisRolikai)
        self.kiekisEntry.setPlaceholderText('Number')
        self.kiekisEntry.setFont(QFont("Times", 12))

        self.vietaCombo = QComboBox()
        self.vietaCombo.setEditable(True)
        self.vietaCombo.setPlaceholderText('Text')
        self.vietaCombo.addItems(
            ["BUTRIMONIU", "MITUVOS", "DRAUGYSTE"])
        self.vietaCombo.setCurrentText(self.vietaRolikai)
        self.vietaCombo.setFont(QFont("Times", 12))

        self.tvirtinimasCombo = QComboBox()
        self.tvirtinimasCombo.setEditable(True)
        self.tvirtinimasCombo.setPlaceholderText('Text')
        self.tvirtinimasCombo.addItems(
            ["SRIEGIS", "ASIS", "SESIAKAMPE ASIS"])
        self.tvirtinimasCombo.setCurrentText(self.tvirtinimasRolikai)
        self.tvirtinimasCombo.setFont(QFont("Times", 12))

        self.tipasCombo = QComboBox()
        self.tipasCombo.setEditable(True)
        self.tipasCombo.setPlaceholderText('Text')
        self.tipasCombo.addItems(
            ["-", "2xD5", "1xD5", "PJ", "AT10", "GUMUOTAS", "PVC", "2xD5 GUMUOTAS", "2xD5 PVC",
             "AT10 GUMUOTAS", "AT10 PVC"])
        self.tipasCombo.setCurrentText(self.tipasRolikai)
        self.tipasCombo.setFont(QFont("Times", 12))

        self.komentaraiEntry = QTextEdit(self.komentaraiRolikai)
        self.komentaraiEntry.setPlaceholderText('Text')
        self.komentaraiEntry.setFont(QFont("Times", 12))

        self.okBtn = QPushButton("OK")
        self.okBtn.clicked.connect(self.updateRolikai)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(25)

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.clicked.connect(self.cancelRolikai)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(25)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetLayout.addRow(QLabel("PAVADINIMAS: "), self.pavadinimasCombo)
        self.widgetLayout.addRow(QLabel("ILGIS: "), self.ilgisEntry)
        self.widgetLayout.addRow(QLabel("KIEKIS: "), self.kiekisEntry)
        self.widgetLayout.addRow(QLabel("VIETA: "), self.vietaCombo)
        self.widgetLayout.addRow(QLabel("TVIRTINIMAS: "), self.tvirtinimasCombo)
        self.widgetLayout.addRow(QLabel("TIPAS: "), self.tipasCombo)
        self.widgetLayout.addRow(QLabel("KOMENTARAI: "), self.komentaraiEntry)
        self.widgetLayout.addRow(QLabel(""), self.okBtn)
        self.widgetLayout.addRow(QLabel(""), self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        """add widgets to layouts"""
        self.mainLayout.addWidget(self.widgetFrame)
        self.setLayout(self.mainLayout)

    def save(self):
        query = """SELECT pavadinimas, ilgis, kiekis, vieta, tvirtinimas, tipas, komentarai FROM rolikai"""

        conn = psycopg2.connect(
            **rolikai_db_params
        )
        cur = conn.cursor()

        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

        with open('rolikai_backup', 'w') as f:
            cur.copy_expert(outputquery, f)

        conn.close()

    def updateRolikai(self):
        global rolikaiId

        pavadinimas1 = self.pavadinimasCombo.currentText()
        ilgis1 = self.ilgisEntry.text()
        kiekis1 = self.kiekisEntry.text()
        vieta1 = self.vietaCombo.currentText()
        tvirtinimas1 = self.tvirtinimasCombo.currentText()
        tipas1 = self.tipasCombo.currentText()
        komentarai1 = str(self.komentaraiEntry.toPlainText())

        try:
            conn = psycopg2.connect(
                **rolikai_db_params
            )
            cur = conn.cursor()

            query = "UPDATE rolikai SET pavadinimas = %s, ilgis = %s, kiekis = %s, vieta = %s, tvirtinimas = %s, tipas = %s, komentarai = %s where id = %s"
            cur.execute(query, (pavadinimas1, ilgis1, kiekis1, vieta1, tvirtinimas1, tipas1, komentarai1, rolikaiId))
            conn.commit()
            conn.close()

            self.save()

            self.close()

        except:
            pass

    def cancelRolikai(self):
        self.close()


class openPic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PICTURE")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(300, 200, 800, 600)
        # self.setFixedSize(self.size())

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Picture1')
        # pozition and size
        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))

        except:
            pass

        global atsargosId

        con = psycopg2.connect(
            **komponentai_db_params
        )

        c = con.cursor()

        c.execute("""SELECT * FROM komponentai WHERE ID = %s""", (atsargosId,))
        atsargos = c.fetchone()

        atsargosNuotrauka = atsargos[6]

        c.close()

        my_str = ""

        if atsargosNuotrauka != my_str:
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(atsargosNuotrauka))
            self.setCentralWidget(self.browser)
            self.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("NO FILE...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))

            Bardakas_style_gray.msgsheetstyle(msg)

            x = msg.exec_()

        self.show()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())


class openSanaudosChart(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SANAUDOS")
        self.setWindowIcon(QIcon('icons/uzsakymai_icon.ico'))
        self.setGeometry(300, 200, 205, 203)
        self.setFixedSize(self.size())

        # creates registry folder and subfolder
        self.settings = QSettings('Bardakas', 'Picture1')
        # pozition and size
        try:
            # self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))

        except:
            pass

        self.show()
        self.count_sum()

    def closeEvent(self, event):
        # self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def count_sum(self):
        con = psycopg2.connect(**sanaudos_db_params)

        c = con.cursor()

        list_sum_habasit = []
        list_sum_profiliai = []
        list_sum_uzdengimai = []
        list_sum_galinukas = []
        list_sum_prilaikantis = []
        list_sum_skriemulys = []
        list_sum_skriemulio_asis = []

        list_pav = ['HABASIT', 'PROFILIAI', 'UZDENGIMAI', 'GALINUKAS', 'PRILAIKANTIS', 'SKRIEMULYS', 'SKRIEMULIO ASIS']
        for item in list_pav:
            c.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = '{item}' AND metai = '{year}'""")

            if item == 'HABASIT':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_habasit.append(int(data))

            elif item == 'PROFILIAI':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_profiliai.append(int(data))

            elif item == 'UZDENGIMAI':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_uzdengimai.append(int(data))

            elif item == 'GALINUKAS':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_galinukas.append(int(data))

            elif item == 'PRILAIKANTIS':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_prilaikantis.append(int(data))

            elif item == 'SKRIEMULYS':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_skriemulys.append(int(data))

            elif item == 'SKRIEMULIO ASIS':
                query = c.fetchall()
                for row_date in query:
                    for column_number, data in enumerate(row_date):
                        list_sum_skriemulio_asis.append(int(data))

        con.close()

        self.metrai = " m."
        self.vienetai = " vnt."

        self.list_sum_hab = QLineEdit(str(sum(list_sum_habasit)) + self.metrai)
        self.list_sum_hab.setReadOnly(True)
        self.list_sum_hab.setFixedWidth(80)
        self.list_sum_hab.setAlignment(Qt.AlignCenter)
        self.list_sum_prof = QLineEdit(str(sum(list_sum_profiliai)) + self.metrai)
        self.list_sum_prof.setReadOnly(True)
        self.list_sum_prof.setFixedWidth(80)
        self.list_sum_prof.setAlignment(Qt.AlignCenter)
        self.list_sum_uzdg = QLineEdit(str(sum(list_sum_uzdengimai)) + self.metrai)
        self.list_sum_uzdg.setReadOnly(True)
        self.list_sum_uzdg.setFixedWidth(80)
        self.list_sum_uzdg.setAlignment(Qt.AlignCenter)
        self.list_sum_gal = QLineEdit(str(sum(list_sum_galinukas)) + self.vienetai)
        self.list_sum_gal.setReadOnly(True)
        self.list_sum_gal.setFixedWidth(80)
        self.list_sum_gal.setAlignment(Qt.AlignCenter)
        self.list_sum_pril = QLineEdit(str(sum(list_sum_prilaikantis)) + self.vienetai)
        self.list_sum_pril.setReadOnly(True)
        self.list_sum_pril.setFixedWidth(80)
        self.list_sum_pril.setAlignment(Qt.AlignCenter)
        self.list_sum_skrm = QLineEdit(str(sum(list_sum_skriemulys)) + self.vienetai)
        self.list_sum_skrm.setReadOnly(True)
        self.list_sum_skrm.setFixedWidth(80)
        self.list_sum_skrm.setAlignment(Qt.AlignCenter)
        self.list_sum_skrmasis = QLineEdit(str(sum(list_sum_skriemulio_asis)) + self.vienetai)
        self.list_sum_skrmasis.setReadOnly(True)
        self.list_sum_skrmasis.setFixedWidth(80)
        self.list_sum_skrmasis.setAlignment(Qt.AlignCenter)

        self.mainLayout = QHBoxLayout()
        self.widgetLayout = QFormLayout()

        self.widgetLayout.addRow(QLabel("HABASIT: "), self.list_sum_hab)
        self.widgetLayout.addRow(QLabel("PROFILIAI: "), self.list_sum_prof)
        self.widgetLayout.addRow(QLabel("UZDENGIMAI: "), self.list_sum_uzdg)
        self.widgetLayout.addRow(QLabel("GALINUKAS: "), self.list_sum_gal)
        self.widgetLayout.addRow(QLabel("PRILAIKANTIS: "), self.list_sum_pril)
        self.widgetLayout.addRow(QLabel("SKRIEMULYS: "), self.list_sum_skrm)
        self.widgetLayout.addRow(QLabel("SKRIEMULIO ASIS: "), self.list_sum_skrmasis)

        self.mainLayout.addLayout(self.widgetLayout)
        self.setLayout(self.mainLayout)


def main():
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
    time.sleep(3)  # hold image on screen for a while
    splash.close()  # close the splash screen

    window = MainMenu()

    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
