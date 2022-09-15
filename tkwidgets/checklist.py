import tkinter as tk


# A list of checkbuttons that can be selected and deselected by code or user
class Checklist(tk.Frame):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, scrollbar: bool = False, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)

        self.vars = []
        self.checkbuttons = []
        bg = self.cget("background")

        for choice in listvariable:
            var = tk.StringVar(value=choice)
            self.vars.append(var)
            cb = tk.Checkbutton(self.frame, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0
            )
            cb.grid(row=len(self.checkbuttons), column=0, sticky='w')
            self.checkbuttons.append(cb)

        if scrollbar:
            self.scrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.scrollbar.pack(side='right', fill='y')
            self.frame.bind("<Configure>", self.onFrameConfigure)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')


    # Returns a list of the values of the checked buttons
    def get_checked_items(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values

    # Selects a button based on index
    def select(self, index:int):
        self.checkbuttons[index].select()

    # Deselects a buttons based on index
    def deselect(self, index:int):
       self.checkbuttons[index].deselect()

    # Selects the buttons in index_list, and deselects buttons not in index_lsit
    def check_items(self, index_list):
        for i in range(len(self.checkbuttons)):
            if i in index_list:
                self.checkbuttons[i].select()
            else:
                self.checkbuttons[i].deselect()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))