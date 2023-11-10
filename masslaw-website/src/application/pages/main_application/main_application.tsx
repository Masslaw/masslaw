import React from 'react';
import {PageProtector, StatusConditionType} from "../../infrastructure/user_management/page_protector";
import {UsersManager} from "../../infrastructure/user_management/users_manager";
import {Outlet} from "react-router-dom";
import {UserStatus} from "../../infrastructure/user_management/user_status";
import {ApplicationRoutingManager} from "../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../infrastructure/routing/application_routes";
import {MasslawLoggedInTop} from "../../shared/components/masslaw_logged_in_top/masslaw_logged_in_top";

ApplicationRoutingManager.getInstance().setRoutePreloadFunction(ApplicationRoutes.APP, () => {
    if (ApplicationRoutingManager.getInstance().getCurrentRoute() === ApplicationRoutes.APP)
        ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.DASHBOARD);
    PageProtector.getInstance().updateStatusCondition(UserStatus.FULLY_APPROVED, StatusConditionType.MINIMUM, null);
    UsersManager.getInstance().updateMyCachedUserData().then();
    return true;
});

export function MainApplication() {

    return (
        <MasslawLoggedInTop pageDisplayNode={
            <Outlet />
        } />
    );
}
