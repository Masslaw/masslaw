import React, { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheckCircle, faExclamationCircle, faEye, faEyeSlash } from "@fortawesome/free-solid-svg-icons";

import "./css.css"

export function InputField(props: {
    value: string,
    onChange: React.EventHandler<any>,
    id?: string,
    label?: string,
    placeHolder?: string,
    message?: string,
    valid?: string,
    type?: string,
    hasValidationIcon?: boolean,
    tooltip?: React.ReactNode,
    locked?: boolean,
    isParagraph?: boolean,
    hasPasswordShow?: boolean,}) {

    const [isPasswordVisible, setPasswordVisible] = useState(false);

    const togglePasswordVisibility = () => {
        setPasswordVisible(!isPasswordVisible);
    };

    return (
        <div id={props.id}
             className={`input-field-container ${props.valid || ''} ${props.locked ? 'locked' : ''}`}>
            <div className={`input-field-input-container`}>
                <div className={`input-field-label-outside`}>{props.label || ''}</div>
                <div className={`input-field-input`}
                     style={(props.hasValidationIcon) ? {width: 'calc(100% - 30px)'} : {width: '100%'}}>
                    {
                        props.isParagraph ?
                        <>
                            <textarea
                                dir={'auto'}
                                value={props.value}
                                placeholder={props.placeHolder || ''}
                                spellCheck="false"
                                onChange={e => {
                                    e.preventDefault();
                                    props.onChange(e);
                                }}
                                autoComplete={props.type === "password" ? "off" : "on"}
                            />
                        </>
                        :
                        <>
                            <input
                                dir={'auto'}
                                type={props.type === "password" && !isPasswordVisible ? "password" : "text"}
                                value={props.value}
                                placeholder={props.placeHolder || ''}
                                spellCheck="false"
                                onChange={e => {
                                    e.preventDefault();
                                    props.onChange(e);
                                }}
                                autoComplete={props.type === "password" ? "off" : "on"}
                            />
                        </>
                    }
                    {props.type === "password" && props.hasPasswordShow && (
                        <FontAwesomeIcon icon={isPasswordVisible ? faEyeSlash : faEye}
                                         onClick={togglePasswordVisibility}
                                             className={`password-toggle-icon`} />)}
                </div>
                <div className={`input-field-input-validation`}></div>
                <div className={`input-message`}>{props.message || ''}</div>
                <FontAwesomeIcon icon={(props.valid === 'valid') ? faCheckCircle : faExclamationCircle}
                                 style={(props.hasValidationIcon) ? {} : {display: 'none'}}
                                 className={`input-validation-icon`} />
                <div className={`popup input-field-tooltip ${props.tooltip ? 'enabled shown' : ''}`}>{props.tooltip}</div>
            </div>
        </div>
    )
}