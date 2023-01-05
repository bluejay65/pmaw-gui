import tkinter as tk
import datetime
import time as t


class BaseGUI(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select File', command=self.select_file)
        self.file_button.grid(row=0, column=0, columnspan=2)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.columnconfigure(0, pad=20)
        self.columnconfigure(0, pad=20)


    def date_time_to_epoch(self, date: datetime.date, time: datetime.time):
        struct_time = t.struct_time([date.year, date.month, date.day, time.hour, time.minute, 0, 0, 1, -1])
        return int(t.mktime(struct_time))