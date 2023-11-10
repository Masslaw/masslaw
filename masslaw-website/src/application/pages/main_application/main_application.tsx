import React, {useContext, useEffect} from 'react';
import {Outlet} from "react-router-dom";
import {MasslawLoggedInTop} from "../../shared/components/masslaw_logged_in_top/masslaw_logged_in_top";
import {NavigationFunctionState,RouteMatchState} from "../../infrastructure/application_base/routing/application_global_routing";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../infrastructure/application_base/routing/application_page_renderer";
import {ApplicationRoutes} from "../../infrastructure/application_base/routing/application_routes";
import {
    useGlobalState,
} from "../../infrastructure/application_base/global_functionality/global_states";


export const MainApplication: ApplicationPage = (props: ApplicationPageProps) => {

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const [route_match_function, setRoutMatchFunction] = useGlobalState(RouteMatchState);

    useEffect(() => {
        if (route_match_function(ApplicationRoutes.APP)) {
            navigate_function(ApplicationRoutes.DASHBOARD);
        }
    }, [navigate_function, route_match_function]);

    return (
        <MasslawLoggedInTop pageDisplayNode={
            <Outlet />
        } />
    );
}
