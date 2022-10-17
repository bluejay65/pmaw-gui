import tkinter as tk
import comment_gui, data_gui, submission_gui
import constants
from tkinter import ttk


class PmawGUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Data Collection for Reddit "+constants.version)
        self.root.columnconfigure(0, weight=100)
        self.root.rowconfigure(0, weight=100)
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(sticky='news')

        self.comment_page = comment_gui.CommentGUI(self.notebook, self.root)
        self.notebook.add(self.comment_page, text='Comments', sticky='news')

        self.submission_page = submission_gui.SubmissionGUI(self.notebook, self.root)
        self.notebook.add(self.submission_page, text='Submissions', sticky='news')

        self.data_page = data_gui.DataGUI(self.notebook, self.root)
        self.notebook.add(self.data_page, text='Data Analysis', sticky='news')

        self.notebook.bind('<<NotebookTabChanged>>', self.change_window)
        self.change_window()

        self.root.mainloop()


    def change_window(self, event=None):
        page = self.notebook.index(self.notebook.select())

        if page == 0:
            self.root.geometry(str(constants.comment_width)+'x'+str(constants.comment_height))
        elif page == 1:
            self.root.geometry(str(constants.submission_width)+'x'+str(constants.submission_height))
        elif page == 2:
            self.root.geometry(str(constants.data_width)+'x'+str(constants.data_height))


gui = PmawGUI()

#TODO have little windows pop up when hovering over something to describe what it does
#TODO have the return fields that don't work with the apis remove when switching, but save their selection (a hide method?)
#TODO fix error when opening files already in use (line 125 in search_pmaw.py)
#TODO allow user to not select a date after putting something in, and to only put a year, or a year and a month