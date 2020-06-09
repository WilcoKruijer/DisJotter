
class InspectorBase:
    def __init__(self, notebook):
        self.notebook = notebook

    def available(self):
        return False

    def get_variables(self, cell_index):
        return []
