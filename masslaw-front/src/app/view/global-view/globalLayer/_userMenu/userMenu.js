import React, {useCallback} from "react";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import styled from "styled-components";
import {model} from "../../../../model/model";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {pushPopup} from "../_global-layer-components/popups";
import {VerticalGap} from "../../../components/verticalGap";

const UserMenuCatchClicks = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: all;
    top: 0;
    left: 0;
    z-index: 90;
`


const UserMenuContainer = styled.div`
    position: absolute;
    display: flex;
    top: 56px;
    right: 0;
    margin: 16px;
    width: 256px;
    max-height: calc(100% - 56px - 32px);
    flex-direction: column;
    background: #3b3b3b;
    z-index: 91;
    overflow: hidden;
    border-radius: 12px;
`

const UserMenuSectionTitle = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    color: #808080;
    width: calc(100% - 24px);
    margin: 12px 16px 4px 16px;
    border: 0 solid lightgrey;
    background: none;
    font-size: 12px;
`

const UserMenuItem = styled.button`
    position: relative;
    display: flex;
    flex-direction: row;
    color: white;
    width: calc(100% - 16px);
    padding: 12px;
    margin: 0 8px;
    border: none;
    background: none;
    font-size: 14px;
    border-radius: 6px;
    letter-spacing: 1px;
    
    &:hover {
        background: #4b4b4b;
    }
`

export function UserMenu(props) {

    const [s_userMenuOpen, setUserMenuOpen] = useModelValueAsReactState('$.application.view.state.userMenuOpen');

    return <>
        {
            s_userMenuOpen ?
            <>
                <UserMenuCatchClicks onClick={() => setUserMenuOpen(false)}/>
                <UserMenuContainer>
                    <UserMenuSectionTitle>Account</UserMenuSectionTitle>
                    <UserMenuItem onClick={() => model.application.navigate(constructUrl(ApplicationRoutes.MY_PROFILE))}>My Profile</UserMenuItem>
                    <UserMenuItem onClick={() => model.application.navigate(constructUrl(ApplicationRoutes.EDIT_PROFILE))}>Edit Profile</UserMenuItem>
                    <UserMenuItem onClick={() => pushPopup({ id: 'logout', component: LogoutPopup,})}>Log Out</UserMenuItem>
                    <UserMenuSectionTitle>Cases</UserMenuSectionTitle>
                    <UserMenuItem onClick={() => model.application.navigate(constructUrl(ApplicationRoutes.MY_CASES))}>My Cases</UserMenuItem>
                    <VerticalGap gap={'8px'} />
                </UserMenuContainer>
            </>
            : <></>
        }
    </>
}

const LogoutPopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 384px;
    height: 128px;
    background: #303030;
    border-radius: 12px;
    padding: 32px
`

const LogoutPopupTitle = styled.div`
    position: relative;
    color: white;
    font-size: 16px;
`

const LogoutPopupText = styled.div`
    position: relative;
    color: #808080;
    font-size: 14px;
`

const LogoutPopupButtonsSection = styled.div`
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: row-reverse;
    align-self: flex-end;
    margin-top: auto;
    
    & button {
        position: relative;
        border: 1px solid white;
        height: 32px;
        margin-left: 8px;
        width: 72px;
        border-radius: 8px;
        font-size: 14px;
    }
`

const LogoutPopupLogoutButton = styled.button`
    color: black;
    background: white;
`

const LogoutPopupCancelButton = styled.button`
    color: white;
    background: none;
`

export function LogoutPopup(props) {

    const c_logout = useCallback(() => {
        model.users.mine.authentication.login = {email: '', password: ''};
        model.users.mine.authentication.tokens = {refresh: '', access: ''};
        model.users.mine.authentication.status = 0;
        window.location.href = constructUrl(ApplicationRoutes.LOGIN);

        const modelToLocalStorageManager = model.services['modelToLocalStorageManager'];
        modelToLocalStorageManager.removePathFromSavedPaths('$.users.mine.authentication.login.email');
        modelToLocalStorageManager.removePathFromSavedPaths('$.users.mine.authentication.login.password');

        props.dismiss();
        model.application.view.state.userMenuOpen = false;
    }, [props.dismiss]);

    return <>
        <LogoutPopupContainer>
            <LogoutPopupTitle>Log Out</LogoutPopupTitle>
            <VerticalGap gap={"8px"} />
            <LogoutPopupText>Are you sure you want to log out?</LogoutPopupText>
            <LogoutPopupButtonsSection>
                <LogoutPopupLogoutButton onClick={() => c_logout()}>Log Out</LogoutPopupLogoutButton>
                <LogoutPopupCancelButton onClick={() => props.dismiss()}>Cancel</LogoutPopupCancelButton>
            </LogoutPopupButtonsSection>
        </LogoutPopupContainer>
    </>
}
