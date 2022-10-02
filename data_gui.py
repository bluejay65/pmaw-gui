from msilib.schema import File
import tkinter as tk
from tkinter import filedialog, messagebox
from tkwidgets import Checklist, Radiolist
from base_gui import BaseGUI
from constants import FileType
import pmaw_data
from search_pmaw import CallPmaw
import pandas as pd


class DataGUI(BaseGUI): #TODO get way to count total comments returned

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.frequency_file = ''
        self.frequency_entries = Checklist(self, [], title='Get frequency grouped by', scrollbar=True, command='check_checklists')
        self.frequency_file_button = tk.Button(self, text='Select File to Save to', command=lambda: self.save_file(self.frequency_file, self.frequency_file_button))
        self.frequency_file_type_button = Radiolist(self, options=[e.value for e in FileType], title='Save As')
        self.frequency_entries.grid(row=0, column=0)
        self.frequency_entries.grid_remove()
        self.frequency_file_button.grid(row=1, column=0)
        self.frequency_file_button.grid_remove()
        self.frequency_file_type_button.grid(row=2, column=0)
        self.frequency_file_type_button.grid_remove()
        

        self.agg_sum_file = ''
        self.agg_sum_entries = Checklist(self, [], title='Get aggregate sum grouped by', scrollbar=True, command='check_checklists')
        self.agg_sum_file_button = tk.Button(self, text='Select File to Save to', command=lambda: self.save_file(self.agg_sum_file, self.agg_sum_file_button))
        self.agg_sum_file_type_button = Radiolist(self, options=[e.value for e in FileType], title='Save As')
        self.agg_sum_entries.grid(row=0, column=1)
        self.agg_sum_entries.grid_remove()
        self.agg_sum_file_button.grid(row=1, column=1)
        self.agg_sum_file_button.grid_remove()
        self.agg_sum_file_type_button.grid(row=2, column=1)
        self.agg_sum_file_type_button.grid_remove()

        self.clear_entries()


        self.datafile = ''
        self.data_button_frame = tk.Frame(self)
        self.data_button_frame.grid(row=1, column=0, columnspan=2)
        self.data_button_frame.columnconfigure(0, pad=20)
        self.data_button_frame.columnconfigure(1, pad=20)

        self.datafile_button = tk.Button(self, text='Select Data File to Use', command=lambda: self.open_file())
        self.datafile_button.grid(row=2, column=0, columnspan=2)

        self.run_button = tk.Button(self, text='Run', command=self.run)
        self.run_button.grid(row=3, column=0, columnspan=2)
        self.run_button.grid_remove()

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)

        self.columnconfigure(0, pad=20)
        self.columnconfigure(0, pad=20)


    def run(self):
        can_run = True
        entry_dict = self.get_entries()

        self.root.withdraw()

        if self.datafile.endswith(FileType.CSV.value):
            df = pd.read_csv(self.datafile, sep=',', usecols=CallPmaw.get_csv_cols(self.datafile))
            self.data = pmaw_data.Data(df)
        elif self.datafile.endswith(FileType.XLSX.value):
            df = pd.read_excel(self.datafile)
            self.data = pmaw_data.Data(df)
        else:
            can_run = False
            print('File Selected is not a recognized file type. Must be .csv or .xlsx')
        
        if 'count' in entry_dict and can_run:
            self.data.save_count_fields(entry_dict['count'], self.frequency_file, self.frequency_file_type_button.get_choice())
        if 'sum' in entry_dict and can_run:
            self.data.save_sum_fields(entry_dict['sum'], self.agg_sum_file, self.agg_sum_file_type_button.get_choice())

        if can_run:
            self.root.deiconify()
            self.clear_entries()

    
    def save_file(self, file, file_button):
        file = filedialog.asksaveasfilename()

        if file:
            self.run_button.grid()
            file_button['text'] = 'File Selected'

        else:
            self.run_button.grid_remove()
            file_button['text'] = 'Select File to Save to'

        if file_button is self.frequency_file_button:
            self.frequency_file = file
        elif file_button is self.agg_sum_file_button:
            self.agg_sum_file = file


    def open_file(self):
        self.datafile = filedialog.askopenfilename()
        if self.datafile:
            self.datafile_button['text'] = 'Data File Selected'
            self.show_entries()
            if self.get_entries():
                self.run_button.grid()
        else:
            self.datafile_button['text'] = 'Select Data File to Use'
            self.hide_entries()
            self.run_button.grid_remove()


    def show_entries(self):
        if self.datafile.endswith('.csv'):
            cols = CallPmaw.get_csv_cols(self.datafile)
        elif self.datafile.endswith('xlsx'):
            cols = CallPmaw.get_xlsx_cols(self.datafile)
        else:
            print('File type not recognized. File was: '+self.datafile)

        self.frequency_entries.remove_all_items()
        self.frequency_entries.add_items(cols)
        self.frequency_entries.clear()
        self.frequency_entries.grid()

        self.agg_sum_entries.remove_all_items()
        self.agg_sum_entries.add_items(cols)
        self.agg_sum_entries.clear()
        self.agg_sum_entries.grid()


    def hide_entries(self):
        self.frequency_entries.grid_remove()
        self.agg_sum_entries.grid_remove()


    def get_entries(self):
        entry_dict = {}

        if self.frequency_entries.get_checked_items():
            entry_dict['count'] = self.frequency_entries.get_checked_items()
        if self.agg_sum_entries.get_checked_items():
            entry_dict['sum'] = self.agg_sum_entries.get_checked_items()

        return entry_dict


    def clear_entries(self):
        self.frequency_entries.clear()
        self.agg_sum_entries.clear()

    
    def raise_error(msg: str, title:str = ''):
        messagebox.showinfo(message=msg, title=title)


    def check_checklists(self):
        if self.frequency_entries.get_checked_items():
            self.frequency_file_button.grid()
            self.frequency_file_type_button.grid()
        else:
            self.frequency_file_button.grid_remove()
            self.frequency_file_type_button.grid_remove()
        if self.agg_sum_entries.get_checked_items():
            self.agg_sum_file_button.grid()
            self.agg_sum_file_type_button.grid()
        else:
            self.agg_sum_file_button.grid_remove()
            self.agg_sum_file_type_button.grid_remove()
            
            

