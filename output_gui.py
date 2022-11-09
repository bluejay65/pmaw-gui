import tkinter as tk
from tkinter import ttk
from base_gui import BaseGUI
from tkwidgets import VerticalScrolledFrame


class OutputGUI(BaseGUI):

    def __init__(self, parent, root, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root

        self.label_frame = tk.LabelFrame(self, text='Waiting for Process', labelanchor='n')
        self.label_frame.grid(row=0, column=0, padx=5, pady=5, sticky='news')

        self.remaining_text = tk.StringVar()
        self.remaining_text_label = tk.Label(self.label_frame, textvariable=self.remaining_text)
        self.remaining_text_label.grid(row=0, column=0)

        self.progress_bar = ttk.Progressbar(self.label_frame, orient='horizontal', length=510, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0)
        self.progress_bar.grid_remove()
        self.progress_made = 0

        self.shard_frame = tk.Frame(self.label_frame)
        self.shard_text = tk.StringVar()
        self.shard_values = {}
        self.shard_text_label = tk.Label(self.shard_frame, textvariable=self.shard_text)
        self.shard_frame.grid(row=2, column=0)
        self.shard_text_label.grid(row=0, column=0)
        self.shard_text_label.grid_remove()

        self.scroll_frame = VerticalScrolledFrame(self.label_frame, height=200)
        self.scroll_frame.grid(row=3, column=0, sticky='sew')

        self.text = tk.StringVar()
        self.output = tk.Label(self.scroll_frame.interior, textvariable=self.text, wraplength=510, width=72, justify=tk.LEFT, anchor='nw')
        self.output.grid()


    def set_title(self, text:str):
        self.label_frame['text'] = text


    def set_remaining(self, remaining:int):
        self.remaining_text.set(f'Remaining: {remaining}')


    def set_shards(self, available:int, total:int):
        shard_str = f'{available}/{total}'
        num_shards = len(self.shard_values)

        if shard_str not in [key for key in self.shard_values.keys()]:
            if num_shards <= 0:
                print('add title')
                self.shard_text.set('Shards Online:')
                self.shard_text_label.grid()
            else:
                last_label = self.shard_values[next(reversed(self.shard_values))]
                last_label.configure(text=f'{last_label.cget("text")},')

            shard_label = tk.Label(self.shard_frame, text=shard_str)
            self.shard_values[shard_str] = shard_label

            if available < total:
                shard_label.config(fg='red')
            else:
                shard_label.config(fg='green')

            shard_label.grid(row=0, column=1+num_shards)


    def start_progress_bar(self):
        self.progress_bar.grid()
        self.progress_bar.start()
        self.progress_bar.configure(mode='indeterminate')


    def stop_progress_bar(self):
        self.progress_bar.stop()


    def update_progress_bar(self, remaining, largest_remaining):
        mode = str(self.progress_bar.cget('mode'))
        if mode == 'indeterminate':
            self.progress_bar.config(mode='determinate')
            self.progress_bar.stop()
            self.progress_made = 0
        step = ((largest_remaining - remaining) / largest_remaining) * 100 - self.progress_made
        self.progress_made += step
        self.progress_bar.step(step)


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
