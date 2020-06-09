import ast

from ._base import InspectorBase

class PythonInspector(InspectorBase):
    def __init__(self, notebook):
        super().__init__(notebook)

    def available(self):
        return True

    def get_variables(self, cell_idx: int):
        cell_code = self.notebook['content']['cells'][cell_idx]['source']

        variables = set()

        root = ast.parse(cell_code)
        for node in ast.walk(root):
            #  Only variables that are loaded should be changed
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                variables.add(node.id)

        return list(variables)


inspector = PythonInspector
