import tkinter as tk
import comment_gui, data_gui, submission_gui
from tkinter import ttk



class PmawGUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Reddit Data Collection")
        self.root.columnconfigure(0, weight=100)
        self.root.rowconfigure(0, weight=100)
        self.root.resizable(True, True)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(sticky='news')

        self.comment_page = comment_gui.CommentGUI(self.notebook, self.root)
        self.notebook.add(self.comment_page, text='Comments', sticky='news')

        self.submission_page = submission_gui.SubmissionGUI(self.notebook, self.root)
        self.notebook.add(self.submission_page, text='Submissions', sticky='news')

        self.data_page = data_gui.DataGUI(self.notebook, self.root)
        self.notebook.add(self.data_page, text='Data Analysis', sticky='news')

        self.root.mainloop()

        #TODO when tab is changed, window size is changed


gui = PmawGUI()