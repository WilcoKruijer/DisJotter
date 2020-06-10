import json

from typing import List
from queue import Empty

from jupyter_client import manager as kernel_manager, kernelspec


class NotebookRunner:
    def __init__(self, notebook_path):
        self.path = notebook_path

        with open(notebook_path, 'r') as notebook_file:
            self.json = json.load(notebook_file)

            self.kernel_name = self.json['metadata']['kernelspec']['name']
            self.cells = self.json['cells']

        # Might raise kernelspec.NoSuchKernel
        m, c = kernel_manager.start_new_kernel(kernel_name=self.kernel_name)

        self.manager = m
        self.client = c

        self.run_before = {}

    def set_run_before(self, cell_idx, source):
        self.run_before[cell_idx] = source

    def shutdown(self):
        self.client.shutdown()

    def execute_code_and_wait(self, command):
        cmd_id = self.client.execute(command)

        state = 'busy'
        ret_content = {}

        #  TODO this only returns the last message of one type. I.e. when a
        #  a cell draws multiple images only the last one will be sent.

        while state != 'idle':
            try:
                msg = self.client.get_iopub_msg(timeout=10)

                if msg['parent_header']['msg_id'] != cmd_id:
                    continue

                if not 'content' in msg: 
                    continue

                msg_type = msg['msg_type']

                if msg_type == 'status':
                    state = msg['content']['execution_state']

                if state == 'idle':
                    break

                content = msg['content']
                if msg_type == "stream":
                    ret_content[content['name']] = content['text']
                elif msg_type == 'execute_result':
                    ret_content['result'] = content
                elif msg_type == 'display_data':
                    ret_content['display'] = content
                elif msg_type == 'error':
                    ret_content['error'] = content
            except Empty:
                return {}

        return ret_content

    def run(self):
        self.run_until()

    def run_until(self, until_cell_idx=None) -> List[any]:
        results = []
        for idx, cell in enumerate(self.cells):
            if cell['cell_type'] == 'code':
                if idx in self.run_before:
                    self.execute_code_and_wait(self.run_before[idx])

                res = self.execute_code_and_wait("".join(cell['source']))
                results.append(res)
            else:
                results.append({})

            if idx == until_cell_idx:
                break

        return results
