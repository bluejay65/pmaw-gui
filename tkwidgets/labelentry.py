import tkinter as tk
import tkwidgets as tkw


# A frame with two widgets, a label and an entry
class LabelEntry(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, tooltip :str = None, number: bool = False, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.entry_str = tk.StringVar()

        if not number:
            self.entry = tk.Entry(parent, textvariable=self.entry_str)
        else:
            self.vcmd = (parent.register(self.check_limit_digit), '%P')
            self.entry = tk.Entry(parent, textvariable=self.entry_str, validate='all', validatecommand=self.vcmd)

        self.label = tk.Label(parent, text=text)

        if tooltip != None:
            self.tooltip = tkw.ToolTip(self.entry, tooltip)
        else:
            self.tooltip = tooltip


        self.label.grid(row=row, column=column, sticky='w')
        self.entry.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)


    # Returns the string in the entry
    def get_entry(self):
        return self.entry_str.get()

    # Sets the entry to entry
    def set_entry(self, entry):
        self.entry_str.set(entry)

    def set_tooltip(self, text):
        if self.tooltip != None:
            self.tooltip.set_text(text)
        else:
            self.tooltip = tkw.ToolTip(self.entry, text)

    def check_limit_digit(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False