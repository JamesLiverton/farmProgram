'''
REMEMBER TO git pull BEFORE MAKING CHANGES LOCALLY

TO ADD TO GITHUB

 - git add .
 - git commit -m "your message here"
 - git push OR git push origin main

'''
from tkinter import *
from tkinter.ttk import *
import sqlite3
from datetime import date
from functools import partial
from PIL import Image, ImageTk
import ctypes
user32 = ctypes.windll.user32
x, y = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class Database():
    def __init__(self): # creates a connection with the database
        self.db = 'database.db'
        self.conn = sqlite3.connect(self.db)
        self.cur = self.conn.cursor()

    def fetch_data(self):
        sql = '''SELECT * FROM machines'''
        self.cur.execute(sql) # runs the query
        rows = self.cur.fetchall()

        return [rows] # allows for all of the database to be stored in one variable

    def add_machine(self, data): # data variable must be a tuple. Example: data = ('PLL123','hedgecutter','19/04/2021', '27/04/2021', 'Felixstowe')
        sql = '''INSERT INTO machines(id, machineName, RentStartDate, ReturnDate, Location)
        VALUES (?,?,?,?,?);'''
        self.cur.execute(sql, data) # replaces the '?' in sql with the information in the data variable and then runs the query
        self.conn.commit() # saves the changes to the database
    
    def location_change(self,data):
        sql = '''UPDATE machines
            SET Location = ?
            WHERE id = ?;'''
        self.cur.execute(sql, data) # replaces the '?' in sql with the information in the data variable and then runs the query
        self.conn.commit() #saves the changes to the database

db = Database()
#db.add_machine(('PLL126','hedgecutter','1/04/2021','7/04/2021','Felixstowe'))


data = db.fetch_data()
today = date.today()
for d in data:
    for entity in d:
        temp = entity[3]
        temp = temp.split('/')

        if int(temp[2]) <= today.year:
            if int(temp[1]) <= today.month:
                if int(temp[0]) <= today.day:
                    db.location_change(("Yard", entity[0]))


def main_window():
    tk = Tk() # intitailizes the window
    canvas = Canvas(tk, width=str(x), height=str(y))#to hold image
    canvas.pack()
    canvas.place(relx=0, rely=0)


    tk.state('zoomed')
    tk.wm_iconbitmap('assets/favicon.ico')#sets logo of the window - must use .ico files
    tk.title("James Super Duper program he made himself for Tracey x")

    #------------------TEMPORARY UNTIL TABLE IS FULLY FUNCTIONING ---------
    #Button(tk, text='Tractor 1', command=tractor1_window).grid(row=0, column=1) #button to open machine 
    #--------------------------------------------------------------------

    #logo
    img = PhotoImage(file="assets/pllLogo.png") #loads image and assigns it to variable to make usable

    #background
    image = Image.open("assets/testbg.png")
    image = image.resize((x,y), Image.ANTIALIAS)

    bg = ImageTk.PhotoImage(image)

    #display data
    canvas.create_image(0,0, anchor=NW, image=bg)
    canvas.create_image(0,0, anchor=NW, image=img)

    

    tree = Treeview(tk) # creates a tree
    tree['columns']=('id','machineName','RentStartDate','ReturnDate','Location') #creates names of columns
    tree['show'] = 'headings' 

    
    tree.column("id", width=int(x/7.68))
    tree.column("machineName", width=int(x/4.8))
    tree.column("RentStartDate", width=int(x/6.4))
    tree.column("ReturnDate", width=int(x/6.4))
    tree.column("Location", width=int(x/12.8))
    
    tree.heading("id", text="Machine Identification", anchor=W)
    tree.heading("machineName", text="Machine Name")
    tree.heading("RentStartDate", text="Hire Start Date")
    tree.heading("ReturnDate", text="Hire Return Date")
    tree.heading("Location", text="Location")

    

    data = db.fetch_data()
    
    for d in data:
        for entity in d:
            tree.insert('','end',values=[entity[0],entity[1],entity[2],entity[3],entity[4]])

    tree.bind("<Double-1>", partial(on_press, tree))

    tree.place(relx=0.5, rely=0.5, anchor=CENTER)
    
    tk.mainloop()

def on_press(tree, event):
    item = tree.selection()
    for i in item:
        selected = tree.item(i, "values")
    
    tk = Tk()
    tk.title(selected[0]+' '+selected[1])
    tk.geometry('1500x1000')


main_window()
