from json import tool
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkwidgets import LabelEntryList, Checklist, EntryType, Radiolist
from base_gui import BaseGUI
from enum import Enum
from constants import ExportFileType, SearchType
import textwrap
import constants


class Dropdowns(Enum):
    NSFW = ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only')
    VIDEO = ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos')
    LOCKED = ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only')
    STICKIED = ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied')
    SPOILERS = ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers')
    CONTEST = ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode')



class SubmissionGUI(BaseGUI):
    search_fields = {
                    'Search Title and Body': EntryType.ENTRY,
                    #'Exclude Search Term': EntryType.ENTRY,
                    'Search Title': EntryType.ENTRY,
                    #'Exclude Title Text': EntryType.ENTRY,
                    'Search Body': EntryType.ENTRY,
                    #'Exclude Body Text': EntryType.ENTRY,
                    'Max Results': EntryType.ENTRY,
                    'Author': EntryType.ENTRY,
                    'Subreddit': EntryType.ENTRY,
                    #'Score': EntryType.RANGE,
                    #'Number of Comments': EntryType.RANGE,
                    ('NSFW Submissions', 'No Filter', 'NSFW Only', 'SFW Only'): EntryType.DROPDOWN,
                    ('Video Submissions', 'No Filter', 'Video Only', 'Exclude Videos'): EntryType.DROPDOWN,
                    ('Locked Comments', 'No Filter', 'Locked Only', 'Unlocked Only'): EntryType.DROPDOWN,
                    ('Stickied Submission', 'No Filter', 'Stickied Only', 'Exlude Stickied'): EntryType.DROPDOWN,
                    ('Spoliers', 'No Filter', 'Spoliers Only', 'Exclude Spoilers'): EntryType.DROPDOWN,
                    ('Using Contest Mode', 'No Filter', 'Contest Mode Only', 'Exclude Contest Mode'): EntryType.DROPDOWN,
                    'Posted after': EntryType.DATETIME,
                    'Posted before': EntryType.DATETIME
    }

    tooltip_fields = {
                    'Search Title and Body': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s title or body. To search for multiple terms that all must be included in the same submission, use commas to delineate them.', constants.TEXT_WRAP),
                    'Search Title': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s title. To search for multiple terms that all must be included in the same title, use commas to delineate them.', constants.TEXT_WRAP),
                    'Search Body': textwrap.fill('Returns submissions that include the term(s) in the filter in the submission’s body. To search for multiple terms that all must be included in the body, use commas to delineate them.', constants.TEXT_WRAP),
                    'Max Results': textwrap.fill('Sets the maximum amount of results that DCfR will try to return. If there are fewer results available than the number you input, it will return every result it can.', constants.TEXT_WRAP),
                    'Author': textwrap.fill('Returns submissions posted by the author in the filter.', constants.TEXT_WRAP),
                    'Subreddit': textwrap.fill('Returns submissions from the subreddit(s) in the filter. To search in multiple subreddits, use commas to delineate them.', constants.TEXT_WRAP)
    }

    api_fields = {
                    'Search Title and Body': 'q',
                    'Exclude Search Term': 'q:not',
                    'Search Title': 'title',
                    'Exclude Title Text': 'title:not',
                    'Search Body': 'selftext',
                    'Exclude Body Text': 'selftext:not',
                    'Max Results': 'limit',
                    'Author': 'author',
                    'Subreddit': 'subreddit',
                    'Score': 'score',
                    'Number of Comments': 'num_comments',
                    'NSFW Submissions': 'over_18',
                    'Video Submissions': 'is_video',
                    'Locked Comments': 'locked',
                    'Stickied Submission': 'stickied',
                    'Spoliers': 'spoiler',
                    'Using Contest Mode': 'contest_mode',
                    'Posted after': 'after',
                    'Posted before': 'before'
    }

    def __init__(self, pmaw, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.pmaw = pmaw
        self.root = root

        self.label_entries = LabelEntryList(self, self.search_fields, title='Search Filters', tooltip_dict=self.tooltip_fields)
        self.label_entries.grid(row=0, column=0, rowspan=2)
        self.label_entries.update()

        self.return_entries = Checklist(self, constants.SUBMISSION_RETURN_FIELDS, title='Data to Return', scrollbar=True, height=450)

        self.return_entries.grid(row=0, column=1)
        self.reset_return_fields()

        self.file_type_button = Radiolist(self, options=[e.value for e in ExportFileType], title='Save as File Type')

        self.search_type_button = Radiolist(self, options=[e.value for e in SearchType], title='Download Data Using')
        self.search_type_button.grid(row=1, column=1)
        self.search_type_button.select(SearchType.PRAW.value)

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
        if entry_dict['q'] is None and entry_dict['title'] is None and entry_dict['selftext'] is None and entry_dict['author'] is None and entry_dict['subreddit'] is None:
            if not messagebox.askokcancel(message='May return few results if no query, subreddit, or author is defined', title='Data Warning'):
                return
        self.root.withdraw()
        self.pmaw.save_submission_file(entry_dict, file=self.file_selected, file_type=self.file_type_button.get_choice(), search_type=self.search_type_button.get_choice())
        self.root.deiconify()

    
    def select_file(self):
        self.file_selected = filedialog.asksaveasfilename()

        if self.file_selected:
            self.run_button.grid(row=0, column=1)
            self.file_button.grid(row=0, column=0)
        else:
            self.run_button.grid_forget()
            self.file_button.grid(row=0, column=0)


    def reset_return_fields(self):
        self.return_entries.check_items([
                                        'author',
                                        'created_datetime',
                                        'score',
                                        'selftext',
                                        'subreddit',
                                        'title'
                                        ])


    def get_entries(self):
        entry_dict = {}

        for key in self.search_fields.keys():
            if type(key) is tuple:
                entry_dict[self.api_fields[key[0]]] = self.label_entries.get_entry(key[0])

                if entry_dict[self.api_fields[key[0]]] == '' or entry_dict[self.api_fields[key[0]]] == key[1]:
                    entry_dict[self.api_fields[key[0]]] = None
                elif entry_dict[self.api_fields[key[0]]] == key[2]:
                    entry_dict[self.api_fields[key[0]]] = 'true'
                elif entry_dict[self.api_fields[key[0]]] == key[3]:
                    entry_dict[self.api_fields[key[0]]] = 'false'

            else:
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