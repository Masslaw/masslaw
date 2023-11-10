import React, {useCallback, useEffect} from "react";
import {globalStateDeclaration, useGlobalState} from "../../global_states";
import {UserStatusManager} from "../../../../user_management/user_status_manager";
import {UserStatus} from "../../../../user_management/user_status";

export const UserStatusState: globalStateDeclaration<UserStatus> = ['USER_STATUS', UserStatus.UNKNOWN];
export const PreviousUserStatusState: globalStateDeclaration<UserStatus> = ['PREVIOUS_USER_STATUS', UserStatus.UNKNOWN];

export const UserStatusListener = React.memo(() => {

    const [user_status, setUserStatus] = useGlobalState(UserStatusState);
    const [previous_user_status, setPreviousUserStatus] = useGlobalState(PreviousUserStatusState);

    const userStatusManager = UserStatusManager.getInstance();

    const updateUserStatus = useCallback((status: UserStatus) => {
        if (status == UserStatus.UNKNOWN) return;
        if (status === user_status) return;
        setPreviousUserStatus(user_status);
        setUserStatus(status);
        console.log('User Status Updated :: previous =',user_status,", current = ",status);
    }, [user_status, previous_user_status]);

    useEffect(() => {
        const handleVisibilityChange = (e: Event) => {
            const status = (e as CustomEvent<UserStatus>).detail;
            updateUserStatus(status);
        }
        document.addEventListener(userStatusManager.STATUS_CHANGED_EVENT_NAME, handleVisibilityChange);
        return () => document.removeEventListener(userStatusManager.STATUS_CHANGED_EVENT_NAME, handleVisibilityChange);
    }, []);

    useEffect(() => {
        userStatusManager.getUserStatus().then(s => {
            updateUserStatus(s)
        });
    }, []);

    return (<></>);
});