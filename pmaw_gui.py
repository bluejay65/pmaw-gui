import tkinter as tk
import comment_gui, data_gui, submission_gui
import constants
import webbrowser
from tkinter import ttk
from search_pmaw import CallPmaw
import sys

sys.path.append('base')


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
        self.page = 1

        self.comment_page = comment_gui.CommentGUI(self.pmaw, self.notebook, self.root)
        text = 'Comments'
        self.notebook.add(self.comment_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.submission_page = submission_gui.SubmissionGUI(self.pmaw, self.notebook, self.root)
        text = 'Submissions'
        self.notebook.add(self.submission_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.data_page = data_gui.DataGUI(self.notebook, self.root)
        text = 'Data Analysis'
        self.notebook.add(self.data_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        label = tk.Label()
        text = 'Guide'
        self.notebook.add(label, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.notebook.bind('<<NotebookTabChanged>>', self.change_window)
        self.change_window()

        self.root.mainloop()


    def change_window(self, event=None):
        last_page = self.page
        self.page = self.notebook.index(self.notebook.select())

        if self.page == 0:
            self.root.geometry(str(constants.COMMENT_WIDTH)+'x'+str(constants.COMMENT_HEIGHT))
        elif self.page == 1:
            self.root.geometry(str(constants.SUBMISSION_WIDTH)+'x'+str(constants.SUBMISSION_HEIGHT))
        elif self.page == 2:
            self.root.geometry(str(constants.DATA_WIDTH)+'x'+str(constants.DATA_HEIGHT))
        elif self.page == 3:
            self.notebook.select(last_page)
            webbrowser.open_new_tab(constants.GUIDE_URL)


gui = PmawGUI()

#TODO work with different OS (test)
#TODO make tooltips for data analysis
#TODO have the return fields that don't work with the apis remove when switching, but save their selection (a hide method?)
#TODO let user clear date
#TODO save recent searches and let them fill them back in
#TODO visualization