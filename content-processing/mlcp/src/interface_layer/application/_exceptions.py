class MLCPProcessConfigurationNotFoundException(Exception):

    def __init__(self):
        super().__init__("MLCP Process Configuration not found")


class MLCPRequiredProcessActionExecutionFailedException(Exception):

    def __init__(self, action_name):
        self._action_name = action_name
        super().__init__("A Required Process Action Execution Failed During Application Execution")

    def get_action_name(self):
        return self._action_name
