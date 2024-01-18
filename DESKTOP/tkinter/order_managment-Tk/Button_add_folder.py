import os
import sqlite3
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

gui = Tk()
gui.geometry("400x400")
gui.title("FC")

conn = sqlite3.connect('uzsakymai.db')

c = conn.cursor()

c.execute("""CREATE TABLE if not exists uzsakymai (
        IMONE text,
        KONSTRUKTORIUS text,
        PROJEKTAS text,
        TERMINAS text,
        STATUSAS text,
        ID text
        )
        """)


def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)


def doStuff():
    folderPath.get()


folderPath = StringVar()
a = Label(gui, text="Enter name")
a.grid(row=0, column=0)
E = Entry(gui, textvariable=folderPath)
E.grid(row=0, column=1)
btnFind = ttk.Button(gui, text="Browse Folder", command=getFolderPath)
btnFind.grid(row=0, column=2)

c = ttk.Button(gui, text="find", command=doStuff)
c.grid(row=4, column=0)


def breziniai():
    path = E.get()
    path = os.path.realpath(path)
    os.startfile(path)


order_files = Button(gui, text='Open', command=breziniai, bg='lightgrey',
                     font='sans 10')
order_files.grid(row=4, column=1)

gui.mainloop()
