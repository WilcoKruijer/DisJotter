from typing import Optional

from notebook.base.handlers import IPythonHandler, APIHandler, HTTPError

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
