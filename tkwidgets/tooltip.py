import tkinter as tk


class ToolTip:
    def __init__(self, widget, text: str=None, delay=0):

        def on_enter(event):
            self.tooltip=tk.Toplevel(bd=1, bg='#000000')
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')

            self.label=tk.Label(self.tooltip, text=self.text, bg='#FFFFFF')
            self.label.pack()

        def on_leave(event):
            self.tooltip.destroy()

        self.widget=widget
        self.text=text

        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Leave>',on_leave)

    def set_text(self, text):
        self.text = text