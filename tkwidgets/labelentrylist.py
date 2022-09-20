import tkinter as tk
import tkwidgets as tkw



# A frame containing a list of LabelEntries
class LabelEntryList(tk.Frame):
    def __init__(self, parent, dictvariable: dict, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.label_entry_dict = {}

        row = 0
        for key, value in dictvariable.items():
            if value == tkw.EntryType.ENTRY:
                label_entry = tkw.LabelEntry(self, row=row, column=0, text=key)
                self.label_entry_dict[key] = label_entry

                row += 1

            elif value == tkw.EntryType.DATE:
                label_date = tkw.LabelDate(self, row=row, column=0, text=key)
                self.label_entry_dict[key] = label_date

                row += 1

            elif value == tkw.EntryType.DATETIME:
                label_datetime = tkw.LabelDateTime(self, row=row, column=0, text=key)
                self.label_entry_dict[key] = label_datetime

                row += 2

            elif value == tkw.EntryType.DROPDOWN:
                options = list(key)
                text = options.pop(0)
                label_dropdown = tkw.LabelCombobox(self, row=row, column=0, text=text, options=options)
                self.label_entry_dict[text] = label_dropdown

                row += 1

            elif value == tkw.EntryType.RANGE:
                label_range = tkw.LabelRange(self, row=row, column=0, text=key)
                self.label_entry_dict[key] = label_range

                row += 1

            elif value == tkw.EntryType.TIME:
                label_time = tkw.LabelTime(self, row=row, column=0, text=key)
                self.label_entry_dict[key] = label_time

                row += 1

        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)

    # Returns the string in the entry corresponding to the label provided
    def get_entry(self, label: str):
        return self.label_entry_dict[label].get_entry()

    # Sets the entry of the label provided
    def set_entry(self, label: str, entry):
        self.label_entry_dict[label].set_entry(entry)