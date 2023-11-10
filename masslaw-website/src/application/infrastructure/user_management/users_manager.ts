import {CognitoManager} from "../server_communication/cognito_client";
import {ApiManager} from "../server_communication/api_client";
import {UserData} from "./user_data";
import {MasslawApiCallData, MasslawApiCalls} from "../server_communication/api_config";

export class UsersManager {

    private static _instance = new UsersManager();

    public static getInstance() {
        return this._instance
    }

    constructor() {
        if (UsersManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }

    private _cachedDataKey = 'my_cached_user_data';
    private _cognitoManager = CognitoManager.getInstance();
    private _myUserDataCached = {} as UserData;


    public getMyCachedUserData() : UserData {
        return this._myUserDataCached;
    }

    public async setMyUserData(new_data: UserData) {
        let callData : MasslawApiCallData = MasslawApiCalls.SET_USER_DATA;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {},
            headers: {},
            payload: { user_data: new_data },
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let data = response.data as typeof callData.responseDataShape
        this._myUserDataCached = data.user_data;
    }

    public async updateMyCachedUserData() {
        this._myUserDataCached = await this.getUserData('');
    }

    public async updateMyData(newData: UserData) {
        let callData : MasslawApiCallData = MasslawApiCalls.SET_USER_DATA;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {},
            headers: {},
            payload: {
                user_data: newData
            },
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let data = response.data as typeof callData.responseDataShape;
        this._myUserDataCached = data.user_data;
    }

    public async getUserData(userId: string) : Promise<UserData> {
        let callData : MasslawApiCallData = MasslawApiCalls.GET_USER_DATA;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: { user_id: userId, },
            headers: {},
            payload: {},
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let data = response.data as typeof callData.responseDataShape
        return data.user_data;
    }
}
