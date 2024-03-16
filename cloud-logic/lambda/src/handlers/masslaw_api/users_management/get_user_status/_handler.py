from src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction


class GetUserStatus(AuthenticatedMasslawUserHttpInvokedLambdaFunction):
    pass


def handler(event, context):
    handler_instance = GetUserStatus()
    handler_instance.call_handler(event, context)
    return handler_instance.get_response()
