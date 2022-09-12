import tkinter as tk
from tkinter import messagebox, filedialog
from tktimepicker import SpinTimePickerModern, constants
import time
import search_pmaw


data_dict = {}

root = tk.Tk()
root.title("Reddit Data Collection")
root.columnconfigure(0, weight=100)
root.rowconfigure(0, weight=100)
root.resizable(False, False)

frame_main = tk.Frame(root, padx=20)
frame_main.grid(sticky='news')


def main():
    root.mainloop()

def select_file():
    global file_str 
    file_str = filedialog.asksaveasfilename()
    if file_str != '':
        if len(file_str) > 20:
            file_button['text'] = file_str[-20:-1] + file_str[-1]
        else:
            file_button['text'] = file_str
    else:
        file_button['text'] = 'Select File'

def raise_error(msg: str, title:str = ''):
    messagebox.showinfo(message=msg, title=title)


def check_limit_digit(P):
    if str.isdigit(P) or P == '':
        return True
    else:
        return False


def date_to_epoch(date_time: str):
    try:
        return int(time.mktime(time.strptime(date_time, '%d-%m-%Y')))
    except:
        return int(time.mktime(time.strptime(date_time, '%d/%m/%Y')))


def time_to_epoch(time_tuple):
    added_time = 0

    if time_tuple[0] == 12:
        time_tuple[0] = 0

    if time_tuple[2] == 'PM':
        added_time = 43200

    return time_tuple[0] * 3600 + time_tuple[1] * 60 + added_time


def start_data():
    data_dict['q'] = q_strvar.get()
    if data_dict['q'] == '':
        data_dict['q'] = None

    data_dict['limit'] = int(limit_strvar.get())

    data_dict['fields'] = fields_listbox.selection_get().splitlines()
    if len(data_dict['fields']) <= 0:
        data_dict['fields'] = None

    data_dict['author'] = author_strvar.get()
    if data_dict['author'] == '':
        data_dict['author'] = None

    data_dict['subreddit'] = subreddit_strvar.get()
    if data_dict['subreddit'] == '':
        data_dict['subreddit'] = None

    if after_date_strvar.get() == '':
        data_dict['after'] = None
    else:
        try:
            data_dict['after'] = date_to_epoch(after_date_strvar.get()) + time_to_epoch(after_time_picker.time())
            print(data_dict['after'])
        except:
            raise_error('The date must be formatted using D/M/YYYY or D-M-YYYY', 'Date Entry Error')
            return

    if before_date_strvar.get() == '':
        data_dict['before'] = None
    else:
        try:
            data_dict['before'] = date_to_epoch(before_date_strvar.get()) + time_to_epoch(before_time_picker.time())
        except:
            raise_error('The date must be formatted using D/M/YYYY or D-M-YYYY', 'Date Entry Error')
            return

    if file_str != '':
        data_dict['file'] = file_str

    if data_dict['q'] == None and data_dict['author'] == None and data_dict['subreddit'] == None:
        if not messagebox.askokcancel(message='Data collection is unpredictable if no query, subreddit, or author is defined', title='Data Warning'):
            return
        
    root.withdraw()

    api = search_pmaw.CallPmaw()
    api.get_df(data_dict)

    root.deiconify()


def reset_fields():
    fields_listbox.selection_set(0)
    fields_listbox.selection_clear(1)
    fields_listbox.selection_clear(2)
    fields_listbox.selection_clear(3)
    fields_listbox.selection_clear(4)
    fields_listbox.selection_set(5)
    fields_listbox.selection_set(6)
    fields_listbox.selection_set(7)
    fields_listbox.selection_clear(8)
    fields_listbox.selection_clear(9)
    fields_listbox.selection_clear(10)
    fields_listbox.selection_clear(11)
    fields_listbox.selection_clear(12)
    fields_listbox.selection_clear(13)
    fields_listbox.selection_clear(14)
    fields_listbox.selection_set(15)
    fields_listbox.selection_clear(16)
    fields_listbox.selection_set(17)
    fields_listbox.selection_clear(18)


vcmd = (root.register(check_limit_digit), '%P')


q_label = tk.Label(frame_main, text="Query")
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
fields_listbox = tk.Listbox(frame_main, listvariable=fields_strvar, selectmode='multiple')
author_entry = tk.Entry(frame_main, textvariable=author_strvar)
subreddit_entry = tk.Entry(frame_main, textvariable=subreddit_strvar)
after_date_entry = tk.Entry(frame_main, textvariable=after_date_strvar)
after_time_picker = SpinTimePickerModern(frame_main)
before_date_entry = tk.Entry(frame_main, textvariable=before_date_strvar)
before_time_picker = SpinTimePickerModern(frame_main)
default_fields_button = tk.Button(frame_main, text='Set Fields to Default', command=reset_fields)
file_button = tk.Button(frame_main, text='Select CSV File', command=select_file)

reset_fields()
fields_scrollbar = tk.Scrollbar(frame_main, command=fields_listbox.yview)
fields_listbox.configure(yscrollcommand=fields_scrollbar.set)

after_time_picker.addAll(constants.HOURS12)
after_time_picker.configureAll(bg="#dddddd", width=4, hoverbg="#aaaaaa", clickedbg="#000000", clickedcolor="#ffffff")
after_time_picker.configure_separator(bg="#dddddd")
after_time_picker.setMins(0)
before_time_picker.addAll(constants.HOURS12)  # adds hours clock, minutes and period
before_time_picker.configureAll(bg="#dddddd", width=4, hoverbg="#aaaaaa", clickedbg="#000000", clickedcolor="#ffffff")
before_time_picker.configure_separator(bg="#dddddd")
before_time_picker.setMins(0)

run_button = tk.Button(frame_main, text='Run', command=start_data)

q_label.grid(row=0, column=0, sticky='w')
#ids_label.grid(row=1, column=0, sticky='w') TODO add ids
limit_label.grid(row=1, column=0, sticky='w')
fields_label.grid(row=2, column=0, sticky='w')
author_label.grid(row=4, column=0, sticky='w')
subreddit_label.grid(row=5, column=0, sticky='w')
after_date_label.grid(row=6, column=0, sticky='w')
after_time_label.grid(row=7, column=0, sticky='w')
before_date_label.grid(row=8, column=0, sticky='w')
before_time_label.grid(row=9, column=0, sticky='w')
file_label.grid(row=10, column=0, sticky='w')
running_label.grid(row=11, column=2)

q_entry.grid(row=0, column=2)
#ids_entry.grid(row=1, column=2) TODO add ids
limit_entry.grid(row=1, column=2)
fields_listbox.grid(row=2, column=2)
fields_scrollbar.grid(row=2, column=3, sticky="nsw")
default_fields_button.grid(row=3, column=2, sticky='n')
author_entry.grid(row=4, column=2)
subreddit_entry.grid(row=5, column=2)
after_date_entry.grid(row=6, column=2)
after_time_picker.grid(row=7, column=2)
before_date_entry.grid(row=8, column=2)
before_time_picker.grid(row=9, column=2)
file_button.grid(row=10, column=2)

run_button.grid(row=11, column=1)

frame_main.rowconfigure(0, pad=20)
frame_main.rowconfigure(1, pad=20)
frame_main.rowconfigure(2, pad=20)
#frame_main.rowconfigure(3, pad=20)
frame_main.rowconfigure(4, pad=20)
frame_main.rowconfigure(5, pad=20)
frame_main.rowconfigure(6, pad=20)
frame_main.rowconfigure(7, pad=20)
frame_main.rowconfigure(8, pad=20)
frame_main.rowconfigure(9, pad=20)
frame_main.rowconfigure(10, pad=20)
frame_main.rowconfigure(11, pad=20)


main()