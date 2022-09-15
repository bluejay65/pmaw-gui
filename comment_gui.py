import tkinter as tk
from tkinter import filedialog
from tkwidgets import LabelEntryList, Checklist, EntryType
from search_pmaw import CallPmaw
from base_gui import BaseGUI


class CommentGUI(BaseGUI):

    search_fields = {
                    'Search term': EntryType.ENTRY,
                    'Max results': EntryType.ENTRY,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    'Posted after': EntryType.DATETIME,
                    'Posted before': EntryType.DATETIME
    }

    api_fields = {
                    'Search term': 'q',
                    'Max results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Posted after': 'after',
                    'Posted before': 'before'
    }

    return_fields = [
                    'all_awardings',            # 0
                    'archived',                 # 1
                    'author',                   # 2
                    'author_fullname',          # 3
                    'body',                     # 4
                    'comment_type',             # 5
                    'controversiality',         # 6
                    'created_utc',              # 7
                    'gilded',                   # 8 
                    'id',                       # 9
                    'link_id',                  # 10
                    'locked',                   # 11
                    'parent_id',                # 12
                    'permalink',                # 13
                    'retrieved_utc',            # 14
                    'score',                    # 15
                    'score_hidden',             # 16
                    'send_replies',             # 17
                    'stickied',                 # 18
                    'subreddit',                # 19
                    'subreddit_id',             # 20
                    'subreddit_name_prefixed',  # 21
                    'subreddit_type',           # 22 
                    'total_awards_received',    # 23
                    'treatment_tags'            # 24
    ]

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.label_entries = LabelEntryList(self, self.search_fields)
        self.label_entries.grid(row=0, column=0)

        self.label_entries.set_entry('Max results', 500)

        self.return_entries = Checklist(self, self.return_fields, title='Data to Return', scrollbar=True)

        self.return_entries.grid(row=0, column=1)
        self.reset_return_fields()

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select File', command=self.select_file)
        self.file_button.grid(row=0, column=0, columnspan=2)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.columnconfigure(0, pad=20)
        self.columnconfigure(0, pad=20)

        self.pmaw = CallPmaw()




    def run(self):
        data_dict = self.get_data()
        self.root.withdraw()
        self.pmaw.save_csv(data_dict, self.file_selected)
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
        self.return_entries.check_items([2, 4, 6, 7, 15, 19])

    def get_data(self):
        data_dict = {}

        for key in self.search_fields.keys():
            data_dict[self.api_fields[key]] = self.label_entries.get_entry(key)

            if data_dict[self.api_fields[key]] == '':
                data_dict[self.api_fields[key]] = None
                
        data_dict['limit'] = int(data_dict['limit'])
        data_dict['fields'] = self.return_entries.get_checked_items()

        if data_dict['after']['date']:
            data_dict['after'] = self.date_time_to_epoch(data_dict['after']['date'], data_dict['after']['time'])
        else:
            data_dict['after'] = None
            
        if data_dict['before']['date']:
            data_dict['before'] = self.date_time_to_epoch(data_dict['before']['date'], data_dict['before']['time'])
        else:
            data_dict['before'] = None

        return data_dict