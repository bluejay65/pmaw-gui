import tkinter as tk


# A frame with two widgets, a label and an entry
class LabelEntry(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.entry_str = tk.StringVar()

        self.label = tk.Label(parent, text=text)
        self.entry = tk.Entry(parent, textvariable=self.entry_str)

        self.label.grid(row=row, column=column, sticky='w')
        self.entry.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)

    # Returns the string in the entry
    def get_entry(self):
        return self.entry_str.get()

    # Sets the entry to entry
    def set_entry(self, entry):
        self.entry_str.set(entry)