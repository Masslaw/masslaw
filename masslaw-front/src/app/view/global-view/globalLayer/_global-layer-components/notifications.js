import {model} from "../../../../model/model";
import React, {useEffect} from "react";
import styled, {keyframes} from "styled-components";
import {SVG_PATHS} from "../../../config/svgPaths";

const notificationTotalUpTime = 7000;
const slideDuration = 300;

export function pushNotification(notificationData) {
    if (notificationData.id && model.application.view.state.notificationsQueue.find(notification => notification.id === notificationData.id)) return;
    model.application.view.state.notificationsQueue.push(notificationData);
}

export function ApplicationNotifications(props) {

    const [s_displayedNotification, setDisplayedNotification] = React.useState(<></>);

    let uniqueIdentifier = 0;
    useEffect(() => {
        const modelStateManager = model.services['modelStateManager'];
        modelStateManager.listenToModelChange('$.application.view.state.notificationsQueue', notificationsQueue => {
            console.log("Notifications: ", notificationsQueue);
            if (notificationsQueue.length === 0) {
                setDisplayedNotification(<></>);
                return;
            };
            const notificationElement = <Notification
                key={++uniqueIdentifier}
                notificationData={notificationsQueue[0]}
                dismissBehavior={() => {
                    console.log("Notification dismissed");
                    model.application.view.state.notificationsQueue.shift();
                }}
            />
            setDisplayedNotification(notificationElement);
        });
    }, []);

    return <>
        {s_displayedNotification}
    </>
}

const slideUpAndDown = keyframes`
  0% {
    transform: translateY(200%); // Start below the screen
  }
  ${(slideDuration / notificationTotalUpTime * 100).toFixed(2)}% {
    transform: translateY(0); // Slide up
  }
  ${((notificationTotalUpTime - slideDuration) / notificationTotalUpTime * 100).toFixed(2)}% {
    transform: translateY(0); // Stay
  }
  100% {
    transform: translateY(200%); // Slide back down
  }
`;

const NotificationContainer = styled.div`
    position: absolute;
    bottom: 0;
    right: 0;
    width: 40vh;
    font-size: 1.75vh;
    background: #303030;
    border-radius: 0.5vh;
    margin: 2vh;
    animation: ${slideUpAndDown} ${notificationTotalUpTime}ms linear forwards;
    z-index: 100;
`

const NotificationDismissButton = styled.button`
    position: absolute;
    right: 0;
    top: 0;
    width: 1em;
    height: 1em;
    background: none;
    border: none;
    padding: 0;
    margin: 1em;
    pointer-events: all;
    
    svg {
        width: 1em;
        height: 1em;
        path {
            fill: white;
        }
    }
`

const NotificationTitle = styled.div`
    position: relative;
    font-size: 1em;
    width: calc(100% - 2em);
    height: 1em;
    line-height: 1em;
    margin: 1em;
    color: white;
`

const NotificationBody = styled.div`
    position: relative;
    font-size: 0.75em;
    width: calc(100% - 2em);
    line-height: 1.1em;
    margin: 1em;
    color: lightgrey;
`

function Notification(props) {

    useEffect(() => {
        const timeOutId = setTimeout(() => {
            props.dismissBehavior();
        }, notificationTotalUpTime);
        return () => clearTimeout(timeOutId);
    }, []);

    return <>
        <NotificationContainer>
            <NotificationDismissButton
                onClick={() => props.dismissBehavior()}
            >
                <svg viewBox={"0 0 1 1"}>
                    <path d={SVG_PATHS.crossMark} />
                </svg>
            </NotificationDismissButton>
            <NotificationTitle>
                {props.notificationData.title}
            </NotificationTitle>
            <NotificationBody>
                {props.notificationData.body}
            </NotificationBody>
        </NotificationContainer>
    </>
}