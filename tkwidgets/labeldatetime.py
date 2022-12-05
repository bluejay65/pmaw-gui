import tkinter as tk
import tkwidgets as tkw
import datetime


# A frame containing a label and a timepicker widget that can return the time in 24 hour time
class LabelDateTime(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, can_clear:bool = False, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label_frame = tk.Frame(parent)
        self.label = tk.Label(self.label_frame, text=text)

        self.entry_frame = tk.LabelFrame(parent)

        self.date_entry = tkw.DateEntry(self.entry_frame)
        self.time_entry = tkw.TimeEntry(self.entry_frame)

        if can_clear:
            self.clear_button = tk.Button(self.label_frame, text='Clear', command=self.clear_date)
            self.clear_button.grid(row=1, column=0)
            self.clear_button.grid_remove()

            self.date_entry.bind_selection(self.show_clear)

        self.label_frame.grid(row=row, column=column, sticky='w')
        self.label.grid(row=0, column=0)
        self.entry_frame.grid(row=row, column=column+1)
        self.date_entry.grid(row=0, column=0, padx=5, pady=(5,0))
        self.time_entry.grid(row=1, column=0, padx=5, pady=5)

        parent.rowconfigure(row, pad=padx)

    # Returns the date and time in the entry
    def get_entry(self):
        return {'date': self.date_entry.get_entry(), 'time': self.time_entry.get_entry()}

    # Sets the date and time in the entry according to a datetime.date and a datetime.time
    def set_entry(self, date: datetime.date, time: datetime.time):
        self.date_entry.set_entry(date)
        self.time_entry.set_entry(time)

    def show_clear(self, event):
        self.clear_button.grid()

    def clear_date(self):
        self.date_entry.clear()
        self.clear_button.grid_remove()