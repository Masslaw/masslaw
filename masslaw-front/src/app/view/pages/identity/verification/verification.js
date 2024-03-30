import styled from "styled-components";
import React, {useEffect, useMemo} from "react";
import {model} from "../../../../model/model";
import {IdentityBackground} from "../_shared/background";
import {IdentityForm} from "../_shared/form";
import {TextInput} from "../../../components/textInput";
import {VerticalGap} from "../../../components/verticalGap";
import {UserStatus} from "../../../../config/userStatus";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";

const inputWidth = "calc(33vh + 3em)";
const inputHeight = "3em";

const Title = styled.div`
    position: relative;
    font-size: 2em;
    margin: 0.75em;
    width: calc(100% - 2em);
    height: 1em;
    line-height: 1em;
`

const Prompt = styled.div`
    position: relative;
    font-size: 1em;
    width: ${inputWidth};
    margin: 1em;
`

const CodeResendInteraction = styled.button`
    position: relative;
    font-size: 1em;
    width: ${inputWidth};
    color: cornflowerblue;
    background: none;
    border: none;
    margin: 1em;
    text-align: left;
    padding: 0;
    pointer-events: ${({clickable}) => clickable ? "auto" : "none"};
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

export function Verification(props) {

    const usersManager = model.services['usersManager'];
    const cognitoClient = model.services['cognitoClient'];
    const modelStateManager = model.services['modelStateManager'];
    const modelToLocalStorageManager = model.services['modelToLocalStorageManager'];

    const emailToVerify = model.users.mine.authentication.login.email;
    const obfuscatedEmail = emailToVerify.replace(/^(.{2}).*?(@)/, (_, c1, c2) => c1 + "*".repeat((emailToVerify || '').indexOf(c2) - 3) + c2);

    model.application.view.state.header.shown = false;
    model.application.pages.currentPage.maximumUserStatus = UserStatus.UNVERIFIED;
    model.application.pages.currentPage.minimumUserStatus = UserStatus.LOGGED_IN;
    model.application.pages.currentPage.name = 'Verification';

    const [s_verificationCode, setVerificationCode] = React.useState(model.users.mine.authentication.verification.email || "");

    const [s_codeResendButtonData, setCodeResendButtonData] = React.useState({prompt: "", clickable: false});
    const [s_errorMessage, setErrorMessage] = React.useState("");

    const [s_sendingCode, setSendingCode] = React.useState(false);
    const [s_timeToSendCode, setTimeToSendCode] = React.useState(0);
    const [s_currentTime, setCurrentTime] = React.useState(Date.now());
    const [s_lastCodeSendingTime, setLastCodeSendingTime] = useModelValueAsReactState('$.users.mine.authentication.verification.lastCodeSendingTime');

    const m_timeToSendCode = useMemo(() => {
        return parseInt(s_lastCodeSendingTime) ? parseInt(s_lastCodeSendingTime) + 60000 - s_currentTime : 0;
    }, [s_currentTime, s_lastCodeSendingTime]);

    useEffect(() => {
        if (!s_sendingCode) {
            if (m_timeToSendCode <= 0) setCodeResendButtonData({prompt: "Resend Verification Code", clickable: true});
            else setCodeResendButtonData({prompt: `You will be able to send a new code in: ${Math.ceil(m_timeToSendCode / 1000)}`, clickable: false});
        }
        setTimeToSendCode(m_timeToSendCode);
    }, [s_currentTime, s_lastCodeSendingTime, m_timeToSendCode]);

    const c_sendCode = React.useCallback(async () => {
        if (s_timeToSendCode > 0) return;
        setSendingCode(true);
        setCodeResendButtonData({prompt: "Sending Code...", clickable: false});
        setErrorMessage("");
        await cognitoClient.sendEmailConfirmationCode();
        model.users.mine.authentication.verification.lastCodeSendingTime = Date.now();
        setCodeResendButtonData({prompt: "Code Sent.", clickable: false});
        await new Promise(r => setTimeout(r, 1500));
        setSendingCode(false);
    }, [s_timeToSendCode]);

    const c_verification = React.useCallback(async () => {
        setErrorMessage("");
        setCodeResendButtonData(p => {return {prompt: p.prompt, clickable: false}});
        model.application.view.state.loading['verification_submit'] = true;
        const result = await cognitoClient.attemptEmailVerification(s_verificationCode);
        if (result) {
            switch (result.status) {
                case 'ExpiredCodeException':
                    setErrorMessage("The verification code has expired. Please request a new one.");
                    break;
                default:
                    setErrorMessage("An error occurred. Please try again.");
            }
            model.application.view.state.loading['verification_submit'] = false;
            return;
        };
        await cognitoClient.logIn();
        await usersManager.fetchMyStatus();
        model.application.view.state.loading['verification_submit'] = false;
    }, [s_verificationCode]);

    useEffect(() => {
        modelStateManager.listenToModelChange("$.users.mine.authentication.verification.lastCodeSendingTime", setLastCodeSendingTime);
        modelToLocalStorageManager.addPathToSavedPaths("$.users.mine.authentication.verification.lastCodeSendingTime");
        modelToLocalStorageManager.loadModelValueAtPath("$.users.mine.authentication.verification.lastCodeSendingTime");

        if (m_timeToSendCode <= 0) { c_sendCode(); }

        const interval = setInterval(() => {
            setCurrentTime(Date.now());
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return <>
        <IdentityBackground/>
        <IdentityForm>
            <Title>Verification</Title>
            <Prompt>An email with a verification code has been sent to {obfuscatedEmail}. Please provide it here:</Prompt>
            <TextInput
                id={"code"}
                label={"Verification Code"}
                subLabel={"Enter the verification code sent to your email"}
                type={"text"}
                placeholder={"123123"}
                width={inputWidth}
                height={inputHeight}
                value={s_verificationCode}
                setValue={setVerificationCode}
            />
            <VerticalGap gap={"1em"}/>
            <CodeResendInteraction
                clickable={s_codeResendButtonData.clickable}
                onClick={c_sendCode}
            >
                {s_codeResendButtonData.prompt}
            </CodeResendInteraction>
            <ErrorMessage>{s_errorMessage}</ErrorMessage>
            <ContinueButton
                clickable={s_verificationCode.length > 0}
                onClick={c_verification}
            >Continue</ContinueButton>
        </IdentityForm>
    </>
}
