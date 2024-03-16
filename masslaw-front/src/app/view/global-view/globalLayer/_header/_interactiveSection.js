
import React, {useCallback, useEffect} from 'react';
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {model} from "../../../../model/model";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import styled from "styled-components";
import {UserStatus} from "../../../../config/userStatus";
import {ProfilePicture} from "../../../components/profilePicture";

export function HeaderInteractiveSection(props) {

    const [s_userStatus, setUserStatus] = useModelValueAsReactState('$.users.mine.authentication.status');

    useEffect(() => {
        console.log("Header User Section - displayed according to user status: ", s_userStatus);
    }, [s_userStatus]);

    return <>
        {
            typeof s_userStatus !== 'number' ? <></>

            : s_userStatus === UserStatus.UNKNOWN ||
            s_userStatus === UserStatus.GUEST ? <GuestDisplay/>

            : s_userStatus > UserStatus.GUEST ? <LoggedInDisplay/>

            : <></>
        }
    </>
}

const HeaderLoginButton = styled.button`
    height: 38px;
    width: 128px;
    border-radius: 21px;
    border: 1px solid white;
    color: white;
    font-size: 14px;
    letter-spacing: 2px;
    font-weight: bold;
    background: none;
    font-family: sans-serif;
    cursor: pointer;
    margin-left: auto;
    margin-right: 16px;

    &:hover {
        background: white;
        color: black;
    }
`

function GuestDisplay(props) {
    return <>
        <HeaderLoginButton onClick={_ => model.application.navigate(constructUrl(ApplicationRoutes.LOGIN))}>Login</HeaderLoginButton>
    </>
}

const LoggedInDisplayContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 100%;
    margin-left: auto;
    margin-right: 16px;
    width: 100%;
`

const LoggedInUserSection = styled.div`
    display: flex;
    flex-direction: row-reverse;
    justify-content: center;
    align-items: center;
    pointer-events: all;
    cursor: pointer;
    margin-left: auto;
`

const LoggedInUserProfilePictureContainer = styled.div`
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: #999999;
    overflow: hidden;
    border: 1px solid white;
`

const LoggedInUserInfoSection = styled.div`
    margin-right: 16px;
    text-align: right;
`

const LoggedInDisplayUserName = styled.div`
    color: white;
    font-size: 14px;
`

const LoggedInDisplayUserEmail = styled.div`
    color: grey;
    font-size: 12px;
`

const UserMenuCatchClicks = styled.div`
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: all;
`

function LoggedInDisplay(props) {

    const [s_userData, setUserData] = useModelValueAsReactState('$.users.mine.data');

    useEffect(() => {
        const usersManager = model.services['usersManager'];
        usersManager.fetchMyUserData(true).then();
    }, []);

    const [s_displayedName, setDisplayedName] = React.useState("Loading...");
    const [s_displayedEmail, setDisplayedEmail] = useModelValueAsReactState('$.users.mine.authentication.login.email');

    useEffect(() => {
        updateUserName();
    }, [s_userData]);

    const updateUserName = useCallback(() => {
        if (!s_userData) {
            setDisplayedName("");
            return;
        }
        if (!s_userData.first_name || !s_userData.last_name) {
            setDisplayedName("");
            return;
        }
        setDisplayedName(`${s_userData.first_name || ''} ${s_userData.last_name}`);
    }, [s_userData]);

    return <>
        <LoggedInDisplayContainer>
            <LoggedInUserSection onClick={() => model.application.view.state.userMenuOpen = true}>
                <LoggedInUserProfilePictureContainer>
                    <ProfilePicture userId={s_userData && s_userData.User_ID} size={'small'}/>
                </LoggedInUserProfilePictureContainer>
                <LoggedInUserInfoSection>
                    <LoggedInDisplayUserName>
                        {s_displayedName}
                    </LoggedInDisplayUserName>
                    <LoggedInDisplayUserEmail>
                        {s_displayedEmail}
                    </LoggedInDisplayUserEmail>
                </LoggedInUserInfoSection>
            </LoggedInUserSection>
        </LoggedInDisplayContainer>
    </>
}
