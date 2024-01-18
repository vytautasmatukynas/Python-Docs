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

import config
from static import style
from scaling_dpi.scaling import scaling_dpi

params = config.params

datetime = QDate.currentDate()
year = datetime.year()
month = datetime.month()
day = datetime.day()

__author__ = 'Vytautas Matukynas'
__copyright__ = f'Copyright (C) {year}, Vytautas Matukynas'
__credits__ = ['Vytautas Matukynas']
__license__ = 'Vytautas Matukynas'
__version__ = '1.00'
__maintainer__ = 'Vytautas Matukynas'
__email__ = 'vytautas.matukynas@gmail.com'
__status__ = 'Beta'
__AppName__ = 'Order App'

LINK_TO_VERSION = "link to version file"
LINK_TO_FILE = "link to setup file"


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        """Delegate style to items. ALIGNMENT center.
        Align for QTable class."""
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class MainMenu(QMainWindow, scaling_dpi):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Order App")
        self.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        self.setGeometry(int(100 / self.scale_factor), int(100 / self.scale_factor),
                         int(1200 * self.scale_factor), int(720 * self.scale_factor))
        self.showMaximized()

        # Shows treeview at start
        self.option = True

        self.show()
        self.UI()

    def UI(self):
        """Functions that starts when you start App"""
        style.SheetStyle(self)
        self.menubar()
        self.toolBarInside()
        self.searchWidgets()
        self.default_widgets()
        self.treeTableWidget()
        self.tableWidgets()
        self.timeWidget()
        self.layouts()
        self.updateInfoOnStart()

    def menubar(self):
        """Main-menu bar"""
        self.menuBarMain = self.menuBar()
        self.menuBarMain.isRightToLeft()

        # File bar
        file = self.menuBarMain.addMenu("File")
        # Submenu bar
        new = QAction("New", self)
        new.triggered.connect(self.add_orders)
        new.setShortcut("Ctrl+N")
        file.addAction(new)

        file.addSeparator()
        save = QAction("Save", self)
        save.triggered.connect(self.save)
        save.setShortcut("Ctrl+S")
        save.setIcon(QIcon("static/icons/save.png"))
        file.addAction(save)

        saveAs = QAction("Save As", self)
        saveAs.triggered.connect(self.saveAs)
        saveAs.setShortcut("Alt+S")
        saveAs.setIcon(QIcon("static/icons/saveas.png"))
        file.addAction(saveAs)

        file.addSeparator()

        delete = QAction("Delete", self)
        delete.triggered.connect(self.deleteItem)
        delete.setIcon(QIcon("static/icons/delete.png"))
        file.addAction(delete)

        file.addSeparator()

        refresh = QAction("Refresh", self)
        refresh.triggered.connect(self.listTables)
        refresh.setShortcut("F5")
        refresh.setIcon(QIcon("static/icons/refresh.png"))
        file.addAction(refresh)

        file.addSeparator()

        print = QAction("Print", self)
        print.triggered.connect(self.handlePreview)
        print.setShortcut("Ctrl+P")
        print.setIcon(QIcon("static/icons/print.png"))
        file.addAction(print)

        file.addSeparator()

        exit = QAction("Exit", self)
        exit.triggered.connect(self.MainClose)
        exit.setShortcut("Ctrl+Q")
        exit.setIcon(QIcon("static/icons/exit.png"))
        file.addAction(exit)

        # Setting bar
        Settings = self.menuBarMain.addMenu("Settings")
        Style = Settings.addMenu("Style")
        Style.setIcon(QIcon("static/icons/design.png"))
        Group = QActionGroup(Style)
        style2 = QAction("Retro_Style", self)
        style2.setCheckable(True)
        style2.setChecked(True)
        Style.addAction(style2)
        Group.addAction(style2)
        # Check only one item in GroupBox
        Group.setExclusive(True)

        Settings.addSeparator()

        combo_box = QAction("Add Combo_Box Items", self)
        combo_box.triggered.connect(self.add_combo)
        Settings.addAction(combo_box)

        # Help bar
        help = self.menuBarMain.addMenu("Help")

        # Submenu bar
        UpdateApp = QAction("Check for Updates", self)
        UpdateApp.setIcon(QIcon("static/icons/update.png"))
        UpdateApp.triggered.connect(self.updateInfo)
        help.addAction(UpdateApp)

        help.addSeparator()

        Info = QAction("About", self)
        Info.setIcon(QIcon("static/icons/info.png"))
        Info.triggered.connect(self.helpinfo)
        help.addAction(Info)

    def updateInfoOnStart(self):
        """This func checks App version. It gets info prof version file and if version is higher then current
        App version ir offers to download new setup with update from link where you store update .exe"""
        try:
            # Version file link
            response = requests.get(
                f'{LINK_TO_VERSION}')
            data = response.text

            if float(data) > float(__version__):
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                style.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    webbrowser.open_new_tab(f'{LINK_TO_FILE}')

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
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def updateInfo(self):
        """This func checks App version. It gets info prof version file and if version is higher then current
            App version ir offers to download new setup with update from link where you store update .exe"""
        try:
            response = requests.get(f'{LINK_TO_VERSION}')
            data = response.text

            if float(data) > float(__version__):
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('Update! Version {} to {}.'.format(__version__, data))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                style.msgsheetstyle(msg)

                x = msg.exec_()

                if (x == QMessageBox.Yes):
                    webbrowser.open_new_tab(f'{LINK_TO_FILE}')

                    self.MainClose()

                else:
                    pass

            else:
                msg = QMessageBox()
                msg.setWindowTitle("UPDATE MANAGER")
                msg.setText('No updates, version {}.'.format(__version__))
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

                style.msgsheetstyle(msg)

                x = msg.exec_()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("Error, check your internet connection or\n"
                        "contact system administrator.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def helpinfo(self):
        """ABOUT App info."""
        msg = QMessageBox()
        msg.setWindowTitle("ABOUT")
        msg.setText("Order App version {} ({})\n"
                    "\n"
                    "{}".format(__version__, __status__, __copyright__))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

        style.msgsheetstyle(msg)

        x = msg.exec_()

    def tableWidgets(self):
        """Order table. This func creates order table - columns, rows and etc."""
        self.emptyTable = QTableWidget()
        self.emptyTable.setColumnCount(0)
        if self.emptyTable:
            self.treeTableItems()

        self.ordersTable = QTableWidget()
        self.ordersTable.setColumnCount(11)
        self.ordersTable.setColumnHidden(0, True)
        self.ordersTable.setSortingEnabled(True)

        headers_uzsk = ["ID", "COMPANY", "CLIENT", "PHONE NUMBER", "ORDER NAME", "ORDER TERM",
                        "STATUS", "COMMENTS", "FOLDER LINK", "ORDER FILE", "UPDATED"]

        for column_number in range(0, len(headers_uzsk)):
            while column_number < len(headers_uzsk):
                header_name = headers_uzsk[column_number]
                self.ordersTable.setHorizontalHeaderItem(column_number, QTableWidgetItem(header_name))
                column_number += 1

        self.ordersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.horizontalHeader().setHighlightSections(False)
        self.ordersTable.horizontalHeader().setDisabled(True)
        self.ordersTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.ordersTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ordersTable.pressed.connect(self.order_select)
        self.ordersTable.doubleClicked.connect(self.updateorders)

        # Align delegate Class
        delegate = AlignDelegate()
        for number in [1, 2, 3, 4, 5, 6, 9, 10]:
            self.ordersTable.setItemDelegateForColumn(number, delegate)

    def searchWidgets(self):
        """Search bar widgets and buttons"""
        self.cancelButton1 = QPushButton("CANCEL")
        self.cancelButton1.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelButton1.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.cancelButton1.clicked.connect(self.clearSearchEntry)
        self.cancelButton1.setFont(QFont("Times", 10))

        self.searchButton1 = QPushButton("SEARCH")
        self.searchButton1.setFixedHeight(self.BUTTON_HEIGHT)
        self.searchButton1.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.searchButton1.clicked.connect(self.searchTables)
        self.searchButton1.setFont(QFont("Times", 10))

        self.searchEntry1 = QLineEdit()
        self.searchEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.searchEntry1.setPlaceholderText('Filter table...')

        self.cancelButton2 = QPushButton("CANCEL")
        self.cancelButton2.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelButton2.setFixedWidth(self.SEARCH_BUTTON_WIDTH)
        self.cancelButton2.clicked.connect(self.clearSearchEntry2)
        self.cancelButton2.setFont(QFont("Times", 10))

        self.searchEntry2 = QLineEdit()
        self.searchEntry2.setFixedHeight(self.ENTRY_COMBO_HEIGHT)
        self.searchEntry2.setPlaceholderText('Select table items...')
        self.searchEntry2.textChanged.connect(self.searchTables2)

    def treeTableWidget(self):
        """Treeview table widget"""
        self.treeTable = QTreeWidget()
        self.treeTable.setAnimated(True)
        self.treeTable.setHeaderHidden(True)
        self.treeTable.setColumnCount(1)
        self.treeTable.setMaximumWidth(self.TREE_TABLE_WIDTH)
        self.treeTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def treeTableItems(self):
        """Fill tree-table widget with elements from sql like order_name"""
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute("""SELECT order_name FROM orders""")
        query = cur.fetchall()
        con.close()

        self.ordersSelect = QTreeWidgetItem(self.treeTable, ["Orders"])
        self.ordersSelect.setExpanded(True)

        self.get_headers = [i[0] for i in query]
        # clean headers
        self.clean_get_header = set(self.get_headers)
        self.headers_clean = list(self.clean_get_header)
        self.headers = [head for head in self.headers_clean if head != "" and head != None]
        ################
        self.headers.sort()

        self.ordersSelect_child = self.headers
        for item in self.ordersSelect_child:
            self.ordersSelect.addChild(QTreeWidgetItem([item]))

        self.treeTable.clicked.connect(self.listTables)

    def toolBarInside(self):
        """Toolbar inside table"""
        self.tb2 = QtWidgets.QToolBar("Action tb")
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.tb2.setIconSize(QtCore.QSize(self.TB_ICON_WIDTH, self.TB_ICON_HEIGHT))

        self.add_tb = QAction(QIcon("static/icons/add.png"), "../add", self)
        self.tb2.addAction(self.add_tb)
        self.add_tb.triggered.connect(self.add_orders)

        self.delete_tb = QAction(QIcon("static/icons/delete.png"), "Delete", self)
        self.tb2.addAction(self.delete_tb)
        self.delete_tb.triggered.connect(self.deleteItem)

        self.tb2.addSeparator()

        self.refresh_tb = QAction(QIcon("static/icons/refresh.png"), "Refresh", self)
        self.tb2.addAction(self.refresh_tb)
        self.refresh_tb.triggered.connect(self.listTables)

        self.tb2.addSeparator()

        self.save_tb = QAction(QIcon("static/icons/save.png"), "../save", self)
        self.tb2.addAction(self.save_tb)
        self.save_tb.triggered.connect(self.save)

        self.saveAs_tb = QAction(QIcon("static/icons/saveas.png"), "Save As...", self)
        self.tb2.addAction(self.saveAs_tb)
        self.saveAs_tb.triggered.connect(self.saveAs)

    def timeWidget(self):
        """Timer ir left buttom corner"""
        self.Timer = QLabel()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

    def showTime(self):
        """Gets current time to timer"""
        self.currentTime = QTime.currentTime()
        self.displayTxt = self.currentTime.toString('hh:mm:ss')
        self.Timer.setText(self.displayTxt)

    def default_widgets(self):
        """Button to expand/collapse tree-table"""
        self.expand_button = QPushButton()
        self.expand_button.setIcon(QIcon("static/icons/to_left.png"))
        self.expand_button.setIconSize(QSize(int(19 * self.scale_factor), int(19 * self.scale_factor)))
        self.expand_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.expand_button.setFixedWidth(int(20 * self.scale_factor))
        self.expand_button.clicked.connect(self.treeTableHideShow)

    def layouts(self):
        """MainWindow layouts"""
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
        self.treeLeftLayout.addLayout(self.LeftLayoutTop)

        # Right side search
        self.searchLayout_table.addWidget(self.cancelButton2)
        self.searchLayout_table.addWidget(self.searchEntry2)

        # Right side tb
        self.tbLayout_table.addWidget(self.tb2)

        # Right side tables
        self.tableRightLayout.addWidget(self.ordersTable)
        self.tableRightLayout.addWidget(self.emptyTable)
        self.tableRightLayout.setCurrentIndex(1)

        # Right layout with search
        self.mainRightLayout.addLayout(self.searchLayout_table, 1)
        self.mainRightLayout.addLayout(self.tbLayout_table, 1)
        self.mainRightLayout.addLayout(self.tableRightLayout, 97)

        # Bottom layout
        self.bottomLayout.addWidget(QLabel(f"Order App {__version__} ({__status__})"), 98, alignment=Qt.AlignLeft)
        self.bottomLayout.addWidget(QLabel(f"{datetime.toPyDate()}"), 1, alignment=Qt.AlignRight)
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

    def treeTableHideShow(self):
        """func that expands/collapse tree-table"""
        if self.option:
            self.treeTable.hide()
            self.expand_button.setIcon(QIcon("static/icons/to_right.png"))

            self.option = False

        else:
            self.treeTable.show()
            self.expand_button.setIcon(QIcon("static/icons/to_left.png"))

            self.option = True

    def order_select(self):
        """selects order by ID"""
        global ordersId

        self.listorders = []
        self.num = 0
        self.listorders.append(self.ordersTable.item(self.ordersTable.currentRow(), self.num).text())

        ordersId = self.listorders[0]

    def contextMenuEvent(self, event):
        """Right mouse button select and menu-bar"""
        if self.ordersTable.underMouse():
            global ordersId

            contextMenu = QMenu(self)

            openFolder = contextMenu.addAction("Open Folder")
            openFolder.triggered.connect(self.openFolder)
            openFolder.setShortcut("Alt+D")
            openFolder.setIcon(QIcon("static/icons/drawings.png"))

            contextMenu.addSeparator()

            openFile = contextMenu.addAction("Open File")
            openFile.triggered.connect(self.openFile)
            openFile.setShortcut("Alt+L")
            openFile.setIcon(QIcon("static/icons/files.png"))

            contextMenu.addSeparator()

            new2 = contextMenu.addAction("New")
            new2.triggered.connect(self.add_orders)
            new2.setShortcut("Ctrl+N")

            contextMenu.addSeparator()

            Refresh2 = contextMenu.addAction("Refresh")
            Refresh2.triggered.connect(self.listTables)
            Refresh2.setShortcut("F5")
            Refresh2.setIcon(QIcon("static/icons/refresh.png"))

            contextMenu.addSeparator()

            delete = contextMenu.addAction("Delete")
            delete.triggered.connect(self.deleteItem)

            action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def display_table(self):
        """Fills table with data from sql"""
        # Get current date
        if datetime.day() <= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-0{2}".format(year, month, day))
        elif datetime.day() <= 9 and datetime.month() >= 10:
            date = ("{0}-{1}-0{2}".format(year, month, day))
        elif datetime.day() >= 9 and datetime.month() <= 9:
            date = ("{0}-0{1}-{2}".format(year, month, day))
        else:
            date = ("{0}-{1}-{2}".format(year, month, day))

        # Cleans table
        self.ordersTable.setFont(QFont("Times", 10))

        for i in reversed(range(self.ordersTable.rowCount())):
            self.ordersTable.removeRow(i)

        # Connect to SQL table
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(
            """SELECT id, company, client, phone_number, order_name,
            order_term, status, comments, order_folder, order_file, update_date,
            filename, filetype, filedir FROM orders 
            ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
        query = cur.fetchall()

        # Sort table values and adds to table, change color of some values
        for row_date in query:
            row_number = self.ordersTable.rowCount()
            self.ordersTable.insertRow(row_number)
            for column_number, data in enumerate(row_date):
                setitem = QTableWidgetItem(str(data))
                # check current date and table entry, if nor equal or bigger make it red
                listdata = []
                if column_number == 5:
                    listdata.append(str(data))
                    if listdata[0] == "+" or listdata[0] == "-":
                        listdata.pop()
                for i in listdata:
                    if int(i[5:7]) > int(date[5:7]) or int(i[0:4]) > int(date[0:4]):
                        setitem.setBackground(QtGui.QColor(255, 255, 255))
                    elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                            or int(i[0:4]) < int(date[0:4]):
                        setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                        # setitem.setForeground(QtGui.QColor(255, 255, 255))

                # list of names and list of colours to name
                list_names = ['FINISHED', 'IN PROCESS']
                list_colors = [(0, 204, 0, 110), (122, 197, 205)]
                for count_num in range(0, len(list_names)):
                    while count_num < len(list_names):
                        if data == list_names[count_num]:
                            setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                        count_num += 1

                self.ordersTable.setItem(row_number, column_number, setitem)

        # Edit column cell disable
        self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        con.close()

    def listTables(self):
        """Fills and sorts data from sql to table"""
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
            if self.treeTable.currentItem() == self.ordersSelect:
                self.tableRightLayout.setCurrentIndex(0)
                self.display_table()

            else:
                con = psycopg2.connect(**params)

                for index_number in range(0, len(self.headers)):
                    if self.treeTable.currentItem() == self.ordersSelect.child(index_number):
                        self.tableRightLayout.setCurrentIndex(0)
                        self.ordersTable.setFont(QFont("Times", 10))
                        for i in reversed(range(self.ordersTable.rowCount())):
                            self.ordersTable.removeRow(i)

                        cur = con.cursor()
                        cur.execute(
                            f"""SELECT id, company, client, phone_number, order_name,
                            order_term, status, comments, order_folder, order_file, update_date,
                            filename, filetype, filedir FROM orders
                            WHERE order_name = '{self.headers[index_number]}' 
                            ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
                        query = cur.fetchall()

                        for row_date in query:
                            row_number = self.ordersTable.rowCount()
                            self.ordersTable.insertRow(row_number)
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
                                        pass
                                    elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                            or int(i[0:4]) < int(date[0:4]):
                                        setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                        # setitem.setForeground(QtGui.QColor(255, 255, 255))

                                # list of names and list of colours to name
                                list_names = ['FINISHED', 'IN PROCESS']
                                list_colors = [(0, 204, 0, 110), (122, 197, 205)]
                                for count_num in range(0, len(list_names)):
                                    while count_num < len(list_names):
                                        if data == list_names[count_num]:
                                            setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                        count_num += 1

                                self.ordersTable.setItem(row_number, column_number, setitem)

                        self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def refresh_tree_pavaros_items(self):
        """Refresh table func"""
        self.treeTable.clear()
        self.treeTableItems()
        self.treeTable.setCurrentItem(self.ordersSelect)

    def add_combo(self):
        """Opens add_combo widnow"""
        self.edit_combobox = AddCombo()
        self.edit_combobox.exec_()

    def add_orders(self):
        """Opens add-order widnow"""
        try:
            self.neworders = Addorders()
            # Refresh table after executing QDialog .exec_
            self.neworders.exec_()
            self.display_table()
            self.refresh_tree_pavaros_items()

        except:
            pass

    def updateorders(self):
        """Opens update_order widnow and select row data and fills entries with current data from that row"""
        global ordersId

        try:
            self.display = orderUpdate()
            self.display.show()
            self.display.exec_()
            self.display_table()
            self.refresh_tree_pavaros_items()

        except:
            pass

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
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                search_form = self.searchEntry1.text()

                self.ordersTable.setFont(QFont("Times", 10))
                for i in reversed(range(self.ordersTable.rowCount())):
                    self.ordersTable.removeRow(i)

                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute(f"""SELECT * FROM orders WHERE
                    company ILIKE '%{search_form}%' OR client ILIKE '%{search_form}%' 
                    OR phone_number ILIKE '%{search_form}%' OR order_name ILIKE '%{search_form}%' 
                    OR comments ILIKE '%{search_form}%'""")
                query = cur.fetchall()

                for row_date in query:
                    row_number = self.ordersTable.rowCount()
                    self.ordersTable.insertRow(row_number)
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
                                pass
                            elif int(i[8:10]) < int(date[8:10]) or int(i[5:7]) < int(date[5:7]) \
                                    or int(i[0:4]) < int(date[0:4]):
                                setitem.setBackground(QtGui.QColor(255, 0, 0, 110))
                                # setitem.setForeground(QtGui.QColor(255, 255, 255))

                        # list of names and list of colours to name
                        list_names = ['FINISHED', 'IN PROCESS']
                        list_colors = [(0, 204, 0, 110), (122, 197, 205)]
                        for count_num in range(0, len(list_names)):
                            while count_num < len(list_names):
                                if data == list_names[count_num]:
                                    setitem.setBackground(QtGui.QColor(*list_colors[count_num]))
                                count_num += 1

                        self.ordersTable.setItem(row_number, column_number, setitem)

                self.ordersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

                conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def clearSearchEntry(self):
        """Search cancel and refresh table"""
        self.searchEntry1.clear()

        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                self.listTables()

        except:
            pass

    def searchTables2(self, s):
        """Search for items and select matched items"""
        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                # Clear current selection
                self.ordersTable.setCurrentItem(None)

                if not s:
                    # Empty string, do not search
                    return

                matching_items = self.ordersTable.findItems(s, Qt.MatchContains)
                if matching_items:
                    # if it finds something
                    for item in matching_items:
                        item.setSelected(True)
                        item.setSelected(True)

        except:
            pass

    def clearSearchEntry2(self):
        """Clears search entry"""
        self.searchEntry2.clear()

    def deleteItem(self):
        """Deletes item and refresh list"""
        mbox = QMessageBox()
        mbox.setWindowTitle("DELETE")
        mbox.setText("DELETE?")
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        style.mboxsheetstyle(mbox)

        x = mbox.exec_()

        try:
            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):

                global ordersId

                try:
                    if (x == QMessageBox.Yes):
                        conn = psycopg2.connect(
                            **params
                        )

                        cur = conn.cursor()
                        cur.execute("DELETE FROM orders WHERE id = %s", (ordersId,))
                        conn.commit()
                        conn.close()

                        self.display_table()

                        self.refresh_tree_pavaros_items()

                    elif (x == QMessageBox.No):
                        pass

                except (Exception, psycopg2.Error) as error:
                    print("Error while fetching data from PostgreSQL", error)
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR...")
                    msg.setText(f"Please first select ROW you want to delete.")
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

                    style.msgsheetstyle(msg)

                    x = msg.exec_()

        except:
            pass

    def save(self):
        """Save table as .csv file to './save' dir"""
        try:
            self.table_name = ""

            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                self.table_name = "orders"

            conn = psycopg2.connect(
                **params
            )
            cur = conn.cursor()
            cur.execute("""SELECT * FROM {}""".format(self.table_name))
            query = cur.fetchall()

            data = pandas.DataFrame(query)

            path = "save"
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)

            data.to_csv(f"save/{self.table_name}-{datetime.toPyDate()}")

            conn.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def saveAs(self):
        """Save table as .xlsx or .csv file to selected dir"""

        headers = ""
        table = ""
        table_name = ""

        try:

            if self.treeTable.currentItem() == self.ordersSelect or \
                    self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                    self.treeTable.currentItem() == self.ordersSelect.child(1):
                headers = ["COMPANY", "CLIENT", "PHONE NUMBER", "ORDER NAME", "ORDER TERM",
                           "STATUS", "COMMENTS", "FOLDER LINK", "ORDER FILE", "UPDATED"]
                table = self.ordersTable
                table_name = "orders"

            filename, file_end = QFileDialog.getSaveFileName(self, 'Save', '',
                                                             "(*.xlsx);; (*.csv)")
            dir_path = os.path.dirname(filename)
            file_name = os.path.basename(filename).split(".")[0]

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

            elif file_end == ".csv(*.csv)":
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

                    data.append(row_data)
                data_table = pandas.DataFrame(data,
                                              columns=headers)

                data_table.to_csv(f"{dir_path}/{file_name}", index=False)

        except KeyError:
            print(KeyError)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"{KeyError}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def handlePrint(self):
        """Sends info to print and prints"""
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        """Print preview"""
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        """Paint print table"""
        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(0.5)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0)
        tableFormat.setTopMargin(0)
        tableFormat.setCellPadding(4)
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)

        if self.treeTable.currentItem() == self.ordersSelect or \
                self.treeTable.currentItem() == self.ordersSelect.child(0) or \
                self.treeTable.currentItem() == self.ordersSelect.child(1):
            table_name = self.ordersTable

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
        """Open selected folder"""
        try:
            global ordersId

            conn = psycopg2.connect(
                **params
            )

            cur = conn.cursor()
            cur.execute("""SELECT * FROM orders WHERE ID=%s""", (ordersId,))
            uzsakymas = cur.fetchone()

            uzsakymasFolder = uzsakymas[8]

            conn.close()

            isExist = os.path.exists(uzsakymasFolder)

            if isExist:
                webbrowser.open(os.path.realpath(uzsakymasFolder))

            else:
                if not isExist:
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR...")
                    msg.setText("NO FOLDER...")
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

                    style.msgsheetstyle(msg)

                    x = msg.exec_()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to open.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def ordersWriteToFile(self, data, filename):
        """Convert binary data to proper format and write it on Hard Disk"""
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def openFile(self):
        """Download selected file from sql and open it"""
        global ordersId

        try:
            con = psycopg2.connect(
                **params
            )

            c = con.cursor()

            c.execute("""SELECT * FROM orders WHERE ID = %s""", (ordersId,))
            uzsakymai = c.fetchone()

            self.filename = uzsakymai[11]
            self.photo = uzsakymai[12]
            self.filetype = uzsakymai[13]

            str_none = ""

            if self.filetype == None or self.filetype == str_none \
                    or self.photo == None or self.photo == str_none \
                    or self.filename == None or self.filename == str_none:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText("NO FILE...")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

                style.msgsheetstyle(msg)

                x = msg.exec_()

            else:
                path = "uzsakymai_list"
                # Check whether the specified path exists or not
                if not os.path.isdir(path):
                    os.makedirs(path)

                photoPath = "uzsakymai_list/" + self.filename + self.filetype

                if not os.path.isfile(photoPath):
                    self.ordersWriteToFile(self.photo, photoPath)

                os.startfile(os.path.abspath(os.getcwd()) + "/" + photoPath, 'open')

                con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Please first select ROW you want to open.")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def MainClose(self):
        """Exit app"""
        self.destroy()


class orderUpdate(QDialog, scaling_dpi):
    """Double mouse click window, update selected order data"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle('UPDATE')
        self.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(800 * self.scale_factor), int(431 * self.scale_factor))
        self.setFixedSize(self.size())

        style.QDialogsheetstyle(self)

        # creates registry folder and subfolder
        self.settings = QSettings('Order App', 'Update1')
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
        self.ordersDetails()
        self.widgets()
        self.layouts()

    def ordersDetails(self):
        global ordersId

        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM orders WHERE ID=%s""", (ordersId,))
        orders = cur.fetchone()
        conn.close()

        self.uzsakymasCompany = orders[1]
        self.uzsakymasClient = orders[2]
        self.uzsakymasPhone = orders[3]
        self.uzsakymasName = orders[4]
        self.uzsakymasTerm = orders[5]
        self.uzsakymasStatus = orders[6]
        self.uzsakymasComments = orders[7]
        self.uzsakymasFolder = orders[8]
        self.uzsakymasFile = orders[9]
        self.filename = orders[12]
        self.photo = orders[13]
        self.filetype = orders[14]

    def widgets(self):
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM combo_orders ORDER BY id ASC""")
        query = cur.fetchall()

        list_company_start = [item[1] for item in query]
        list_company = []
        for a in list_company_start:
            list_company.append(a)
            if a == None or a == "":
                list_company.remove(a)

        list_client_start = [item[2] for item in query]
        list_client = []
        for b in list_client_start:
            list_client.append(b)
            if b == None or b == "":
                list_client.remove(b)

        list_phone_start = [item[3] for item in query]
        list_phone = []
        for c in list_phone_start:
            list_phone.append(c)
            if c == None or c == "":
                list_phone.remove(c)

        list_name_start = [item[4] for item in query]
        list_name = []
        for d in list_name_start:
            list_name.append(d)
            if d == None or d == "":
                list_name.remove(d)

        conn.close()

        self.companyCombo1 = QComboBox()
        self.companyCombo1.setEditable(True)
        self.companyCombo1.addItems(list_company)
        self.companyCombo1.setCurrentText(self.uzsakymasCompany)
        self.companyCombo1.setFont(QFont("Times", 12))
        self.companyCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.clientCombo1 = QComboBox()
        self.clientCombo1.setEditable(True)
        self.clientCombo1.addItems(list_client)
        self.clientCombo1.setCurrentText(self.uzsakymasClient)
        self.clientCombo1.setFont(QFont("Times", 12))
        self.clientCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.phoneCombo1 = QComboBox()
        self.phoneCombo1.setEditable(True)
        self.phoneCombo1.setPlaceholderText('Text')
        self.phoneCombo1.addItems(list_phone)
        self.phoneCombo1.setCurrentText(self.uzsakymasPhone)
        self.phoneCombo1.setFont(QFont("Times", 12))
        self.phoneCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.nameCombo1 = QComboBox()
        self.nameCombo1.setEditable(True)
        self.nameCombo1.setPlaceholderText('Text')
        self.nameCombo1.addItems(list_name)
        self.nameCombo1.setCurrentText(self.uzsakymasName)
        self.nameCombo1.setFont(QFont("Times", 12))
        self.nameCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.termEntry1 = QComboBox()
        self.termEntry1.addItems(["-", "+"])
        self.termEntry1.setEditable(True)
        self.termEntry1.setCurrentText(self.uzsakymasTerm)
        self.termEntry1.setFont(QFont("Times", 12))
        self.termEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.statusCombo1 = QComboBox()
        self.statusCombo1.addItems(['FINISHED', 'IN PROCESS'])
        self.statusCombo1.setEditable(True)
        self.statusCombo1.setCurrentText(self.uzsakymasStatus)
        self.statusCombo1.setFont(QFont("Times", 12))
        self.statusCombo1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.commentsEntry1 = QTextEdit()
        self.commentsEntry1.setText(self.uzsakymasComments)
        self.commentsEntry1.setFont(QFont("Times", 12))

        self.locEntry = QLineEdit()
        self.locEntry.setText(self.uzsakymasFolder)
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;}")
        self.locEntry.setFont(QFont("Times", 12))
        self.locEntry.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.folderBtn = QPushButton("LINK TO FOLDER")
        self.folderBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.folderBtn.clicked.connect(self.OpenFolderDialog)
        self.folderBtn.setFont(QFont("Times", 10))

        self.ListEntry1 = QLineEdit()
        self.ListEntry1.setText(self.uzsakymasFile)
        self.ListEntry1.setReadOnly(True)
        self.ListEntry1.setFont(QFont("Times", 12))
        self.ListEntry1.setStyleSheet("QLineEdit{background: darkgrey;}")
        self.ListEntry1.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.fileBtn = QPushButton("CHANGE FILE")
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("CHANGE DATE")
        self.dateBtn.setFixedWidth(int(110 * self.scale_factor))
        self.dateBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFont(QFont("Times", 10))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.clicked.connect(self.updateorders)
        self.okBtn.setFont(QFont("Times", 10))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.clicked.connect(self.cancelorders)
        self.cancelBtn.setFont(QFont("Times", 10))

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QHBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()
        self.widgetFrame.setFont(QFont("Times", 12))
        self.widgetFrame2.setFont(QFont("Times", 12))

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.termEntry1)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("Company:"), self.companyCombo1)
        self.widgetLayout.addRow(QLabel("Client:"), self.clientCombo1)
        self.widgetLayout.addRow(QLabel("Phone Number:"), self.phoneCombo1)
        self.widgetLayout.addRow(QLabel("Order Name:"), self.nameCombo1)
        self.widgetLayout.addRow(QLabel("Order Term:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("Order Status:"), self.statusCombo1)
        self.widgetLayout.addRow(QLabel("Add Folder:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.folderBtn)
        self.widgetLayout.addRow(QLabel("Add File:"), self.ListEntry1)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("Comments:"))
        self.widgetLayout2.addRow(self.commentsEntry1)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        self.mainLayout1.addWidget(self.widgetFrame, 50)
        self.mainLayout1.addWidget(self.widgetFrame2, 50)

        self.mainLayout.addLayout(self.mainLayout1)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def terminasCalendar(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QWidget()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(int(780 / self.scale_factor), int(280 / self.scale_factor),
                                        int(350 * self.scale_factor), int(350 * self.scale_factor))
        self.calendarWindow.setWindowTitle('ORDER TERM')
        self.calendarWindow.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        style.QCalendarstyle(self)
        self.calendarWindow.show()

        def get_date(qDate):
            if qDate.day() <= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            elif qDate.day() <= 9 and qDate.month() >= 10:
                date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            elif qDate.day() >= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            else:
                date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry1.setCurrentText(date)
            self.calendarWindow.close()

        self.cal.clicked.connect(get_date)

    def cal_cancel(self):
        self.calendarWindow.close()

    def convertToBinaryDataFile(self, filename):
        """Convert digital data to binary format"""
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData

        except:
            pass

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*.pdf;*.txt;*.jpg;*.png;*.xls)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name

        justfilename = getfullfilename[:-4]
        filetype = getfullfilename[-4:]

        self.ListDir.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetype))

        self.ListEntry1.setText(f"{justfilename}{filetype}")

    def updateorders(self):
        global ordersId

        company1 = self.companyCombo1.currentText().upper()
        client1 = self.clientCombo1.currentText().upper()
        phone1 = self.phoneCombo1.currentText().upper()
        name1 = self.nameCombo1.currentText()
        term1 = self.termEntry1.currentText()
        status1 = self.statusCombo1.currentText().upper()
        comments1 = str(self.commentsEntry1.toPlainText())
        folder1 = self.locEntry.text()
        file1 = self.ListEntry1.text()
        update_date1 = self.update_date.text()

        filename1 = self.ListFileName.text()
        blobPhoto1 = self.convertToBinaryDataFile(self.ListDir.text())
        filetype1 = self.ListFileType.text()
        filedir1 = self.ListDir.text()

        term_entry = ""

        if term1 != term_entry:
            try:
                if self.ListDir.text() != "":
                    conn = psycopg2.connect(**params)

                    cur = conn.cursor()
                    query = "UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, " \
                            "order_term = %s, status = %s, comments = %s, order_folder = %s, order_file = %s, " \
                            "update_date = %s, filename = %s, photo = %s, filetype = %s, filedir = %s " \
                            "where id = %s"
                    cur.execute(query, (company1, client1, phone1, name1, term1, status1, comments1,
                                        folder1, file1, update_date1, filename1, blobPhoto1, filetype1, filedir1,
                                        ordersId))
                    conn.commit()
                    conn.close()

                else:
                    conn = psycopg2.connect(
                        **params
                    )

                    cur = conn.cursor()

                    query = "UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, " \
                            "order_term = %s, status = %s, comments = %s, order_folder = %s, order_file = %s, " \
                            "update_date = %s where id = %s"
                    cur.execute(query, (company1, client1, phone1, name1, term1, status1, comments1,
                                        folder1, file1, update_date1, ordersId))
                    conn.commit()
                    conn.close()

            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText(f"Error while fetching data from PostgreSQL: {error}")
                msg.setIcon(QMessageBox.Information)
                msg.setWindowIcon(QIcon('static/icons/icon.ico'))

                style.msgsheetstyle(msg)

                x = msg.exec_()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("ORDER TERM can't be empty...")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('static/icons/icon.ico'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelorders(self):
        self.close()


class AddCombo(QDialog, scaling_dpi):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ADD ComboBox ITEMS')
        self.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(400 * self.scale_factor), int(280 * self.scale_factor))
        self.setFixedSize(self.size())

        style.QDialogsheetstyle(self)

        self.settings = QSettings('Order App', 'Combo')

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
        self.companyE = QLineEdit()
        self.companyE.setFont(QFont("Times", 12))
        self.companyE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.clientE = QLineEdit()
        self.clientE.setFont(QFont("Times", 12))
        self.clientE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.phoneE = QLineEdit()
        self.phoneE.setFont(QFont("Times", 12))
        self.phoneE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.nameE = QLineEdit()
        self.nameE.setFont(QFont("Times", 12))
        self.nameE.setFixedHeight(self.ENTRY_COMBO_HEIGHT)

        self.okBtn = QPushButton("UPDATE")
        self.okBtn.clicked.connect(self.addCombo)
        self.okBtn.setFont(QFont("Times", 10))
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)

        self.cancelBtn = QPushButton("CLOSE")
        self.cancelBtn.clicked.connect(self.closeAddCombo)
        self.cancelBtn.setFont(QFont("Times", 10))
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)

    def layouts(self):
        self.mainLayout = QGridLayout()

        self.widgetLayout = QFormLayout()
        self.widgetFrame = QGroupBox("Order Combo Items:")
        self.widgetFrame.setFont(QFont("Times", 12))

        self.widgetLayout.addRow(QLabel("Company: "), self.companyE)
        self.widgetLayout.addRow(QLabel("Client: "), self.clientE)
        self.widgetLayout.addRow(QLabel("Phone Number: "), self.phoneE)
        self.widgetLayout.addRow(QLabel("Order Name: "), self.nameE)
        self.widgetLayout.addRow(QLabel(""))
        self.widgetFrame.setLayout(self.widgetLayout)

        self.mainLayout.addWidget(self.widgetFrame, 0, 0)
        self.mainLayout.addWidget(self.okBtn, 1, 0)
        self.mainLayout.addWidget(self.cancelBtn, 2, 0)

        self.setLayout(self.mainLayout)

    def addCombo(self):
        company = self.companyE.text().upper()
        client = self.clientE.text().upper()
        phone = self.phoneE.text().upper()
        name = self.nameE.text()

        try:
            con = psycopg2.connect(**params)
            c = con.cursor()
            c.execute('''INSERT INTO combo_orders (company, client, phone_number, 
                        order_name) VALUES (%s, %s, %s, %s)''',
                      (company, client, phone, name))
            con.commit()
            con.close()

        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Error while fetching data from PostgreSQL: {error}")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

        finally:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText(f"Has been successfully added.")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

    def closeAddCombo(self):
        self.close()


class Addorders(QDialog, scaling_dpi):
    """Add new record window"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NEW")
        self.setWindowIcon(QIcon('static/icons/uzsakymai_icon.png'))
        self.setGeometry(int(400 / self.scale_factor), int(300 / self.scale_factor),
                         int(800 * self.scale_factor), int(432 * self.scale_factor))
        self.setFixedSize(self.size())

        self.UI()

        self.show()

        style.QDialogsheetstyle(self)

        self.settings = QSettings('Order App', 'Add1')

        try:
            self.resize(self.settings.value('window size'))
            self.move(self.settings.value('window position'))
        except:
            pass

    def closeEvent(self, event):
        self.settings.setValue('scale_aware', True)
        self.settings.setValue('window size', self.size())
        self.settings.setValue('window position', self.pos())

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""SELECT * FROM combo_orders ORDER BY id ASC""")
        query = cur.fetchall()

        list_company = [item[1] for item in query if item != None and item != ""]
        list_client = [item[2] for item in query if item != None and item != ""]
        list_phone = [item[3] for item in query if item != None and item != ""]
        list_name = [item[4] for item in query if item != None and item != ""]

        conn.close()

        self.companyCombo = QComboBox()
        self.companyCombo.setEditable(True)
        self.companyCombo.setPlaceholderText('Text')
        self.companyCombo.addItems(list_company)
        self.companyCombo.setFont(QFont("Times", 12))

        self.clientCombo = QComboBox()
        self.clientCombo.setEditable(True)
        self.clientCombo.setPlaceholderText('Text')
        self.clientCombo.addItems(list_client)
        self.clientCombo.setFont(QFont("Times", 12))

        self.phoneCombo = QComboBox()
        self.phoneCombo.setEditable(True)
        self.phoneCombo.setPlaceholderText('Text')
        self.phoneCombo.addItems(list_phone)
        self.phoneCombo.setFont(QFont("Times", 12))

        self.nameCombo = QComboBox()
        self.nameCombo.setEditable(True)
        self.nameCombo.setPlaceholderText('Text')
        self.nameCombo.addItems(list_name)
        self.nameCombo.setFont(QFont("Times", 12))

        self.termEntry = QComboBox()
        self.termEntry.setEditable(True)
        self.termEntry.addItems(
            ["-", "+"])
        self.termEntry.setFont(QFont("Times", 12))

        self.statusEntry = QComboBox()
        self.statusEntry.setEditable(True)
        self.statusEntry.setPlaceholderText('Text')
        self.statusEntry.addItems(
            ["FINISHED", "IN PROCESS"])
        self.statusEntry.setFont(QFont("Times", 12))

        self.commentsEntry = QTextEdit()
        self.commentsEntry.setFont(QFont("Times", 12))
        self.commentsEntry.setPlaceholderText('Text')

        self.locEntry = QLineEdit()
        self.locEntry.setReadOnly(True)
        self.locEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                    "color:black;}")
        self.locEntry.setFont(QFont("Times", 12))

        self.folderBtn = QPushButton("ADD LINK TO FOLDER")
        self.folderBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.folderBtn.clicked.connect(self.OpenFolderDialog)
        self.folderBtn.setFont(QFont("Times", 10))

        self.ListEntry = QLineEdit()
        self.ListEntry.setReadOnly(True)
        self.ListEntry.setStyleSheet("QLineEdit{background: darkgrey;"
                                     "color:black;}")

        self.ListEntry.setFont(QFont("Times", 12))

        self.fileBtn = QPushButton("ADD FILE")
        self.fileBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.fileBtn.clicked.connect(self.getFileInfo)
        self.fileBtn.setFont(QFont("Times", 10))

        self.dateBtn = QPushButton("ADD DATE")
        self.dateBtn.setFixedWidth(int(110 * self.scale_factor))
        self.dateBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.dateBtn.clicked.connect(self.terminasCalendar)
        self.dateBtn.setFont(QFont("Times", 10))

        self.okBtn = QPushButton("OK")
        self.okBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.okBtn.clicked.connect(self.addorders)
        self.okBtn.setFont(QFont("Times", 10))

        self.cancelBtn = QPushButton("CANCEL")
        self.cancelBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.cancelBtn.clicked.connect(self.cancelordersAdd)
        self.cancelBtn.setFont(QFont("Times", 10))

        self.update_date = QLineEdit()
        self.update_date.setText("{}".format(datetime.toPyDate()))

        self.ListDir = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

    def layouts(self):
        self.topmainLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.mainLayout1 = QVBoxLayout()
        self.mainLayout2 = QVBoxLayout()
        self.widgetLayout = QFormLayout()
        self.widgetLayout2 = QFormLayout()
        self.widgetFrame = QFrame()
        self.widgetFrame2 = QFrame()
        self.widgetFrame.setFont(QFont("Times", 12))
        self.widgetFrame2.setFont(QFont("Times", 12))

        self.qhbox3 = QHBoxLayout()
        self.qhbox3.addWidget(self.termEntry)
        self.qhbox3.addWidget(self.dateBtn)

        self.widgetLayout.addRow(QLabel("Company:"), self.companyCombo)
        self.widgetLayout.addRow(QLabel("Client:"), self.clientCombo)
        self.widgetLayout.addRow(QLabel("Phone Number:"), self.phoneCombo)
        self.widgetLayout.addRow(QLabel("Order Name:"), self.nameCombo)
        self.widgetLayout.addRow(QLabel("Order Term:"), self.qhbox3)
        self.widgetLayout.addRow(QLabel("Order Status:"), self.statusEntry)

        self.widgetLayout.addRow(QLabel("Add Folder:"), self.locEntry)
        self.widgetLayout.addRow(QLabel(""), self.folderBtn)
        self.widgetLayout.addRow(QLabel("Add File:"), self.ListEntry)
        self.widgetLayout.addRow(QLabel(""), self.fileBtn)
        self.widgetLayout.addRow(QLabel(""))

        self.widgetLayout.addRow(self.okBtn)
        self.widgetLayout.addRow(self.cancelBtn)
        self.widgetFrame.setLayout(self.widgetLayout)

        self.widgetLayout2.addRow(QLabel("Comments:"))
        self.widgetLayout2.addRow(self.commentsEntry)
        self.widgetFrame2.setLayout(self.widgetLayout2)

        self.mainLayout1.addWidget(self.widgetFrame)
        self.mainLayout2.addWidget(self.widgetFrame2)

        self.mainLayout.addLayout(self.mainLayout1, 50)
        self.mainLayout.addLayout(self.mainLayout2, 50)

        self.setLayout(self.mainLayout)

    def OpenFolderDialog(self):
        """Get folder dir"""
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.locEntry.setText('{}'.format(directory))

    def convertToBinaryDataFile(self, filename):
        """Convert digital data to binary format"""
        try:
            with open(filename, 'rb') as file:
                blobData = file.read()
            return blobData
        except:
            pass

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "(*All;*)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name
        justfilename = getfullfilename.split(".")[0]
        filetype = getfullfilename.split(".")[1]
        print(filetype)

        self.ListDir.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetype))

        self.ListEntry.setText(f"{justfilename}.{filetype}")

    def terminasCalendar(self):
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.calBtn = QPushButton("CANCEL")
        self.calBtn.setFont(QFont("Times", 10))
        self.calBtn.setFixedHeight(self.BUTTON_HEIGHT)
        self.calBtn.clicked.connect(self.cal_cancel)

        self.calendarWindow = QDialog()
        self.hbox = QVBoxLayout()
        self.hbox.addWidget(self.cal)
        self.hbox.addWidget(self.calBtn)
        self.calendarWindow.setLayout(self.hbox)
        self.calendarWindow.setGeometry(int(780 / self.scale_factor), int(280 / self.scale_factor),
                                        int(350 * self.scale_factor), int(350 * self.scale_factor))
        self.calendarWindow.setWindowTitle('TERMINAS')
        self.calendarWindow.setWindowIcon(QIcon('icons/uzsakymai_icon.png'))
        style.QCalendarstyle(self)
        self.calendarWindow.show()

        def get_date(qDate):
            if qDate.day() <= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            elif qDate.day() <= 9 and qDate.month() >= 10:
                date = ("{0}-{1}-0{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            elif qDate.day() >= 9 and qDate.month() <= 9:
                date = ("{0}-0{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            else:
                date = ("{0}-{1}-{2}".format(qDate.year(), qDate.month(), qDate.day()))
                self.termEntry.setCurrentText(date)
            self.calendarWindow.close()

        self.cal.clicked.connect(get_date)

    def cal_cancel(self):
        self.calendarWindow.close()

    def addorders(self):
        company = self.companyCombo.currentText().upper()
        client = self.clientCombo.currentText().upper()
        phone = self.phoneCombo.currentText().upper()
        name = self.nameCombo.currentText()
        term = self.termEntry.currentText()
        status = self.statusEntry.currentText().upper()
        comments = str(self.commentsEntry.toPlainText())
        folder = self.locEntry.text()
        file = self.ListEntry.text()
        update_date1 = self.update_date.text()

        filename = self.ListFileName.text()
        byteaPhoto = self.convertToBinaryDataFile(self.ListDir.text())
        listfiletype = self.ListFileType.text()
        listentry = self.ListDir.text()

        terminas_date = ""

        if term != terminas_date:
            try:
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                cur.execute('''INSERT INTO orders (company, client, phone_number, order_name,
                    order_term, status, comments, order_folder, order_file, update_date,
                    filename, photo, filetype, filedir) VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                            (company, client, phone, name,
                             term, status, comments, folder, file, update_date1,
                             filename, byteaPhoto, listfiletype, listentry))
                conn.commit()
                conn.close()

            except (Exception, psycopg2.Error) as error:
                print("Error while fetching data from PostgreSQL", error)
                msg = QMessageBox()
                msg.setWindowTitle("ERROR...")
                msg.setText(f"Error while fetching data from PostgreSQL: {error}")
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowIcon(QIcon('icons/uzsakymai_icon.png'))

                style.msgsheetstyle(msg)

                x = msg.exec_()

        else:
            msg = QMessageBox()
            msg.setWindowTitle("ERROR...")
            msg.setText("TERMINAS can't be empty...")
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowIcon(QIcon('icons/uzsakymai_icon.png'))

            style.msgsheetstyle(msg)

            x = msg.exec_()

        self.close()

    def cancelordersAdd(self):
        self.close()


def main():
    App = QApplication(sys.argv)
    window = MainMenu()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()
