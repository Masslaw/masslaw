import React from 'react';

import {ApplicationGlobalStates} from "./global_functionality/global_states";
import {ApplicationRouter} from "./routing/application_router";
import {GlobalLogic} from "./global_functionality/global_logic/global_logic";
import {GlobalComponents} from "./global_functionality/global_components/global_components";

export function Base() {
    return (
        <>
            <ApplicationGlobalStates>
                <ApplicationRouter/>
                <GlobalComponents/>
                <GlobalLogic/>
            </ApplicationGlobalStates>
        </>
    )
}