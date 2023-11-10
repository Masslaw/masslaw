import React, {useCallback, useContext, useEffect, useState} from "react";
import {
    globalStateDeclaration,
    useGlobalState
} from "../../global_states";
import {UserStatus} from "../../../../user_management/user_status";
import {
    PreviousUserStatusState,
    UserStatusState
} from "../user_status/user_status";
import {
    NavigationFunctionState,
    RouteMatchState
} from "../../../routing/application_global_routing";
import {ApplicationRoutes} from "../../../routing/application_routes";
import {faExclamation} from "@fortawesome/free-solid-svg-icons";
import {
    DialogPopup,
    DialogPopupProps
} from "../../global_components/application_global_layer/popups/built_in/dialog_popup/dialog_popup";
import {CognitoManager} from "../../../../server_communication/server_modules/cognito_client";
import {
    GlobalNotificationsInterfaceState
} from "../../global_components/application_global_layer/notifications/notifications";
import {GlobalPopupsInterfaceState} from "../../global_components/application_global_layer/popups/popups";

export interface statusPolicy {
    minimumStatus?: UserStatus,
    maximumStatus?: UserStatus,
    invalidStatuses?: UserStatus[],
    matchesRoute?: string,
    failBehaviorOverrides?: {[s:number]: () => void},
}

export const StatusPolicyState: globalStateDeclaration<statusPolicy> = ['STATUS_POLICY', {} as statusPolicy];

export const StatusPolicyHandler = React.memo( () => {

    const [global_notifications_interface, setGlobalNotificationInterface] = useGlobalState(GlobalNotificationsInterfaceState);
    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [route_match, setRouteMatch] = useGlobalState(RouteMatchState);
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const [user_status, setUserStatus] = useGlobalState(UserStatusState);
    const [previous_user_status, setPreviousUserStatus] = useGlobalState(PreviousUserStatusState);

    const [status_policy, setStatusPolicy] = useGlobalState(StatusPolicyState);

    const statusPolicyFailDefaultBehavior: {[s:number]: () => void} = {
        [UserStatus.UNKNOWN]: () => {},
        [UserStatus.GUEST]: useCallback(() => {
            if (previous_user_status >= UserStatus.LOGGED_IN) {
                global_popups_interface.pushPopup({
                    popupComponent: DialogPopup,
                    additionalProps: {
                        title: 'You have been logged out',
                        text: 'We are just playing it safe. Log back in to continue your session.',
                        primaryButton: {
                            caption: 'Log In',
                            behavior: async () => {
                                if (await CognitoManager.getInstance().attemptLogIn())
                                    return;
                                navigate_function(ApplicationRoutes.IDENTITY, {}, {'choose': 'login'});
                            }
                        }
                    } as DialogPopupProps,
                })
            } else {
                navigate_function(ApplicationRoutes.HOME);
            }
        }, [previous_user_status, navigate_function, global_popups_interface]),
        [UserStatus.LOGGED_IN]: useCallback(() => {
            navigate_function(ApplicationRoutes.PROFILE);
        }, [navigate_function]),
        [UserStatus.UNVERIFIED]: useCallback(() => {
            navigate_function(ApplicationRoutes.VERIFICATION);
            global_notifications_interface.pushNotification({
                title: "Verification Needed",
                text: "Your account requires verification.",
                icon: faExclamation,
                duration: 10
            });
        }, [global_notifications_interface, navigate_function]),
        [UserStatus.MISSING_ATTRIBUTES]: useCallback(() => {
            navigate_function(ApplicationRoutes.PROFILE);
            global_notifications_interface.pushNotification({
                title: "Missing Account Information",
                text: "Some required attributes are missing from your account information.",
                icon: faExclamation,
                duration: 10
            });
        }, [global_notifications_interface, navigate_function]),
        [UserStatus.FULLY_APPROVED]: useCallback(() => {
            navigate_function(ApplicationRoutes.APP);
        }, [navigate_function]),
    }

    useEffect(() => {
        checkStatusPolicy();
    }, [user_status, status_policy, route_match]);


    const checkStatusPolicy = useCallback(() => {

        if (user_status === UserStatus.UNKNOWN) return;

        if (status_policy.matchesRoute !== undefined && !route_match(status_policy.matchesRoute)) return

        if ((status_policy.minimumStatus !== undefined && user_status < status_policy.minimumStatus) ||
            (status_policy.maximumStatus !== undefined && user_status > status_policy.maximumStatus) ||
            (status_policy.invalidStatuses !== undefined && status_policy.invalidStatuses.includes(user_status))
        ) {
            onPolicyCheckFailed();
        }
    }, [user_status, status_policy, route_match]);

    const onPolicyCheckFailed = useCallback(() => {
        let behavior = status_policy.failBehaviorOverrides !== undefined &&
            status_policy.failBehaviorOverrides[user_status] ||
            statusPolicyFailDefaultBehavior[user_status];
        behavior();
    }, [status_policy, user_status]);

    return (<></>);
});