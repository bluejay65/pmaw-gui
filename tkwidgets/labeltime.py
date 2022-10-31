import tkinter as tk
from tktimepicker import SpinTimePickerModern, constants
import datetime



# A frame containing a label and a timepicker widget that can return the time in 24 hour time
class LabelTime(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)
        self.time_entry = TimeEntry(parent)

        self.label.grid(row=row, column=column, sticky='w')
        self.time_entry.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)

    # Returns the time in the entry as a datetime.time
    def get_entry(self):
        return self.time_entry.get_entry()

    # Sets the time in the entry according to a datetime.time
    def set_entry(self, time: datetime.time):
        self.time_entry.set_entry(time)



# Defines an Entry which can be used to enter a time
class TimeEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.time_entry = SpinTimePickerModern(self, orient=constants.HORIZONTAL)
        self.time_entry.addAll(constants.HOURS12)
        self.time_entry.configureAll(bg="#cdcdcd", width=4, hoverbg="#a6a6a6", clickedbg="#606060", clickedcolor="#ffffff")
        self.time_entry.configure_separator(bg="#cdcdcd")
        self.time_entry.setMins(0)

        self.time_entry.grid(row=0, column=0)


    # Returns the time in the entry as a datetime.time
    def get_entry(self):
        time = self.time_entry.time()
        temp_time = [time[0], time[1], time[2]]
        if temp_time[2] == 'PM':
            temp_time[0] += 12
        elif temp_time[0] == 12:
            temp_time[0] = 0

        return datetime.time(temp_time[0], temp_time[1])

    # Sets the date in the entry according to a datetime.time
    def set_entry(self, time: datetime.time):
        if time.hour >= 12:
            self.time_entry.setPeriod(constants.PM)
            self.time_entry.set12Hrs(time.hour-12)
        else:
            self.time_entry.setPeriod(constants.AM)
            if time.hour == 0:
                self.time_entry.set12Hrs(12)
            else:
                self.time_entry.set12Hrs(time.hour)
            
            self.time_entry.setMins(time.minute)
        