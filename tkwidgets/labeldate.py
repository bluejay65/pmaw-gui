from msilib.schema import ComboBox
import tkinter as tk
import calendar
from tkinter import ttk
import datetime



# A frame with two widgets, a label and an entry
class LabelDate(tk.Frame):
    def __init__(self, parent, row: int, column: int, text: str, padx=10, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label = tk.Label(parent, text=text)
        self.date_entry = DateEntry(parent)

        self.label.grid(row=row, column=column, sticky='w')
        self.date_entry.grid(row=row, column=column+1)

        parent.rowconfigure(row, pad=padx)

    # Returns the date in the entry
    def get_entry(self):
        return self.date_entry.get_entry()

    # Sets the date in the entry
    def set_entry(self, date: datetime.date):
        self.date_entry.set_entry(date)



# Defines an Entry that can be used to enter a date
class DateEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.month_list = []
        for i in range(1, 13):
            self.month_list.append(calendar.month_name[i])
        
        self.month_str = tk.StringVar()
        self.day_str = tk.StringVar()
        self.year_str = tk.StringVar()

        self.month_combobox = ttk.Combobox(self, textvariable=self.month_str, values=self.month_list, state='readonly', width=10)
        self.month_combobox.bind('<<ComboboxSelected>>', self.month_selected)

        self.day_combobox = ttk.Combobox(self, textvariable=self.day_str, state='readonly', width=3)

        year = datetime.date.today().year
        self.valid_years = [year]
        while(year > 2005):
            year -= 1
            self.valid_years.insert(0, year)

        self.year_combobox = ttk.Combobox(self, textvariable=self.year_str, values=self.valid_years, state='readonly', width=5)
        self.year_combobox.bind('<<ComboboxSelected>>', self.year_selected)

        self.month_combobox.grid(row=0, column=0)
        self.day_combobox.grid(row=0, column=1)
        self.year_combobox.grid(row=0, column=2)

        self.columnconfigure(0, pad=2)
        self.columnconfigure(1, pad=2)
        self.columnconfigure(2, pad=2)

    # Sets the correct number of days when a month is selected
    def month_selected(self, event):
        if self.month_str.get() == 'January' or self.month_str.get() == 'March' or self.month_str.get() == 'May' or self.month_str.get() == 'July' or self.month_str.get() == 'August' or self.month_str.get() == 'October' or self.month_str.get() == 'December':
            self.set_num_days(31)
        elif self.month_str.get() == 'April' or self.month_str.get() == 'June' or self.month_str.get() == 'September' or self.month_str.get() == 'November':
            self.set_num_days(30)
        else:
            self.set_num_days(self.get_february_days())

        if self.year_str.get() == '':
            self.set_year(0)
        if self.day_str.get() == '':
            self.set_day(1)


    # Sets the correct number of days when a year is selected
    def year_selected(self, event):
        if self.month_str.get() == 'February':
            self.set_num_days(self.get_february_days())

        if self.month_str.get() == '':
            self.set_month(0)
        if self.day_str.get() == '':
            self.set_day(1)

    def set_day(self, day: int):
        self.day_str.set(day)

    def set_month(self, month_num: int):
        self.month_str.set(self.month_list[month_num])
        self.month_selected(None)

    def set_year(self, year_num: int):
        self.year_str.set(self.valid_years[0])
        self.year_selected(None)

    # Changes the number of days shown
    def set_num_days(self, num_days):
        days_list = ['']
        for i in range(num_days):
            days_list.append(i+1)

        if self.day_str.get() != '' and int(self.day_str.get()) > num_days:
            self.day_str.set(num_days)
        
        self.day_combobox['values'] = days_list

    # Checks how many days are in february based on the year selected
    def get_february_days(self):
        if self.year_str.get() != '' and calendar.isleap(int(self.year_str.get())):
            return 29
        return 28

    # Returns the date in a datetime.date
    def get_entry(self):
        if self.year_str.get() != '':
            year = int(self.year_str.get())
        else:
            return
        if self.month_str.get() != '':
            datetime_month = datetime.datetime.strptime(self.month_str.get(), '%B')
            month = datetime_month.month
        else:
            return
        if self.day_str.get() != '':
            day = int(self.day_str.get())
        else:
            return

        return datetime.date(year, month, day)

    # Sets the date based on a datetime.date
    def set_entry(self, date: datetime.date):
        self.year_str['value'] = date.year
        self.month_str['value'] = date.month
        self.day_str['value'] = date.day