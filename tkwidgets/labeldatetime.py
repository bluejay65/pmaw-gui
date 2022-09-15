import tkinter as tk
import tkwidgets as tkw


# A frame containing a label and a timepicker widget that can return the time in 24 hour time
class LabelDateTime(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)
        self.date_entry = tkw.DateEntry(parent)
        self.time_entry = tkw.TimeEntry(parent)

        self.label.grid(row=row, column=column, sticky='w', rowspan=2)
        self.date_entry.grid(row=row, column=column+1)
        self.time_entry.grid(row=row+1, column=column+1)

        parent.rowconfigure(row, pad=padx)
        parent.rowconfigure(row+1, pad=padx)

    # Returns the date in the entry
    def get_entry(self):
        return [self.date_entry.get_entry(), self.time_entry.get_entry()]

    # Sets the date in the entry according to a time_list defined as [hours12, minutes, period]
    def set_entry(self, date_list: list, time_list: list):
        self.date_entry.set_entry(date_list)
        self.time_entry.set_entry(time_list)