from interface_layer.application._application_execution import ApplicationExecution
from shared_layer.mlcp_logger import logger


class Application:
    def __init__(self):
        logger.info('MLCP :)')
        self._execution = ApplicationExecution()

    @logger.process_function('Setting Up Application')
    def setup(self):
        self._execution.setup()

    @logger.process_function('Running Application')
    def run(self):
        self._execution.run()

    @logger.process_function('Executing Application Process')
    def __call__(self, *args, **kwargs):
        self.setup()
        self.run()
