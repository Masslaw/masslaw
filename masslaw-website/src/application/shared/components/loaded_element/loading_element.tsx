import React, {ReactNode, useEffect, useState} from "react";
import {Outlet} from "react-router-dom";
import {Simulate} from "react-dom/test-utils";
import load = Simulate.load;
import {LoadingIcon} from "../loading_icon/loading_icon";

import './css.css'


export function LoadingElement(props: {
    loadingElement: ReactNode,
    loaded: boolean,
    loadingIconColor?: string}) {

    return (
        <>
            {
                props.loaded ? props.loadingElement :
                <div className={'loading-element-container'}>
                    <LoadingIcon color={props.loadingIconColor || 'var(--masslaw-dark-text-color)'}
                                 width={70}/>
                </div>
            }
        </>
    )
}