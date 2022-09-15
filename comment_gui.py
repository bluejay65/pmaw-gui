#import base_gui
import tkinter as tk
from tkinter import messagebox
from tkwidgets import LabelEntryList, Checklist, EntryType


class CommentGUI(tk.Frame):#base_gui.BaseGUI):

    search_fields = {
                    'Search term': EntryType.ENTRY, 
                    'Max results': EntryType.ENTRY, 
                    'Author': EntryType.ENTRY, 
                    'Subreddit': EntryType.ENTRY,
                    'Posted after': EntryType.DATETIME,
                    'Posted before': EntryType.DATETIME
    }

    return_fields = [
                    'all_awardings',
                    'archived',
                    'author',
                    'author_fullname',
                    'body',
                    'comment_type',
                    'controversiality',
                    'created_utc',
                    'gilded',
                    'id',
                    'link_id',
                    'locked',
                    'parent_id',
                    'permalink',
                    'retrieved_utc',
                    'score',
                    'score_hidden',
                    'send_replies',
                    'stickied',
                    'subreddit',
                    'subreddit_id',
                    'subreddit_name_prefixed',
                    'subreddit_type',
                    'total_awards_received',
                    'treatment_tags'
    ]

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        print(self.return_fields)

        self.label_entries = LabelEntryList(self, self.search_fields)
        self.label_entries.grid(row=0, column=0, sticky='nw')

        self.label_entries.set_entry('Max results', 500)

        self.return_entries_label = tk.Label(self, text='Data to Return')
        self.return_entries = Checklist(self, self.return_fields, True)

        self.return_entries_label.grid(row=0, column=1)
        self.return_entries.grid(row=0, column=2)




    def start_data(self):
        data_dict = {}

        data_dict['q'] = self.q_strvar.get()
        if data_dict['q'] == '':
            data_dict['q'] = None

        data_dict['limit'] = int(self.limit_strvar.get())

        data_dict['fields'] = self.fields_checklist.get_checked_items()
        if len(data_dict['fields']) <= 0:
            data_dict['fields'] = None

        data_dict['author'] = self.author_strvar.get()
        if data_dict['author'] == '':
            data_dict['author'] = None

        data_dict['subreddit'] = self.subreddit_strvar.get()
        if data_dict['subreddit'] == '':
            data_dict['subreddit'] = None

        if self.after_date_strvar.get() == '':
            data_dict['after'] = None
        else:
            try:
                data_dict['after'] = self.date_to_epoch(self.after_date_strvar.get()) + self.time_to_epoch(self.after_time_picker.time())
            except:
                self.raise_error('The date must be formatted using D/M/YYYY or D-M-YYYY', 'Date Entry Error')
                return

        if self.before_date_strvar.get() == '':
            data_dict['before'] = None
        else:
            try:
                data_dict['before'] = self.date_to_epoch(self.before_date_strvar.get()) + self.time_to_epoch(self.before_time_picker.time())
            except:
                self.raise_error('The date must be formatted using D/M/YYYY or D-M-YYYY', 'Date Entry Error')
                return

        if self.file_str != '':
            data_dict['file'] = self.file_str
        else:
            self.raise_error('You must select a file before running the search', 'File Select Error')
            return

        if data_dict['q'] == None and data_dict['author'] == None and data_dict['subreddit'] == None:
            if not messagebox.askokcancel(message='Data collection is unpredictable if no search term, subreddit, or author is defined', title='Data Warning'):
                return

        self.process_data(data_dict)


    def reset_fields(self):
        self.fields_checklist.check_items([0, 5, 6, 7, 15, 17])


root = tk.Tk()
frame_main = tk.Frame(root, padx=20)
frame_main.grid(sticky='news')

comments = CommentGUI(frame_main)
comments.grid(row=0, column=0)

root.mainloop()