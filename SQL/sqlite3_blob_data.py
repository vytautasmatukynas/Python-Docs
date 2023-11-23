import sqlite3
import sys
from pathlib import Path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)

        layout = QVBoxLayout()
        self.btn = QPushButton("Choose")
        self.btn.clicked.connect(self.getFileInfo)

        self.ListEntry = QLabel()
        self.ListFileName = QLabel()
        self.ListFileType = QLabel()

        self.btn1 = QPushButton("Add")
        self.btn1.clicked.connect(self.addfile)

        self.btn2 = QPushButton("Copy")
        self.btn2.clicked.connect(self.readblobfile)

        self.btn3 = QPushButton("Open")
        self.btn3.clicked.connect(self.openFile)

        layout.addWidget(self.btn)
        layout.addWidget(self.ListEntry)
        layout.addWidget(self.ListFileName)
        layout.addWidget(self.ListFileType)
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        layout.addWidget(self.btn3)

        self.setLayout(layout)
        self.setWindowTitle("File Dialog demo")

    def getFileInfo(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(self, "", "", "Images (*.jpg)")
        (directory, fileType) = dialog

        getfullfilename = Path(directory).name

        justfilename = getfullfilename[:-4]
        filetypejpg = getfullfilename[-4:]

        print(directory)
        print(justfilename)
        print(filetypejpg)

        self.ListEntry.setText('{}'.format(directory))
        self.ListFileName.setText('{}'.format(justfilename))
        self.ListFileType.setText('{}'.format(filetypejpg))

    ##################load file to SQL#####################
    def convertToBinaryData(self, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def insertBLOB(self, empId, name, photo, filetype, filedir):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')

            cursor = sqliteConnection.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL, 
            photo BLOB NOT NULL,
            filetype TEXT NOT NULL,
            filedir TEXT NOT NULL);""")

            print("Connected to SQLite")
            sqlite_insert_blob_query = """ INSERT INTO employees
                                      (id, name, photo, filetype, filedir) VALUES (?, ?, ?, ?, ?)"""

            empPhoto = self.convertToBinaryData(photo)
            # Convert data into tuple format
            data_tuple = (empId, name, empPhoto, filetype, filedir,)
            cursor.execute(sqlite_insert_blob_query, data_tuple)
            sqliteConnection.commit()
            print("Image and file inserted successfully as a BLOB into a table")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("the sqlite connection is closed")

    def addfile(self):
        self.insertBLOB(3, self.ListFileName.text(), self.ListEntry.text(), self.ListFileType.text(),
                        self.ListEntry.text())

    ############load file and create to loc dir####################
    def writeTofile(self, data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")

    def readBlobData(self, empId):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute("""SELECT * from employees where id = ?""", (empId,))
            record = cursor.fetchall()
            print(record)
            for row in record:
                print("Id = ", row[0], "Name = ", row[1], "FileType = ", row[3])
                name = row[1]
                photo = row[2]
                filetype = row[3]

                print("Storing employee image and resume on disk \n")
                photoPath = "C:/Projektai/New folder//" + name + filetype
                self.writeTofile(photo, photoPath)

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")

    def readblobfile(self):
        self.readBlobData(3)

    ###################open file##################
    def openFile(self):
        import os
        try:
            empId = 3
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            cursor.execute("""SELECT * from employees where id = ?""", (empId,))
            record = cursor.fetchall()
            print(record)
            for row in record:
                print(row[4])
                filedir = row[4]

                photoPath = (filedir)
                print(photoPath)
                os.startfile(photoPath)

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read blob data from sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("sqlite connection is closed")


def main():
    app = QApplication(sys.argv)
    ex = filedialogdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
