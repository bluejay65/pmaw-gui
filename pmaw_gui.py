import tkinter as tk
import comment_gui, data_gui, submission_gui
from tkinter import ttk



class PmawGUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Reddit Data Collection")
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

        self.root.mainloop()

        #TODO when tab is changed, window size is changed

    def change_window(self, event):
        page = self.notebook.index(self.notebook.select())

        if page == 0:
            self.root.geometry('488x356')
        elif page == 1:
            self.root.geometry('540x759')
        elif page == 2:
            self.root.geometry('1349x759')


gui = PmawGUI()