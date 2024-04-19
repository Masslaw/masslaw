import {model} from "../../../../model/model";
import React, {useEffect} from "react";
import styled, {keyframes} from "styled-components";
import {SVG_PATHS} from "../../../config/svgPaths";

export function pushPopup(popupData) {
    console.log("push popup", popupData)
    if (popupData.id && model.application.view.state.popupsQueue.find(popup => popup.id === popupData.id)) return;
    model.application.view.state.popupsQueue.push(popupData);
}

export function ApplicationPopups(props) {

    const [s_displayedPopup, setDisplayedPopup] = React.useState(<></>);

    let uniqueIdentifier = 0;
    useEffect(() => {
        const modelStateManager = model.services['modelStateManager'];
        modelStateManager.listenToModelChange('$.application.view.state.popupsQueue', popupsQueue => {
            console.log("Popups: ", popupsQueue);
            if (popupsQueue.length === 0) {
                setDisplayedPopup(<></>);
                return;
            };
            const popupElement = <Popup
                key={++uniqueIdentifier}
                popupData={popupsQueue[0]}
                dismissBehavior={() => {
                    console.log("Popup dismissed");
                    model.application.view.state.popupsQueue.shift();
                }}
            />
            setDisplayedPopup(popupElement);
        });
    }, []);

    return <>
        {s_displayedPopup}
    </>
}

const PopupCatchClicks = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: all;
    background: rgba(0, 0, 0, 0.5);
    z-index: 100;
`

const PopupContainer = styled.div`
    position: absolute;
    max-width: calc(100% - 16px);
    max-height: calc(100% - 16px);
    overflow: auto;
    border-radius: 12px;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 100;
    pointer-events: all;
    &::-webkit-scrollbar { display: none; }
`

const PopupDismissButton = styled.button`
    position: fixed;
    right: 0;
    top: 0;
    width: 1em;
    height: 1em;
    background: none;
    border: none;
    padding: 0;
    margin: 1em;
    pointer-events: all;
    z-index: 101;
    
    svg {
        width: 1em;
        height: 1em;
        path {
            fill: white;
        }
    }
`

function Popup(props) {

    return <>
        <PopupCatchClicks />
        <PopupContainer>
            <PopupDismissButton
                onClick={() => props.dismissBehavior()}
            >
                <svg viewBox={"0 0 1 1"}>
                    <path d={SVG_PATHS.crossMark}/>
                </svg>
            </PopupDismissButton>
            <props.popupData.component
                dismiss={() => props.dismissBehavior()}
                {...props.popupData.componentProps}
            />
        </PopupContainer>
    </>
}