import base64
import json
import os
import importlib

from typing import Optional

from tornado.web import RequestHandler, HTTPError

from .notebook_runner import NotebookRunner
from .util import get_config

class NotebookRunnerHandler(RequestHandler):
    def get(self, path):
        try:
            nr = NotebookRunner(path)
        except FileNotFoundError:
            raise HTTPError(404, path + " not found.")

        cell = self._int_argument('cell')
        cell_results = nr.run_until(cell)

        nr.shutdown()

        if cell is not None and cell >= 0 and cell < len(cell_results):
            self._write_cell(cell_results[cell])
        else:
            self.write({
                'data': cell_results
            })

    def on_finish(self):
        print(end='', flush=True)

    def _write_cell(self, cell, prefer=None):
        self.set_header('Access-Control-Allow-Origin', '*')
        
        if 'display' in cell or 'result' in cell:
            if 'display' in cell:
                data = cell['display']['data']
            else:
                data = cell['result']['data']

            if 'image/png' in data:
                img = data['image/png']

                self.set_header('Content-Type', 'image/png')
                self.write(base64.b64decode(img))
            if 'application/json' in data:
                self.set_header('Content-Type', 'application/json')
                self.write(data['application/json'])
            elif 'text/html' in data:
                #  TODO Render in html-page
                self.set_header('Content-Type', 'text/html')
                self.write('<html><body>' + data['text/html'] + '</body></html>')
            elif 'text/markdown' in data:
                #  TODO Render markdown (maybe)
                self.set_header('Content-Type', 'text/markdown')
                self.write(data['text/markdown'])
            elif 'text/plain' in data:
                self.set_header('Content-Type', 'text/plain')
                self.write(data['text/plain'])
            else:
                self.write('ERROR, found no renderable text.')

        elif 'stderr' in cell:
            self.write(cell['stderr'])

        elif 'stdout' in cell:
            self.write(cell['stdout'])

        elif 'error' in cell:
            self.write(cell['error'])

        else:
            self.set_status(201)

    def _int_argument(self, name, default=None) -> Optional[int]:
        try:
            return int(self.get_argument(name, default))
        except (ValueError, TypeError):
            return default


class MainHandler(NotebookRunnerHandler):
    def _get_inspector(self, kernel, config):
        try:
            inspector_module = importlib.import_module(
                f'.inspection.{kernel}', package="disjotter")

            return inspector_module.inspector()
        except ModuleNotFoundError:
            return None

    def post(self):
        return self.get()

    def get(self):
        config = get_config()

        idx = config['index']

        try:
            nr = NotebookRunner(config['path'])
        except FileNotFoundError:
            raise HTTPError(404, config['path'] + " not found.")

        runner = self._get_inspector(nr.kernel_name, config)

        if runner:
            nr.set_run_before(idx, runner.run_pre_cell(config, self))

        cell_results = nr.run_until(idx)

        nr.shutdown()

        self._write_cell(cell_results[idx])
