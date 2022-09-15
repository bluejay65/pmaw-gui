import tkinter as tk
from tkinter import filedialog, messagebox
from tkwidgets import Checklist
from base_gui import BaseGUI
import constants, pmaw_data
from search_pmaw import CallPmaw
import pandas as pd


class DataGUI(BaseGUI):

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.frequency_entries = Checklist(self, constants.return_fields, title='Get frequency grouped by', scrollbar=True)
        self.frequency_entries.grid(row=0, column=0)

        self.agg_sum_entries = Checklist(self, constants.return_fields, title='Get aggregate sum grouped by', scrollbar=True)
        self.agg_sum_entries.grid(row=0, column=1)

        self.clear_entries()


        self.datafile_selected = ''
        self.data_button_frame = tk.Frame(self)
        self.data_button_frame.grid(row=1, column=0, columnspan=2)
        self.data_button_frame.columnconfigure(0, pad=20)
        self.data_button_frame.columnconfigure(1, pad=20)

        self.use_file_var = tk.IntVar()
        #self.use_file_button = tk.Checkbutton(self.data_button_frame, var=self.use_file_var, text='Use data file (.csv)', command=self.use_file_changed)
        self.datafile_button = tk.Button(self.data_button_frame, text='Select Data File to Use', command=self.select_data_file)
        #self.use_file_button.grid(row=0, column=0)
        self.datafile_button.grid(row=0, column=0) #TODO let users download and parse data at the same time


        self.saveasfile_selected = ''
        self.run_button_frame = tk.Frame(self)
        self.run_button_frame.grid(row=2, column=0, columnspan=2)
        self.run_button_frame.columnconfigure(0, pad=20)
        self.run_button_frame.columnconfigure(1, pad=20)


        self.run_button = tk.Button(self.run_button_frame, text='Run', command=self.run)
        self.saveasfile_button = tk.Button(self.run_button_frame, text='Select File to Save to', command=self.select_file)
        self.saveasfile_button.grid(row=0, column=0)


        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)

        self.columnconfigure(0, pad=20)
        self.columnconfigure(0, pad=20)




    def run(self):
        entry_dict = self.get_entries()

        if self.datafile_selected and entry_dict != {}: #TODO make the user able to save files after getting the data
            self.root.withdraw()

            df = pd.read_csv(self.datafile_selected, sep=',', usecols=CallPmaw.get_csv_cols(self.datafile_selected))
            self.data = pmaw_data.Data(df)
            
            if 'count' in entry_dict:
                print(self.data.count_fields(entry_dict['count']))
            if 'sum' in entry_dict:
                print(self.data.sum_fields(entry_dict['sum']))

            self.root.deiconify()
            self.clear_entries()

    
    def select_file(self):
        self.saveasfile_selected = filedialog.asksaveasfilename()

        if self.saveasfile_selected:
            self.run_button.grid(row=0, column=0)
            self.saveasfile_button.grid(row=0, column=1)
        else:
            self.run_button.grid_forget()
            self.saveasfile_button.grid(row=0, column=0)


    def get_entries(self):
        entry_dict = {}

        if self.frequency_entries.get_checked_items():
            entry_dict['count'] = self.frequency_entries.get_checked_items()
        if self.agg_sum_entries.get_checked_items():
            entry_dict['sum'] = self.agg_sum_entries.get_checked_items()

        return entry_dict


    def use_file_changed(self):
        if self.use_file_var.get():
            self.datafile_button.grid(row=0, column=0)
            self.use_file_button.grid(row=1, column=0)
        else:
            self.datafile_button.grid_forget()
            self.use_file_button.grid(row=0, column=0)


    def select_data_file(self):
        self.datafile_selected = filedialog.askopenfilename()


    def clear_entries(self):
        self.frequency_entries.clear()
        self.agg_sum_entries.clear()

    
    def raise_error(msg: str, title:str = ''):
        messagebox.showinfo(message=msg, title=title)
