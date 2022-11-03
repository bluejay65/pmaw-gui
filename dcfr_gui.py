import tkinter as tk
import comment_gui, data_gui, submission_gui, output_gui
import constants
import webbrowser
from tkinter import ttk
from search_pmaw import CallPmaw
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.append('base')


class DcfrGUI():
    def __init__(self) -> None:
        #with ThreadPoolExecutor(max_workers=10) as executor:
        executor = None
        self.root = tk.Tk()
        self.root.title(constants.APP_NAME+" "+constants.VERSION)
        self.root.columnconfigure(0, weight=100)
        self.root.rowconfigure(0, weight=100)
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(sticky='news')
        self.page = 1

        self.output_page = output_gui.OutputGUI(self.notebook, self.root)
        self.pmaw = CallPmaw(self.output_page)

        self.comment_page = comment_gui.CommentGUI(self.pmaw, self.notebook, self.root, executor=executor)
        text = 'Comments'
        self.notebook.add(self.comment_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.submission_page = submission_gui.SubmissionGUI(self.pmaw, self.notebook, self.root, executor=executor)
        text = 'Submissions'
        self.notebook.add(self.submission_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.data_page = data_gui.DataGUI(self.notebook, self.root, executor=executor)
        text = 'Data Analysis'
        self.notebook.add(self.data_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        text = 'Output'
        self.notebook.add(self.output_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        label = tk.Label()
        text = 'Guide'
        self.notebook.add(label, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

        self.notebook.bind('<<NotebookTabChanged>>', self.change_window)
        self.change_window()

        self.root.mainloop()


    def change_window(self, event=None):
        last_page = self.page
        self.page = self.notebook.index(self.notebook.select())

        if self.page == constants.NotebookPage.COMMENT_PAGE.value:
            self.root.geometry(str(constants.COMMENT_WIDTH)+'x'+str(constants.COMMENT_HEIGHT))
        elif self.page == constants.NotebookPage.SUBMISSION_PAGE.value:
            self.root.geometry(str(constants.SUBMISSION_WIDTH)+'x'+str(constants.SUBMISSION_HEIGHT))
        elif self.page == constants.NotebookPage.DATA_PAGE.value:
            self.root.geometry(str(constants.DATA_WIDTH)+'x'+str(constants.DATA_HEIGHT))
        elif self.page == constants.NotebookPage.OUTPUT_PAGE.value:
            self.root.geometry(str(constants.COMMENT_WIDTH)+'x'+str(constants.COMMENT_HEIGHT))
        elif self.page == constants.NotebookPage.GUIDE_PAGE.value:
            self.notebook.select(last_page)
            webbrowser.open_new_tab(constants.GUIDE_URL)


gui = DcfrGUI()


#TODO search filters too specific versus no data available in time frame
#TODO explain results remaining
#TODO fix data errors, (not using error with gini)
#TODO add select all button for return fields
#TODO work with different OS (test)
#TODO let user clear date
#TODO save recent searches and let them fill them back in
#TODO visualization
