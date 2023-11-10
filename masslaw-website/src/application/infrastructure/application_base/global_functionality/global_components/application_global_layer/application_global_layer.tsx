import React, {useCallback, useContext, useEffect, useState} from "react";
import {ApplicationGlobalLayerPopups} from "./popups/popups";
import {ApplicationGlobalLayerNotifications} from "./notifications/notifications";

export function ApplicationGlobalLayer() {

    return (<>
        <ApplicationGlobalLayerPopups />
        <ApplicationGlobalLayerNotifications />
    </>);
}
