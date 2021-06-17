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
from datetime import datetime
from functools import partial
from PIL import Image, ImageTk
import ctypes
from tkcalendar import *
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
    def date_update(self): # this method is only for the auto change of the dates for each machine.
        data = self.fetch_data()
        today = datetime.now()
        for d in data:
            for entity in d:
                mid = entity[0]
                nexthires = entity[5]
                rentstartdate = entity[2]
                if nexthires:
                    if rentstartdate != '-':
                        listofhires = nexthires.split(',')
                        nexthire = listofhires.pop(0)
                        location, rsd, rd = nexthire.split('-')
                        startdate = datetime(int(rsd.split('/')[2]),int(rsd.split('/')[1]),int(rsd.split('/')[0]))
                        if not((startdate - today).days <= 0):
                            listofhires.insert(0,nexthire)
                            location = 'Yard'
                            rsd = '-'
                            rd = '-'
                            nh = ','.join(listofhires)
                        values = (rsd, rd, location, nh, mid)
                        sql = '''UPDATE machines
                                SET RentStartDate = ?, ReturnDate = ?, Location = ?, NextHires = ?
                                WHERE id = ?'''
                        self.cur.execute(sql, values)
                        self.conn.commit()
                elif (not nexthires) and rentstartdate != '-':
                    temp = entity[3].split('/')
                    temp = datetime(int(temp[2]), int(temp[1]), int(temp[0]))
                    if temp < today:
                        location = 'Yard'
                        rsd = '-'
                        rd = '-'
                        values = (rsd, rd, location, mid)
                        sql = '''UPDATE machines
                                SET RentStartDate = ?, ReturnDate = ?, Location = ?
                                WHERE id = ?'''
                        self.cur.execute(sql, values)
                        self.conn.commit()

    def fetch_hires(self, machineName):
        sql = '''SELECT RentStartDate, ReturnDate, NextHires FROM Machines WHERE id = ?;'''
        self.cur.execute(sql, (machineName,))
        data = self.cur.fetchall()

        return data

                        
db = Database()
#db.add_machine(('PLL126','hedgecutter','1/04/2021','7/04/2021','Felixstowe'))

db.date_update()

data = db.fetch_data()
today = datetime.now()
for d in data:
    print('running')
    for entity in d:
        print(entity)
        temp = entity[3]
        if temp == '-':
            break
        temp = temp.split('/')
        temp = datetime(int(temp[2]), int(temp[1]), int(temp[0]))
        if temp < today:
            db.location_change(('Yard', entity[0]))




def main_window():
    tk = Tk() # intitailizes the window
    canvas = Canvas(tk, width=str(x), height=str(y))#to hold image
    canvas.pack()
    canvas.place(relx=0, rely=0)


    tk.state('zoomed')
    tk.wm_iconbitmap('assets/favicon.ico')#sets logo of the window - must use .ico files
    tk.title("James Super Duper program he made himself for Tracey x")

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

    cframe = Frame(tk, height=800, width=800)
    cframe.pack()

    cal = Calendar(cframe, selectmode='day')


    cal.pack(fill="both", expand=True)

    #getting hires for current machine
    print('selectd', selected[0])
    machineName = selected[0]
    data = db.fetch_hires(machineName)
    print('data', data)
    data = data[0]
    s = data[0]
    e = data[1]
    nh = data[2]

    nh = nh.split(',')
    for i in range(len(nh)):
        print(nh[i])
        nh[i] = nh[i].split('-')
        location = nh[i].pop(0)

        for j in range(len(nh[i])):
            nh[i][j] = datetime(int(nh[i][j].split('/')[2]), int(nh[i][j].split('/')[1]), int(nh[i][j].split('/')[0]))

        currentday = nh[i][0].day
        currentmonth = nh[i][0].month
        currentyear = nh[i][0].year

        endday = nh[i][1].day
        endmonth = nh[i][1].month
        endyear = nh[i][1].year

        while True:
            print(currentday, currentmonth, currentyear)
            cal.calevent_create(datetime(currentyear, currentmonth, currentday), location, 'hired')
            
            if currentmonth == 12 and currentday == 31:
                currentyear += 1
                currentday = 1
                currentmonth = 1

            elif currentmonth == 3 and currentday == 28:
                currentmonth += 1
                currentday = 1

            elif currentmonth % 2 == 0 and currentday == 31:
                currentmonth += 1
                currentday = 1

            elif currentmonth % 2 != 0 and currentday == 30:
                currentmonth += 1
                currentday = 1

            else:
                currentday += 1

            if currentmonth == 14:
                break
            if currentday == endday and currentmonth == endmonth and currentyear == endyear:
                cal.calevent_create(datetime(currentyear, currentmonth, currentday), location, 'hired')

                break
        cal.tag_config('hired', background='red')



    #---------------------------------------

    tk.mainloop()


main_window()