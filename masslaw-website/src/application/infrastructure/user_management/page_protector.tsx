import {useNavigate, useLocation} from "react-router-dom";
import React, {useEffect} from 'react';
import {ApplicationRoutes} from "../routing/application_routes";
import {UserStatus} from "./user_status";
import {UserStatusManager} from "./user_status_manager";
import {ApplicationRoutingManager} from "../routing/application_routing_manager";

export enum StatusConditionType {
    MINIMUM,
    EXACT,
    MAXIMUM,
}
interface StatusConditionData {
    status : UserStatus;
    type: StatusConditionType;
    failedRedirect: { [status in UserStatus]: ApplicationRoutes; }
}

const defaultStatusConditionData : StatusConditionData = {
    status: UserStatus.GUEST,
    type: StatusConditionType.MINIMUM,
    failedRedirect: {
        [UserStatus.GUEST] : ApplicationRoutes.HOME,
        [UserStatus.LOGGED_IN] : ApplicationRoutes.MASSLAWYER,
        [UserStatus.UNVERIFIED] : ApplicationRoutes.VERIFICATION,
        [UserStatus.MISSING_CREDENTIALS] : ApplicationRoutes.PROFILE,
        [UserStatus.FULLY_APPROVED] : ApplicationRoutes.APP,
    }
}

export class PageProtector {
    private static _instance = new PageProtector();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (PageProtector._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }

        document.addEventListener(UserStatusManager.getInstance().STATUS_CHANGED_EVENT_NAME, e=>{ this.handleCurrentStatus() })
    }


    private _statusConditionData : StatusConditionData = defaultStatusConditionData;

    public updateStatusCondition(status : UserStatus | null,
                              type: StatusConditionType | null,
                              failedRedirect: {[status in UserStatus]: ApplicationRoutes;} | null) : boolean {
        this._statusConditionData = defaultStatusConditionData;

        if (status != null) this._statusConditionData.status = status;

        if (type != null) this._statusConditionData.type = type;

        if (failedRedirect != null)
            for (const status in failedRedirect)
                this._statusConditionData.failedRedirect[status as unknown as UserStatus] =
                    failedRedirect[status as unknown as UserStatus]

        console.debug(`setting new status condition for page [${ApplicationRoutingManager.getInstance().getCurrentRoute()}]`);
        console.debug(this._statusConditionData)

        return this.handleCurrentStatus();
    }

    private handleCurrentStatus() : boolean {
        let currentStatus = UserStatusManager.getInstance().getCachedUserStatus();
        if (this.checkCondition(currentStatus)) return true;
        console.debug(`user status [${currentStatus}] didn't pass the page's [${ApplicationRoutingManager.getInstance().getCurrentRoute()}] status condition`)
        console.debug(this._statusConditionData)
        this.redirectFailed(currentStatus);
        return false;
    }

    private checkCondition(status: UserStatus) : boolean {
        switch (this._statusConditionData.type) {
            case StatusConditionType.MINIMUM:
                return status >= this._statusConditionData.status;
            case StatusConditionType.EXACT:
                return status === this._statusConditionData.status;
            case StatusConditionType.MAXIMUM:
                return status <= this._statusConditionData.status;
        }
        return false;
    }

    private redirectFailed(status: UserStatus) {
        let failed_redirect = this._statusConditionData.failedRedirect[status];
        console.debug(`redirecting due to status condition check fail ${failed_redirect}`);
        ApplicationRoutingManager.getInstance().navigateToRoute(failed_redirect);
    }
}