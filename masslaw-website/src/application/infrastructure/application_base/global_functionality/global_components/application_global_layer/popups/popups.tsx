import React, {useCallback, useContext, useEffect, useState} from "react";
import './css.css'
import {
    globalStateDeclaration,
    useGlobalState
} from "../../../global_states";

interface globalPopupsInterface {
    pushPopup: (entry: PopupEntry) => void,
    closeCurrentPopup: () => void,
}

interface PopupEntry {
    popupComponent: PopupComponent,
    additionalProps: any,
    onClose?: () => void,
}

export const GlobalPopupsInterfaceState: globalStateDeclaration<globalPopupsInterface> = ['GLOBAL_POPUPS_INTERFACE_KEY', {} as globalPopupsInterface];

export function ApplicationGlobalLayerPopups() {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [popupStack, setPopupStack] = useState([] as PopupEntry[]);
    const [currentPopupCloseBehavior, setCurrentPopupCloseBehavior] = useState<()=>void>(() => {});

    const renderCurrentPopup = useCallback(() => {
        if (!popupStack.length) return <></>;
        const currentPopupEntry = popupStack[popupStack.length - 1];
        const CurrentPopupComponent = currentPopupEntry.popupComponent;
        const currentPopupProps = currentPopupEntry.additionalProps;
        return <CurrentPopupComponent
            {...currentPopupProps}
            setOnCloseBehavior={setCurrentPopupCloseBehavior}
        />;
    }, [popupStack]);

    const closeCurrentPopup = () => {
        try { currentPopupCloseBehavior(); } catch (e) { }
        setPopupStack((currentStack) => {
            const currentPopupEntry = currentStack[0];
            if (currentPopupEntry.onClose) currentPopupEntry.onClose();
            return [...currentStack.slice(1)]
        });
        setCurrentPopupCloseBehavior(()=>{}); // reset the close behavior
    }

    const pushPopup = (entry: PopupEntry) => {
        setPopupStack((prev) => [entry, ...prev]);
    }

    useEffect(() => {
        setGlobalPopupsInterface({
            pushPopup: pushPopup,
            closeCurrentPopup: closeCurrentPopup,
        });
    }, []);

    return (<>
        {popupStack.length > 0 ? <>
            <div className={'global-popup-background-catch-clicks'}
                 style={{
                 }}>
                <div className={'global-popup-component-container'}>
                    <div className={'global-popup-component-container-inner'}>
                        {renderCurrentPopup()}
                    </div>
                </div>
            </div>
        </> : <>
        </>}
    </>);
}


export interface PopupComponentProps{
    setOnCloseBehavior: (behavior: () => void) => void,
}
export type PopupComponent = React.FC<PopupComponentProps & any>;
