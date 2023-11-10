class ApplicationActionLoadingException(ImportError):
    def __init__(self, error_data: ImportError):
        super().__init__(f'An error occured trying to load an application action implementation: {error_data}')


class ApplicationActionImplementationNotFoundException(Exception):
    def __init__(self, action_name):
        super().__init__(f'Could not find a action implementation for action "{action_name}"')


class ApplicationActionRequiredParamMissingException(Exception):
    def __init__(self, action_name, param_name):
        super().__init__(f'A required parameter "{param_name}" is missing from the Application action {action_name} params')


class ApplicationActionExecutionException(Exception):
    def __init__(self, reason=''):
        super().__init__(reason or '')
