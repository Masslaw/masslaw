import React, {Component, ReactNode, useEffect, useRef, useState} from "react";
import './css.css'
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {UsersManager} from "../../../infrastructure/user_management/users_manager";
import {UserPhoto} from "../user_photo/user_photo";
import {Outlet} from "react-router-dom";


export function MasslawLoggedInTop(props: {pageDisplayNode: ReactNode}) {

    const [is_menu_open, setMenuOpen] = useState(false);
    const menuOpenRef = useRef<HTMLButtonElement>(null);

    useEffect(() => {
        document.addEventListener('click', (event: MouseEvent) => {
            if (menuOpenRef.current && !menuOpenRef.current.contains(event.target as Node))
                setMenuOpen(false);
        });
    }, [menuOpenRef]);

    let userData = UsersManager.getInstance().getMyCachedUserData();

    let full_name = (userData.first_name + ' ' + userData.last_name);
    let email = userData.email;

    return (
        <>
            <div className={`top-main-container`}>
                <div className={`top-main-graphic`}>
                </div>
                <div className={`top-masslaw-icon`}
                     onClick={e => {ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.HOME)}}>
                </div>
                <div className={`top-masslaw-account-container`}>
                    <button className={`top-masslaw-account-button`}
                            ref={menuOpenRef}
                            onClick={() => { setMenuOpen(true) }}>
                        <UserPhoto id={`top-masslaw-account-image-button`} size={34}/>
                    </button>
                    <div className={`top-masslaw-account-menu popup ${is_menu_open ? 'shown' : 'hidden'}`}>
                        <div className={`menu-account-container`}>
                            <div className={`top-masslaw-account-image-menu top-masslaw-account-image`} />
                            <div className={`top-account-menu-name`} ><p>{full_name}</p></div>
                            <div className={`top-account-menu-email`} ><p>{email}</p></div>
                        </div>
                        <div className={`top-menu-divider`} />
                        <button className={`top-menu-button`}
                                onClick={() => {
                                    ApplicationRoutingManager
                                        .getInstance().navigateToRoute(ApplicationRoutes.PROFILE)
                                }}>Profile</button>
                        <button className={`top-menu-button`}
                                onClick={() => {}}>Settings</button>
                        <div className={`top-menu-divider`} />
                        <button className={`top-menu-button`}
                                onClick={() => {
                                    ApplicationRoutingManager
                                        .getInstance().navigateToRoute(ApplicationRoutes.DASHBOARD)
                                }}>Dashboard</button>
                        <div className={`top-menu-divider`} />
                        <button className={`top-menu-button`}
                                onClick={() => {
                                    ApplicationRoutingManager
                                        .getInstance().navigateToRoute(ApplicationRoutes.LOGOUT)
                                }}>Log Out</button>
                    </div>
                </div>
            </div>
            <div className={'page-display'}>
                {props.pageDisplayNode}
            </div>
        </>
    )
}