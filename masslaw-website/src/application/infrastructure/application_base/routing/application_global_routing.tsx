import React, {useCallback, useContext, useEffect, useState} from "react";
import {ApplicationRoutes} from "./application_routes";
import {globalStateDeclaration, useGlobalState} from "../global_functionality/global_states";
import {Outlet, useLocation, useNavigate, useParams} from "react-router-dom";


export const NavigationFunctionState: globalStateDeclaration<
    (route: ApplicationRoutes, params?: {[key:string]: string}, queryStringParams?: {[key:string]: string}) => void> =
    ['NAVIGATION_FUNCTION', () => {}];
export const RouteMatchState: globalStateDeclaration<(path:  string) => boolean> = ['ROUTE_MATCH', () => false];
export const QueryStringParamsState: globalStateDeclaration<{[key:string]:string}> = ['QUERY_STRING_PARAMS', {}];


export function ApplicationGlobalRouting() {

    const [navigation_function, setNavigationFunction] = useGlobalState(NavigationFunctionState);

    const [route_match_function, setRoutMatchFunction] = useGlobalState(RouteMatchState);

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const navigate = useNavigate();
    const location = useLocation();
    let pathParams = useParams();

    const navigateFunction = useCallback((
        route: ApplicationRoutes,
        params?: {[key:string]: string},
        queryStringParams?: {[key:string]: string}
    ) => {

        let finalRoute: string = route;
        let _params = params || {};

        for (let key of Object.keys(_params))
            finalRoute = finalRoute.replace(`:${key}`, _params[key]);

        if (queryStringParams) {
            const searchParams = new URLSearchParams(queryStringParams).toString();
            finalRoute += '?' + searchParams;
        }

        navigate(finalRoute);
    }, [navigate]);

    const routeMatch = useCallback((route: string) => {
        let _params = {...pathParams};
        let path = Object.keys(_params).reduce((currentPath, key) => {
            return (String(currentPath)).replace(`:${key}`, pathParams[key] || '--');
        }, route || '');

        return location.pathname === path
    }, [navigate, location, pathParams]);

    const getSearchParamsFromUrl = () => {
        const searchParams = new URLSearchParams(location.search);
        let params: {[key:string]:string} = {};
        for(let pair of searchParams.entries()) {
            params[pair[0]] = pair[1];
        }
        return params;
    }

    useEffect(() => {
        const params = getSearchParamsFromUrl();
        setQueryStringParams(params);
    }, []);

    useEffect(() => {
        const searchParams = new URLSearchParams({...query_string_params});
        navigate(location.pathname + '?' + searchParams.toString(), { replace: true });
    }, [query_string_params]);

    useEffect(() => {
        setNavigationFunction(() => navigateFunction);
    }, [navigateFunction]);

    useEffect(() => {
        setRoutMatchFunction(() => routeMatch);
    }, [routeMatch]);

    return (<Outlet/>);
}