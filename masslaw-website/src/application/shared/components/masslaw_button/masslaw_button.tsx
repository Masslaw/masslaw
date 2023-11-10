import React from "react";

import './css.css'
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {faCheckCircle, faExclamationCircle} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export enum MasslawButtonTypes {
    MAIN = 'main-button',
    SECONDARY = 'secondary-button',
    TEXTUAL = 'textual-button',
}

export function MasslawButton(props: {
    caption: string,
    icon?: IconProp,
    onClick: React.MouseEventHandler<HTMLButtonElement>,
    size?: {w: number, h: number},
    buttonType?: MasslawButtonTypes,}) {

    let size = props.size || {w: 120, h: 30};

    return (
        <>
            <button className={`masslaw-generic-button ${props.buttonType || MasslawButtonTypes.MAIN}`}
                    onClick={e => {
                        e.preventDefault();
                        props.onClick(e);
                    }}
                    style={{
                        width: `${size.w}px`,
                        height: `${size.h}px`,
                        fontSize: `${Math.floor(size.h / 2.5)}px`,
                    }}>
                {props.icon ?
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
            </button>
        </>
    )
}