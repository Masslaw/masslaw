import React, {MouseEventHandler} from "react";
import LoadingIcon from "../loading_icon/loading_icon";

import './css.css';

export function LoadingButton(props: {
        clickable: boolean,
        onClick: MouseEventHandler<HTMLButtonElement>,
        size?: {h: number, w: number}
        id?: string,
        loading?: boolean,
        caption?: string
    }) {

    let onClickInternal : MouseEventHandler<HTMLButtonElement> = (e) => {
        e.preventDefault();
        props.onClick(e);
    }

    return (
        <>
            <button id={props.id}
                    className={`loading_button ${props.clickable ? 'clickable' : 'unclickable'}`}
                    style={props.size != null ? {
                        width: `${props.size.w}px`,
                        height: `${props.size.h}px`,
                        fontSize: `${Math.floor(props.size.h / 2.5)}px`} : {}}
                    onClick={onClickInternal}>
                <span style={{ display: `${(props.loading) ? 'none' : 'block'}`}}>{(props.caption != null) ? props.caption : ''}</span>
                <div style={{ display: `${(props.loading) ? 'block' : 'none'}`,
                    position: 'absolute',
                    top: '0',
                    left: '0',
                    width: '100%',
                    height: '100%'}}>
                    <LoadingIcon ballSize={props.size ? (props.size.h) / 3.33 : 15}/>
                </div>
            </button>
        </>
    )
}