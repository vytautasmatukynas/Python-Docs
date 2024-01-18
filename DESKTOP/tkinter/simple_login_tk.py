from tkinter import *
from tkinter import messagebox


root = Tk()
root.title('Login')

root_width = 280
root_height = 120

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (root_width / 2)
y = (screen_height / 2) - (root_height / 2)

root.geometry(f'{root_width}x{root_height}+{int(x)}+{int(y)}')


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=5)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)

a_en = Label(root, text="ID", font='sans 12')
a_en.grid(column=0, row=0, pady=(10, 0))
b_en = Label(root, text="Password", font='sans 12')
b_en.grid(column=0, row=1)

a_en_entrys = Entry(root, textvariable=StringVar(), font='sans 12', width=20)
a_en_entrys.grid(column=1, row=0, pady=(10, 0))
b_en_entrys = Entry(root, show='*', textvariable=StringVar(), font='sans 12', width=20)
b_en_entrys.grid(column=1, row=1)




# import shoftware
def atidaryti():
    import file_name

def atidaryti1():
    import file_name


def uzdaryti():
    root.destroy()


def prisijungimas():
    if a_en_entrys.get() == 'sandelis' and b_en_entrys.get() == 'sandelis123':
        atidaryti(),



    elif a_en_entrys.get() == 'ofisas' and b_en_entrys.get() == 'ofisas123':
        atidaryti1()



    else:
        messagebox.showerror('Login', 'Try again...!!!')


def prisijungimas1(e):
    if a_en_entrys.get() == 'sandelis' and b_en_entrys.get() == 'sandelis123':
        atidaryti() and root.destroy()

    elif a_en_entrys.get() == 'ofisas' and b_en_entrys.get() == 'ofisas123':
        atidaryti1() and root.destroy()

    else:
        messagebox.showerror('Login', 'Try again...!!!')


def uzdaryti1(e):
    root.destroy()


login_button = Button(root, text="OK", command=prisijungimas, bg="lightgrey", width=5, font='sans 10')
login_button.grid(column=1, row=2)
cancel_button = Button(root, text="Cancel", command=uzdaryti, bg="lightgrey", width=6, font='sans 10')
cancel_button.grid(column=1, row=2, padx=(112, 0))

root.bind('<Return>', prisijungimas1)
root.bind('<Escape>', uzdaryti1)

mainloop()
