import styled from "styled-components";
import React, {useEffect, useMemo} from "react";
import {model} from "../../../../model/model";
import {IdentityBackground} from "../_shared/background";
import {IdentityForm} from "../_shared/form";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {TextInput} from "../../../components/textInput";
import {VerticalGap} from "../../../components/verticalGap";
import {SVG_PATHS} from "../../../config/svgPaths";
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

const SignUpInstead = styled.button`
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
    border-radius: 0.75em;
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

const RememberMe = styled.div`
    display: flex;
    position: relative;
    width: calc(100% - 4em);
    margin: 1em;
    flex-direction: row;
    align-items: center;
    font-size: 1em;
    height: 1.5em;
    
    svg {
        height: 1.5em;
        width: 1.5em;
        margin-right: 0.25em;
    }
    
    path {
        fill: ${({checked}) => checked ? "white" : "none"};
        stroke: white;
        stroke-width: 100;
    }
`

export function Login(props) {

    const usersManager = model.services['usersManager'];
    const cognitoClient = model.services['cognitoClient'];
    const modelToLocalStorageManager = model.services['modelToLocalStorageManager'];
    
    model.application.view.state.header.shown = false;
    model.application.pages.currentPage.maximumUserStatus = UserStatus.GUEST;
    model.application.pages.currentPage.minimumUserStatus = null;
    model.application.pages.currentPage.name = 'Login';

    const [s_email, setEmail] = React.useState(model.users.mine.authentication.login.email || "");
    const [s_password, setPassword] = React.useState(model.users.mine.authentication.login.password || "");
    const [s_rememberMe, setRememberMe] = React.useState(true);

    const [s_errorMessage, setErrorMessage] = React.useState("");

    const login = React.useCallback(async () => {
        model.application.view.state.header.shown = false;
        model.application.view.state.loading['login'] = true;
        model.users.mine.authentication.login.email = s_email;
        model.users.mine.authentication.login.password = s_password;
        setErrorMessage("");
        const result = await cognitoClient.logIn();
        console.log("login result: ", result);
        if (result) {
            switch (result) {
                case 'UserNotConfirmedException':
                    model.users.mine.authentication.status = UserStatus.UNVERIFIED;
                    break;
                default:
                    setErrorMessage("An error occurred trying to log you in.");
            }

            model.application.view.state.loading['login'] = false;
            return;
        }
        await usersManager.fetchMyStatus();
        if (s_rememberMe) {
            modelToLocalStorageManager.addPathToSavedPaths('$.users.mine.authentication.login.email');
            modelToLocalStorageManager.addPathToSavedPaths('$.users.mine.authentication.login.password');
            modelToLocalStorageManager.saveModelValueAtPath('$.users.mine.authentication.login.email');
            modelToLocalStorageManager.saveModelValueAtPath('$.users.mine.authentication.login.password');
        } else {
            if (model.users.mine.authentication.status > UserStatus.UNVERIFIED) model.users.mine.authentication.login.password = "";
            modelToLocalStorageManager.removePathFromSavedPaths('$.users.mine.authentication.login.email');
            modelToLocalStorageManager.removePathFromSavedPaths('$.users.mine.authentication.login.password');
        }
        model.application.view.state.loading['login'] = false;
    }, [s_email, s_password, s_rememberMe]);

    const inputWidth = "calc(33vh + 3em)";
    const inputHeight = "3em";

    return <>
        <IdentityBackground/>
        <IdentityForm>
            <Title>Login</Title>
            <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.SIGNUP)}>
                <SignUpInstead>Don't have an account? <u>Sign-Up</u></SignUpInstead>
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
            />
            <VerticalGap gap={"2em"}/>
            <TextInput
                id={"password"}
                label={"Password"}
                subLabel={"Enter Your Password"}
                type={"password"}
                placeholder={"********"}
                width={inputWidth}
                height={inputHeight}
                value={s_password}
                setValue={setPassword}
            />
            <VerticalGap gap={"1em"}/>
            <RememberMe
                checked={s_rememberMe}
                onClick={() => setRememberMe(v => !v)}
            ><span>
                <svg viewBox={"-250 -350 1500 1500"}>
                    <path d={SVG_PATHS.circle}/>
                </svg>
            </span>Remember Me</RememberMe>
            <ErrorMessage>{s_errorMessage}</ErrorMessage>
            <ContinueButton
                clickable={s_email && s_password}
                onClick={login}
            >Continue</ContinueButton>
        </IdentityForm>
    </>
}
