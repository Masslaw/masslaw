import React, {useState} from "react";
import {PageProtector, StatusConditionType} from "../../../infrastructure/user_management/page_protector";
import {UserStatus} from "../../../infrastructure/user_management/user_status";

import "./css.css";

import {GoogleLogin} from "@leecheuk/react-google-login";

import {
    CognitoManager,
    LoginMethods,
    LoginResult,
    SignupResult
} from "../../../infrastructure/server_communication/cognito_client";

import {InputField} from "../../../shared/components/input_field/input_field";

import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCheckCircle, faExclamationCircle} from '@fortawesome/free-solid-svg-icons'
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {UserStatusManager} from "../../../infrastructure/user_management/user_status_manager";
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";

ApplicationRoutingManager.getInstance().setRoutePreloadFunction(ApplicationRoutes.IDENTITY, () => {
    PageProtector.getInstance().updateStatusCondition(UserStatus.GUEST, StatusConditionType.MAXIMUM, null);
    UserStatusManager.getInstance().fetchUserStatus().then();
    return true;
});


export function Identity() {

    let cognitoManager = CognitoManager.getInstance();

    const [display_form, setDisplayForm] = useState("login");

    const [submit_button_message, setSubmitMessage] = useState("");

    const {email, password} = cognitoManager.getRememberedUserLoginCredentials();
    const [email_value, setEmail] = useState(email == null ? '' : email);
    const [password_value, setPassword] = useState(password == null ? '' : password);
    const [remember_me_checked, setRememberMeChecked] = useState(false);

    const [login_credentials_valid, setLoginCredentialsValid] = useState("");

    const [signup_email, setSignupEmail] = useState("");
    const [signup_email_valid, setSignupEmailValid] = useState("");
    const [signup_email_message, setSignupEmailMessage] = useState("");
    const [signup_password, setSignupPassword] = useState("");
    const [signup_password_valid, setSignupPasswordValid] = useState("");
    const [signup_password_verify, setSignupVerifyPassword] = useState("");
    const [signup_password_verify_message, setSignupVerifyPasswordMessage] = useState("");
    const [signup_password_verify_valid, setSignupVerifyPasswordValid] = useState("");

    const [signup_password_valid_length, setSignupPasswordValidLength] = useState("");
    const [signup_password_valid_number, setSignupPasswordValidNumber] = useState("");
    const [signup_password_valid_special, setSignupPasswordValidSpecial] = useState("");
    const [signup_password_valid_upper, setSignupPasswordValidUpper] = useState("");
    const [signup_password_valid_lower, setSignupPasswordValidLower] = useState("");

    const loginToolkit = cognitoManager.getLoginToolkit(async (result: LoginResult, method: LoginMethods) => {
        setSubmitLoading(false);
        if (result === LoginResult.SUCCEEDED) {
            setSubmitLoading(true);
            setLoginCredentialsValid('valid');
            if (remember_me_checked) cognitoManager.securelyRememberUserLoginCredentials(email_value, password_value)
            ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.APP);
        } else if (result === LoginResult.VERIFICATION_NEEDED) {
            cognitoManager.securelyRememberUserLoginCredentials(email_value, '');
            ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.VERIFICATION);
        } else {
            if (method === LoginMethods.MASSLAW) {
                setLoginCredentialsValid('invalid');
                setSubmitMessage('An error occurred trying to log you in.')
            }
        }
    });

    const signupToolkit = cognitoManager.getSignupToolkit((result: SignupResult) => {
        setSubmitLoading(false);
        if (result === SignupResult.SUCCEEDED) {
            setSubmitLoading(true);
            setSignupEmailValid('valid');
            setSignupEmailMessage('');
            loginToolkit.loginDefault(signup_email, signup_password).then();
        } else if (result === SignupResult.FAILED_INVALID_EMAIL) {
            setSignupEmailValid('invalid');
            setSignupEmailMessage('This email is invalid, or already in use.');
        } else {
            setSubmitMessage('An error occurred trying to sign you up.')
        }
    });

    const [submit_loading, setSubmitLoading] = useState(false);

    const submitLogin = async (event: any) => {
        setSubmitLoading(true);
        await loginToolkit.loginDefault(email_value, password_value);
    };

    const submitSignup = async (event: any) => {
        setSubmitLoading(true);
        await signupToolkit.signupDefault(signup_email, signup_password);
    };

    let signupEmailOnChange: React.ChangeEventHandler<HTMLInputElement>;
    let signupPasswordOnChange : React.ChangeEventHandler<HTMLInputElement>;
    let signupVerifyPasswordOnChange :  React.ChangeEventHandler<HTMLInputElement>;

    signupEmailOnChange = (e) => {
        let new_value = (e.target as HTMLInputElement).value
        setSignupEmail(new_value);
        let valid = ((/^[^\s@]+@[^\s@]+\.[^\s@]+$/).test(new_value));
        setSignupEmailValid(valid ? 'valid' : 'invalid');
        setSignupEmailMessage(valid ? '' : 'Invalid email');
    };

    signupPasswordOnChange = e => {
        let new_value = (e.target as HTMLInputElement).value
        setSignupPassword(new_value);
        let valid = true;
        if (new_value.length < 8) { valid = false; setSignupPasswordValidLength("invalid");
        } else { setSignupPasswordValidLength("valid"); }

        if (!(/\d/).test(new_value)) { valid = false; setSignupPasswordValidNumber("invalid");
        } else { setSignupPasswordValidNumber("valid"); }

        if (!(/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]/).test(new_value)) { valid = false; setSignupPasswordValidSpecial("invalid");
        } else { setSignupPasswordValidSpecial("valid"); }

        if (!(/[A-Z]/).test(new_value)) { valid = false; setSignupPasswordValidUpper("invalid");
        } else { setSignupPasswordValidUpper("valid"); }

        if (!(/[a-z]/).test(new_value)) { valid = false; setSignupPasswordValidLower("invalid");
        } else { setSignupPasswordValidLower("valid"); }

        setSignupPasswordValid(valid ? 'valid' : 'invalid');

        const signupVerifyPasswordInput = document.querySelector('#signup-password-verify-input input');
        if (signupVerifyPasswordInput) {
            signupVerifyPasswordInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
    };

    signupVerifyPasswordOnChange = e => {
        let new_value = (e.target as HTMLInputElement).value
        setSignupVerifyPassword(new_value)
        let valid = new_value === signup_password;
        setSignupVerifyPasswordValid(valid ? 'valid' : 'invalid');
        setSignupVerifyPasswordMessage(valid ? '' : 'The two passwords do not match');
    };

    return (
        <>
            <div className={`fill-parent main-background`}>
                <div className={`form-container`}>
                    <div className={`form-select ${display_form}`}>
                        <div className={`form-selection-thingy`}></div>
                        <button className={`form-selection-button login`} onClick={e => {setDisplayForm(`login`)}}>Login</button>
                        <button className={`form-selection-button signup`} onClick={e => {setDisplayForm(`signup`)}}>Signup</button>
                    </div>
                    <div className={`form-section ${display_form}`}>
                        <form className={`form-section-section login-form-container`}>
                            <InputField id={'login-email-input'}
                                        placeHolder={'Email'}
                                        message={''}
                                        valid={login_credentials_valid}
                                        value={email_value}
                                        type={'text'}
                                        onChange={e => setEmail(e.target.value)} />
                            <InputField id={'login-password-input'}
                                        placeHolder={'Password'}
                                        message={''}
                                        valid={login_credentials_valid}
                                        value={password_value}
                                        type={'password'}
                                        hasPasswordShow={true}
                                        onChange={e => setPassword(e.target.value)} />
                            <label style={{fontSize: '13px', marginLeft: '25px', color: 'var(--masslaw-light-text-color)'}}>
                                <input type="checkbox"
                                       checked={remember_me_checked}
                                       onChange={e => setRememberMeChecked(e.target.checked)} />
                                Remember me
                            </label>
                            <div className={'identity-forgot-password-container'}>
                                <MasslawButton caption={'Forgot Password'}
                                               buttonType={MasslawButtonTypes.TEXTUAL}
                                               onClick={e => ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.PASSWORD)} />
                            </div>
                        </form>
                        <form className={`form-section-section signup-form-container `}
                              style={{display: display_form === 'signup' ? 'block' : 'none'}} >
                            <InputField id={'signup-email-input'}
                                        placeHolder={'Email'}
                                        message={signup_email_message}
                                        valid={signup_email_valid}
                                        value={signup_email}
                                        type={'text'}
                                        hasValidationIcon={true}
                                        onChange={signupEmailOnChange} />
                            <InputField id={'signup-password-input'}
                                        placeHolder={'Password'}
                                        message={''}
                                        valid={signup_password_valid}
                                        value={signup_password}
                                        type={'password'}
                                        hasValidationIcon={true}
                                        tooltip={<div className={`signup-password-qualifications`}>
                                            <PasswordValidation validation={signup_password_valid_length}
                                                                message={`Password is at least 8 characters long`} />
                                            <PasswordValidation validation={signup_password_valid_number}
                                                                message={`Password contains at least one number`} />
                                            <PasswordValidation validation={signup_password_valid_special}
                                                                message={`Password contains at least one special character`} />
                                            <PasswordValidation validation={signup_password_valid_upper}
                                                                message={`Password contains at least one upper-case letter`} />
                                            <PasswordValidation validation={signup_password_valid_lower}
                                                                message={`Password contains at least one lower-case letter`} />
                                        </div>}
                                        onChange={ signupPasswordOnChange }/>
                            <InputField id={'signup-password-verify-input'}
                                        placeHolder={'Verify Password'}
                                        message={signup_password_verify_message}
                                        valid={signup_password_verify_valid}
                                        value={signup_password_verify}
                                        type={'password'}
                                        hasValidationIcon={true}
                                        onChange={ signupVerifyPasswordOnChange }/>
                        </form>
                    </div>
                    <div>
                        <LoadingButton clickable={(display_form === 'signup' &&(signup_email_valid ===  'valid' && signup_password_valid === 'valid' && signup_password_verify_valid === 'valid')) || ((display_form === 'login') && (email_value.length > 0 && password_value.length > 0))}
                                       onClick={(display_form === 'signup') ? submitSignup : submitLogin}
                                       loading={submit_loading}
                                       caption={'Continue'} />
                        <div className={`submit-button-message`}>{submit_button_message}</div>
                    </div>
                    <div className={`or-element-cont`}>
                        <div className={`or-element-text`}>OR</div>
                    </div>
                    <div className={`other-login-options`}>
                        <div className={`other-login-option`} onClick={
                            () => {document.getElementsByClassName('google-login-button')[0].dispatchEvent(new Event(`click`))}}>
                            <GoogleLogin
                                {...loginToolkit.googleLoginParams}
                                className={'google-login-button'}
                                buttonText="Continue with Google"
                            />
                        </div>
                    </div>
                </div>
             </div>
        </>
    );
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