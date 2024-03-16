import styled from "styled-components";
import React, {useEffect} from "react";
import {SVG_PATHS} from "../../../config/svgPaths";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "../../../components/loadingIcon";

const LoadingScreenBackground = styled.div`
    display: ${({displaying}) => displaying === "true" ? "block" : "none"};
    position: absolute;
    width: 100%;
    height: 100%;
    background: black;
    padding: 0;
    margin: 0;
    z-index: 1000;
    pointer-events: all;
`

const LoadingScreenLogo = styled.div`
    position: absolute;
    width: 20vh;
    height: 20vh;
    left: calc(50vw - 10vh);
    top: 40vh;
    
    svg {
        width: 20vh;
        height: 20vh;
        background: none;
    }
    
    path {
        stroke-width: 5;
        stroke: white;
        fill: white;
        filter: drop-shadow(0 0 30px gold);
    }
`

const LoadingIconContainer = styled.div`
    position: absolute;
    width: 5vh;
    height: 5vh;
    top: calc(50% + 15vh);
    left: 50%;
    transform: translate(-50%, -50%);
`

export function LoadingScreen(props) {

    const [s_loading, setLoading] = useModelValueAsReactState("$.application.view.state.loading");

    useEffect(() => {
        const loadingStates = [];
        for (const state in s_loading) if (s_loading[state]) loadingStates.push(state);
        console.log(`Loading states:`, loadingStates);
    }, [s_loading]);

    return <LoadingScreenBackground displaying={`${Object.values(s_loading).reduce((a, b) => a || b, false)}`}>
        <LoadingScreenLogo>
            <svg viewBox={"-50 0 2100 1000"}>
                <path d={SVG_PATHS.logo}/>
            </svg>
        </LoadingScreenLogo>
        <LoadingIconContainer>
            <LoadingIcon/>
        </LoadingIconContainer>
    </LoadingScreenBackground>
}