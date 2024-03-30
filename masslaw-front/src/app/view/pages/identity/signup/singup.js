import {IdentityBackground} from "../_shared/background";
import {IdentityForm} from "../_shared/form";
import {TextInput} from "../../../components/textInput";
import styled from "styled-components";
import {VerticalGap} from "../../../components/verticalGap";
import React, {useEffect, useMemo} from "react";
import {model} from "../../../../model/model";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {UserStatus} from "../../../../config/userStatus";
import {RedirectButtonWrapper} from "../../../components/redirectButtonWrapper";

const Title = styled.div`
    position: relative;
    font-size: 2em;
    margin: 0.75em;
    width: calc(100% - 2em);
    height: 1em;
    line-height: 1em;
`

const LogInInstead = styled.button`
    position: absolute;
    font-size: 0.9em;
    right: 2em;
    top: 2em;
    padding: 0.25em;
    color: cornflowerblue;
    text-decoration: none;
    cursor: pointer;
    background: none;
    border: none;
`

const ErrorMessage = styled.div`
    position: relative;
    font-size: 1em;
    width: calc(100% - 2em);
    height: 3em;
    line-height: 3em;
    text-align: center;
    color: red;
`

const ContinueButton = styled.button`
    position: absolute;
    align-self: flex-end;
    font-size: 1em;
    width: 12em;
    height: 3em;
    border-radius: 1.5em;
    border: 0.1em solid ${({clickable}) => clickable ? "white" : "gray"};
    background: ${({clickable}) => clickable ? "white" : "none"};
    color: ${({clickable}) => clickable ? "black" : "gray"};
    right: 1.5em;
    bottom: 1.5em;
    pointer-events: ${({clickable}) => clickable ? "auto" : "none"};
    
    &:hover {
        filter: ${({clickable}) => clickable ? "drop-shadow(0 0 0.25em white)" : ""};
    }
`

const PasswordValidationToolkit = styled.div`
    position: absolute;
    width: 20em;
    top: 27vh;
    left: 105%;
    border-radius: 1em;
    background: black;
    border: 1px solid white;
`

const PasswordValidationToolkitItem = styled.div`
    position: relative;
    font-size: 1em;
    width: calc(100% - 2em);
    color: ${({valid}) => valid ? "forestgreen" : "red"};
    margin: 1em;
`

export function Signup(props) {

    const cognitoClient = model.services['cognitoClient'];
    const usersManager = model.services['usersManager'];

    model.application.view.state.header.shown = false;
    model.application.pages.currentPage.maximumUserStatus = UserStatus.GUEST;
    model.application.pages.currentPage.minimumUserStatus = null;
    model.application.pages.currentPage.name = 'Signup';

    const [s_email, setEmail] = React.useState("");
    const [s_password, setPassword] = React.useState("");
    const [s_repeatPassword, setRepeatPassword] = React.useState("");

    const s_emailValid = useMemo(() => {
        return s_email.length > 0 && s_email.includes("@") && s_email.includes(".");
    }, [s_email]);

    const s_passwordValidation = useMemo(() => {
        return {length: s_password.length > 7, upper: (s_password.match(/[A-Z]/) || []).length > 0, lower: (s_password.match(/[a-z]/) || []).length > 0, number: (s_password.match(/[0-9]/) || []).length > 0, special: (s_password.match(/[^A-Za-z0-9]/) || []).length > 0,};
    }, [s_password]);

    const [s_errorMessage, setErrorMessage] = React.useState("");

    const signup = React.useCallback(async () => {
        model.application.view.state.loading['signup'] = true;
        const signupResult = await cognitoClient.signUp(s_email, s_password);
        console.log("signup result: ", signupResult);
        if (signupResult) {
            switch (signupResult){
                case 'UsernameExistsException':
                    setErrorMessage("An account with this email already exists.")
                    break;
                default:
                    setErrorMessage("An error occurred trying to sign you up.")
            }
            model.application.view.state.loading['signup'] = false;
            return;
        }
        setErrorMessage("");
        model.users.mine.authentication.login.email = s_email;
        model.users.mine.authentication.login.password = s_password;
        const loginResult = await cognitoClient.logIn();
        console.log("login result: ", loginResult);
        if (loginResult) {
            switch (loginResult) {
                case 'UserNotConfirmedException':
                    model.users.mine.authentication.status = UserStatus.UNVERIFIED;
                    break;
                default:
                    setErrorMessage("An error occurred trying to log you in.");
            }
            model.application.view.state.loading['signup'] = false;
            return;
        }
        await usersManager.fetchMyStatus();
        model.application.view.state.loading['signup'] = false;
        model.users.mine.authentication.login.password = "";
    }, [s_email, s_password, s_repeatPassword]);

    const inputWidth = "33vh";
    const inputHeight = "3em";

    return <>
        <IdentityBackground/>
        <IdentityForm>
            <Title>Sign-up</Title>
            <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.LOGIN)}>
                <LogInInstead>Already have an account? <u>Login</u></LogInInstead>
            </RedirectButtonWrapper>
            <TextInput
                id={"email"}
                label={"Email"}
                subLabel={"Enter your email"}
                type={"email"}
                placeholder={"example@email.com"}
                width={inputWidth}
                height={inputHeight}
                value={s_email}
                setValue={setEmail}
                valid={s_emailValid}
                hasIndicator={true}
                indicatorColor={s_email.length === 0 ? "none" : null}
                indicatorGoodPath={"circle"}
                indicatorBadPath={"circle"}
            />
            <VerticalGap gap={"1em"}/>
            <TextInput
                id={"password"}
                label={"Password"}
                subLabel={"Enter A Strong Password"}
                type={"password"}
                placeholder={"********"}
                width={inputWidth}
                height={inputHeight}
                value={s_password}
                setValue={setPassword}
                valid={(Object.values(s_passwordValidation).every(value => value === true))}
                hasIndicator={true}
                indicatorColor={s_password.length === 0 ? "none" : null}
                indicatorGoodPath={"circle"}
                indicatorBadPath={"circle"}
            />
            <VerticalGap gap={"1em"}/>
            <TextInput
                id={"repeat-password"}
                label={"Repeat Password"}
                subLabel={"Repeat Your Password"}
                type={"password"}
                placeholder={"********"}
                width={inputWidth}
                height={inputHeight}
                value={s_repeatPassword}
                setValue={setRepeatPassword}
                valid={s_repeatPassword === s_password}
                hasIndicator={true}
                indicatorColor={s_repeatPassword.length === 0 ? "none" : null}
                indicatorGoodPath={"circle"}
                indicatorBadPath={"circle"}
                disableShowPassword={true}
            />
            <ErrorMessage>{s_errorMessage}</ErrorMessage>
            <ContinueButton
                clickable={s_emailValid && Object.values(s_passwordValidation).every(value => value === true) && s_repeatPassword === s_password}
                onClick={signup}
            >Continue</ContinueButton>
            {s_password.length > 0 && <PasswordValidationToolkit>
                <PasswordValidationToolkitItem valid={s_passwordValidation.length}>Password must be at least 8 characters long.</PasswordValidationToolkitItem>
                <PasswordValidationToolkitItem valid={s_passwordValidation.upper}>Password must contain at least one uppercase letter.</PasswordValidationToolkitItem>
                <PasswordValidationToolkitItem valid={s_passwordValidation.lower}>Password must contain at least one lowercase letter.</PasswordValidationToolkitItem>
                <PasswordValidationToolkitItem valid={s_passwordValidation.number}>Password must contain at least one number.</PasswordValidationToolkitItem>
                <PasswordValidationToolkitItem valid={s_passwordValidation.special}>Password must contain at least one special character.</PasswordValidationToolkitItem>
            </PasswordValidationToolkit> || <></>}
        </IdentityForm>
    </>
}
