import tkinter as tk
import comment_gui
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

        self.notebook.add(self.comment_page, text='Comments')

        self.root.mainloop()


gui = PmawGUI()