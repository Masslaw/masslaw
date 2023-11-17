
class StatusCodes:
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class EventKeys:
    QUERY_STRING_PARAMETERS = 'queryStringParameters'
    PATH_PARAMETERS = 'pathParameters'
    HEADER_PARAMETERS = 'headers'
    BODY = 'body'
    PAYLOAD = 'payload'
    REQUEST_CONTEXT = 'requestContext'
    HTTP_METHOD = 'httpMethod'
    REQUEST_ID = 'requestId'
    RESOURCE_PATH = 'resourcePath'
    STATUS_CODE = 'statusCode'
    RESPONSE_MESSAGE = 'message'
    USER_STATUS = 'userStatus'


class HttpMethods:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class RequestHeaders:
    ACCEPT = 'accept'
    ACCEPT_ENCODING = 'accept-encoding'
    AUTHORIZATION = 'Authorization'
    CACHE_CONTROL = 'cache-control'
    CONTENT_TYPE = 'content-type'
    COOKIE = 'cookie'
    HOST = 'host'
    REFERER = 'referer'
    USER_AGENT = 'user-agent'
    ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'


class ContentTypes:
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'
    APPLICATION_XHTML_XML = 'application/xhtml+xml'
    APPLICATION_FORM_URLENCODED = 'application/x-www-form-urlencoded'
    MULTIPART_FORM_DATA = 'multipart/form-data'
    TEXT_PLAIN = 'text/plain'
    TEXT_HTML = 'text/html'


class ResponseMessages:
    OPERATION_EXECUTED_SUCCESSFULLY = "Operation executed successfully"
    POORLY_PROVIDED_PARAMETERS = 'Parameters provided poorly'
    CREDENTIALS_INVALID = 'Invalid Credentials'
    DATA_INVALID = 'Invalid Data'
    RESOURCE_NOT_FOUND = 'Resource not found'
    RESOURCE_ALREADY_EXISTS = 'Resource already exists'
    INTERNAL_SERVER_ERROR = 'Internal server error'
    ACCESS_DENIED = 'Access denied'
    INVALID_CREDENTIALS = 'Invalid credentials'
    INVALID_DATA = 'Invalid data'
    REQUEST_TIMEOUT = 'Request timeout'
    BAD_REQUEST = 'Bad request'
    FORBIDDEN = 'Forbidden'
    METHOD_NOT_ALLOWED = 'Method not allowed'
    UNSUPPORTED_MEDIA_TYPE = 'Unsupported media type'
    UNAUTHORIZED_REQUEST = 'Unauthorized'

