export enum APIs {
    MASSLAW = 'masslaw',
}


export enum HttpMethod {
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    DELETE = "DELETE",
    HEAD = "HEAD",
    OPTIONS = "OPTIONS",
    PATCH = "PATCH",
    TRACE = "TRACE",
    CONNECT = "CONNECT",
}

export enum HttpStatus {
    OK = 200,
    CREATED = 201,
    BAD_REQUEST = 400,
    UNAUTHORIZED = 401,
    FORBIDDEN = 403,
    NOT_FOUND = 404,
    INTERNAL_SERVER_ERROR = 500,
    SERVICE_UNAVAILABLE = 503
}


export interface ApiCallData {
    api: APIs,
    method: HttpMethod,
    rout: string,
}

export const MasslawApiCalls = {
    GET_MY_STATUS : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/users/me/status'} as ApiCallData,
    GET_USER_DATA : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/users/user-data'} as ApiCallData,
    SET_USER_DATA : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/users/user-data'} as ApiCallData,
    CREATE_CASE : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/create'} as ApiCallData,
    GET_MY_CASES : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/get-mine'} as ApiCallData,
    GET_CASE_DATA : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/data'} as ApiCallData,
    SET_CASE_DATA : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/case/data'} as ApiCallData,
    GET_CASE_FILES : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/files'} as ApiCallData,
    START_CASE_FILE_UPLOAD : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/case/files/start-file-upload'} as ApiCallData,
    FINISH_CASE_FILE_UPLOAD : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/case/files/finish-file-upload'} as ApiCallData,
    GET_CASE_FILE_CONTENT : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/files/get-content'} as ApiCallData,
    GET_CASE_FILE_DATA : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/files/get-file-data'} as ApiCallData,
    DELETE_CASE_FILE : {api: APIs.MASSLAW, method:HttpMethod.DELETE, rout:'/cases/case/files/delete-file'} as ApiCallData,
    SEARCH_CASE_FILES_TEXT : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/files/search-text'} as ApiCallData,
    GET_CASE_ANNOTATIONS : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/annotations'} as ApiCallData,
    SET_CASE_ANNOTATION : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/case/annotations'} as ApiCallData,
    DELETE_CASE_ANNOTATION : {api: APIs.MASSLAW, method:HttpMethod.DELETE, rout:'/cases/case/annotations'} as ApiCallData,
    SET_FILE_DESCRIPTION : {api: APIs.MASSLAW, method:HttpMethod.POST, rout:'/cases/case/files/set-description'} as ApiCallData,
    GET_CASE_KNOWLEDGE_ITEM_DATA : {api: APIs.MASSLAW, method:HttpMethod.GET, rout:'/cases/case/knowledge/items/data'} as ApiCallData,
}

export const ApiRoots: {[key in APIs]: {[key in DevelopmentStages]: string}} = {
    [APIs.MASSLAW]: {
        [DevelopmentStages.PRODUCTION]: 'https://5vcihdhjs8.execute-api.us-east-1.amazonaws.com/prod',
        [DevelopmentStages.DEVELOPMENT]: 'https://uz878qkx1b.execute-api.us-east-1.amazonaws.com/dev',
    },
};
