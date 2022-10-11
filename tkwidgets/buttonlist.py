import tkinter as tk
from tkinter import ttk
import tkwidgets as tkw


# A list of checkbuttons that can be selected and deselected by code or user
class ButtonList(ttk.Labelframe):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, height:int = None, title: str = None, command: str = None, scrollbar: bool = False, relief=tk.RAISED, **kwargs):
        ttk.Labelframe.__init__(self, parent, text=title, **kwargs)

        self.command = command
        self.parent = parent
        self.relief = relief

        if scrollbar:
            self.frame = tkw.VerticalScrolledFrame(self, height=height)
            self.edit_frame = self.frame.interior
        else:
            self.frame = self.edit_frame = tk.Frame(self, height=height)

        self.frame.grid(row=0, column=0)
        self.buttons = {}

        self.add_items(listvariable)


    def add_items(self, items: list):
        for i in items:
            btn = tk.Button(self.edit_frame, text=i, anchor="w", relief=self.relief)

            if self.command:
                btn['command'] = (lambda parent=self.parent, command=self.command, button=btn: self.run_command(parent, command, button))

            btn.grid(row=len(self.buttons), column=0, sticky='w')
            self.buttons[i] = btn

    def remove_items(self, items: list):
        for i in items:
            if i in self.buttons.keys():
                self.buttons[i].grid_forget()
                self.buttons.pop(i)

    def remove_all_items(self):
        for i in self.buttons.keys():
            i.grid_forget()
        self.buttons = {}

    # Selects a button
    def select(self, item:str):
        self.buttons[item].invoke()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run_command(self, parent, command, button):
        button.focus_set()
        func = getattr(parent, command)
        func(button['text'])