import React, {useContext, useEffect, useState} from "react";
import {
    globalStateDeclaration,
    useGlobalState
} from "../../global_states";
import {GlobalPopupsInterfaceState} from "../../global_components/application_global_layer/popups/popups";

export const ApplicationVisibilityState: globalStateDeclaration<boolean> = ['APPLICATION_VISIBILITY'];

export const ApplicationVisibility = React.memo(() => {

    const [application_visibility, setApplicationVisibility] = useGlobalState(ApplicationVisibilityState);

    const [page_visible, setPageVisible] = useState(false);

    useEffect(() => {
        const handleVisibilityChange = () => {
            setPageVisible(document.visibilityState === 'visible');
        }
        document.addEventListener('visibilitychange', handleVisibilityChange);
        return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
    }, []);

    useEffect(() => {
        setApplicationVisibility(page_visible);
    }, [page_visible]);

    return (<></>);
});