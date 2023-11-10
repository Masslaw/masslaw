import {ApiManager, HTTPRequest} from "../server_communication/api/api_client";
import {MasslawUserData} from "./user_data";
import {MasslawApiCalls} from "../server_communication/api/api_config";

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


    private _myUserDataCached = {} as MasslawUserData;


    public getMyCachedUserData() : MasslawUserData {
        return this._myUserDataCached;
    }

    public async setMyUserData(new_data: MasslawUserData) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{user_data: MasslawUserData}>({
            call: MasslawApiCalls.SET_USER_DATA,
            body: {user_data: new_data} as {[key:string]: any},
        } as HTTPRequest);
        this._myUserDataCached = response.data.user_data;
    }

    public async updateMyCachedUserData() {
        this._myUserDataCached = await this.getUserData('');
    }

    public async getUserData(userId: string) : Promise<MasslawUserData> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{user_data: MasslawUserData}>({
            call: MasslawApiCalls.GET_USER_DATA,
            queryStringParameters: {user_id: userId} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.user_data;
    }
}
