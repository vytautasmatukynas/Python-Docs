def SheetStyle(self):
    """app.py style"""
    self.setStyleSheet("""QWidget{
                            background-color:lightgrey;
                            }

                            QGroupBox{
                            background-color:lightgrey;
                            border: 1px solid black;
                            padding-top:10px;
                            }

                            QGroupBox::title {
                            color: black;
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


                            QTreeWidget{
                            background:floralwhite;
                            padding: 3%;
                            }

                            QTreeWidget::item:hover{
                            background:steelblue;
                            color: white;
                            }

                            QTreeWidget::item:selected{
                            background:slategray;
                            color:white;
                            border: 1px solid black;
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



                            QLineEdit{
                            background-color:white;
                            color:black;
                            border:1px solid black;
                            padding:2px;
                            }



                            QMenuBar{
                            background-color: dimgray;
                            color: white;
                            border:1px solid black;
                            }

                            QMenuBar::item{
                            background-color: dimgray;
                            color: white;
                            padding:5px;
                            }

                            QMenuBar::item::selected{
                            background-color: steelblue;
                            color: white;
                            }

                            QMenu{
                            background-color: dimgray;
                            color: white;
                            border:1px solid black;
                            padding:3px;
                            }

                            QMenu::selected{
                            background-color: steelblue;
                            color: white;
                            }

                            QMenu::separator{
                            background-color:black;
                            margin:4px;
                            }



                            QToolBar{
                            background-color:dimgray;
                            color:darkgray;
                            border:1px solid black;
                            }

                            QToolBar::separator{
                            background-color:black;
                            margin:3px;
                            margin-left:2px;
                            }

                            QToolButton{
                            background-color:dimgray;
                            color:white;
                            padding:2px;
                            }

                            QToolButton::hover{
                            background-color:steelblue;
                            color:white;
                            }


                            """)


def msgsheetstyle(msg):
    msg.setStyleSheet("""QMessageBox{
                            background-color:lightgrey;
                            }

                            QPushButton{
                            background-color:dimgray;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            min-Width:40px;
                            }

                            QPushButton::hover{
                            background-color:steelblue;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }

                            """)
#
#
def mboxsheetstyle(mbox):
    mbox.setStyleSheet("""QMessageBox{
                            background-color:lightgrey;
                            }

                            QPushButton{
                            background-color:dimgray;
                            color:white;
                            border:1px solid black;
                            padding:3px;
                            min-Width:60px;
                            }

                            QPushButton::hover{
                            background-color:steelblue;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }

                            """)
#
def QDialogsheetstyle(self):
    self.setStyleSheet("""QDialog{
                            background-color:lightgray;
                            }


                            QLabel{
                            font-size: 12pt;
                            }

                            QPushButton{
                            background-color:dimgray;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::hover{
                            background-color:steelblue;
                            color:white;
                            border:1px solid black;
                            }

                            QPushButton::pressed{
                            background-color:black;
                            color:white;
                            }
                            """)

def QCalendarstyle(self):
    self.calendarWindow.setStyleSheet("""QPushButton{
                                        background-color:dimgray;
                                        color:white;
                                        border-radius:3px;
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