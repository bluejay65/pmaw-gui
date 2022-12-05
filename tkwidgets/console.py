import tkinter as tk
import queue


class Console(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master)
        self.text = tk.Text(self, wrap='word', **kwargs)
        self.text.pack()
        self.text.config(state='disabled')
        self.sequence = ['-', '\\', '|', '/']
        self.load = False
        self.queue = queue.Queue()
        self.update_me()
    def write(self, line, link=None):
        self.queue.put((line,link))
    def clear(self):
        self.queue.put((None, None))
    def update_me(self):
        try:
            while 1:
                line, link = self.queue.get_nowait()

                self.text.config(state='normal')
                if line is None:
                    self.text.delete(1.0, tk.END)
                elif link and link == 'loader':
                    self.load = True
                    self.text.delete(self.text.index("end-2c"))
                    self.text.insert(self.text.index("end-1c"), str(line))
                else:
                    if self.load:
                        self.text.delete(self.text.index("end-2c"))
                        self.text.insert(self.text.index("end-1c"), str(line))
                    else:
                        self.text.insert(tk.END, str(line))
                    self.load = False
                self.text.see(tk.END)
                self.update_idletasks()
                self.text.config(state='disabled')
        except queue.Empty:
            pass
        self.after(100, self.update_me)
        if self.load:
            self.queue.put((self.sequence[0], 'loader'))
            self.sequence.append(self.sequence.pop(0))

    def start_wheel(self, msg=''):
        self.write(msg, 'loader')

    def clear_wheel(self):
        self.write('')
        self.clear()