import React from "react";

import './css.css';


export function UserPhoto(props: {id?: string, size: number}) {
    return (
        <>
            <div className={`masslaw-account-image`}
                 id={props.id}
                 style={{width: `${props.size}px`, height: `${props.size}px`, borderRadius: `25%`}} />
        </>
    )
}