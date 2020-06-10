import sys
from glob import glob

import tornado.ioloop
from tornado.web import Application
from jupyter_client import manager as kernel_manager, kernelspec
from jupyter_core.paths import jupyter_runtime_dir

from .handlers import MainHandler, NotebookRunnerHandler
from .util import get_config


def start_helper():
    print("DisJotter helper starting.\n", flush=True)

    try:
        config = get_config()

        cell_num = config['index'] + 1
        path = config['path']

        print('Available routes:')
        print('  - /')
        print(f'      This will run cell {cell_num} of {path}.')
        print()
        print('      Available variables:')

        for var in config['variables']:
            var_type = config['variables'][var]
            print(f'        {var} - {var_type}')

        print()
        for notebook in glob('*.ipynb'):
            print(f'  - /notebook/{notebook}?cellIdx=<index>')
            print(f'      This will run cell <index> of {notebook}.')
            print()
            print('      No available variables.')

        print(flush=True)

    except FileNotFoundError:
        print('Unable to load config file. Exiting.', file=sys.stderr)
        return

    app = Application([
        (r"/notebook/(.+\.ipynb)", NotebookRunnerHandler),
        (r"/", MainHandler)
    ], autoreload=True)
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()
