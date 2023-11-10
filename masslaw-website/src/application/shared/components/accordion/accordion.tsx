import React, { useState } from 'react';
import './css.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faAngleDown, faAngleRight} from "@fortawesome/free-solid-svg-icons";

export function Accordion(props: {
    title: string;
    component: React.ReactNode;
}) {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="accordion">
            <div className="accordion-header clickable" onClick={
                (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    setIsOpen(prev => !prev);
                }
            }>
                <FontAwesomeIcon
                    icon={isOpen && faAngleDown || faAngleRight}
                />
                <span> </span>
                {props.title}
            </div>
            {isOpen && <div className="accordion-content">{props.component}</div>}
        </div>
    );
};