import {UserData} from "../user_management/user_data";


export enum HttpMethod {
    GET = "GET",
    POST = "POST",
    PUT = "PUT",
    DELETE = "DELETE",
    HEAD = "HEAD",
    OPTIONS = "OPTIONS",
    PATCH = "PATCH",
    TRACE = "TRACE",
    CONNECT = "CONNECT"
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

export interface MasslawApiRequest {
    queryStringParameters: object,
    headers: {
        [key: string]: any,
    },
    payload: {
        [key: string]: any,
    },
}

export interface MasslawApiResponseData{
    [key: string]: any,
}

export interface MasslawApiCallData {
    method: HttpMethod,
    rout: string,
    requires_login: boolean,
    requestShape: MasslawApiRequest,
    responseDataShape: MasslawApiResponseData,
}

export class MasslawApiCalls {

    static GET_MY_STATUS: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/users/me/status',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {},
        } as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
        } as MasslawApiResponseData,
    };

    static GET_USER_DATA: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/users/user-data',
        requires_login: false,
        requestShape: {
            queryStringParameters: {
                user_id: '',
            },
            headers: {},
            payload: {},
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            user_data: {} as UserData,
        } as MasslawApiResponseData,
    };

    static SET_USER_DATA: MasslawApiCallData = {
        method: HttpMethod.POST,
        rout: '/users/user-data',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {
                user_data: {} as UserData,
            },
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            user_data: {} as UserData,
        } as MasslawApiResponseData,
    };

    static GET_MY_CASES: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/cases/get-mine',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {},
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            my_cases: [],
        } as MasslawApiResponseData,
    };

    static CREATE_CASE: MasslawApiCallData = {
        method: HttpMethod.POST,
        rout: '/cases/create',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {
                case_data: {},
            },
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            case_id: '',
        } as MasslawApiResponseData,
    };

    static GET_CASE_DATA: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/cases/case/get-data',
        requires_login: false,
        requestShape: {
            queryStringParameters: {
                case_id: ''
            },
            headers: {},
            payload: {},
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            case_data: '',
        } as MasslawApiResponseData,
    };

    static GET_CASE_FILES: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/cases/case/files',
        requires_login: false,
        requestShape: {
            queryStringParameters: {
                case_id: ''
            },
            headers: {},
            payload: {},
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            case_files: {
                files: []
            },
        } as MasslawApiResponseData,
    };

    static START_CASE_FILE_UPLOAD: MasslawApiCallData = {
        method: HttpMethod.POST,
        rout: '/cases/case/files/start-file-upload',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {
                case_id: '',
                file_name: '',
                num_parts: '',
                languages: [],
            },
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0,
            upload_id: '',
            upload_urls: '',
            file_id: '',
        } as MasslawApiResponseData,
    };

    static FINISH_CASE_FILE_UPLOAD: MasslawApiCallData = {
        method: HttpMethod.POST,
        rout: '/cases/case/files/finish-file-upload',
        requires_login: true,
        requestShape: {
            queryStringParameters: {},
            headers: {},
            payload: {
                case_id: '',
                file_id: '',
                parts: {}
            },
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            userStatus: 0
        } as MasslawApiResponseData,
    };

    static GET_CASE_FILE_DOWNLOAD: MasslawApiCallData = {
        method: HttpMethod.GET,
        rout: '/cases/case/files/get-file-download',
        requires_login: true,
        requestShape: {
            queryStringParameters: {
                case_id: '',
                file_id: '',
                file_form: '',
            },
            headers: {},
            payload: {},
        }as MasslawApiRequest,
        responseDataShape: {
            message: '',
            download_url: ''
        } as MasslawApiResponseData,
    };


}