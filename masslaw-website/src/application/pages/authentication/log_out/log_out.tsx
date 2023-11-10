import React from "react";
import "./css.css";
import {CognitoManager,} from "../../../infrastructure/server_communication/server_modules/cognito_client";
import {ApplicationRoutes} from "../../../infrastructure/application_base/routing/application_routes";
import {UserPhoto} from "../../../shared/components/user_photo/user_photo";
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";
import {NavigationFunctionState} from "../../../infrastructure/application_base/routing/application_global_routing";

import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {UserStatusManager} from "../../../infrastructure/user_management/user_status_manager";
import {useGlobalState,} from "../../../infrastructure/application_base/global_functionality/global_states";
import {useNavigate} from "react-router-dom";

export const LogOut: ApplicationPage = (props: ApplicationPageProps) => {

    const navigate = useNavigate();

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    let logout = () => {
        CognitoManager.getInstance().logOutUser();
        UserStatusManager.getInstance().forceResetStatus();
        navigate_function(ApplicationRoutes.HOME);
    }

    return (
        <>
            <div className={`fill-parent main-background`}>
                <form className={`form-container`}>
                    <div className={`top-title`}>Log Out?</div>
                    <UserPhoto size={100} id={'user-photo'}/>
                    <div className={'logout-email'}>{CognitoManager.getInstance().getLoggedInUserEmail()}</div>
                    <div className={'logout-message'}>Are you sure you want to log out of masslaw?</div>
                    <div style={{height: '20px'}}/>
                    <MasslawButton
                        onClick={logout}
                        size={{w: 310, h: 50}}
                        caption={'Log Out'}
                    />
                    <div style={{height: '20px'}}/>
                    <MasslawButton
                        caption={'Go Back'}
                        buttonType={MasslawButtonTypes.SECONDARY}
                        size={{w: 310, h: 50}}
                        onClick={e => navigate(-1)}
                    />
                    <div style={{height: '20px'}} />
                </form>
            </div>
        </>
    )
}