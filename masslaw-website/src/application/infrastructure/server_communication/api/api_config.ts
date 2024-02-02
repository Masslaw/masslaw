
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
    method: HttpMethod,
    rout: string,
}

export const MasslawApiCalls = {
    GET_MY_STATUS : {method:HttpMethod.GET, rout:'/users/me/status'} as ApiCallData,
    GET_USER_DATA : {method:HttpMethod.GET, rout:'/users/user-data'} as ApiCallData,
    SET_USER_DATA : {method:HttpMethod.POST, rout:'/users/user-data'} as ApiCallData,
    CREATE_CASE : {method:HttpMethod.POST, rout:'/cases/create'} as ApiCallData,
    GET_MY_CASES : {method:HttpMethod.GET, rout:'/cases/get-mine'} as ApiCallData,
    GET_CASE_DATA : {method:HttpMethod.GET, rout:'/cases/case/data'} as ApiCallData,
    SET_CASE_DATA : {method:HttpMethod.POST, rout:'/cases/case/data'} as ApiCallData,
    GET_CASE_FILES : {method:HttpMethod.GET, rout:'/cases/case/files'} as ApiCallData,
    START_CASE_FILE_UPLOAD : {method:HttpMethod.POST, rout:'/cases/case/files/start-file-upload'} as ApiCallData,
    FINISH_CASE_FILE_UPLOAD : {method:HttpMethod.POST, rout:'/cases/case/files/finish-file-upload'} as ApiCallData,
    GET_CASE_FILE_CONTENT : {method:HttpMethod.GET, rout:'/cases/case/files/get-content'} as ApiCallData,
    GET_CASE_FILE_DATA : {method:HttpMethod.GET, rout:'/cases/case/files/get-file-data'} as ApiCallData,
    DELETE_CASE_FILE : {method:HttpMethod.DELETE, rout:'/cases/case/files/delete-file'} as ApiCallData,
    SEARCH_CASE_FILES_TEXT : {method:HttpMethod.GET, rout:'/cases/case/files/search-text'} as ApiCallData,
    GET_CASE_ANNOTATIONS : {method:HttpMethod.GET, rout:'/cases/case/annotations'} as ApiCallData,
    SET_CASE_ANNOTATION : {method:HttpMethod.POST, rout:'/cases/case/annotations'} as ApiCallData,
    DELETE_CASE_ANNOTATION : {method:HttpMethod.DELETE, rout:'/cases/case/annotations'} as ApiCallData,
    SET_FILE_DESCRIPTION : {method:HttpMethod.POST, rout:'/cases/case/files/set-description'} as ApiCallData,
    GET_CASE_KNOWLEDGE : {method:HttpMethod.GET, rout:'/cases/case/knowledge'} as ApiCallData,
    GET_CASE_KNOWLEDGE_ITEM_DATA : {method:HttpMethod.GET, rout:'/cases/case/knowledge/items/data'} as ApiCallData,
}
