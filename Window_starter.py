from tkinter import *
import tkinter as tk
from tkinter import ttk
from algorithm import searchButton_pressed, backButton_pressed, display_details

#creates and structures the main Window
class startFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='orange')
        self.Header = Label(self,bg = "orange",fg = "black", text="Enter desired Travel Route", width=20, font=("bold", 25)).place(x=55, y=53)

        self.label_journeyStart = Label(self,bg = "orange",fg = "black", text= "From:" , width = 20, font = ("bold", 15)).place(x = 30, y = 145)
        self.label_journeyEnd = Label(self,  bg = "orange",fg = "black", text="To:", width = 20, font = ("bold", 15)).place(x = 40, y = 175)
        #creates the entry and then places it on the GUI.
        self.entry_journeyStart = Entry(self, font=("Calibri 12"))
        self.entry_journeyStart.place(x = 180, y = 150) 
        self.entry_journeyEnd = Entry(self, font=("Calibri 12"))
        self.entry_journeyEnd.place(x = 180, y = 180)
        #creates the button that will initialize the dijkstra algorithm.
        self.searchButton = Button(self, text="Search",font=("Calibri 12"), width = 20, bg='black', fg='white', command=lambda: searchButton_pressed(self, controller)).place(x = 160, y = 300)    



#creates and structures the window where the journey details will be presented.
class nextFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg = "orange")
        self.Header = Label(self,bg = "orange",fg = "black", text="Journey Details", width=20, font=("bold", 15)).place(x=0, y=5)
        #creates the button that will allow the user to change the stations being searched.
        self.backButton = Button(self,bg = "black",fg = "white", text="New Trip", width = 10,  command=lambda: backButton_pressed(self, controller)).place(x = 400, y = 5)    
        #creates the button that will allow the user to get details on the trip(destinations and expected travel time)
        self.displayButton = Button(self,bg = "black",fg = "white", text="Display Route", width = 28, command=lambda: display_details(self, controller)).place(x = 20, y = 65)
        #creates the style for the tree and allows the background,fieldbackground and foreground to be changed.
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview",background = "orange",fieldbackground = "orange",foreground = "white")
        self.tree = ttk.Treeview(self)
        
        self.tree.canvas = Canvas(width=500, height=500, relief='sunken')
        self.tree['columns'] = ("line", "from", "to", "stationTime", "totalTime")

        self.tree.column('#0', stretch=False, minwidth=0, width=100)
        self.tree.column('#1', stretch=False, minwidth=0, width=100)
        self.tree.column('#2', stretch=False, minwidth=0, width=100)
        self.tree.column('#3', stretch=False, minwidth=0, width=100)
        self.tree.column('#4', stretch=False, minwidth=0, width=100)

        self.tree.heading("line", text="Line", anchor=W)
        self.tree.heading("from", text="From", anchor=W)
        self.tree.heading("to", text="To", anchor=W)
        self.tree.heading("stationTime", text="Station Time", anchor=W)
        self.tree.heading("totalTime", text="Total Time", anchor=W)
        self.tree.place(x=-100, y=100)
        
        self.end_data = tk.Text(self, width=60, heigh=9)
        self.end_data.configure(bg = "orange",fg = "black")
        self.end_data.place(x=5, y=335)
        self.end_data.config(relief="sunken")