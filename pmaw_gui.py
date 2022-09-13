import tkinter as tk



class PmawGUI():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Reddit Data Collection")
        self.root.columnconfigure(0, weight=100)
        self.root.rowconfigure(0, weight=100)
        self.root.resizable(False, False)

        self.frame_main = tk.Frame(self.root, padx=20)
        self.frame_main.grid(sticky='news')



        self.root.mainloop()