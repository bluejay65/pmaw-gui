import tkinter as tk

class Checklist(tk.Frame):
    def __init__(self, parent, listvariable, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.vars = []
        self.checkbuttons = []
        bg = self.cget("background")
        for choice in listvariable:
            var = tk.StringVar(value=choice)
            self.vars.append(var)
            cb = tk.Checkbutton(self, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0
            )
            self.checkbuttons.append(cb)
            cb.pack(side="top", fill="x", anchor="w")


    def get_checked_items(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values

    def select(self, index:int):
        self.checkbuttons[index].select()

    def deselect(self, index:int):
       self.checkbuttons[index].deselect()