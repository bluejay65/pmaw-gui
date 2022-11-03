import tkinter as tk
from tkinter import filedialog, messagebox
from tkwidgets import Checklist, ButtonList
from base_gui import BaseGUI
from constants import FileType, ExportFileType, DataType
from dcfr_data import Data
from search_pmaw import CallPmaw
import pandas as pd
import textwrap
import constants


class DataGUI(BaseGUI): #TODO get way to count total comments returned

    tooltip_fields = {
                    DataType.AGGREGATE_SUM.value: textwrap.fill('Returns the sum of all numeric columns for every distinct member of the groups chosen', constants.TEXT_WRAP),
                    DataType.FREQUENCY.value: textwrap.fill('Returns the number of times every distinct member of the groups chosen appears in the data set', constants.TEXT_WRAP),
                    DataType.GINI_COEFFICIENCT.value: textwrap.fill('Returns a value representing the inequality in data. A value of 0 means all values are the same, and a value of 1 means every value is different', constants.TEXT_WRAP),
    }

    def __init__(self, parent, root, executor, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root
        self.executor = executor
        self.data_entries = {}

        self.data_entries[DataType.AGGREGATE_SUM.value] = DataEntry(self, datatype=DataType.AGGREGATE_SUM, function=Data.save_sum_fields, title='Get aggregate sum grouped by')
        self.data_entries[DataType.FREQUENCY.value] = DataEntry(self, datatype=DataType.FREQUENCY, function=Data.save_count_fields, title='Get frequency grouped by')
        self.data_entries[DataType.GINI_COEFFICIENCT.value] = DataEntry(self, datatype=DataType.GINI_COEFFICIENCT, function=Data.save_gini_coefficent, title='Get gini coefficient of')

        for entry in self.data_entries.values():
            entry.grid(row=0, column=1)
            entry.grid_remove()

        self.on_data_selection(next(iter(self.data_entries)))

        self.datatype_selection = ButtonList(self, title='Data Functions', listvariable=[d.value for d in DataType], command='on_data_selection', relief=tk.RIDGE, tooltip_dict=self.tooltip_fields)
        self.datatype_selection.grid(row=0, column=0)

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select Data File', command=self.open_file)
        self.run_button.grid(row=0, column=1)
        self.run_button.grid_remove()
        self.file_button.grid(row=0, column=0)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=0)

        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)


    def run(self):
        if self.datafile.endswith(FileType.CSV.value):
            df = pd.read_csv(self.datafile, sep=',', usecols=CallPmaw.get_csv_cols(self.datafile))
        elif self.datafile.endswith(FileType.XLSX.value):
            df = pd.read_excel(self.datafile)
        else:
            messagebox.showerror('File Selected is not a recognized file type. Must be .csv or .xlsx')
            return
        
        self.executor.submit(self.current_data_entry.save_data, df, self.datafile)



    def open_file(self):
        self.datafile = filedialog.askopenfilename()
        if self.datafile:
            self.file_button['text'] = 'Data File Selected'
            self.show_entries()
            self.run_button.grid()
        else:
            self.file_button['text'] = 'Select Data File'
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

    def hide_entries(self):
        for entry in self.data_entries.values():
                entry.hide_entries()


            
            
class DataEntry(tk.Frame):
    def __init__(self, parent, datatype: DataType, title:str, function, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.datatype = datatype
        self.function = function

        self.entries = Checklist(self, [], title=title, scrollbar=True)
        self.entries.clear()

        self.entries.grid(row=0, column=0)


    def show_entries(self, datafile: str):
        if datafile.endswith('.csv'):
            cols = CallPmaw.get_csv_cols(datafile)
        elif datafile.endswith('xlsx'):
            cols = CallPmaw.get_xlsx_cols(datafile)
        else:
            print('File type not recognized. File was: '+datafile)

        self.entries.remove_all_items()
        self.entries.add_items(cols)
        self.entries.clear()

    def hide_entries(self):
        self.entries.remove_all_items()

    def get_entries(self):
        return self.entries.get_checked_items()

    
    def get_save_file(self, datafile: str):
        file_name_index = datafile.rfind('/')
        savefile = datafile[0 : file_name_index+1] + self.datatype.value +' of '+ str(self.get_entries())[1:-1] +' in '+datafile[file_name_index+1 :]
        savefile = CallPmaw.add_file_type(savefile, ExportFileType.CSV.value)
        return savefile

    def save_data(self, df: pd.DataFrame, datafile: str):
        self.function(df, self.get_entries(), self.get_save_file(datafile), ExportFileType.CSV.value)



