import tkinter as tk
import constants
from tkinter import ttk, font, messagebox
from base_gui import BaseGUI
from tkwidgets import HorizontalScrolledFrame, Console


class OutputGUI(BaseGUI):

    width = constants.OUTPUT_WIDTH
    height = constants.OUTPUT_HEIGHT

    msg_height = constants.OUTPUT_HEIGHT + 40

    cancel_task = False

    def __init__(self, parent, root, resource_manager, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.root = root
        self.parent = parent
        self.resource_manager = resource_manager

        self.label_frame = tk.LabelFrame(self, text='Waiting for Process', labelanchor='n')
        self.label_frame.grid(row=0, column=0, padx=5, pady=5, sticky='news')

        self.cancel_img = self.resource_manager.load_image('x.png', size=(10,10))
        self.cancel_button = tk.Button(self, command=self.cancel_download, relief=tk.FLAT, image=self.cancel_img, bd=0, takefocus=False)

        self.progress_bar = ttk.Progressbar(self.label_frame, orient='horizontal', mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky='new', padx=10, pady=(10,0), columnspan=2)
        self.progress_bar.grid_remove()
        self.progress_made = 0

        self.remaining_text = tk.StringVar()
        self.remaining_text_label = tk.Label(self.label_frame, textvariable=self.remaining_text)
        self.remaining_text_label.grid(row=1, column=0, sticky='new', columnspan=2)

        self.shard_frame = tk.Frame(self.label_frame)
        self.shard_text = tk.StringVar()
        self.shard_values = {}
        self.shard_text_label = tk.Label(self.shard_frame, textvariable=self.shard_text)
        self.shard_frame.grid(row=2, column=0, sticky='sw')
        self.shard_text_label.grid(row=0, column=0)

        self.wheel = Console(self.label_frame, width=10, height=1, bg=self.root.cget('bg'), relief=tk.FLAT, font=font.nametofont("TkDefaultFont"))
        self.wheel.grid(row=2, column=1, sticky='se')

        self.label_frame.grid_rowconfigure(2, weight=1)
        self.label_frame.grid_columnconfigure(0, weight=5)

        self.msg_frame = tk.LabelFrame(self)
        self.msg_scroll_frame = HorizontalScrolledFrame(self.msg_frame, width=self.width-30)
        self.msg_text = tk.Text(self.msg_scroll_frame.interior, bg=self.root.cget('bg'), relief=tk.FLAT, font=font.nametofont("TkDefaultFont"), height=1, state='disabled')
        self.msg_frame.grid(row=1, column=0, sticky='sew', padx=5, pady=5)
        self.msg_scroll_frame.grid(row=0, column=0, sticky='news', padx=5)
        self.msg_text.grid(row=0, column=0)
        self.msg_frame.grid_remove()

        self.columnconfigure(0, weight=5)
        self.rowconfigure(0, weight=10000)
        self.rowconfigure(1, weight=1)


    
    def cancel_download(self):
        if messagebox.askyesno(title='Cancel Download', message='Are you sure you want to cancel the download? You will lose all the data downloaded so far'):
            self.cancel_task = True
            self.wheel.start_wheel('Closing   ')
            self.set_title('Cancelling Download')


    def show_cancel_button(self):
        self.cancel_button.place(height=10, width=10, bordermode=tk.INSIDE, relx=0.977, rely=0.01)


    def set_title(self, text:str):
        self.label_frame['text'] = text


    def reset(self):
        self.cancel_task = False
        self.clear_msg()
        self.clear_shards()
        self.stop_progress_bar()
        self.set_title('Waiting for Process')
        self.progress_bar.grid_remove()
        self.msg_frame.grid_remove()
        self.set_geometry(constants.OUTPUT_WIDTH, constants.OUTPUT_HEIGHT) 


    def set_save_file(self, save_file:str):
        self.set_geometry(constants.OUTPUT_WIDTH, self.msg_height)
        self.msg_text.config(width=len(save_file)+10, state='normal', fg='black')
        self.msg_text.replace(1.0, tk.END, f'Saved to: {save_file}')
        self.msg_text.config(state='disabled')
        self.msg_frame.grid()
        self.cancel_button.place_forget()


    def send_error(self, msg:str):
        self.set_geometry(constants.OUTPUT_WIDTH, self.msg_height)
        self.msg_text.config(fg='red', width=len(msg), state='normal')
        self.msg_text.replace(1.0, tk.END, '')
        self.msg_text.insert(tk.END, msg)
        self.msg_text.config(state='disabled')
        self.msg_frame.grid()
        self.wheel.clear_wheel()
        self.cancel_button.place_forget()

    
    def clear_msg(self):
        self.msg_text.delete(1.0, tk.END)
        self.msg_text.config(fg='black')
        self.msg_frame.grid_remove()
        self.set_geometry(constants.OUTPUT_WIDTH, constants.OUTPUT_HEIGHT)


    def set_remaining(self, remaining:int):
        self.remaining_text.set(f'Remaining: {remaining}')


    def set_geometry(self, width, height):
        self.width = width
        self.height = height
        self.msg_frame['width'] = width
        if self.parent.index(self.parent.select()) == constants.NotebookPage.OUTPUT_PAGE.value:
            self.root.geometry(str(width)+'x'+str(height))

    
    def set_successful(self, returned:int, expected:int):
        if returned >= expected:
            self.remaining_text.set(f'{returned} results returned')
        else:
            self.remaining_text.set(f'{expected - returned}/{expected} results missing')
        self.wheel.clear_wheel()
        self.cancel_button.place_forget()
        self.fill_progress_bar()



    def set_shards(self, available:int, total:int):
        shard_str = f'{available}/{total}'
        num_shards = len(self.shard_values)

        if shard_str not in [key for key in self.shard_values.keys()]:
            if num_shards <= 0:
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

    
    def clear_shards(self):
        for value in self.shard_values.values():
            value.grid_forget()
        self.shard_values = {}
        self.shard_text.set('')


    def start_progress_bar(self):
        self.show_cancel_button()
        self.progress_bar.grid()
        self.progress_bar.start()
        self.wheel.start_wheel('Running   ')
        self.progress_bar.configure(mode='indeterminate')
        self.progress_made = 0


    def stop_progress_bar(self):
        self.progress_bar.stop()
        self.wheel.clear_wheel()


    def update_progress_bar(self, remaining, largest_remaining):
        mode = str(self.progress_bar.cget('mode'))
        if mode == 'indeterminate':
            self.progress_bar.config(mode='determinate')
            self.progress_bar.stop()
        if largest_remaining == remaining:
            self.progress_bar['value'] = 100
        else:
            self.progress_bar['value'] = ((largest_remaining - remaining) / largest_remaining) * 100

    
    def fill_progress_bar(self):
        mode = str(self.progress_bar.cget('mode'))
        if mode == 'indeterminate':
            self.progress_bar.config(mode='determinate')
            self.progress_bar.stop()
        self.progress_bar['value'] = 100

