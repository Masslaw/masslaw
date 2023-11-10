import React, {MouseEventHandler, useEffect, useState} from "react";

import './css.css'
import {CognitoManager} from "../../../infrastructure/server_communication/cognito_client";
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {InputField} from "../../../shared/components/input_field/input_field";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheckCircle, faExclamationCircle} from "@fortawesome/free-solid-svg-icons";


let cognitoChangePasswordToolkit: { sendCode: any; attemptVerification: (verificationCode: string) => Promise<boolean>; } | null = null;

export function Password() {

    const [change_password_verify, setChangePasswordVerify] = useState(false);

    const [continue_button_message, setContinueMessage] = useState("");
    const [continue_button_loading, setContinueButtonLoading] = useState(false);
    const [submit_button_message, setSubmitButtonMessage] = useState('');

    const [email, setEmail] = useState(CognitoManager.getInstance().getLoggedInUserEmail());
    const [email_valid, setEmailValid] = useState(email ? 'valid' : '');
    const [email_message, setEmailMessage] = useState("");
    const [password, setPassword] = useState("");
    const [password_valid, setPasswordValid] = useState("");

    const [password_valid_length, setPasswordValidLength] = useState("");
    const [password_valid_number, setPasswordValidNumber] = useState("");
    const [password_valid_special, setPasswordValidSpecial] = useState("");
    const [password_valid_upper, setPasswordValidUpper] = useState("");
    const [password_valid_lower, setPasswordValidLower] = useState("");

    let EmailOnChange: React.ChangeEventHandler<HTMLInputElement>;
    let PasswordOnChange : React.ChangeEventHandler<HTMLInputElement>;

    EmailOnChange = (e) => {
        let new_value = (e.target as HTMLInputElement).value
        setEmail(new_value);
        let valid = ((/^[^\s@]+@[^\s@]+\.[^\s@]+$/).test(new_value));
        setEmailValid(valid ? 'valid' : 'invalid');
        setEmailMessage(valid ? '' : 'Invalid email');
    };

    PasswordOnChange = e => {
        let new_value = (e.target as HTMLInputElement).value
        setPassword(new_value);
        let valid = true;
        if (new_value.length < 8) { valid = false; setPasswordValidLength("invalid");
        } else { setPasswordValidLength("valid"); }

        if (!(/\d/).test(new_value)) { valid = false; setPasswordValidNumber("invalid");
        } else { setPasswordValidNumber("valid"); }

        if (!(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/).test(new_value)) { valid = false; setPasswordValidSpecial("invalid");
        } else { setPasswordValidSpecial("valid"); }

        if (!(/[A-Z]/).test(new_value)) { valid = false; setPasswordValidUpper("invalid");
        } else { setPasswordValidUpper("valid"); }

        if (!(/[a-z]/).test(new_value)) { valid = false; setPasswordValidLower("invalid");
        } else { setPasswordValidLower("valid"); }

        setPasswordValid(valid ? 'valid' : 'invalid');

        const VerifyPasswordInput = document.querySelector('#-password-verify-input input');
        if (VerifyPasswordInput) {
            VerifyPasswordInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    };

    async function continuePressed() {
        setContinueButtonLoading(true);
        cognitoChangePasswordToolkit = CognitoManager.getInstance().getForgotPasswordToolkit(email, password);
        if (await cognitoChangePasswordToolkit.sendCode()) setChangePasswordVerify(true);
        else setContinueMessage('An error occurred trying to continue this process.');
    }

    const [code, setCode] = useState('');
    const [input_valid, setInputValid] = useState('');
    const [submit_loading, setSubmitLoading] = useState(false);

    const lastResendTimeLocalStorageKey = 'last-verification-code-request-time';
    const numSecondsBetweenCodeResends = 60;
    const [time_to_allow_resend, setTimeToAllowResend] = useState(0);

    useEffect(() => {
        const intervalId = setInterval(() => {
            const now = new Date();
            let last_resend_time = parseInt(localStorage.getItem(lastResendTimeLocalStorageKey) || new Date().getTime().toString())
            let delta = now.getTime() - last_resend_time;
            setTimeToAllowResend(Math.max(0, numSecondsBetweenCodeResends - Math.floor(delta / 1000)));
        }, 1000);
        return () => clearInterval(intervalId);
    }, []);

    let onSubmit = async () => {
        setSubmitLoading(true);
        if (cognitoChangePasswordToolkit != null) {
            if (!await cognitoChangePasswordToolkit.attemptVerification(code)) {
                setSubmitLoading(false);
                setSubmitButtonMessage('An error occurred trying to verify your email.')
                return;
            }
            let loginToolkit = CognitoManager.getInstance().getLoginToolkit(() => {})
            await loginToolkit.loginDefault(email, password);
            setSubmitLoading(false);
            setSubmitButtonMessage('');
            ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes._);
            return;
        }
        setSubmitLoading(false);
        setSubmitButtonMessage('An error occurred trying to verify your email.');
    }

    let resendVerificationCode : MouseEventHandler<HTMLButtonElement> = async (e) => {
        e.preventDefault();
        localStorage.setItem(lastResendTimeLocalStorageKey, new Date().getTime().toString());
        if (time_to_allow_resend <= 0 && cognitoChangePasswordToolkit) {
            await cognitoChangePasswordToolkit.sendCode();
        }
    }

    return (
        <>
            <div className={'fill-parent main-background'}>
                <div className={`form-container`}>
                    <div className={`top-title`}>Change Password</div>
                    { !change_password_verify ?
                        <>
                            <form style={{height: '300px'}}>
                                <InputField placeHolder={'Email'}
                                            message={email_message}
                                            valid={email_valid}
                                            value={email}
                                            type={'text'}
                                            hasValidationIcon={true}
                                            onChange={EmailOnChange} />
                                <InputField placeHolder={'New Password'}
                                            message={''}
                                            valid={password_valid}
                                            value={password}
                                            type={'password'}
                                            hasValidationIcon={true}
                                            tooltip={<div className={`-password-qualifications`}>
                                                <PasswordValidation validation={password_valid_length}
                                                                    message={`Password is at least 8 characters long`} />
                                                <PasswordValidation validation={password_valid_number}
                                                                    message={`Password contains at least one number`} />
                                                <PasswordValidation validation={password_valid_special}
                                                                    message={`Password contains at least one special character`} />
                                                <PasswordValidation validation={password_valid_upper}
                                                                    message={`Password contains at least one upper-case letter`} />
                                                <PasswordValidation validation={password_valid_lower}
                                                                    message={`Password contains at least one lower-case letter`} />
                                            </div>}
                                            onChange={ PasswordOnChange }/>
                            </form>
                            <LoadingButton clickable={(email_valid ===  'valid' && password_valid === 'valid')}
                                           onClick={e => continuePressed()}
                                           loading={continue_button_loading}
                                           caption={'Continue'} />
                            <div className={`continue-button-message`}>{continue_button_message}</div>

                        </> :
                        <>
                            <div className={'dialog-text'}>
                                {`An email has been sent to ${email.replace(/^(.{2}).*?(@)/, (_, c1, c2) => c1 + "*".repeat((email || '').indexOf(c2) - 3) + c2)} containing a verification code. To verify your email, please provide it here:`}
                            </div>
                            <InputField id={'verification-code-input'}
                                        label={'Verification Code'}
                                        message={''}
                                        valid={input_valid}
                                        value={code}
                                        type={'text'}
                                        hasValidationIcon={false}
                                        tooltip={null}
                                        onChange={e => setCode(e.target.value)} />
                            <div className={`resend-verification-code`}>
                                <button className={(time_to_allow_resend <= 0) ? 'clickable' : 'unclickable'} onClick={resendVerificationCode}>
                                    {(time_to_allow_resend <= 0) ? `Resend Verification Code` : `You'll be able to request a new code in ${time_to_allow_resend} seconds`}
                                </button>
                            </div>
                            <div>
                                <div className={'resend-code-button'}>{}</div>
                                <LoadingButton clickable={code.length > 0}
                                               onClick={onSubmit}
                                               loading={submit_loading}
                                               caption={'Continue'} />
                                <div className={`submit-button-message`}>{submit_button_message}</div>
                            </div>
                        </>
                    }
                </div>
            </div>
        </>
    )
}

function PasswordValidation(props: {validation: string, message: string}) {
    let {validation, message} = props;

    return (
        <div className={`password-validation-element ${validation}`}>
            <FontAwesomeIcon icon={(validation === 'valid') ? faCheckCircle : faExclamationCircle}
                             className={`password-validation-icon`}></FontAwesomeIcon>
            <div className={`password-validation-message`}>{message}</div>
        </div>
    )
}