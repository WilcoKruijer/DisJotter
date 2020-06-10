import ast
import json

from ._base import InspectorBase
from tornado.web import RequestHandler


class PythonInspector(InspectorBase):
    def __init__(self):
        super().__init__()

    def available(self):
        return True

    def get_variables(self, notebook, cell_idx: int):
        cell_code = notebook['content']['cells'][cell_idx]['source']

        variables = set()

        root = ast.parse(cell_code)
        for node in ast.walk(root):
            #  Only variables that are loaded should be changed
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                variables.add(node.id)

        return list(variables)

    def run_pre_cell(self, config, req: RequestHandler) -> str:
        variables = config['variables']
        
        if req.request.method == 'POST':
            json_body = json.loads(req.request.body)
        else:
            json_body = {}

        code = ''

        for v in variables.keys():
            var_type = variables[v]

            if var_type == 'query':
                arg_string = req.get_argument(v, None)
                if arg_string is not None:
                    code += f'{v} = {arg_string}\n'
            if var_type == 'post' and req.request.method == 'POST':
                arg_string = json_body.get(v, None)

                if arg_string is not None:
                    code += f'{v} = {arg_string}\n'

        return code


inspector = PythonInspector
