import json
import os
import tempfile
import shutil
import importlib

from typing import Optional

import docker
from notebook.base.handlers import IPythonHandler, APIHandler, HTTPError
from notebook.utils import url_path_join
from pigar.core import parse_packages

from ..container.creator import ContainerCreator

def determine_packages(dir=os.getcwd()):
    libs, guess = parse_packages(dir)
    print('>> determine', libs, guess)
    determined = [(key, libs[key].version) for key in libs.keys()]
    determined.extend([(key, None) for key in guess.keys()])

    return determined


def write_requirements(packages):
    requirements = ""

    for lib, version in packages:
        if version:
            requirements += f"{lib}=={version}\n"
        else:
            requirements += f"{lib}\n"

    return requirements



class BaseHandler(APIHandler):
    def check_xsrf_cookie(self):
        # Hack to not get missing _xsrf error. Probably makes the routes insecure.

        # [W 14:42:46.388 NotebookApp] 403 POST /notebook/empty.ipynb/build (127.0.0.1): '_xsrf' argument missing from POST
        # [W 14:42:46.389 NotebookApp] '_xsrf' argument missing from POST
        return

    def _int_body(self, name, default: int =None) -> Optional[int]:
        try:
            return int(self.get_json_body()[name])
        except (ValueError, TypeError, KeyError):
            return default

    def _int_argument(self, name, default: int = None) -> Optional[int]:
        try:
            return int(self.get_argument(name, default))
        except (ValueError, TypeError):
            return default


class DeterminePackagesHandler(BaseHandler):
    def get(self, path):        
        # notebook = self.contents_manager.get(path, content=True)
        notebook_path = os.path.join(os.getcwd(), path)

        #  Create a temporary dir which will be our build context.
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copyfile(notebook_path, tmpdir + "/notebook.ipynb")

            packages = determine_packages(tmpdir)
        
        reqs = write_requirements(packages)

        self.finish(json.dumps({
            'data': reqs
        }))


class InspectHandler(BaseHandler):
    def _get_inspector(self, notebook):
        kernel = notebook['content']['metadata']['kernelspec']['name']

        try:
            #  ext_module.backend.inspection
            inspection_package = __name__.rsplit('.', 2)[0] + ".inspection"
            inspector_module = importlib.import_module(
                f'..inspection.{kernel}', package=inspection_package)

            inspector = inspector_module.inspector(notebook)
            
            if inspector.available():
                return inspector
        except ModuleNotFoundError:
            pass

        raise HTTPError(501, 'inspector_unavailable')


    def get(self, path, command):
        notebook = self.contents_manager.get(path, content=True)
        inspector = self._get_inspector(notebook)

        if command == 'available':
            self.set_status(201)
            self.finish()
        elif command == 'variables':
            cell_index = self._int_argument('cellIdx')

            if cell_index is None:
                raise HTTPError(400, 'invalid_cell_idx')

            variables = inspector.get_variables(cell_index)

            self.finish(json.dumps({
                'data': variables
            }))

        raise HTTPError(400, 'no_cmd')

    def post(self, path, command):
        pass


class CommandHandler(BaseHandler):
    def post(self, image_name, command):
        if command == 'run':
            return self._run(image_name)
        elif command == 'stop':
            return self._stop(image_name)

        raise HTTPError(400, 'no_cmd')

    def get(self, image_name, command):
        if command == 'status':
            return self._status(image_name)

        raise HTTPError(400, 'no_cmd')

    def _stop(self, image_name):
        client = docker.from_env()
        
        try:
            container = client.containers.get(image_name)
            container.stop(timeout=1)
            status = container.status
        except docker.errors.NotFound:
            status = 'not_found'
        finally:
            self.finish(json.dumps({
                'data': status
            }))

    def _run(self, image_name):
        body = self.get_json_body()
        print('bod', body)
        port = self._int_body('port', 10000)

        if port is None:
            raise HTTPError(400, 'def')

        print('pot', port)

        cc = ContainerCreator('.', image_name, None)
        container = cc.run_container(port)

        self.finish(json.dumps({
            'data': container.status
        }))

    def _status(self, image_name):
        client = docker.from_env()

        try:
            container = client.containers.get(image_name)
            status = container.status
        except docker.errors.NotFound:
            status = 'not_found'
        finally:
            self.finish(json.dumps({
                'data': status
            }))

