from typing import List

class InspectorBase:
    def available(self):
        return False

    def get_variables(self, notebook, cell_index) -> List[str]:
        return []

    def run_pre_cell(self, config, req) -> str:
        """Returns code as string that will run before the final cell does."""
        return ''
