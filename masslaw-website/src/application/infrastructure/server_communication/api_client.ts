import {CognitoManager} from "./cognito_client";
import axios, {AxiosRequestConfig} from "axios";
import {UserStatusManager} from "../user_management/user_status_manager";
import {DevelopmentStages, DevelopmentStagesManager} from "../development_staging/development_stages_manager";
import {HttpStatus, MasslawApiCallData, MasslawApiRequest, MasslawApiResponseData} from "./api_config";


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

    private _masslawApiStageRoots : Map<DevelopmentStages, string> = new Map([
        [DevelopmentStages.PRODUCTION, 'https://m75viyz474.execute-api.us-east-1.amazonaws.com/prod'],
        [DevelopmentStages.DEVELOPMENT, 'https://g3cd8tsx89.execute-api.us-east-1.amazonaws.com/dev'],
    ])


    public async MasslawAPICall(callData: MasslawApiCallData, request: MasslawApiRequest) : Promise<{success: boolean, data: MasslawApiResponseData}> {

        let response = await this.MakeMasslawCall(callData, request);

        if (response.success) this.handleMasslawMasslawApiResponseInternal(response.data);

        return response;
    }

    private async MakeMasslawCall(callData: MasslawApiCallData, request: MasslawApiRequest) : Promise<{success: boolean, data: MasslawApiResponseData}> {

        type callResponseDataShape = typeof callData.responseDataShape;

        let accessToken = this._cognitoManager.getAccessToken();
        if (accessToken) {
            request.headers['Authorization'] = `Bearer ${accessToken}`
        } else if (callData.requires_login) {
            return {
                success: false,
                data: {
                    statusCode: HttpStatus.UNAUTHORIZED,
                    headers: {},
                    body: { message: 'unauthorized'},
                    userStatus: 0,
                } as callResponseDataShape
            };
        }

        request.headers['Content-Type'] = 'application/json';

        let apiUrl = new URL(this.getCurrentStageApiBaseUrl() + callData.rout);
        for (const [key, value] of Object.entries(request.queryStringParameters))
            if (key && value) apiUrl.searchParams.append(key, value);

        let response = {} as callResponseDataShape;
        try {
            response = await axios.request({
                url: apiUrl.href,
                method: callData.method,
                headers: request.headers,
                data: request.payload,
            } as AxiosRequestConfig);
            return {
                success: true,
                data: response.data as callResponseDataShape,
            };
        } catch (error) {
            return {
                success: false,
                data: callData.responseDataShape as callResponseDataShape,
            };
        }
    }

    private handleMasslawMasslawApiResponseInternal(responseData: MasslawApiResponseData) {
        let discoveredStatus = -1;
        if (responseData.userStatus != null) discoveredStatus = responseData.userStatus as number
        UserStatusManager.getInstance().setDiscoveredStatus(discoveredStatus);
    }

    private getCurrentStageApiBaseUrl() : string {
        return this._masslawApiStageRoots.get(DevelopmentStagesManager.getInstance().getDevelopmentStage()) || '';
    }
}

