import React, {MouseEventHandler, useContext, useEffect, useState} from "react";

import "./css.css";
import {InputField} from "../../../shared/components/input_field/input_field";
import {
    CognitoManager,
    EmailVerificationResult,
    LoginResult
} from "../../../infrastructure/server_communication/server_modules/cognito_client";
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {ApplicationRoutes} from "../../../infrastructure/application_base/routing/application_routes";
import {
    NavigationFunctionState
} from "../../../infrastructure/application_base/routing/application_global_routing";

import {ApplicationPage, ApplicationPageProps} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {
    useGlobalState,
} from "../../../infrastructure/application_base/global_functionality/global_states";

export const Verification: ApplicationPage = (props: ApplicationPageProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    let cognitoManager = CognitoManager.getInstance();

    const [code, setCode] = useState('');
    const [submit_button_message, setSubmitButtonMessage] = useState('');
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

    let loginToolkit = cognitoManager.getLoginToolkit((result: LoginResult) => { })

    let {email, password} = cognitoManager.getRememberedUserLoginAttributes();
    email = cognitoManager.getLoggedInUserEmail() || email;

    if (email == null) {
        navigate_function(ApplicationRoutes.IDENTITY);
        return <></>;
    }

    let emailVerificationToolkit = cognitoManager.getEmailVerificationToolkit(email,async (result: EmailVerificationResult) => {
        if (result === EmailVerificationResult.SUCCEEDED) {
            if (password != null) await loginToolkit.loginDefault(email || '', password);
            navigate_function(ApplicationRoutes.IDENTITY);
            return <></>;
        } else if (result === EmailVerificationResult.FAILED_EXPIRED) {
            setInputValid('invalid');
            setSubmitButtonMessage('The provided code is expired. A new code has been sent to your email.');
            setSubmitLoading(false);
        } else {
            setInputValid('invalid');
            setSubmitButtonMessage('An error occurred trying to validate your email, the provided code might may be incorrect.');
            setSubmitLoading(false);
        }
    });

    let onSubmit = async () => {
        setSubmitLoading(true);
        await emailVerificationToolkit.attemptVerification(code);
    }

    let resendVerificationCode : MouseEventHandler<HTMLButtonElement> = async (e) => {
        e.preventDefault();
        localStorage.setItem(lastResendTimeLocalStorageKey, new Date().getTime().toString());
        if (time_to_allow_resend <= 0) await emailVerificationToolkit.resendCode();
    }

    return (
        <>
            <div className={`fill-parent main-background`}>
                <form className={`form-container`}>
                    <div className={'form-headline'}>
                        {`Verification Needed`}
                    </div>
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
                </form>
            </div>
        </>
    )
}