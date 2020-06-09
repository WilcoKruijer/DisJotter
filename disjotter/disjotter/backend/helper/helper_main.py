# import io, os, sys, types

# from IPython import get_ipython
# from nbformat import read
# from IPython.core.interactiveshell import InteractiveShell

# class NotebookLoader(object):
#     """Module Loader for Jupyter Notebooks"""
#     def __init__(self, path=None):
#         self.shell = InteractiveShell.instance()
#         self.path = path

#     def load_module(self, fullname):
#         """import a notebook as a module"""
#         path = "Untitled.ipynb"

#         print ("importing Jupyter notebook from %s" % path)

#         # load the notebook object
#         with io.open(path, 'r', encoding='utf-8') as f:
#             nb = read(f, 4)


#         for cell in nb.cells:
#             if cell.cell_type == 'code':
#                 # transform the input to executable Python
#                 code = self.shell.input_transformer_manager.transform_cell(cell.source)
#                 self.shell.run_cell(code)

    # l = NotebookLoader()
    # l.load_module('test_nb')



# def list_files(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))

import json
import sys

import tornado.ioloop

from tornado.web import Application
from jupyter_client import manager as kernel_manager, kernelspec
from jupyter_core.paths import jupyter_runtime_dir

from main_handler import MainHandler, NotebookRunnerHandler

if __name__ == "__main__":
    print("HELLO from helper_main", flush=True)

    app = Application([
        (r"/notebook/(.+\.ipynb)", NotebookRunnerHandler),
        (r"/", MainHandler)
    ], autoreload=True)
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()

