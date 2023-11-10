import React, {useContext, useEffect, useState} from "react";
import {
    statusPolicy,StatusPolicyState
} from "../global_functionality/global_logic/status_policy_handler/status_policy_handler";
import {useGlobalState} from "../global_functionality/global_states";

export function ApplicationPageRenderer(props: {
    pageComponent: ApplicationPage,
    preLoadFunction?: () => Promise<void>,
    statusPolicy?: statusPolicy,
}) {

    const [status_policy, setStatusPolicy] = useGlobalState(StatusPolicyState);

    const [pageProps, setPageProps] = useState({} as ApplicationPageProps);

    const [page_loaded, setPageLoaded] = useState(false);

    const preLoad = async () => {
        setPageLoaded(false);
        await (props.preLoadFunction && props.preLoadFunction());
        setPageLoaded(true);
    }

    useEffect(() => {
        preLoad();
    }, []);

    useEffect(() => {
        if (props.statusPolicy === undefined) return;
        setStatusPolicy(props.statusPolicy);
    },[props.statusPolicy]);

    return <>
        {page_loaded && <props.pageComponent {...pageProps} />}
    </>
}


export interface ApplicationPageProps { }
export type ApplicationPage = React.FC<ApplicationPageProps>;