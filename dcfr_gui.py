import tkinter as tk
import comment_gui, data_gui, submission_gui, output_gui
import constants
import webbrowser
from resource_manager import ResourceManager
from app_info import AppInfo
from tkinter import ttk
from search_pmaw import CallPmaw
import sys
import signal
from threading import Event
from concurrent.futures import ThreadPoolExecutor
import logging

sys.path.append('base')
AppInfo.configure_log()
logging.basicConfig(filename=AppInfo.get_log_path(), level=logging.INFO)
logging.info('Opened %s %s on %s', constants.APP_NAME, constants.VERSION, sys.platform)

log = logging.getLogger(__name__)


class DcfrGUI():
    def __init__(self) -> None:
        self.exit = Event()
        self.setup_sigs()
        self.resource_manager = ResourceManager(AppInfo.get_resource_folder())

        with ThreadPoolExecutor(max_workers=10) as self.executor:
            self.root = tk.Tk()
            self.root.title(constants.APP_NAME+" "+constants.VERSION)
            self.root.columnconfigure(0, weight=100)
            self.root.rowconfigure(0, weight=100)
            self.root.resizable(False, False)

            self.notebook = ttk.Notebook(self.root)
            self.notebook.grid(sticky='news')
            self.page = 1

            self.output_page = output_gui.OutputGUI(self.notebook, self.root, self.resource_manager)
            self.pmaw = CallPmaw(gui=self, output=self.output_page, executor=self.executor, main_thread=self)

            self.comment_page = comment_gui.CommentGUI(self.pmaw, self.notebook, self.root, executor=self.executor)
            text = 'Comments'
            self.notebook.add(self.comment_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

            self.submission_page = submission_gui.SubmissionGUI(self.pmaw, self.notebook, self.root, executor=self.executor)
            text = 'Submissions'
            self.notebook.add(self.submission_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

            self.data_page = data_gui.DataGUI(self.notebook, self.root, executor=self.executor, output=self.output_page)
            text = 'Data Analysis'
            self.notebook.add(self.data_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

            text = 'Output'
            self.notebook.add(self.output_page, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

            label = tk.Label()
            text = 'Guide'
            self.notebook.add(label, text=text.center(constants.NOTEBOOK_WRAP), sticky='news')

            self.notebook.bind('<<NotebookTabChanged>>', self.change_window)
            self.change_window()

            self.root.mainloop()


    def change_window(self, event=None):
        last_page = self.page
        self.page = self.notebook.index(self.notebook.select())

        if self.page == constants.NotebookPage.COMMENT_PAGE.value:
            self.root.geometry(str(constants.COMMENT_WIDTH)+'x'+str(constants.COMMENT_HEIGHT))
        elif self.page == constants.NotebookPage.SUBMISSION_PAGE.value:
            self.root.geometry(str(constants.SUBMISSION_WIDTH)+'x'+str(constants.SUBMISSION_HEIGHT))
        elif self.page == constants.NotebookPage.DATA_PAGE.value:
            self.root.geometry(str(self.data_page.width)+'x'+str(self.data_page.height))
        elif self.page == constants.NotebookPage.OUTPUT_PAGE.value:
            self.root.geometry(str(self.output_page.width)+'x'+str(self.output_page.height))
        elif self.page == constants.NotebookPage.GUIDE_PAGE.value:
            self.notebook.select(last_page)
            webbrowser.open_new_tab(constants.GUIDE_URL)


    def setup_sigs(self):
        try:
            getattr(signal, 'SIGHUP')
            sigs = ('TERM', 'HUP', 'INT')
        except AttributeError:
            sigs = ('TERM', 'INT')

        for sig in sigs:
            signal.signal(getattr(signal, 'SIG'+sig), self.set_exit)

    def set_exit(self, *args):
        self.exit.set()
        self.executor.shutdown(wait=False, cancel_futures=True)

    def disable_run(self):
        self.comment_page.disable_run()
        self.submission_page.disable_run()

    def enable_run(self):
        self.comment_page.enable_run()
        self.submission_page.enable_run()

try:
    gui = DcfrGUI()
except:
    log.critical(constants.CRITICAL_MESSAGE, exc_info=True)


#TODO guide crashes if not connected to internet
#TODO if file is open save to another file
#TODO save recent searches and let user fill them back in
#TODO make sure pngs work even if not connected to internet (have alternatives)
#TODO get signal working (test with linux)
#TODO work with different OS (test)
#TODO change name
#TODO design and add icon
#TODO add more lines to output text


#TODO fix typing in time
#TODO visualization
#TODO search filters too specific versus no data available in time frame (have search of just the before and after, see what happens)
#TODO move everything that has to do with editing file names to its own file

#reddit data collection and analysis tool (redcat)
