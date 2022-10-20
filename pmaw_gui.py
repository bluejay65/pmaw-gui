import tkinter as tk
import comment_gui, data_gui, submission_gui
import constants
from tkinter import ttk
from search_pmaw import CallPmaw


class PmawGUI():
    def __init__(self) -> None:
        self.pmaw = CallPmaw()

        self.root = tk.Tk()
        self.root.title(constants.APP_NAME+" "+constants.VERSION)
        self.root.columnconfigure(0, weight=100)
        self.root.rowconfigure(0, weight=100)
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(sticky='news')

        self.comment_page = comment_gui.CommentGUI(self.pmaw, self.notebook, self.root)
        self.notebook.add(self.comment_page, text='Comments', sticky='news')

        self.submission_page = submission_gui.SubmissionGUI(self.pmaw, self.notebook, self.root)
        self.notebook.add(self.submission_page, text='Submissions', sticky='news')

        self.data_page = data_gui.DataGUI(self.notebook, self.root)
        self.notebook.add(self.data_page, text='Data Analysis', sticky='news')

        self.notebook.bind('<<NotebookTabChanged>>', self.change_window)
        self.change_window()

        self.root.mainloop()


    def change_window(self, event=None):
        page = self.notebook.index(self.notebook.select())

        if page == 0:
            self.root.geometry(str(constants.COMMENT_WIDTH)+'x'+str(constants.COMMENT_HEIGHT))
        elif page == 1:
            self.root.geometry(str(constants.SUBMISSION_WIDTH)+'x'+str(constants.SUBMISSION_HEIGHT))
        elif page == 2:
            self.root.geometry(str(constants.DATA_WIDTH)+'x'+str(constants.DATA_HEIGHT))


gui = PmawGUI()

#TODO check what pmaw_search returns when filters return nothing
#TODO work with different OS
#TODO have little windows pop up when hovering over something to describe what it does
#TODO have the return fields that don't work with the apis remove when switching, but save their selection (a hide method?)
#TODO fix error when opening files already in use (line 125 in search_pmaw.py)
#TODO have date fill itself in after user picks anything, also let user clear date
#TODO save recent searches and let them fill them back in
#TODO visualization