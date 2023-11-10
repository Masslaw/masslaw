import {GlobalPopupsInterfaceState, PopupComponent, PopupComponentProps} from "../../popups";
import './css.css'
import {
    MasslawButton,
    MasslawButtonTypes
} from "../../../../../../../../shared/components/masslaw_button/masslaw_button";
import {useContext, useState} from "react";
import {useGlobalState} from "../../../../../global_states";

export interface DialogPopupProps extends PopupComponentProps {
    title: string,
    text: string,
    primaryButton: {
        caption: string,
        behavior: () => Promise<void>
    },
    secondaryButton?: {
        caption: string,
        behavior: () => Promise<void>
    },
}
export const DialogPopup: PopupComponent = (props: DialogPopupProps) => {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);
    
    const [primary_button_loading, setPrimaryButtonLoading] = useState(false);
    const [secondary_button_loading, setSecondaryButtonLoading] = useState(false);
    
    return <div className={'dialog-popup-container'}>
        <div className={'dialog-popup-title'}>{props.title}</div>
        <div className={'dialog-popup-text'}>{props.text}</div>
        <div className={'dialog-popup-buttons'}>
            {
                props.secondaryButton &&
                <div className={'dialog-popup-secondary-button'}>
                    <MasslawButton
                        caption={props.secondaryButton.caption}
                        onClick={() => {
                            setSecondaryButtonLoading(true);
                            props.secondaryButton && props.secondaryButton.behavior().then(() => {
                                global_popups_interface.closeCurrentPopup()
                            })
                        }}
                        loading={secondary_button_loading}
                        clickable={!(primary_button_loading || secondary_button_loading)}
                        buttonType={MasslawButtonTypes.SECONDARY}
                        size={{w: 120, h: 30}}
                    />
                </div>
            }
            {
                <div className={'dialog-popup-primary-button'}>
                    <MasslawButton
                        caption={props.primaryButton.caption}
                        onClick={() => {
                            setPrimaryButtonLoading(true);
                            props.primaryButton && props.primaryButton.behavior().then(() => {
                                global_popups_interface.closeCurrentPopup()
                            })
                        }}
                        loading={primary_button_loading}
                        clickable={!(primary_button_loading || secondary_button_loading)}
                        buttonType={MasslawButtonTypes.MAIN}
                        size={{w: 120, h: 30}}
                    />
                </div>
            }
        </div>
    </div>
}