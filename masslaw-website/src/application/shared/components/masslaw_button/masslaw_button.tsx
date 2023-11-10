import React from "react";

import './css.css'
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {LoadingIcon} from "../loading_icon/loading_icon";

export enum MasslawButtonTypes {
    MAIN = 'main-button',
    SECONDARY = 'secondary-button',
    TEXTUAL = 'textual-button',
    CLEAR = 'clear-button',
    DESTRUCTIVE = 'destructive-button'
}

export function MasslawButton(props: {
    caption: string,
    icon?: IconProp,
    loading?: boolean
    clickable?: boolean
    onClick: React.MouseEventHandler<HTMLButtonElement>,
    size?: {w: number, h: number},
    buttonType?: MasslawButtonTypes,
    fontSize?: number
}) {

    let size = props.size || {w: 120, h: 30};

    return (
        <>
            <button className={`masslaw-generic-button clickable ` +
                `${props.buttonType || MasslawButtonTypes.MAIN} ` +
                `${props.clickable === false && 'click-blocked' || ''} `}
                    onClick={e => {
                        e.preventDefault();
                        if (props.loading || props.clickable === false) return;
                        props.onClick(e);
                    }}
                    style={{
                        width: `${size.w}px`,
                        height: `${size.h}px`,
                        fontSize: `${props.fontSize || Math.floor(size.h / 2.5)}px`,
                    }}>
                {
                    props.loading ?
                    <LoadingIcon /> :
                    <>
                        {
                            props.icon ?
                                <>
                        <span>
                            <FontAwesomeIcon icon={props.icon}
                                             className={`masslaw-button-icon`}></FontAwesomeIcon>
                        </span>
                                    <span>{' '}</span>
                                </>:
                                <>
                                </>
                        }
                        <span>
                    {props.caption}
                </span>
                    </>
                }
            </button>
        </>
    )
}