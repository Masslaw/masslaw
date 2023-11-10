import React from 'react';
import {useNavigate} from 'react-router-dom';
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {UserStatus} from "../../../infrastructure/user_management/user_status";
import {PageProtector, StatusConditionType} from "../../../infrastructure/user_management/page_protector";

ApplicationRoutingManager.getInstance().setRoutePreloadFunction(ApplicationRoutes.HOME, () => {
    PageProtector.getInstance().updateStatusCondition(UserStatus.GUEST, StatusConditionType.MAXIMUM, null);
    return true;
});

export function Home() {
    let navigate = useNavigate()
    return (
        <>
            <button onClick={e => {e.preventDefault(); navigate(ApplicationRoutes.IDENTITY)}}></button>
        </>
    );
}
