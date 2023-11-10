import React, {useCallback, useContext, useEffect, useState} from "react";
import "./css.css";
import {GoogleLogin} from "@leecheuk/react-google-login";
import {
    CognitoManager,
    LoginMethods,
    LoginResult,
    SignupResult
} from "../../../infrastructure/server_communication/server_modules/cognito_client";
import {InputField} from "../../../shared/components/input_field/input_field";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faCheckCircle, faExclamationCircle} from '@fortawesome/free-solid-svg-icons'
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {ApplicationRoutes} from "../../../infrastructure/application_base/routing/application_routes";
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";
import {ApplicationPage, ApplicationPageProps} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {UserStatusManager} from "../../../infrastructure/user_management/user_status_manager";
import {
    NavigationFunctionState,
    QueryStringParamsState
} from "../../../infrastructure/application_base/routing/application_global_routing";
import {useGlobalState} from "../../../infrastructure/application_base/global_functionality/global_states";

export const Identity: ApplicationPage = (props: ApplicationPageProps) => {

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    let cognitoManager = CognitoManager.getInstance();

    const [display_form, setDisplayForm] = useState("login");

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const setDisplayFormName = useCallback(async (displayForm: string) => {
        setQueryStringParams({'choose': displayForm});
    }, [display_form]);

    useEffect(() => {
        setDisplayForm((prev) => query_string_params['choose'] || prev);
    }, [query_string_params]);

    const [submit_button_message, setSubmitMessage] = useState("");

    const [email_value, setEmail] = useState('');
    const [password_value, setPassword] = useState('');
    const [remember_me_checked, setRememberMeChecked] = useState(true);

    useEffect(() => {
        const rememberedInfo = cognitoManager.getRememberedUserLoginAttributes();
        setEmail(rememberedInfo.email || email_value);
        setPassword(rememberedInfo.password || password_value);
    }, []);

    const [login_attributes_valid, setLoginAttributesValid] = useState("");

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

    const loginToolkit = cognitoManager.getLoginToolkit(useCallback(async (result: LoginResult, method: LoginMethods) => {
        setSubmitLoading(false);
        if (result === LoginResult.SUCCEEDED) {
            setSubmitLoading(true);
            setLoginAttributesValid('valid');
            if (remember_me_checked) cognitoManager.securelyRememberUserLoginAttributes(email_value, password_value);
        } else if (result === LoginResult.VERIFICATION_NEEDED) {
            cognitoManager.securelyRememberUserLoginAttributes(email_value, remember_me_checked && password_value || '');
            navigate_function(ApplicationRoutes.VERIFICATION);
        } else {
            if (method === LoginMethods.MASSLAW) {
                setLoginAttributesValid('invalid');
                setSubmitMessage('An error occurred trying to log you in.')
            }
        }
        await UserStatusManager.getInstance().forceResetStatus();
    }, [email_value, password_value]));

    const signupToolkit = cognitoManager.getSignupToolkit(useCallback((result: SignupResult) => {
        setSubmitLoading(false);
        if (result === SignupResult.SUCCEEDED) {
            setSubmitLoading(true);
            setSignupEmailValid('valid');
            setSignupEmailMessage('');
            if (remember_me_checked) cognitoManager.securelyRememberUserLoginAttributes(email_value, password_value);
            loginToolkit.loginDefault(signup_email, signup_password).then();
        } else if (result === SignupResult.FAILED_INVALID_EMAIL) {
            setSignupEmailValid('invalid');
            setSignupEmailMessage('This email is invalid, or already in use.');
        } else {
            setSubmitMessage('An error occurred trying to sign you up.')
        }
    }, [signup_email, signup_password]));

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
                        <button className={`form-selection-button login`} onClick={e => {setDisplayFormName(`login`)}}>Login</button>
                        <button className={`form-selection-button signup`} onClick={e => {setDisplayFormName(`signup`)}}>Signup</button>
                    </div>
                    <div className={`form-section ${display_form}`}>
                        <form
                            className={`form-section-section login-form-container`}
                            onKeyDownCapture={e => e.key == 'Enter' && e.preventDefault()}
                        >
                            <InputField id={'login-email-input'}
                                        placeHolder={'Email'}
                                        message={''}
                                        valid={login_attributes_valid}
                                        value={email_value}
                                        type={'text'}
                                        onChange={e => setEmail(e.target.value)} />
                            <InputField id={'login-password-input'}
                                        placeHolder={'Password'}
                                        message={''}
                                        valid={login_attributes_valid}
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
                                               onClick={e => navigate_function(ApplicationRoutes.PASSWORD)} />
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
                            <label style={{fontSize: '13px', marginLeft: '25px', color: 'var(--masslaw-light-text-color)'}}>
                                <input type="checkbox"
                                       checked={remember_me_checked}
                                       onChange={e => setRememberMeChecked(e.target.checked)} />
                                Remember me
                            </label>
                        </form>
                    </div>
                    <div style={{padding: '20px'}}>
                        <LoadingButton clickable={(display_form === 'signup' &&(signup_email_valid ===  'valid' && signup_password_valid === 'valid' && signup_password_verify_valid === 'valid')) || ((display_form === 'login') && (email_value.length > 0 && password_value.length > 0))}
                                       onClick={(display_form === 'signup') ? submitSignup : submitLogin}
                                       loading={submit_loading}
                                       caption={'Continue'} />
                        <div className={`submit-button-message`}>{submit_button_message}</div>
                    </div>
                    {/*<div className={`or-element-cont`}>*/}
                    {/*    <div className={`or-element-text`}>OR</div>*/}
                    {/*</div>*/}
                    {/*<div className={`other-login-options`}>*/}
                    {/*    <div className={`other-login-option`} onClick={*/}
                    {/*        () => {document.getElementsByClassName('google-login-button')[0].dispatchEvent(new Event(`click`))}}>*/}
                    {/*        <GoogleLogin*/}
                    {/*            {...loginToolkit.googleLoginParams}*/}
                    {/*            className={'google-login-button'}*/}
                    {/*            buttonText="Continue with Google"*/}
                    {/*        />*/}
                    {/*    </div>*/}
                    {/*</div>*/}
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