import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkwidgets import LabelEntryList, Checklist, EntryType, Radiolist
from search_pmaw import CallPmaw
from base_gui import BaseGUI
from constants import FileType
import constants


class CommentGUI(BaseGUI):

    search_fields = {
                    'Search Term': EntryType.ENTRY,
                    'Max Results': EntryType.ENTRY,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    'Posted After': EntryType.DATETIME,
                    'Posted Before': EntryType.DATETIME
    }

    api_fields = {
                    'Search Term': 'q',
                    'Max Results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Posted After': 'after',
                    'Posted Before': 'before'
    }

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.label_entries = LabelEntryList(self, self.search_fields)
        self.label_entries.grid(row=0, column=0, rowspan=2)

        self.return_entries = Checklist(self, constants.comment_return_fields, title='Data to Return', height = 200, scrollbar=True)

        self.return_entries.grid(row=0, column=1)
        self.reset_return_fields()

        self.file_type_button = Radiolist(self, options=[e.value for e in FileType], title='Save as File Type')
        self.file_type_button.grid(row=1, column=1)

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select File', command=self.select_file)
        self.file_button.grid(row=0, column=0)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, pad=10)
        self.columnconfigure(0, pad=20)
        self.columnconfigure(1, pad=20)




    def run(self):
        entry_dict = self.get_entries()
        if entry_dict['q'] is None and entry_dict['author'] is None and entry_dict['subreddit'] is None:
            if not messagebox.askokcancel(message='May return few results if no query, subreddit, or author is defined', title='Data Warning'):
                return
        self.root.withdraw()
        CallPmaw.save_comment_file(entry_dict, file=self.file_selected, file_type=self.file_type_button.get_choice())
        self.root.deiconify()

    
    def select_file(self):
        self.file_selected = filedialog.asksaveasfilename()

        if self.file_selected:
            self.run_button.grid(row=0, column=0)
            self.file_button.grid(row=0, column=1)
        else:
            self.run_button.grid_forget()
            self.file_button.grid(row=0, column=0)


    def reset_return_fields(self):
        self.return_entries.check_items([
                                        'author',
                                        'body',
                                        'created_utc',
                                        'score',
                                        'subreddit'
                                        ])


    def get_entries(self):
        entry_dict = {}

        for key in self.search_fields.keys():
            entry_dict[self.api_fields[key]] = self.label_entries.get_entry(key)

            if entry_dict[self.api_fields[key]] == '':
                entry_dict[self.api_fields[key]] = None

        if entry_dict['limit']:
            entry_dict['limit'] = int(entry_dict['limit']) #TODO Nonetype isn't working if nothing is entered
        else:
            entry_dict['limit'] = sys.maxsize

        entry_dict['fields'] = self.return_entries.get_checked_items()

        if entry_dict['after']['date']:
            entry_dict['after'] = self.date_time_to_epoch(entry_dict['after']['date'], entry_dict['after']['time'])
        else:
            entry_dict['after'] = None
            
        if entry_dict['before']['date']:
            entry_dict['before'] = self.date_time_to_epoch(entry_dict['before']['date'], entry_dict['before']['time'])
        else:
            entry_dict['before'] = None

        return entry_dict