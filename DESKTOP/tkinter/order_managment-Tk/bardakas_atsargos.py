import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import psycopg2


k_atsargos_frame = Tk()

k_atsargos_frame.title('ATSARGOS')
mainWindow_width = 1000
mainWindow_height = 600

screen_width = k_atsargos_frame.winfo_screenwidth()
screen_height = k_atsargos_frame.winfo_screenheight()

x = (screen_width / 2) - (mainWindow_width / 2)
y = (screen_height / 2) - (mainWindow_height / 2)

k_atsargos_frame.geometry(f'{mainWindow_width}x{mainWindow_height}+{int(x)}+{int(y)}')

count = 1

conn = psycopg2.connect(
    **params
)

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS komponentai (
        ID INT GENERATED ALWAYS AS IDENTITY,
        PAVADINIMAS TEXT,
        VIETA TEXT,
        KIEKIS TEXT,
        KOMENTARAS TEXT
        )
        """)

conn.commit()

conn.close()


# Refresh database
def query_database():
    conn = psycopg2.connect(
        **params
    )

    c = conn.cursor()

    c.execute("""SELECT * FROM komponentai""")
    records = c.fetchall()

    my_tree.tag_configure('oddrow', foreground='white')
    my_tree.tag_configure('evenrow', foreground='white')

    global count

    for record in records:
        if count % 2 == 0:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2],
                                   record[3], record[4]), tags=('oddrow'))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='',
                           values=(record[0], record[1], record[2],
                                   record[3], record[4]), tags=('evenrow'))

        count += 1

    conn.commit()

    conn.close()


def search_records_popup():
    # Search Bar
    searchWindow = Toplevel(k_atsargos_frame)
    searchWindow.title('Search')
    searchWindow_width = 300
    searchWindow_height = 70
    searchWindow.resizable(FALSE, FALSE)

    screen_width = searchWindow.winfo_screenwidth()
    screen_height = searchWindow.winfo_screenheight()

    x = (screen_width / 2) - (searchWindow_width / 2)
    y = (screen_height / 2) - (searchWindow_height / 2)

    searchWindow.geometry(f'{searchWindow_width}x{searchWindow_height}+{int(x)}+{int(y)}')
    searchWindow.focus_force()

    searchWindow.columnconfigure(0, weight=1)
    searchWindow.columnconfigure(1, weight=1)
    searchWindow.columnconfigure(2, weight=1)
    searchWindow.columnconfigure(3, weight=1)
    searchWindow.columnconfigure(4, weight=1)
    searchWindow.rowconfigure(0, weight=1)
    searchWindow.rowconfigure(1, weight=1)

    search_box = Entry(searchWindow, bd=3, width=60)
    search_box.grid(row=1, column=0, sticky="news", padx=5)

    def search_records():
        search_record = search_box.get()
        search_record1 = search_box.get()

        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute(
            "SELECT * FROM komponentai WHERE pavadinimas ILIKE %s OR vieta ILIKE %s",
            (search_record, search_record1,))
        records = c.fetchall()

        global count

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2],
                                       record[3], record[4]), tags=('oddrow'))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2],
                                       record[3], record[4]), tags=('evenrow'))
            count += 1

        conn.commit()

        conn.close()

    def clear_search():
        search_box.delete(0, END)
        search_records()
        query_database()

    search_record = Button(searchWindow, text='Search', command=search_records, bg='lightgrey', width=6,
                           font='sans 10')
    search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=5)

    undo_search_record = Button(searchWindow, text="Cancel", command=clear_search, bg='lightgrey', width=6,
                                font='sans 10')
    undo_search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=(65, 0))

    def clear_search_x():
        search_box.delete(0, END)
        search_records()
        query_database()
        searchWindow.destroy()

    searchWindow.protocol("WM_DELETE_WINDOW", clear_search_x)


def search_records_bind(e):
    # Search Bar
    searchWindow = Toplevel(k_atsargos_frame)
    searchWindow.title('Search')
    searchWindow_width = 300
    searchWindow_height = 70
    searchWindow.resizable(FALSE, FALSE)

    screen_width = searchWindow.winfo_screenwidth()
    screen_height = searchWindow.winfo_screenheight()

    x = (screen_width / 2) - (searchWindow_width / 2)
    y = (screen_height / 2) - (searchWindow_height / 2)

    searchWindow.geometry(f'{searchWindow_width}x{searchWindow_height}+{int(x)}+{int(y)}')
    searchWindow.focus_force()

    searchWindow.columnconfigure(0, weight=1)
    searchWindow.columnconfigure(1, weight=1)
    searchWindow.columnconfigure(2, weight=1)
    searchWindow.columnconfigure(3, weight=1)
    searchWindow.columnconfigure(4, weight=1)
    searchWindow.rowconfigure(0, weight=1)
    searchWindow.rowconfigure(1, weight=1)

    search_box = Entry(searchWindow, bd=3, width=60)
    search_box.grid(row=1, column=0, sticky="news", padx=5)

    def search_records():
        search_record1 = search_box.get()

        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute("SELECT * FROM komponentai WHERE pavadinimas ILIKE %s;", (search_record1,))
        records = c.fetchall()

        global count

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2],
                                       record[3], record[4]), tags=('oddrow'))
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[0], record[1], record[2],
                                       record[3], record[4]), tags=('evenrow'))
            count += 1

        conn.commit()

        conn.close()

    def clear_search():
        search_box.delete(0, END)
        search_records()
        query_database()

    search_record = Button(searchWindow, text='Search', command=search_records, bg='lightgrey', width=6,
                           font='sans 10')
    search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=5)

    undo_search_record = Button(searchWindow, text="Cancel", command=clear_search, bg='lightgrey', width=6,
                                font='sans 10')
    undo_search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=(65, 0))

    def clear_search_x():
        search_box.delete(0, END)
        search_records()
        query_database()
        searchWindow.destroy()

    searchWindow.protocol("WM_DELETE_WINDOW", clear_search_x)


# Style
style = ttk.Style()

# Theme
style.theme_use("winnative")
# Treeview colors
style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=(25),
                fieldbackground="white"
                )
# Change selected color
style.map('Treeview',
          background=[('selected', 'black')])

# TreeView frame
tree_frame = Frame(k_atsargos_frame)
tree_frame.pack(side=TOP, pady=10, padx=10, fill=tkinter.BOTH, expand=TRUE)

# Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# selectmode='browse' - leidzia tik 1 eilute selectint
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode='browse')
my_tree.pack(side=TOP, fill=tkinter.BOTH, expand=TRUE)

# Configure scrollbar
tree_scroll.config(command=my_tree.yview)


# Sort columns
def tvsort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=col, command=lambda _col=col:
    tvsort_column(tv, _col, not reverse))


# Column list names
my_tree['columns'] = ("ID", "PAVADINIMAS", "VIETA", "KIEKIS", "KOMENTARAI")

# Column size
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=CENTER, width=0, stretch=NO)
my_tree.column("PAVADINIMAS", anchor=W, width=300, stretch=NO)
my_tree.column("VIETA", anchor=CENTER, width=150, stretch=NO)
my_tree.column("KIEKIS", anchor=CENTER, width=70, stretch=NO)
my_tree.column("KOMENTARAI", anchor=W, width=100)

# Column name
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("PAVADINIMAS", text="PAVADINIMAS", anchor=W)
my_tree.heading("VIETA", text="VIETA", anchor=CENTER)
my_tree.heading("KIEKIS", text="KIEKIS", anchor=CENTER)
my_tree.heading("KOMENTARAI", text="KOMENTARAI", anchor=W)

# sort column
for col in my_tree['columns']:
    my_tree.heading(col, text=col, command=lambda _col=col:
    tvsort_column(my_tree, _col, False))


def new_record():
    new_record_frame1 = Toplevel(k_atsargos_frame)
    new_record_frame1.title('NEW RECORD')

    new_record_frame_width = 600
    new_record_frame_height = 230

    screen_width = new_record_frame1.winfo_screenwidth()
    screen_height = new_record_frame1.winfo_screenheight()

    x = (screen_width / 2) - (new_record_frame_width / 2)
    y = (screen_height / 2) - (new_record_frame_height / 2)

    new_record_frame1.geometry(f'{new_record_frame_width}x{new_record_frame_height}+{int(x)}+{int(y)}')
    new_record_frame1.focus_force()

    data_frame = Frame(new_record_frame1)
    data_frame.pack(pady=5, padx=5, anchor=N)

    pv = Label(data_frame, text="PAVADINIMAS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15,
               height=2)
    pv.grid(row=0, column=0, sticky="nsew")

    vt = Label(data_frame, text="VIETA", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15, height=2)
    vt.grid(row=1, column=0, sticky="nsew")

    ks = Label(data_frame, text="KIEKIS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15, height=2)
    ks.grid(row=2, column=0, sticky="nsew")

    km = Label(data_frame, text="KOMENTARAS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15,
               height=2)
    km.grid(row=3, column=0, sticky="nsew")

    # Data input

    pv_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    pv_box.grid(row=0, column=1, sticky="nsew")

    vt_box = ttk.Combobox(data_frame, font='sans 10', state='normal', textvariable=StringVar(), width=59)
    vt_box['values'] = ('BUTRIMONIU C1', 'BUTRIMONIU C2', 'BUTRIMONIU C3', 'BUTRIMONIU C4', 'MITUVOS', 'OFISAS')
    vt_box.grid(row=1, column=1, sticky="nsew")

    ks_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    ks_box.grid(row=2, column=1, sticky="nsew")

    km_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    km_box.grid(row=3, column=1, sticky="nsew")

    def add_record():
        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute('''INSERT INTO komponentai (pavadinimas, vieta, kiekis, komentaras) VALUES (%s, %s,
        %s, %s)''', (pv_box.get(), vt_box.get(), ks_box.get(), km_box.get()))

        conn.commit()

        conn.close()

        pv_box.delete(0, END)
        vt_box.delete(0, END)
        ks_box.delete(0, END)
        km_box.delete(0, END)

        my_tree.delete(*my_tree.get_children())

        query_database()

        new_record_frame1.destroy()

    def cancel_add_record1():
        global counter
        new_record_frame1.destroy()
        counter = 1

    add_record = Button(data_frame, text="OK", command=add_record, width=8, bg='lightgrey', font='sans 10',
                        height=2)
    add_record.grid(row=4, column=0, sticky="w", pady=(10, 0))

    cancel_add_record = Button(data_frame, text="Cancel", command=cancel_add_record1, width=8, bg='lightgrey',
                               font='sans 10', height=2)
    cancel_add_record.grid(row=4, column=0, sticky="w", padx=(76, 0), pady=(10, 0))


# update record double click frame
update_name_frame = Frame(k_atsargos_frame)
update_name_frame.pack(anchor=W, padx=10)


def new_record_bind(e):
    new_record_frame2 = Toplevel(k_atsargos_frame)
    new_record_frame2.title('NEW RECORD')

    new_record_frame_width = 600
    new_record_frame_height = 230

    screen_width = new_record_frame2.winfo_screenwidth()
    screen_height = new_record_frame2.winfo_screenheight()

    x = (screen_width / 2) - (new_record_frame_width / 2)
    y = (screen_height / 2) - (new_record_frame_height / 2)

    new_record_frame2.geometry(f'{new_record_frame_width}x{new_record_frame_height}+{int(x)}+{int(y)}')
    new_record_frame2.focus_force()

    data_frame = Frame(new_record_frame2)
    data_frame.pack(pady=5, padx=5, anchor=N)

    pv = Label(data_frame, text="PAVADINIMAS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15,
               height=2)
    pv.grid(row=0, column=0, sticky="nsew")

    vt = Label(data_frame, text="VIETA", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15, height=2)
    vt.grid(row=1, column=0, sticky="nsew")

    ks = Label(data_frame, text="KIEKIS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15, height=2)
    ks.grid(row=2, column=0, sticky="nsew")

    km = Label(data_frame, text="KOMENTARAS", relief=RAISED, bd=3, font='sans 10', bg='lightgrey', width=15,
               height=2)
    km.grid(row=3, column=0, sticky="nsew")

    # Data input

    pv_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    pv_box.grid(row=0, column=1, sticky="nsew")

    vt_box = ttk.Combobox(data_frame, font='sans 10', state='normal', textvariable=StringVar(), width=59)
    vt_box['values'] = ('BUTRIMONIU C1', 'BUTRIMONIU C2', 'BUTRIMONIU C3', 'BUTRIMONIU C4', 'MITUVOS', 'OFISAS')
    vt_box.grid(row=1, column=1, sticky="nsew")

    ks_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    ks_box.grid(row=2, column=1, sticky="nsew")

    km_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=61)
    km_box.grid(row=3, column=1, sticky="nsew")

    def add_record():
        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute('''INSERT INTO komponentai (pavadinimas, vieta, kiekis, komentaras) VALUES (%s, %s,
        %s, %s)''', (pv_box.get(), vt_box.get(), ks_box.get(), km_box.get()))

        conn.commit()

        conn.close()

        pv_box.delete(0, END)
        vt_box.delete(0, END)
        ks_box.delete(0, END)
        km_box.delete(0, END)

        my_tree.delete(*my_tree.get_children())

        query_database()

        new_record_frame2.destroy()

    def cancel_add_record():
        global counter
        new_record_frame2.destroy()
        counter = 1

    add_record = Button(data_frame, text="OK", command=add_record, width=8, bg='lightgrey', font='sans 10',
                        height=2)
    add_record.grid(row=4, column=0, sticky="w", pady=(10, 0))

    cancel_add_record = Button(data_frame, text="Cancel", command=cancel_add_record, width=8, bg='lightgrey',
                               font='sans 10', height=2)
    cancel_add_record.grid(row=4, column=0, sticky="w", padx=(76, 0), pady=(10, 0))


# update record double click frame
update_name_frame = Frame(k_atsargos_frame)
update_name_frame.pack(anchor=W, padx=10)


def update_record_double(e):
    top_level_update = Toplevel(k_atsargos_frame)
    top_level_update.title('EDIT RECORD')

    top_level_update_width = 900
    top_level_update_height = 150

    screen_width = top_level_update.winfo_screenwidth()
    screen_height = top_level_update.winfo_screenheight()

    x = (screen_width / 2) - (top_level_update_width / 2)
    y = (screen_height / 2) - (top_level_update_height / 2)

    top_level_update.geometry(f'{top_level_update_width}x{top_level_update_height}+{int(x)}+{int(y)}')
    top_level_update.focus_force()

    data_frame = Frame(top_level_update, relief=SUNKEN)
    data_frame.pack(anchor=N, fill=tkinter.X, pady=5, padx=5)

    data_frame.columnconfigure(0, weight=1)
    data_frame.columnconfigure(1, weight=1)
    data_frame.columnconfigure(2, weight=1)
    data_frame.columnconfigure(3, weight=1)
    data_frame.rowconfigure(0, weight=1)
    data_frame.rowconfigure(1, weight=1)
    data_frame.rowconfigure(2, weight=1)
    data_frame.rowconfigure(3, weight=1)

    # Data name, ID pasleptas

    id = Label(data_frame, text="ID", font='sans 10', relief=RAISED, bd=3, bg='lightgrey', height=2,
               width=20)
    id.grid(row=0, column=3, sticky="nsew")

    pv = Label(data_frame, text="PAVADINIMAS", font='sans 10', relief=RAISED, bd=3, bg='lightgrey', height=2,
               width=30)
    pv.grid(row=0, column=0, sticky="nsew")

    vt = Label(data_frame, text="VIETA", font='sans 10', relief=RAISED, bd=3, bg='lightgrey', height=2,
               width=30)
    vt.grid(row=0, column=1, sticky="nsew")

    ks = Label(data_frame, text="KIEKIS", font='sans 10', relief=RAISED, bd=3, bg='lightgrey', height=2,
               width=10)
    ks.grid(row=0, column=2, sticky="nsew")

    km = Label(data_frame, text="KOMENTARAS", font='sans 10', relief=RAISED, bd=3, bg='lightgrey', height=2,
               width=70)
    km.grid(row=0, column=3, sticky="nsew")

    # Data input
    id_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
    id_box.grid(row=1, column=3, sticky="nsew", ipady=8)

    pv_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, justify='center')
    pv_box.grid(row=1, column=0, sticky="nsew", ipady=8)

    vt_box = ttk.Combobox(data_frame, font='sans 10', state='normal', textvariable=StringVar(), justify='center')
    vt_box['values'] = ('BUTRIMONIU C1', 'BUTRIMONIU C2', 'BUTRIMONIU C3', 'BUTRIMONIU C4', 'MITUVOS', 'OFISAS')
    vt_box.grid(row=1, column=1, sticky="nsew", ipady=8)

    ks_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, justify='center')
    ks_box.grid(row=1, column=2, sticky="nsew", ipady=8)

    km_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
    km_box.grid(row=1, column=3, sticky="nsew", ipady=8)

    def select_record(e):
        # istrina sena irasa

        id_box.delete(0, END)
        pv_box.delete(0, END)
        vt_box.delete(0, END)
        ks_box.delete(0, END)
        km_box.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        # uzpildo langelius

        id_box.insert(0, values[0])
        pv_box.insert(0, values[1])
        vt_box.insert(0, values[2])
        ks_box.insert(0, values[3])
        km_box.insert(0, values[4])



    def update_record_all():
        selected = my_tree.focus()
        my_tree.item(selected, text="", values=(id_box.get(), pv_box.get(), vt_box.get(), ks_box.get(),
                                                km_box.get()))

        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute(
            "UPDATE komponentai SET pavadinimas = %s, vieta = %s, kiekis = %s, komentaras = %s where id = %s",
            (pv_box.get(), vt_box.get(),
             ks_box.get(), km_box.get(), id_box.get()))

        conn.commit()

        conn.close()

        pv_box.delete(0, END)
        vt_box.delete(0, END)
        ks_box.delete(0, END)
        km_box.delete(0, END)

        top_level_update.destroy()

    my_tree.bind("<ButtonRelease-1>", select_record)


    def exit_update_record_all():
        top_level_update.destroy()

    update_record1 = Button(data_frame, text="OK", font='sans 10', command=update_record_all, width=8,
                            bg='lightgrey', height=2)
    update_record1.grid(row=2, column=0, sticky="w", pady=(10, 0))

    cancel_entries = Button(data_frame, text="Cancel", font='sans 10', command=exit_update_record_all, width=8,
                            bg='lightgrey', height=2)
    cancel_entries.grid(row=2, column=0, sticky="w", padx=(76, 0), pady=(10, 0))

    def exit_update_record_all():
        top_level_update.destroy()

    update_record1 = Button(data_frame, text="OK", font='sans 10', command=update_record_all, width=8,
                            bg='lightgrey', height=2)
    update_record1.grid(row=2, column=0, sticky="w", pady=(10, 0))

    cancel_entries = Button(data_frame, text="Cancel", font='sans 10', command=exit_update_record_all, width=8,
                            bg='lightgrey', height=2)
    cancel_entries.grid(row=2, column=0, sticky="w", padx=(76, 0), pady=(10, 0))


# bind on DELETE button
def delete_record():
    lentele = messagebox.askyesno("DELETE RECORD", "Ar tikrai norit istrinti?", parent=k_atsargos_frame)
    if lentele == 1:
        # norimas pasirinkimas
        x = my_tree.selection()

        # create list of ids
        ids_to_delete = []

        # prideti ka nori istrint
        for record in x:
            ids_to_delete.append(my_tree.item(record, 'values')[0])
        # istrinti
        for record in x:
            my_tree.delete(record)

        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute("DELETE FROM komponentai WHERE id = %s", [(a,) for a in ids_to_delete])

        ids_to_delete = []

        conn.commit()

        conn.close()


def delete_record1(e):
    lentele = messagebox.askyesno("DELETE RECORD", "Ar tikrai norit istrinti?", parent=k_atsargos_frame)
    if lentele == 1:
        # norimas pasirinkimas
        x = my_tree.selection()

        # create list of ids
        ids_to_delete = []

        # prideti ka nori istrint
        for record in x:
            ids_to_delete.append(my_tree.item(record, 'values')[0])
        # istrinti
        for record in x:
            my_tree.delete(record)

        conn = psycopg2.connect(
            **params
        )

        c = conn.cursor()

        c.execute("DELETE FROM komponentai WHERE id = %s", [(a,) for a in ids_to_delete])

        ids_to_delete = []

        conn.commit()

        conn.close()


# Copy csv
def save():
    query = """SELECT * FROM komponentai"""

    conn = psycopg2.connect(
        **params
    )

    cur = conn.cursor()

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    with open('komponentai_bakcup', 'w', encoding="utf-8") as f:
        cur.copy_expert(outputquery, f)

    conn.close()


def save1(e):
    query = """SELECT * FROM komponentai"""

    conn = psycopg2.connect(
        **params
    )

    cur = conn.cursor()

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    with open('komponentai_bakcup', 'w', encoding="utf-8") as f:
        cur.copy_expert(outputquery, f)

    conn.close()


# exit gamyba_frame
def exit_top_level():
    k_atsargos_frame.destroy()
    # mainWindow.deiconify()


# bind motion to tree
my_tree.tag_configure('highlight', background='gainsboro')


def highlight_row(event):
    tree = event.widget
    item = tree.identify_row(event.y)
    tree.tk.call(tree, "tag", "remove", "highlight")
    tree.tk.call(tree, "tag", "add", "highlight", item)


my_tree.bind("<Motion>", highlight_row)

# Menu bar
menu_bar1 = Menu(k_atsargos_frame)
k_atsargos_frame.config(menu=menu_bar1)
# tearoff nuima File menu atskyrima
file_menu1 = Menu(menu_bar1, tearoff=0)
menu_bar1.add_cascade(label="File", menu=file_menu1)
file_menu1.add_command(label="New   (CTRL+N)", command=new_record)
file_menu1.add_command(label="Delete", command=delete_record)
file_menu1.add_separator()
file_menu1.add_command(label="Save   (CTRL+S)", command=save)
file_menu1.add_separator()
file_menu1.add_command(label="Exit", command=exit_top_level)

open_menu3 = Menu(menu_bar1, tearoff=0)
menu_bar1.add_cascade(label="Search", menu=open_menu3)
open_menu3.add_command(label="Search   (CTRL+F)", command=search_records_popup)


def do_popup(event):
    try:
        my_menu2.tk_popup(event.x_root, event.y_root)
    finally:
        my_menu2.grab_release()


my_menu2 = Menu(my_tree, tearoff=False)
my_menu2.add_command(label='New', command=new_record)
my_menu2.add_command(label='Delete', command=delete_record)
my_menu2.add_separator()
my_menu2.add_command(label='Search', command=search_records_popup)

# Bind Treeview (pass with 'e' in function), select
my_tree.bind('<Button-3>', do_popup)
my_tree.bind('<Double-Button-1>', update_record_double)
my_tree.bind('<Key-Delete>', delete_record1)
my_tree.bind('<Control-Key-f>', search_records_bind)
my_tree.bind('<Control-Key-n>', new_record_bind)
my_tree.bind('<Control-Key-F>', search_records_bind)
my_tree.bind('<Control-Key-N>', new_record_bind)
my_tree.bind('<Control-Key-s>', save1)
my_tree.bind('<Control-Key-S>', save1)

# put data back to table
query_database()
mainloop()
