import tkinter as tk
from tkinter import filedialog, messagebox
from tkwidgets import Checklist, Radiolist, ButtonList
from base_gui import BaseGUI
from constants import FileType, DataType
from pmaw_data import Data
from search_pmaw import CallPmaw
import pandas as pd


class DataGUI(BaseGUI): #TODO get way to count total comments returned

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root
        self.data_entries = {}

        self.data_entries[DataType.AGGREGATE_SUM.value] = DataEntry(self, datatype=DataType.AGGREGATE_SUM, function=Data.save_sum_fields, title='Get aggregate sum grouped by')
        self.data_entries[DataType.FREQUENCY.value] = DataEntry(self, datatype=DataType.FREQUENCY, function=Data.save_count_fields, title='Get frequency grouped by')
        self.data_entries[DataType.GINI_COEFFICIENCT.value] = DataEntry(self, datatype=DataType.GINI_COEFFICIENCT, function=Data.save_gini_coefficent, title='Get gini coefficient of')

        for entry in self.data_entries.values():
            entry.grid(row=0, column=1)
            entry.grid_remove()

        self.on_data_selection(next(iter(self.data_entries)))

        self.datatype_selection = ButtonList(self, title='Data Functions', listvariable=[d.value for d in DataType], command='on_data_selection', relief=tk.RIDGE)
        self.datatype_selection.grid(row=0, column=0)

        self.datafile = ''
        self.data_button_frame = tk.Frame(self)
        self.data_button_frame.grid(row=1, column=0, columnspan=2)
        self.data_button_frame.columnconfigure(0, pad=10)
        self.data_button_frame.columnconfigure(1, pad=10)

        self.datafile_button = tk.Button(self, text='Select Data File to Use', command=lambda: self.open_file())
        self.datafile_button.grid(row=2, column=0, columnspan=2)

        self.run_button = tk.Button(self, text='Run', command=self.run)
        self.run_button.grid(row=3, column=0, columnspan=2)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=0)

        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)


    def run(self):
        entries = self.current_data_entry.get_entries()

        self.root.withdraw()

        if self.datafile.endswith(FileType.CSV.value):
            df = pd.read_csv(self.datafile, sep=',', usecols=CallPmaw.get_csv_cols(self.datafile))
        elif self.datafile.endswith(FileType.XLSX.value):
            df = pd.read_excel(self.datafile)
        else:
            messagebox.showerror('File Selected is not a recognized file type. Must be .csv or .xlsx')
            return
        
        self.current_data_entry.save_data(df)

        self.root.deiconify()


    def open_file(self):
        self.datafile = filedialog.askopenfilename()
        if self.datafile:
            self.datafile_button['text'] = 'Data File Selected'
            self.show_entries()
        else:
            self.datafile_button['text'] = 'Select Data File to Use'
            self.hide_entries()
            self.run_button.grid_remove()


    def on_data_selection(self, datatype_value):
        for entry in self.data_entries.values():
            entry.grid_remove()
        self.data_entries[datatype_value].grid()
        self.current_data_entry = self.data_entries[datatype_value]

    def show_entries(self):
        for entry in self.data_entries.values():
                entry.show_entries(self.datafile)


            
            
class DataEntry(tk.Frame):
    def __init__(self, parent, datatype: DataType, title:str, function, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.datatype = datatype
        self.file = ''
        self.function = function

        self.entries = Checklist(self, [], title=title, scrollbar=True)
        self.entries.clear()

        self.file_button = tk.Button(self, text='Select File to Save to', command=self.save_file)
        self.file_type_button = Radiolist(self, options=[f.value for f in FileType], title='Save As')

        self.entries.grid(row=0, column=0)
        self.file_button.grid(row=1, column=0)
        self.file_type_button.grid(row=2, column=0)


    def show_entries(self, datafile):
        if datafile.endswith('.csv'):
            cols = CallPmaw.get_csv_cols(datafile)
        elif datafile.endswith('xlsx'):
            cols = CallPmaw.get_xlsx_cols(datafile)
        else:
            print('File type not recognized. File was: '+datafile)

        self.entries.remove_all_items()
        self.entries.add_items(cols)
        self.entries.clear()


    def get_entries(self):
        return self.entries.get_checked_items()

    
    def save_file(self):
        self.file = filedialog.asksaveasfilename()

        if self.file:
            self.file_button['text'] = 'File Selected'

        else:
            self.file_button['text'] = 'Select File to Save to'

    def save_data(self, df: pd.DataFrame):
        self.function(df, self.get_entries(), self.file, self.file_type_button.get_choice())



