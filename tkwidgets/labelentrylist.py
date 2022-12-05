import tkinter as tk
from tkinter import ttk
import tkwidgets as tkw



# A frame containing a list of LabelEntries
class LabelEntryList(tk.LabelFrame):
    def __init__(self, parent, dictvariable: dict, title: str, tooltip_dict: dict = {}, **kwargs):
        tk.LabelFrame.__init__(self, parent, text=title, **kwargs)
        self.parent = parent

        self.label_entry_dict = {}

        row = 0
        column = 0
        for key, value in dictvariable.items():
            if value == tkw.EntryType.ENTRY:
                widget = tkw.LabelEntry(self, row=row, column=column, text=key)
                self.label_entry_dict[key] = widget

                if(key in tooltip_dict):
                    widget.set_tooltip(tooltip_dict[key])

                row += 1

            elif value == tkw.EntryType.DATE:
                widget = tkw.LabelDate(self, row=row, column=column, text=key)
                self.label_entry_dict[key] = widget

                row += 1

            elif value == tkw.EntryType.DATETIME:
                widget = tkw.LabelDateTime(self, row=row, column=column, text=key, can_clear=True)
                self.label_entry_dict[key] = widget

                row += 2

            elif value == tkw.EntryType.DROPDOWN:
                options = list(key)
                text = options.pop(0)
                widget = tkw.LabelCombobox(self, row=row, column=column, text=text, options=options)
                self.label_entry_dict[text] = widget

                row += 1

            elif value == tkw.EntryType.RANGE:
                widget = tkw.LabelRange(self, row=row, column=column, text=key)
                self.label_entry_dict[key] = widget

                row += 1

            elif value == tkw.EntryType.TIME:
                widget = tkw.LabelTime(self, row=row, column=column, text=key)
                self.label_entry_dict[key] = widget

                row += 1

            elif value == tkw.EntryType.NUMBER:
                widget = tkw.LabelEntry(self, row=row, column=column, text=key, number=True)
                self.label_entry_dict[key] = widget

                if(key in tooltip_dict):
                    widget.set_tooltip(tooltip_dict[key])

                row += 1

            #else:
                #raise Exception('value in dictionary is not a recognized type. The value was: {}'.format(value))

        self.columnconfigure(0, pad=10)
        self.columnconfigure(1, pad=10)


    # Returns the string in the entry corresponding to the label provided
    def get_entry(self, label: str):
        return self.label_entry_dict[label].get_entry()

    # Sets the entry of the label provided
    def set_entry(self, label: str, entry):
        self.label_entry_dict[label].set_entry(entry)
            