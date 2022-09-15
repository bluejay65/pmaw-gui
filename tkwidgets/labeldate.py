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
    def set_entry(self, date_list: list):
        self.date_entry.set_entry(date_list)



# Defines an Entry that can be used to enter a date
class DateEntry(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        month_list = []
        for i in range(1, 13):
            month_list.append(calendar.month_name[i])
        
        self.month_str = tk.StringVar()
        self.day_str = tk.StringVar()
        self.year_str = tk.StringVar()

        self.month_combobox = ttk.Combobox(self, textvariable=self.month_str, values=month_list, state='readonly', width=10)
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
        num_days = 0
        if self.month_str.get() == 'January' or self.month_str.get() == 'March' or self.month_str.get() == 'May' or self.month_str.get() == 'July' or self.month_str.get() == 'August' or self.month_str.get() == 'October' or self.month_str.get() == 'December':
            self.set_days(31)
        elif self.month_str.get() == 'April' or self.month_str.get() == 'June' or self.month_str.get() == 'September' or self.month_str.get() == 'November':
            self.set_days(30)
        else:
            self.set_days(self.get_february_days())


    # Sets the correct number of days when a year is selected
    def year_selected(self, event):
        if self.month_str.get() == 'February':
            self.set_days(self.get_february_days())

    # Changes the number of days shown
    def set_days(self, num_days):
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

    # Returns the date in a list defined as [month, day, year]
    def get_entry(self):
        return_date = [0, 0, 0]

        if self.month_str.get() != '':
            datetime_month = datetime.datetime.strptime(self.month_str.get(), '%B')
            return_date[0] = datetime_month.month

        if self.day_str.get() != '':
            return_date[1] = int(self.day_str.get())

        if self.year_str.get() != '':
            return_date[2] = int(self.year_str.get())

        return return_date

    # Sets the date based on date_list defined as [month, day, year]
    def set_entry(self, date_list: list):
        self.month_str['value'] = date_list[0]
        self.day_str['value'] = date_list[1]
        self.year_str['value'] = date_list[2]