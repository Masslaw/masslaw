import styled from "styled-components";
import {ApplicationRouter} from "./routing/applicaitonRouter";
import {ApplicationGlobalLayer} from "./global-view/globalLayer/applicationGlobalLayer";
import React from "react";
import {useModelValueAsReactState} from "../controller/functionality/model/modelReactHooks";


const Application = styled.div`
    width: 100%;
    height: 100%;
    font-family: sans-serif;
    color: white;
    background: black;
    
    & a {
        text-decoration: none;
    }

    & button {
        transition: 0.3s ease-out background-color, 0.3s ease-out color, 0.3s ease-out border-color, 0.3s ease-out box-shadow, 0.3s ease-out fliter;
        cursor: pointer;
        outline: none;
        pointer-events: auto;
        text-decoration: none;
    }

    & button:hover {
        transition-duration: 0s;
    }
    
    & h2 {
        font-weight: normal;
    }

    &::-webkit-scrollbar {
        width: 8px;
        height: 8px;
        z-index: 50;
    }

    &::-webkit-scrollbar-thumb {
        background-color: #ccc;
        border-radius: 5px;
        z-index: 50;
    }

    &::-webkit-scrollbar-thumb:hover {
        background-color: #aaa;
        z-index: 50;
    }

    &::-webkit-scrollbar-track {
        border-radius: 5px;
        z-index: 50;
    }

    &::-webkit-scrollbar-corner {
        background: none;
    }
`

export function ApplicationView(props) {
    const [s_applicationContextKey, _] = useModelValueAsReactState('$.application.contextKey')
    return <Application key={s_applicationContextKey}>
        <ApplicationGlobalLayer>
            <ApplicationRouter/>
        </ApplicationGlobalLayer>
    </Application>
}
