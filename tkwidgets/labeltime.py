import tkinter as tk
from tktimepicker import SpinTimePickerModern, constants



# A frame containing a label and a timepicker widget that can return the time in 24 hour time
class LabelTime(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)
        self.time_entry = TimeEntry(parent)

        self.label.grid(row=row, column=column, sticky='w')
        self.time_entry.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)

    # Returns the date in the entry
    def get_entry(self):
        return self.time_entry.get_entry()

    # Sets the date in the entry according to a time_list defined as [hours12, minutes, period]
    def set_entry(self, time_list: list):
        self.time_entry.set_entry()



# Defines an Entry which can be used to enter a time
class TimeEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.time_entry = SpinTimePickerModern(self)
        self.time_entry.addAll(constants.HOURS12)
        self.time_entry.configureAll(bg="#dddddd", width=4, hoverbg="#aaaaaa", clickedbg="#000000", clickedcolor="#ffffff")
        self.time_entry.configure_separator(bg="#dddddd")
        self.time_entry.setMins(0)

        self.time_entry.grid(row=0, column=0)


    # Returns the date in the entry
    def get_entry(self):
        return self.time_entry.time()

    # Sets the date in the entry according to a time_list defined as [hours12, minutes, period]
    def set_entry(self, time_list: list):
        self.time_entry.set12Hrs(time_list[0])
        self.time_entry.setMins(time_list[1])
        self.time_entry.setPeriod(time_list[2])