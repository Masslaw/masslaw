import {CognitoManager} from "../server_modules/cognito_client";
import axios, {AxiosRequestConfig} from "axios";
import {UserStatusManager} from "../../user_management/user_status_manager";
import {ApiCallData, ApiRoots, APIs} from "./api_config";

export class ApiManager {

    private static _instance = new ApiManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (ApiManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }


    private _cognitoManager = CognitoManager.getInstance();

    public async MakeApiHttpRequest<T>(request: HTTPRequest) : Promise<{success: boolean, data: T}> {

        let request_call = request.call;
        let request_query_string_params = request.queryStringParameters || {};
        let request_headers = request.headers || {};
        let request_body = request.body || {};

        let accessToken = this._cognitoManager.getAccessToken();
        if (accessToken) request_headers['Authorization'] = `Bearer ${accessToken}`;

        request_headers['Content-Type'] = 'application/json';

        let apiUrl = new URL(this.getBaseUrlForApi(request_call.api) + request_call.rout);
        for (const [key, value] of Object.entries(request_query_string_params)) {
            if (key && value) apiUrl.searchParams.append(key, value);
        }

        try {
            let response = await axios.request<T>({
                url: apiUrl.href,
                method: request_call.method,
                headers: request_headers,
                data: request_body,
                validateStatus: () => true,
            } as AxiosRequestConfig);
            this.handleApiResponse(response.data);
            return {
                success: response.status < 300,
                data: response.data,
            };
        } catch (error) {
            return {
                success: false,
                data: {} as T,
            };
        }
    }

    private handleApiResponse(responseData: any) {
        let discoveredStatus = -1;
        if (responseData.userStatus != null) discoveredStatus = responseData.userStatus as number
        UserStatusManager.getInstance().setDiscoveredStatus(discoveredStatus);
    }

    private getBaseUrlForApi(api: APIs) : string {
        return process.env.API_BASE_URL || '';
    }
}

export interface HTTPRequest {
    call: ApiCallData,
    queryStringParameters: {[key: string]: string},
    headers: {[key: string]: string},
    body: {[key: string]: any}
}
