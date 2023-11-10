import React from "react";

import "./css.css";
import {CognitoManager,} from "../../../infrastructure/server_communication/cognito_client";
import {PageProtector, StatusConditionType} from "../../../infrastructure/user_management/page_protector";
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {UserStatus} from "../../../infrastructure/user_management/user_status";
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {UsersManager} from "../../../infrastructure/user_management/users_manager";
import {UserPhoto} from "../../../shared/components/user_photo/user_photo";
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";

ApplicationRoutingManager.getInstance().setRoutePreloadFunction(ApplicationRoutes.LOGOUT, () => {
    if (!PageProtector.getInstance().updateStatusCondition(UserStatus.LOGGED_IN, StatusConditionType.MINIMUM, null)) return;
    UsersManager.getInstance().updateMyCachedUserData().then();
    return true;
});

export function LogOut() {

    let onLogout = async () => {
        CognitoManager.getInstance().logOutUser();
    }

    return (
        <>
            <div className={`fill-parent main-background`}>
                <form className={`form-container`}>
                    <div className={`top-title`}>Log Out?</div>
                    <UserPhoto size={100} id={'user-photo'}/>
                    <div className={'logout-email'}>{CognitoManager.getInstance().getLoggedInUserEmail()}</div>
                    <div className={'logout-message'}>Are you sure you want to log out of masslaw?</div>
                    <LoadingButton clickable={true}
                                   onClick={onLogout}
                                   loading={false}
                                   caption={'Log Out'}/>
                    <MasslawButton caption={'Go Back'}
                                   buttonType={MasslawButtonTypes.SECONDARY}
                                   size={{w: 310, h: 50}}
                                   onClick={e => ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes._)} />
                    <div style={{height: '20px'}} />
                </form>
            </div>
        </>
    )
}