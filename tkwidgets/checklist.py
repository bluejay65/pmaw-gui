import tkinter as tk
from tkinter import ttk
import tkwidgets as tkw


# A list of checkbuttons that can be selected and deselected by code or user
class Checklist(tk.LabelFrame):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, height:int = None, title: str = None, command: str = None, scrollbar: bool = False, can_select_all:bool = False, can_clear_all:bool = False, **kwargs):
        tk.LabelFrame.__init__(self, parent, text=title, **kwargs)

        self.command = command
        self.parent = parent

        if scrollbar:
            self.frame = tkw.VerticalScrolledFrame(self, height=height)
            self.edit_frame = self.frame.interior
        else:
            self.frame = self.edit_frame = tk.Frame(self, height=height)

        num_columns = 0
        if can_select_all:
            self.select_button = tk.Button(self, command=self.select_all, text='Select All')
            self.select_button.grid(row=1, column=num_columns)
            num_columns += 1
        if can_clear_all:
            self.clear_button = tk.Button(self, command=self.clear, text='Clear All')
            self.clear_button.grid(row=1, column=num_columns)
            num_columns += 1

        if num_columns <= 1:
            self.frame.grid(row=0, column=0, sticky='news')
            self.grid_columnconfigure(0, weight=1)
        else:
            self.frame.grid(row=0, column=0, sticky='news', columnspan=num_columns)
            for col in range(num_columns):
                self.grid_columnconfigure(col, weight=1)
                
        self.vars = []
        self.checkbuttons = {}
        self.hidden_checkbuttons = {}

        for choice in listvariable:
            var = tk.StringVar(value=choice)
            self.vars.append(var)

            cb = tk.Checkbutton(self.edit_frame, var=var, text=choice, onvalue=choice, offvalue="", anchor="w")

            if self.command:
                cb['command'] = (lambda: self.run_command(self.parent, self.command))

            cb.grid(row=len(self.checkbuttons), column=0, sticky='w')
            self.checkbuttons[choice] = cb


    # Returns a list of the values of the checked buttons
    def get_checked_items(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value and value not in self.hidden_checkbuttons:
                values.append(value)
        return values

    def add_items(self, items: list):
        for item in items:
            var = tk.StringVar(value=item)
            self.vars.append(var)

            cb = tk.Checkbutton(self.edit_frame, var=var, text=item, onvalue=item, offvalue="", anchor="w")

            if self.command:
                cb['command'] = (lambda: self.run_command(self.parent, self.command))

            cb.grid(row=len(self.checkbuttons), column=0, sticky='w')
            self.checkbuttons[item] = cb

    def remove_items(self, items: list):
        for item in items:
            if item in self.checkbuttons.keys():
                self.checkbuttons[item].grid_forget()
                self.checkbuttons.pop(item)

    def remove_all_items(self):
        for button in self.checkbuttons.values():
            button.grid_forget()
        self.vars = []
        self.checkbuttons = {}

    def hide_items(self, items: list):
        for item in items:
            if item in self.checkbuttons.keys():
                self.checkbuttons[item].grid_remove()
                self.hidden_checkbuttons[item] = self.checkbuttons[item]

    def show_all_items(self):
        for item in self.hidden_checkbuttons.keys():
            self.hidden_checkbuttons[item].grid()
        self.hidden_checkbuttons = {}

    # Selects a button
    def select(self, item:str):
        self.checkbuttons[item].select()

    # Deselects a button
    def deselect(self, item:str):
       self.checkbuttons[item].deselect()

    # Selects the buttons in index_list, and deselects buttons not in index_list
    def check_items(self, index_list):
        for i in self.checkbuttons.keys():
            if i in index_list:
                self.checkbuttons[i].select()
            else:
                self.checkbuttons[i].deselect()

    def select_all(self):
        for i in self.checkbuttons.keys():
            self.checkbuttons[i].select()

    def clear(self):
        self.check_items([])

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run_command(self, parent, command):
        func = getattr(parent, command)
        func()