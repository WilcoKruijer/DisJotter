class RunnerBase:
    def __init__(self, config):
        self.config = config

    def available(self):
        return False

    def run_pre_cell(self) -> str:
        return ''
