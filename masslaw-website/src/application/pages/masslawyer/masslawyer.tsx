import React, {useContext, useEffect, useState} from "react";
import {Outlet} from "react-router-dom";
import {MasslawLoggedInTop} from "../../shared/components/masslaw_logged_in_top/masslaw_logged_in_top";
import './css.css'
import {NavigationFunctionState, RouteMatchState
} from "../../infrastructure/application_base/routing/application_global_routing";
import {ApplicationRoutes} from "../../infrastructure/application_base/routing/application_routes";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../infrastructure/application_base/routing/application_page_renderer";
import {
    useGlobalState,
} from "../../infrastructure/application_base/global_functionality/global_states";


export const Masslawyer: ApplicationPage = (props: ApplicationPageProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const [route_match_function, setRoutMatchFunction] = useGlobalState(RouteMatchState);

    const [currentPageName, setCurrentPageName] = useState('Account');

    useEffect(() => {
        if (route_match_function(ApplicationRoutes.PROFILE))
            setCurrentPageName('Profile');
        else
            setCurrentPageName('Account');
    }, [route_match_function]);

    return (
        <>
            <MasslawLoggedInTop pageDisplayNode={
                <div className={'masslawyer-main-container'}>
                    <div className={'masslawyer-title-section'}>
                        <div>Masslawyer Account</div>
                    </div>
                    <div className={'masslawyer-page-and-main-menu'}>
                        <div className={'masslawyer-main-menu'}>
                            <div
                                className={'masslawyer-main-menu-item clickable'}
                                onClick={e => {navigate_function(ApplicationRoutes.PROFILE)}}
                            >{'Profile'}</div>
                            <div
                                className={'masslawyer-main-menu-item clickable'}
                                onClick={e => {navigate_function(ApplicationRoutes.PROFILE)}}
                            >{'Connections'}</div>
                            <div
                                className={'masslawyer-main-menu-item clickable'}
                                onClick={e => {navigate_function(ApplicationRoutes.PROFILE)}}
                            >{'Settings'}</div>
                        </div>
                        <div className={'page-container'}>
                            <div className={'masslawyer-page-title page-title'}>{currentPageName}</div>
                            <div className={'page-content'}>
                                <Outlet />
                            </div>
                        </div>
                    </div>
                </div>
            } />
        </>
    )
}