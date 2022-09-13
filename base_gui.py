import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tktimepicker import SpinTimePickerModern, constants
import time
import search_pmaw
from comment_gui import CommentGUI



class BaseGUI(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(self, parent, **kwargs)

        self.vcmd = (self.register(self.check_limit_digit), '%P')


    # Opens a file dialog and edits the button to open the dialog to say the name of the file
    def select_file(self):
        global file_str
        file_str = filedialog.asksaveasfilename()
        if file_str != '':
            if len(file_str) > 20:
                self.file_button['text'] = file_str[-20:-1] + file_str[-1]
            else:
                self.file_button['text'] = file_str
        else:
            self.file_button['text'] = 'Select File'

    # Opens a messagebox
    def raise_error(msg: str, title:str = ''):
        messagebox.showinfo(message=msg, title=title)

    # Verifies the text entered are numbers
    def check_limit_digit(self, P):
        if str.isdigit(P) or P == '':
            return True
        else:
            return False

    # Converts a string date to epoch time
    def date_to_epoch(self, date_time: str):
        try:
            return int(time.mktime(time.strptime(date_time, '%m-%d-%Y')))
        except:
            return int(time.mktime(time.strptime(date_time, '%m/%d/%Y')))

    # Converts a time_tuple to epoch time
    def time_to_epoch(self, time_tuple):
        added_time = 0
        hours = 0

        if time_tuple[0] != 12:
            hours = time_tuple[0]

        if time_tuple[2] == 'PM':
            added_time = 43200

        return hours * 3600 + time_tuple[1] * 60 + added_time

    # Runs the data search and saves it to a csv file. The GUI is closed while this happens
    def process_data(self, data_dict):
        self.root.withdraw()

        api = search_pmaw.CallPmaw()
        api.get_df(data_dict)

        self.root.deiconify()


    q_label = tk.Label(frame_main, text="Search term")
    ids_label = tk.Label(frame_main, text="Comment IDs")
    limit_label= tk.Label(frame_main, text="Max Results")
    fields_label = tk.Label(frame_main, text="Data to Return")
    author_label = tk.Label(frame_main, text="Author")
    subreddit_label = tk.Label(frame_main, text="Subreddit")
    after_date_label = tk.Label(frame_main, text="Posted After Date")
    after_time_label = tk.Label(frame_main, text="Posted After Time")
    before_date_label = tk.Label(frame_main, text="Posted Before Date")
    before_time_label = tk.Label(frame_main, text="Posted Before Time")
    file_label = tk.Label(frame_main, text="File to Save To")
    running_label = tk.Label(frame_main, text='')

    q_strvar = tk.StringVar()
    ids_strvar = tk.StringVar()
    limit_strvar = tk.StringVar(value="500")
    fields_list = ["author", "author_created_utc", "author_flair_css_class", "author_flair_text", "author_fullname", "body", "controversiality", "created_utc", "distinguished", "gilded", "id", "link_id", "nest_level", "parent_id", "retrieved_on", "score", "score_hidden", "subreddit", "subreddit_id"]
    fields_strvar = tk.StringVar(value=fields_list)
    author_strvar = tk.StringVar()
    subreddit_strvar = tk.StringVar()
    after_date_strvar = tk.StringVar()
    after_time_strvar = tk.StringVar()
    before_date_strvar = tk.StringVar()
    before_time_strvar = tk.StringVar()
    file_str = ''

    q_entry = tk.Entry(frame_main, textvariable=q_strvar)
    #ids_entry = tk.Entry(frame_main, textvariable=ids_strvar) TODO add ids
    limit_entry = tk.Entry(frame_main, textvariable=limit_strvar, validate='all', validatecommand=vcmd)
    fields_checklist = Checklist(frame_main, listvariable=fields_list)
    author_entry = tk.Entry(frame_main, textvariable=author_strvar)
    subreddit_entry = tk.Entry(frame_main, textvariable=subreddit_strvar)
    after_date_entry = tk.Entry(frame_main, textvariable=after_date_strvar)
    after_time_picker = SpinTimePickerModern(frame_main)
    before_date_entry = tk.Entry(frame_main, textvariable=before_date_strvar)
    before_time_picker = SpinTimePickerModern(frame_main)
    default_fields_button = tk.Button(frame_main, text='Set Fields to Default', command=reset_fields)
    file_button = tk.Button(frame_main, text='Select CSV File', command=select_file)

    reset_fields()

    after_time_picker.addAll(constants.HOURS12)
    after_time_picker.configureAll(bg="#dddddd", width=4, hoverbg="#aaaaaa", clickedbg="#000000", clickedcolor="#ffffff")
    after_time_picker.configure_separator(bg="#dddddd")
    after_time_picker.setMins(0)
    before_time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
    before_time_picker.configureAll(bg="#dddddd", width=4, hoverbg="#aaaaaa", clickedbg="#000000", clickedcolor="#ffffff")
    before_time_picker.configure_separator(bg="#dddddd")
    before_time_picker.setMins(0)

    seperator1 = ttk.Separator(frame_main, orient='vertical')
    run_button = tk.Button(frame_main, text='Run', command=start_comment_data)

    q_label.grid(row=0, column=0, sticky='w')
    fields_label.grid(row=0, column=4, rowspan=11, sticky='w')
    #ids_label.grid(row=1, column=0, sticky='w') TODO add ids
    limit_label.grid(row=1, column=0, sticky='w')
    author_label.grid(row=4, column=0, sticky='w')
    subreddit_label.grid(row=5, column=0, sticky='w')
    after_date_label.grid(row=6, column=0, sticky='w')
    after_time_label.grid(row=7, column=0, sticky='w')
    before_date_label.grid(row=8, column=0, sticky='w')
    before_time_label.grid(row=9, column=0, sticky='w')
    file_label.grid(row=10, column=0, sticky='w')
    running_label.grid(row=11, column=2)

    q_entry.grid(row=0, column=2)
    fields_checklist.grid(row=0, column=5, rowspan=11)
    #ids_entry.grid(row=1, column=2) TODO add ids
    limit_entry.grid(row=1, column=2)
    default_fields_button.grid(row=11, column=5)
    author_entry.grid(row=4, column=2)
    subreddit_entry.grid(row=5, column=2)
    after_date_entry.grid(row=6, column=2)
    after_time_picker.grid(row=7, column=2)
    before_date_entry.grid(row=8, column=2)
    before_time_picker.grid(row=9, column=2)
    file_button.grid(row=10, column=2)

    seperator1.grid(row=0, column=3, rowspan=12, ipady=220) #TODO dynamically resize seperator
    run_button.grid(row=11, column=1)

    frame_main.rowconfigure(0, pad=20)
    frame_main.rowconfigure(1, pad=20)
    frame_main.rowconfigure(2, pad=20)
    frame_main.rowconfigure(3, pad=20)
    frame_main.rowconfigure(4, pad=20)
    frame_main.rowconfigure(5, pad=20)
    frame_main.rowconfigure(6, pad=20)
    frame_main.rowconfigure(7, pad=20)
    frame_main.rowconfigure(8, pad=20)
    frame_main.rowconfigure(9, pad=20)
    frame_main.rowconfigure(10, pad=20)
    frame_main.rowconfigure(11, pad=20)

    frame_main.columnconfigure(0, pad=20)
    frame_main.columnconfigure(1, pad=20)
    frame_main.columnconfigure(2, pad=20)
    frame_main.columnconfigure(3, pad=20)
    frame_main.columnconfigure(4, pad=20)
    frame_main.columnconfigure(5, pad=20)