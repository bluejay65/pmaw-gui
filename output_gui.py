import tkinter as tk
from tkinter import ttk
from base_gui import BaseGUI
from tkwidgets import VerticalScrolledFrame


class OutputGUI(BaseGUI):

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.label_frame = tk.LabelFrame(self, text='Waiting for Process', labelanchor='n')
        self.label_frame.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.frame = VerticalScrolledFrame(self.label_frame, height=200)
        self.edit_frame = self.frame.interior
        self.frame.grid()

        self.text = tk.StringVar()
        self.output = tk.Label(self.edit_frame, textvariable=self.text, wraplength=510, width=72, justify=tk.LEFT, anchor='nw')
        self.output.grid()

        self.shard_text = tk.StringVar()
        self.shard_value_text = tk.StringVar()
        self.shard_text_label = tk.Label(self, textvariable=self.shard_text)
        self.shard_value_label = tk.Label(self, textvariable=self.shard_value_text)
        self.shard_text_label.grid(row=1, column=0, stick='e')
        self.shard_value_label.grid(row=1, column=1, sticky='w')

        self.progress_bar = ttk.Progressbar(self, orient='horizontal', length=510, mode='indeterminate')
        self.progress_bar.grid(row=2, column=0, columnspan=2)
        self.progress_bar.grid_remove()
        self.progress_made = 0

    def update_title(self, text:str):
        self.label_frame['text'] = text

    def append(self, line:str):
        if self.text.get() == '':
            self.text.set(line)
        else:
            self.text.set(self.text.get()+'\n'+line)

    def new_append(self, line:str):
        if self.text.get() == '':
            self.text.set(line)
        else:
            self.text.set(self.text.get()+'\n\n'+line)

    def clear_text(self):
        self.text.set('')

    def set_shards(self, available:int, total:int):
        self.shard_text.set('Shards Online:')
        if available < total:
            self.shard_value_label.config(fg='red')
        else:
            self.shard_value_label.config(fg='green')
        self.shard_value_text.set(f'{available}/{total}')

    def start_progress_bar(self):
        self.progress_bar.grid()
        self.progress_bar.start()

    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        self.progress_made = 0

    def update_progress_bar(self, remaining, largest_remaining):
        self.progress_bar.config(mode='determinate')
        step = (largest_remaining - remaining) / (largest_remaining * 100) - self.progress_made
        self.progress_made += step
        self.progress_bar.step(step)
