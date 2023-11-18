from src.modules.lambda_handler_template_http_invoked_authenticated_masslaw_user import AuthenticatedMasslawUserHttpInvokedLambdaFunction


class GetUserStatus(AuthenticatedMasslawUserHttpInvokedLambdaFunction):
    pass


handler = GetUserStatus()
