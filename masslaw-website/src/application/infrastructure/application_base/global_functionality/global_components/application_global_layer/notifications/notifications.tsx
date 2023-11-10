import React, {useCallback, useContext, useEffect, useState} from "react";
import './css.css'
import {globalStateDeclaration,useGlobalState} from "../../../global_states";
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTimes} from "@fortawesome/free-solid-svg-icons";
import {MasslawButton, MasslawButtonTypes} from "../../../../../../shared/components/masslaw_button/masslaw_button";


interface GlobalNotificationsInterface {
    pushNotification: (entry: NotificationEntry) => void,
    closeCurrentNotification: () => void,
}

interface NotificationEntry {
    title: string,
    text: string,
    icon?: IconProp,
    onClose?: () => void,
    duration?: number,
}

export const GlobalNotificationsInterfaceState: globalStateDeclaration<GlobalNotificationsInterface> = ['GLOBAL_NOTIFICATIONS_INTERFACE'];

export function ApplicationGlobalLayerNotifications() {

    const [notificationStack, setNotificationStack] = useState([] as NotificationEntry[]);
    const [currentNotificationCloseBehavior, setCurrentNotificationCloseBehavior] = useState<()=>void>(() => {});

    const [global_notifications_interface, setGlobalNotificationsInterface] = useGlobalState(GlobalNotificationsInterfaceState);

    const renderCurrentNotification = useCallback(() => {
        if (!notificationStack.length) return <></>;
        const currentNotificationEntry = notificationStack[notificationStack.length - 1];
        return (<>
            <GlobalNotification
                entry={currentNotificationEntry}
                close={closeCurrentNotification}
            />
        </>);
    }, [notificationStack]);

    const closeCurrentNotification = useCallback(() => {
        try { currentNotificationCloseBehavior(); } catch (e) { }
        setNotificationStack((currentStack) => {
            const currentNotificationEntry = currentStack[0];
            if (currentNotificationEntry && currentNotificationEntry.onClose) currentNotificationEntry.onClose();
            return [...currentStack.slice(1)]
        });
        setCurrentNotificationCloseBehavior(()=>{}); // reset the close behavior
    }, []);

    const pushNotification = useCallback((entry: NotificationEntry) => {
        setNotificationStack((prev) => [entry, ...prev]);
    }, [] );

    useEffect(() => {
        setGlobalNotificationsInterface({
            pushNotification: pushNotification,
            closeCurrentNotification: closeCurrentNotification,
        });
    }, []);

    return (<>
        {notificationStack.length > 0 ? <>
            {renderCurrentNotification()}
        </> : <>
        </>}
    </>);
}

function GlobalNotification(props: {
    entry: NotificationEntry,
    close: () => void,
}) {

    if (props.entry.duration) {
        setTimeout(props.close, props.entry.duration * 1000);
    }

    return <div style={{width: '100%', height: '100%'}}>
        <div className={'global-notification'} >
            {
                props.entry.icon &&
                <div className={'global-notification-icon'}>
                    <FontAwesomeIcon icon={props.entry.icon}/>
                </div>
            }
            <div className={'global-notification-content'}>
                <div className={'global-notification-title'}>{props.entry.title}</div>
                <div className={'global-notification-text'}>{props.entry.text}</div>
            </div>
            <div className={'global-notification-close-button'}>
                <MasslawButton
                    caption={''}
                    icon={faTimes}
                    onClick={() => props.close()}
                    size={{w: 60, h: 60}}
                    buttonType={MasslawButtonTypes.CLEAR}
                />
            </div>
        </div>
    </div>
}
