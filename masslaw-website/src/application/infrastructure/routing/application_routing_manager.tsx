import {ApplicationRoutes} from "./application_routes";
import {Outlet, useLocation, useNavigate} from "react-router-dom";
import React, {ReactNode, useEffect, useState} from "react";

export class ApplicationRoutingManager {
    private static _instance = new ApplicationRoutingManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (ApplicationRoutingManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }

    private _onLocationChangeMap : Map<ApplicationRoutes, CallableFunction> = new Map();
    private _currentRoute : ApplicationRoutes = ApplicationRoutes._;

    private _requestedRouteNavigationCheck = false;

    private _locationChangedCallbacks: Function[] = [];

    private static preLoadNavigationRequest: ApplicationRoutes | null = null;
    private static navigateTo = (route : ApplicationRoutes) => { this.preLoadNavigationRequest = route };

    public setRoutePreloadFunction(route: ApplicationRoutes, func: CallableFunction) {
        this._onLocationChangeMap.set(route, func);
    }

    public getCurrentRoute() : ApplicationRoutes{
        return this._currentRoute;
    }

    public navigateToRoute(route: ApplicationRoutes, params?: { [key: string]: string }){
        if (route === this.getCurrentRoute()) return;
        let _r = route as string;
        params = params || {};
        for (const key in (params || {})) _r = _r.replace(`:${key}`, params[key]);
        ApplicationRoutingManager.navigateTo(_r as ApplicationRoutes);
        this._requestedRouteNavigationCheck = true;
    }

    public addOnLocationChangedCallback(callback: Function) {
        this._locationChangedCallbacks.push(callback);
    }

    public removeOnLocationChangedCallback(callback: Function) {
        this._locationChangedCallbacks.splice(this._locationChangedCallbacks.indexOf(callback), 1);
    }

    public getComponent() : () => JSX.Element {
        return () => {
            const location = useLocation();
            const currentRoute = location.pathname as ApplicationRoutes;
            this.onLocationChange(currentRoute);

            const [navigateRoute, setNavigateRoute] = useState(currentRoute);
            const navigate = useNavigate();
            ApplicationRoutingManager.navigateTo = (route : ApplicationRoutes) => {
                setNavigateRoute(route);
                console.debug(`redirecting to ${route}`);
            };

            useEffect(() => {
                if (navigateRoute === currentRoute) return;
                navigate(navigateRoute);
                this.onLocationChange(currentRoute);
                console.debug(`redirected to ${navigateRoute}`);
            }, [navigateRoute]);

            useEffect(() => {
                if (currentRoute === ApplicationRoutes._)
                    ApplicationRoutingManager.navigateTo(ApplicationRoutes.HOME);
            }, [currentRoute, ApplicationRoutingManager.navigateTo]);

            useEffect(() => {
                if (ApplicationRoutingManager.preLoadNavigationRequest != null) {
                    ApplicationRoutingManager.navigateTo(ApplicationRoutingManager.preLoadNavigationRequest);
                    ApplicationRoutingManager.preLoadNavigationRequest = null;
                }
            }, [ApplicationRoutingManager.preLoadNavigationRequest, ApplicationRoutingManager.navigateTo]);

            return (<Outlet />);
        };
    }

    private onLocationChange(newRoute: ApplicationRoutes) {
        this._onLocationChangeMap.get(newRoute);
        if (this.getCurrentRoute() === newRoute) return;
        this._currentRoute = newRoute;
        this.callOnLocationChangedFunctionHierarchy();
        this._locationChangedCallbacks.forEach((f) => {
            try { f(this._currentRoute); } catch (e) {}
        })
    }

    private callOnLocationChangedFunctionHierarchy() {
        let configuredCallbackRoutesHierarchy: string[] = [];
        this._onLocationChangeMap.forEach((func, route) => {
            if (this._currentRoute.includes(route)) configuredCallbackRoutesHierarchy.push(route);
        });
        configuredCallbackRoutesHierarchy.sort((a:string, b:string) => a.length-b.length).forEach((level) => {
            let func = this._onLocationChangeMap.get(level as ApplicationRoutes);
            this._requestedRouteNavigationCheck = false;
            if (!func || !func() || this._requestedRouteNavigationCheck) return;
        });
    }
}
