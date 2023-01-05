import tkinter as tk
from tkinter import filedialog, messagebox, font
from backend.constants import FileType, ExportFileType, DataType
from tkpywidgets import Checklist, ButtonList, Console, HorizontalScrolledFrame
from gui.base_gui import BaseGUI
from backend.dcfr_data import Data
from backend.search_pmaw import CallPmaw
import pandas as pd
import textwrap
import backend.constants as constants


class DataGUI(BaseGUI): #TODO get way to count total comments returned

    width = constants.DATA_WIDTH
    height = constants.DATA_HEIGHT

    msg_height = constants.DATA_HEIGHT + 65

    tooltip_fields = {
                    DataType.AGGREGATE_SUM.value: textwrap.fill('Returns the sum of all numeric columns for every distinct member of the groups chosen', constants.TEXT_WRAP),
                    DataType.FREQUENCY.value: textwrap.fill('Returns the number of times every distinct member of the groups chosen appears in the data set', constants.TEXT_WRAP),
                    DataType.GINI_COEFFICIENCT.value: textwrap.fill('Returns a value representing the inequality in data. A value of 0 means all values are the same, and a value of 1 means every value is different', constants.TEXT_WRAP),
    }

    def __init__(self, parent, root, executor, output, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root
        self.executor = executor
        self.output = output
        self.parent = parent
        self.data_entries = {}

        self.data_entries[DataType.AGGREGATE_SUM.value] = DataEntry(self, datatype=DataType.AGGREGATE_SUM, function=Data.save_sum_fields, rule_function=Data.true_rule, export_file_type=ExportFileType.CSV, title='Get aggregate sum grouped by')
        self.data_entries[DataType.FREQUENCY.value] = DataEntry(self, datatype=DataType.FREQUENCY, function=Data.save_count_fields, rule_function=Data.true_rule, export_file_type=ExportFileType.CSV, title='Get frequency grouped by')
        self.data_entries[DataType.GINI_COEFFICIENCT.value] = DataEntry(self, datatype=DataType.GINI_COEFFICIENCT, function=Data.save_gini_coefficient, rule_function=Data.gini_rule, export_file_type=ExportFileType.TXT, title='Get gini coefficient of')

        for entry in self.data_entries.values():
            entry.grid(row=0, column=1, sticky='news')

        #self.on_data_selection(next(iter(self.data_entries)))

        data_types = [d.value for d in DataType]

        self.datatype_selection = ButtonList(self, title='Data Functions', listvariable=data_types, command='on_data_selection', tooltip_dict=self.tooltip_fields, labelanchor='n', take_focus=False, stay_active=True, active_relief=tk.SUNKEN)
        self.datatype_selection.grid(row=0, column=0, sticky='news', padx=5, pady=5)
        self.datatype_selection.select(data_types[0])

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select Data File', command=self.open_file)
        self.run_button.grid(row=0, column=1)
        self.run_button.grid_remove()
        self.file_button.grid(row=0, column=0)

        self.wheel = Console(self, width=10, height=1, bg='#f0f0f0', relief=tk.FLAT, font=font.nametofont("TkDefaultFont"), state='disabled')
        self.wheel.grid(row=2, column=1, sticky='se')

        self.msg_frame = tk.LabelFrame(self)
        self.msg_scroll_frame = HorizontalScrolledFrame(self.msg_frame, width=self.width-30)
        self.msg_text = tk.Text(self.msg_scroll_frame.interior, bg=self.root.cget('bg'), relief=tk.FLAT, font=font.nametofont("TkDefaultFont"), height=1, state='disabled')
        self.msg_frame.grid(row=3, column=0, sticky='sew', padx=5, pady=(15,5), columnspan=2)
        self.msg_scroll_frame.grid(row=0, column=0)
        self.msg_text.grid(row=0, column=0)
        self.msg_frame.grid_remove()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10000)

        self.grid_rowconfigure(0, weight=1)


    def run(self):
        if self.datafile.endswith(FileType.CSV.value):
            df = pd.read_csv(self.datafile, sep=',', usecols=CallPmaw.get_csv_cols(self.datafile))
        elif self.datafile.endswith(FileType.XLSX.value):
            df = pd.read_excel(self.datafile)
        else:
            messagebox.showerror(title='Data File Error', message='File Selected is not a recognized file type. Must be .csv or .xlsx')
            return
        
        self.executor.submit(self.save_data, df)


    def save_data(self, df):
        self.wheel.start_wheel('Running   ')
        self.current_data_entry.save_data(df, self.datafile, self)
        self.wheel.clear_wheel()


    def open_file(self):
        self.datafile = filedialog.askopenfilename()
        if self.datafile:
            self.file_button['text'] = 'Data File Selected'
            self.replace_entries()
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

    def replace_entries(self):
        valid = True
        for entry in self.data_entries.values():
            if valid:
                valid = entry.replace_entries(self.datafile)

    def hide_entries(self):
        for entry in self.data_entries.values():
                entry.hide_entries()


    def send_message(self, msg:str):
        self.set_geometry(constants.DATA_WIDTH, self.msg_height)
        self.msg_text.config(width=len(msg), state='normal')
        self.msg_text.replace(1.0, tk.END, msg)
        self.msg_text.config(state='disabled')
        self.msg_frame.grid()

    def set_geometry(self, width, height):
        self.width = width
        self.height = height
        self.msg_frame['width'] = width
        if self.parent.index(self.parent.select()) == constants.NotebookPage.DATA_PAGE.value:
            self.root.geometry(str(width)+'x'+str(height))


            
            
class DataEntry(tk.Frame):
    def __init__(self, parent, datatype: DataType, title:str, function, rule_function, export_file_type:ExportFileType, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.datatype = datatype
        self.function = function
        self.rule_function = rule_function
        self.export_file_type = export_file_type

        self.entries = Checklist(self, [], title=title, scrollbar=True, labelanchor='n')
        self.entries.clear()

        self.entries.grid(row=0, column=0, sticky='news', padx=5, pady=5)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)


    def replace_entries(self, datafile: str):
        title = 'Data File Error'
        msg = 'The data file selected is not formatted correctly. The first row of each column should contain the name of that column'
        if datafile.endswith('.csv'):
            try:
                cols = CallPmaw.get_csv_cols(datafile)
            except:
                messagebox.showerror(title=title, message=msg)
                return False
        elif datafile.endswith('xlsx'):
            try:
                cols = CallPmaw.get_xlsx_cols(datafile)
            except:
                messagebox.showerror(title=title, message=msg)
                return False
        else:
            messagebox.showerror(title=title, message='File Selected is not a recognized file type. Must be .csv or .xlsx')
            return False

        self.entries.remove_all_items()
        self.entries.add_items(cols)
        self.entries.clear()
        return True

    def hide_entries(self):
        self.entries.remove_all_items()

    def get_entries(self):
        return self.entries.get_checked_items()

    def get_save_file(self, datafile: str):
        file_name_index = datafile.rfind('/')
        savefile = datafile[0 : file_name_index+1] + self.datatype.value +' of '+ str(self.get_entries())[1:-1] +' in '+datafile[file_name_index+1:]
        return savefile

    def save_data(self, df: pd.DataFrame, datafile: str, output):
        rule_return = self.rule_function(df, self.get_entries())

        if rule_return == True:
            self.function(df, self.get_entries(), self.get_save_file(datafile), self.export_file_type.value, output)
        else:
            messagebox.showerror(title='Group Selection Error', message=rule_return)

        return True



