import sys
from gui.output_gui import OutputGUI


class PMAWOutput():
    def __init__(self, output: OutputGUI):
        self.output = output

    def cancel_is_set(self):
        return self.output.cancel_task

    def output_shards(self, available_shards, total_shards):
        self.output.set_shards(available_shards, total_shards)

    def output_progress(self, remaining, possible_results):
        print(f'{remaining < sys.maxsize and possible_results > 0}: {remaining}/{possible_results}')
        if remaining < sys.maxsize and possible_results > 0:
            self.output.set_remaining(remaining)
            self.output.update_progress_bar(remaining, possible_results)

    def output_final(self):
        if self.limit < 0:
            self.output.set_successful(len(self.req.resp), self.possible_results)
        else:
            self.output.set_successful(len(self.req.resp), self.limit)

    def output_error(self, error_msg):
        self.output.send_error(error_msg)