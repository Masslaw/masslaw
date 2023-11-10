import React, {useState} from "react";

import './css.css'
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {MasslawButton, MasslawButtonTypes} from "../masslaw_button/masslaw_button";
import {faEllipsisV} from "@fortawesome/free-solid-svg-icons";

export function MasslawEllipsisMenu(props: {
    menuItems: {
        caption: string,
        icon?: IconProp,
        onClick: () => void,
        color?: string
    }[],
    buttonSize?: {w: number, h: number}
}) {

    const [is_menu_open, setIsMenuOpen] = useState(false);

    return (
        <>
            <MasslawButton
                caption={''}
                icon={faEllipsisV}
                onClick={() => setIsMenuOpen(!is_menu_open)}
                buttonType={MasslawButtonTypes.CLEAR}
                size={props.buttonSize}
            />
            <div className={`masslaw-ellipsis-menu popup ${is_menu_open ? 'shown' : 'hidden'}`}>
                {
                    props.menuItems.map((item, key) => {
                        return (
                            <div
                                key={key}
                                className={'masslaw-ellipsis-menu-item clickable'}
                                onClick={() => item.onClick()}
                                style={{color: item.color || 'var(--masslaw-dark-text-color)'}}
                            >
                                <div className={'masslaw-ellipsis-menu-item-caption'}>{item.caption}</div>
                                {
                                    item.icon ?
                                    <div className={'masslaw-ellipsis-menu-item-icon-container'}>
                                        <FontAwesomeIcon icon={item.icon} />
                                    </div>
                                        :
                                    <></>
                                }
                            </div>
                        )
                    })
                }
            </div>
        </>
    )
}