import {UserStatus} from "./user_status";
import {ApiManager} from "../server_communication/api_client";
import {CognitoManager} from "../server_communication/cognito_client";
import {ApplicationRoutingManager} from "../routing/application_routing_manager";
import {MasslawApiCallData, MasslawApiCalls} from "../server_communication/api_config";

export class UserStatusManager {
    private static _instance = new UserStatusManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (UserStatusManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }

        ApplicationRoutingManager.getInstance().addOnLocationChangedCallback((_:string)=>{ this.fetchUserStatus().then() });
    }

    private _cachedStatusKey = 'user_status';
    public STATUS_CHANGED_EVENT_NAME = 'user-status-changed';


    public setDiscoveredStatus(status : UserStatus) {
        this.setCurrentStatus(status);
    }

    public async fetchUserStatus() {

        if (!(await CognitoManager.getInstance().checkLoggedIn(true)))
            this.setDiscoveredStatus(UserStatus.GUEST);

        let callData : MasslawApiCallData = MasslawApiCalls.GET_MY_STATUS;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {},
            headers: {},
            payload: {},
        }
        await ApiManager.getInstance().MasslawAPICall(callData, callRequest);

        return this.getCurrentStatus();
    }

    public getCachedUserStatus() : UserStatus {
        return this.getCurrentStatus();
    }

    private setCurrentStatus(status: UserStatus) {
        if (status >= 0) {
            console.debug(`user status discovered to be ${status}`);
            if (this.getCurrentStatus() === status) return;
            sessionStorage.setItem(this._cachedStatusKey, String(Number(status)));
            document.dispatchEvent(new CustomEvent(this.STATUS_CHANGED_EVENT_NAME, { detail: status }));
        }
    }

    private getCurrentStatus() : UserStatus {
        let currentStatusString = Number(sessionStorage.getItem(this._cachedStatusKey));
        return !isNaN(currentStatusString) ? (currentStatusString as UserStatus) : UserStatus.GUEST;
    }
}