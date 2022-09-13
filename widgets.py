import tkinter as tk


# A list of checkbuttons that can be selected and deselected by code or user
class Checklist(tk.Frame):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, **kwargs):
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



# A frame with two widgets, a label and an entry
class LabelEntry(tk.Frame):
    def __init__(self, parent, text: str, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.entry_str = tk.StringVar()

        self.label = tk.Label(self, text=text)
        self.entry = tk.Entry(self, textvariable=self.entry_str)

        self.label.grid(row=0, column=0, sticky='w')
        self.entry.grid(row=0, column=1)

    # Returns the string in the entry
    def get_entry(self):
        return self.entry_str.get()

    # Sets the entry to entry
    def set_entry(self, entry):
        self.entry_str.set(entry)


# A frame containing a list of LabelEntries
class LabelEntryList(tk.Frame):
    def __init__(self, parent, listvariable: list, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label_entry_dict = {}

        for i in range(len(listvariable)):
            label_entry = LabelEntry(self, text=listvariable[i])
            self.label_entry_dict[listvariable[i]] = label_entry

            label_entry.grid(row=0, column=i)

    # Returns the string in the entry corresponding to the label provided
    def get_entry(self, label: str):
        return self.label_entry_dict[label].get_entry()

    # Sets the entry of the label provided
    def set_entry(self, label: str, entry: str):
        self.label_entry_dict[label].set_entry(entry)
