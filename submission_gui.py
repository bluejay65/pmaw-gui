import tkinter as tk
from tkinter import Entry, filedialog
from tkinter import messagebox
from tkwidgets import LabelEntryList, Checklist, EntryType
from search_pmaw import CallPmaw
from base_gui import BaseGUI
import constants


class SubmissionGUI(BaseGUI):

    search_fields = {
                    'Search term': EntryType.ENTRY,
                    'Exclude Search Term': EntryType.ENTRY,
                    'Search Title': EntryType.ENTRY,
                    'Exclude Title Text': EntryType.ENTRY,
                    'Search Body': EntryType.ENTRY,
                    'Exclude Body Text': EntryType.ENTRY,
                    'Max results': EntryType.ENTRY,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    'Score': EntryType.RANGE,
                    'Number of Comments': EntryType.RANGE,
                    ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only'): EntryType.DROPDOWN,
                    ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos'): EntryType.DROPDOWN,
                    ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only'): EntryType.DROPDOWN,
                    ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied'): EntryType.DROPDOWN,
                    ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers'): EntryType.DROPDOWN,
                    ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode'): EntryType.DROPDOWN,
                    'Posted after': EntryType.DATETIME,
                    'Posted before': EntryType.DATETIME
    }

    api_fields = {
                    'Search term': 'q',
                    'Exclude Search Term': 'q:not',
                    'Search Title': 'title',
                    'Exclude Title Text': 'title:not',
                    'Search Body': 'selftext',
                    'Exlude Body Text': 'selftext:not',
                    'Max results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Score': 'score',
                    'Number of Comments': 'num_comments',
                    ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only'): 'over_18',
                    ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos'): 'is_video',
                    ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only'): 'locked',
                    ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied'): 'stickied',
                    ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers'): 'spoiler',
                    ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode'): 'contest_mode',
                    'Posted after': 'after',
                    'Posted before': 'before'
    }

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.label_entries = LabelEntryList(self, self.search_fields)
        self.label_entries.grid(row=0, column=0)

        self.label_entries.set_entry('Max results', 500)

        self.return_entries = Checklist(self, constants.return_fields, title='Data to Return', scrollbar=False)

        self.return_entries.grid(row=0, column=1)
        self.reset_return_fields()

        self.file_selected = ''
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=2)
        self.button_frame.columnconfigure(0, pad=20)
        self.button_frame.columnconfigure(1, pad=20)

        self.run_button = tk.Button(self.button_frame, text='Run', command=self.run)
        self.file_button = tk.Button(self.button_frame, text='Select File', command=self.select_file)
        self.file_button.grid(row=0, column=0)

        self.rowconfigure(0, pad=10)
        self.rowconfigure(1, pad=10)
        self.columnconfigure(0, pad=20)
        self.columnconfigure(0, pad=20)




    def run(self):
        entry_dict = self.get_entries()
        if entry_dict['q'] is None and entry_dict['author'] is None and entry_dict['subreddit'] is None:
            if not messagebox.askokcancel(message='May return few results if no query, subreddit, or author is defined', title='Data Warning'):
                return
        self.root.withdraw()
        CallPmaw.save_csv(entry_dict, self.file_selected)
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

        entry_dict['limit'] = int(entry_dict['limit'])
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