import tkinter as tk
import datetime
import time as t


class BaseGUI(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)


    def date_time_to_epoch(self, date: datetime.date, time: datetime.time):
        struct_time = t.struct_time([date.year, date.month, date.day, time.hour, time.minute, 0, 0, 1, -1])
        return t.mktime(struct_time)