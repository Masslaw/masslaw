import React from 'react';

import {ApplicationRouter} from "./routing/application_router";

function RunBaseCode() {
    console.debug("Running")
}

export function Base() {
    RunBaseCode()
    return (
        <>
            <ApplicationRouter/>
        </>
    )
}