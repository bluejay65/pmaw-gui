import tkinter as tk
from tkinter import font


class LabelRange(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx:int=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)
        self.range_entry = RangeEntry(parent)

        self.label.grid(row=row, column=column, sticky='w')
        self.range_entry.grid(row=row, column=column+1)

        #parent.rowconfigure(row, pad=padx)

    # Returns the string in the entry
    def get_entry(self):
        return self.range_entry.get_entry()

    # Sets the entry to entry
    def set_entry(self, lower_entry:int, upper_entry:int):
        self.range_entry.set_entry(lower_entry, upper_entry)


class RangeEntry(tk.Frame):
    def __init__(self, parent, width:int=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.vcmd = (self.register(self.check_limit_digit), '%P')

        temp_font = font.nametofont('TkDefaultFont').copy()
        temp_font.config(size=7)
        self.lower_label = tk.Label(self, text='Lower\nBoundary', font=temp_font)
        self.upper_label = tk.Label(self, text='Upper\nBoundary', font=temp_font)

        self.lower_str = tk.StringVar()
        self.upper_str = tk.StringVar()
        self.lower_entry = tk.Entry(self, textvariable=self.lower_str, width=width, validate='all', validatecommand=self.vcmd)
        self.upper_entry = tk.Entry(self, textvariable=self.upper_str, width=width, validate='all', validatecommand=self.vcmd)

        self.lower_entry.grid(row=0, column=0)
        self.upper_entry.grid(row=0, column=1)
        self.lower_label.grid(row=1, column=0, sticky='n')
        self.upper_label.grid(row=1, column=1, sticky='n')

    def check_limit_digit(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False

    # Returns the string in the entry
    def get_entry(self):
        return [self.lower_str.get(), self.upper_str.get()]

    # Sets the string in the entry
    def set_entry(self, lower_entry:int=0, upper_entry:int=0):
        self.lower_str.set(lower_entry)
        self.upper_str.set(upper_entry)