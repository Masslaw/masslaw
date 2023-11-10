import {UserStatus} from "./user_status";
import {ApiManager, HTTPRequest} from "../server_communication/api/api_client";
import {CognitoManager} from "../server_communication/server_modules/cognito_client";
import {MasslawApiCalls} from "../server_communication/api/api_config";

export type UserStatusChangedEvent = CustomEvent<{ status: UserStatus }>;

export class UserStatusManager {
    private static _instance = new UserStatusManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (UserStatusManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }

    private _cachedStatusKey = 'user_status';
    private _lastFetchedStatusKey = 'last_fetched_user_status';
    private _validStatusKey = 'is_user_status_valid';

    public STATUS_CHANGED_EVENT_NAME = 'user-status-changed';


    public setDiscoveredStatus(status : UserStatus) {
        this.setCurrentStatus(status);
        this.setStatusValid();
    }

    public async forceResetStatus() {
        await this.fetchUserStatus(true);
    }

    public async getUserStatus() : Promise<UserStatus> {
        let userStatus = this.getCachedUserStatus();
    if (userStatus != undefined) return userStatus;

        userStatus = await this.fetchUserStatus();
        if (userStatus != undefined) return userStatus;

        return UserStatus.GUEST;
    }

    private async fetchUserStatus(force?: boolean) {
        if (
            !force &&
            this.getLastFetchedStatusTime() - Date.now() < (5*1000) &&
            this.isStatusValid()
        ) return this.getCachedUserStatus();

        this.setStatusValid();

        if (!(await CognitoManager.getInstance().checkLoggedIn(true)))
            this.setDiscoveredStatus(UserStatus.GUEST);

        let response= await ApiManager.getInstance().MakeApiHttpRequest({
            call: MasslawApiCalls.GET_MY_STATUS,
        } as HTTPRequest);

        return this.getCachedUserStatus();
    }

    private setCurrentStatus(status: UserStatus) {
        if (status === undefined) return;
        sessionStorage.setItem(this._cachedStatusKey, String(Number(status)));
        document.dispatchEvent(new CustomEvent(this.STATUS_CHANGED_EVENT_NAME, { detail: status }));
    }

    private getCachedUserStatus() : UserStatus | undefined {
        let currentStatus = parseInt(sessionStorage.getItem(this._cachedStatusKey) || '');
        return currentStatus;
    }

    private getLastFetchedStatusTime() : number {
        let lastFetchedStatus = parseInt(sessionStorage.getItem(this._lastFetchedStatusKey) || '');
        return lastFetchedStatus;
    }

    private setLastUpdatedStatusTime(customTime?: number) {
        sessionStorage.setItem(this._lastFetchedStatusKey, String(customTime || Date.now()));
    }

     private isStatusValid(): boolean {
         let isStatusValid = sessionStorage.getItem(this._validStatusKey) === 'valid';
         return isStatusValid
     }

     private setStatusValid() {
        sessionStorage.setItem(this._validStatusKey, 'valid');
         this.setLastUpdatedStatusTime();
     }

     public invalidateStatus() {
         sessionStorage.setItem(this._validStatusKey, 'invalid');
     }
}