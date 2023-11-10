import React, {useEffect, useState} from "react";
import {UsersManager} from "../../infrastructure/user_management/users_manager";
import {Outlet} from "react-router-dom";
import {ApplicationRoutes} from "../../infrastructure/routing/application_routes";
import {ApplicationRoutingManager} from "../../infrastructure/routing/application_routing_manager";
import {UserStatus} from "../../infrastructure/user_management/user_status";
import {PageProtector, StatusConditionType} from "../../infrastructure/user_management/page_protector";
import {MasslawLoggedInTop} from "../../shared/components/masslaw_logged_in_top/masslaw_logged_in_top";

import './css.css'
import {LoadingElement} from "../../shared/components/loaded_element/loading_element";



ApplicationRoutingManager.getInstance().setRoutePreloadFunction(ApplicationRoutes.MASSLAWYER, async () => {
    currentRoute = ApplicationRoutingManager.getInstance().getCurrentRoute();
    if (currentRoute === ApplicationRoutes.MASSLAWYER) {
        ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.PROFILE);
        return false;
    }
    if (!PageProtector.getInstance().updateStatusCondition(UserStatus.LOGGED_IN, StatusConditionType.MINIMUM, null))
        return false;

    await UsersManager.getInstance().updateMyCachedUserData();

    return true;
});

let currentRoute : string | null = null;
let currentPageName = '';

ApplicationRoutingManager.getInstance().addOnLocationChangedCallback((newRoute: string) => {
    currentRoute = newRoute;
    switch (currentRoute) {
        case ApplicationRoutes.PROFILE:
            currentPageName = 'Profile';
            break;
    }
})

export function Masslawyer() {

    return (
        <>
            <MasslawLoggedInTop pageDisplayNode={
                <div className={'masslawyer-main-container'}>
                    <div className={'masslawyer-title-section'}>
                        <div>Masslawyer Account</div>
                    </div>
                    <div className={'masslawyer-main-menu'}>
                    </div>
                    <div className={'page-container'}>
                        <div className={'page-title'}>{currentPageName}</div>
                        <div className={'page-content'}>
                            <Outlet />
                        </div>
                    </div>
                </div>
            } />
        </>
    )
}