import tkinter as tk
import tkwidgets as tkw


# A list of checkbuttons that can be selected and deselected by code or user
class ButtonList(tk.LabelFrame):

    # Creates the checkbuttons from listvariable and adds them to the frame
    def __init__(self, parent, listvariable: list, height:int = None, title: str = None, scrollbar: bool = False, tooltip_dict: dict = {},
        command: str = None,
        relief=tk.RAISED,
        take_focus:bool = True,
        stay_active:bool = False,
        active_relief = None,
        **kwargs):
        
        tk.LabelFrame.__init__(self, parent, text=title, **kwargs)

        self.command = command
        self.parent = parent
        self.relief = relief
        self.take_focus = take_focus
        self.stay_active = stay_active
        self.active_relief = active_relief

        if scrollbar:
            self.frame = tkw.VerticalScrolledFrame(self, height=height)
            self.edit_frame = self.frame.interior
        else:
            self.frame = self.edit_frame = tk.Frame(self, height=height)

        self.frame.grid(row=0, column=0, sticky='news')
        self.grid_columnconfigure(0, weight=1)
        self.buttons = {}
        self.tooltips = {}

        self.add_items(listvariable, tooltip_dict)

        self.active_button = None


    def add_items(self, items: list, tooltips: dict):
        for i in items:
            btn = tk.Button(self.edit_frame, text=i, anchor="w", relief=self.relief, takefocus=self.take_focus)

            if self.command:
                btn['command'] = (lambda parent=self.parent, command=self.command, button=btn: self.run_command(parent, command, button))

            if tooltips != {}:
                self.tooltips[i] = tkw.ToolTip(btn, tooltips[i])

            btn.grid(row=len(self.buttons), column=0, sticky='w', pady=(2), padx=4)
            self.buttons[i] = btn

    def remove_items(self, items: list):
        for i in items:
            if i in self.buttons.keys():
                self.buttons[i].grid_forget()
                self.buttons.pop(i)

    def remove_all_items(self):
        for i in self.buttons.keys():
            i.grid_forget()
        self.buttons = {}

    # Selects a button
    def select(self, item:str):
        self.buttons[item].invoke()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run_command(self, parent, command, button):
        if self.take_focus:
            button.focus_set()
        if self.stay_active and self.active_relief != None:
            if self.active_button != None:
                self.active_button.configure(relief=self.relief)
            button.configure(relief=self.active_relief)
            self.active_button = button
        func = getattr(parent, command)
        func(button['text'])