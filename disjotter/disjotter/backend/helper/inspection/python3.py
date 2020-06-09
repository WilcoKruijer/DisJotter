import json

from .runner_base import RunnerBase

from tornado.web import RequestHandler

class PythonRunner(RunnerBase):
    def __init__(self, config):
        super().__init__(config)

    def available(self):
        return True
        
    def run_pre_cell(self, req: RequestHandler) -> str:
        variables = self.config['variables']
        
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

        print('dding code:\n', code)

        return code

runner = PythonRunner