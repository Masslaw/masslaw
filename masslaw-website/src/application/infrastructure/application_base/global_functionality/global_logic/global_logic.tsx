import {ApplicationVisibility} from "./application_visibility/application_visibility";
import {UserStatusListener} from "./user_status/user_status";
import {StatusPolicyHandler} from "./status_policy_handler/status_policy_handler";
import React from "react";

export const GlobalLogic = React.memo(() => {
    return <>
        <ApplicationVisibility />
        <StatusPolicyHandler />
        <UserStatusListener />
    </>
});