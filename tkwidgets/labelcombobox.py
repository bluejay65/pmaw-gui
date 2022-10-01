import tkinter as tk
from tkinter import ttk


class LabelCombobox(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, options: list, width:int=20, padx:int=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)

        self.combobox_str = tk.StringVar()
        self.combobox = ttk.Combobox(parent, textvariable=self.combobox_str, values=options, state='readonly', width=width)
        self.combobox_str.set(options[0])

        self.label.grid(row=row, column=column, sticky='w')
        self.combobox.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)

    
    # Returns the string in the entry
    def get_entry(self):
        return self.combobox_str.get()

    # Sets the string in the entry
    def set_entry(self, entry):
        self.combobox_str.set(entry)