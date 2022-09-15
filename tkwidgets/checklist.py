import tkinter as tk
from tkinter import ttk
import tkwidgets as tkw


# A list of checkbuttons that can be selected and deselected by code or user
class Checklist(ttk.Labelframe):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, title: str = None, scrollbar: bool = False, **kwargs):
        ttk.Labelframe.__init__(self, parent, text=title, **kwargs)

        if scrollbar:
            self.frame = tkw.VerticalScrolledFrame(self)
            self.edit_frame = self.frame.interior
        else:
            self.frame = self.edit_frame = tk.Frame(self)

        self.frame.grid(row=0, column=0)
        self.vars = []
        self.checkbuttons = []

        for choice in listvariable:
            var = tk.StringVar(value=choice)
            self.vars.append(var)

            cb = tk.Checkbutton(self.edit_frame, var=var, text=choice, onvalue=choice, offvalue="", anchor="w")

            cb.grid(row=len(self.checkbuttons), column=0, sticky='w')
            self.checkbuttons.append(cb)

        


    # Returns a list of the values of the checked buttons
    def get_checked_items(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values

    # Selects a button based on index
    def select(self, index:int):
        self.checkbuttons[index].select()

    # Deselects a buttons based on index
    def deselect(self, index:int):
       self.checkbuttons[index].deselect()

    # Selects the buttons in index_list, and deselects buttons not in index_lsit
    def check_items(self, index_list):
        for i in range(len(self.checkbuttons)):
            if i in index_list:
                self.checkbuttons[i].select()
            else:
                self.checkbuttons[i].deselect()

    def clear(self):
        self.check_items([])

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))