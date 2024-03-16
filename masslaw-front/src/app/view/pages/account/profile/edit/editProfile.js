import React, {useCallback, useEffect, useMemo, useState} from "react";
import {model} from "../../../../../model/model";
import {useModelValueAsReactState} from "../../../../../controller/functionality/model/modelReactHooks";
import styled from "styled-components";
import {UserStatus} from "../../../../../config/userStatus";
import {VerticalGap} from "../../../../components/bits-and-pieces/verticalGap";
import {RedirectButtonWrapper} from "../../../../components/redirectButtonWrapper";
import {ApplicationRoutes} from "../../../../../config/applicaitonRoutes";
import {constructUrl} from "../../../../../controller/functionality/navigation/urlConstruction";
import {TextInput} from "../../../../components/textInput";
import {ProfilePicture} from "../../../../components/profilePicture";
import {pushPopup} from "../../../../global-view/globalLayer/_global-layer-components/popups";
import {ProfilePictureChangingPopup} from "./_profilePictureChangingPopup";
import {MasslawApiCalls} from "../../../../../config/masslawAPICalls";

const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
`

const LayoutContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 768px;
    max-width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    border: 1px solid grey;
    border-top: 0;
    border-bottom: 0;
    overflow-y: scroll;
`

const Header = styled.div`
    position: sticky;
    display: flex;
    flex-direction: row;
    align-items: center;
    height: max-content;
    top: 0;
    left: 0;
    width: 100%;
    background-color: black;
    color: white;
    font-size: 24px;
    z-index: 50;
`

const Title = styled.div`
    color: white;
    font-size: 24px;
    margin: 16px 32px 16px 32px;
`

const SubmitButton = styled.button`
    position: absolute;
    width: 128px;
    height: 32px;
    border: 1px solid white;
    border-radius: 8px;
    background: ${({active}) => active ? 'white' : 'none'};
    color: ${({active}) => active ? 'black' : 'white'};
    right: 16px;
    pointer-events: ${({active}) => active ? 'all' : 'none'};
    z-index: 1;
`

const FormContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 64px);
    padding: 0 32px 0px 32px;
`

const Separator = styled.div`
    width: 100%;
    height: 1px;
    background: rgb(0, 0, 0);
    background: linear-gradient(90deg, black 10%, grey 20%, grey 80%, black 90%);
`

const LabelSpan = styled.span`
    font-size: 14px;
    color: grey;
`

const EmailDisplay = styled.div`
    width: 100%;
    font-size: 14px;
    
    span:nth-child(2) {
        color: white;
        margin-left: 16px;
    }
`

const PasswordDisplay = styled.div`
    width: 100%;
    font-size: 14px;

    a {
        margin-left: 14px;
        color: cornflowerblue;
        cursor: pointer;
        outline: none;
    }
`

const ProfilePictureDisplay = styled.div`
    width: 100%;
    font-size: 16px;
    display: flex;
    flex-direction: row;
`

const ProfilePictureContainer = styled.div`
    position: relative;
    width: 128px;
    height: 128px;
    border-radius: 32px;
    margin-left: 32px;
    cursor: pointer;
    border: 1px solid white;
    overflow: hidden;
    
    div:nth-child(2) {
        display: none;
    }
    
    &:hover div:nth-child(2) {
        display: flex;
        background: rgba(0, 0, 0, 0.5);
        position: absolute;
        width: 100%;
        height: 100%;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
        z-index: 5;
    }
`

const NewProfilePicture = styled.img`
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
`

export function EditProfile() {

    const usersManager = model.services['usersManager'];
    const masslawHttpApiClient = model.services['masslawHttpApiClient'];

    model.application.view.state.header.shown = true;
    model.application.pages.currentPage.minimumUserStatus = UserStatus.MISSING_ATTRIBUTES;
    model.application.pages.currentPage.maximumUserStatus = null;
    model.application.pages.currentPage.name = "Edit Profile";

    useEffect(() => {
        model.application.view.state.loading['profile_edit'] = true;
        usersManager.fetchMyUserData();
    }, []);

    const [s_clientUserData, setClientUserData] = useState({});
    const [s_serverUserData, setServerUserData] = useModelValueAsReactState('$.users.mine.data');

    const [s_newImageData, setNewImageData] = useState(null);

    useEffect(() => {
        setClientUserData(s_serverUserData);
    }, [s_serverUserData]);

    useEffect(() => {
        model.application.view.state.loading['profile_edit'] = !s_clientUserData;
    }, [s_clientUserData]);

    const m_canSubmit = useMemo(() => {
        if (!s_clientUserData) return false;
        if (!s_serverUserData) return false;
        if ((s_clientUserData.first_name || '').trim().length < 2) return false;
        if ((s_clientUserData.last_name || '').trim().length < 2) return false;
        if (s_serverUserData.first_name === s_clientUserData.first_name &&
            s_serverUserData.last_name === s_clientUserData.last_name &&
            !s_newImageData) return false;
        return true;
    }, [s_serverUserData, s_clientUserData, s_newImageData]);

    const submit = useCallback(async () => {
        if (!m_canSubmit) return;
        console.log('submitting');
        model.application.view.state.loading['profile_edit_submit'] = true;
        setClientUserData(p => {
            return {...p,
                first_name: p.first_name.trim(),
                last_name: p.last_name.trim()
            }
        })
        await usersManager.submitMyUserData(s_clientUserData);
        model.application.navigate(constructUrl(ApplicationRoutes.MY_PROFILE));
        if (s_newImageData) await masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_PROFILE_PICTURE,
            body: { image_data: s_newImageData.split(',')[1]}
        });
        model.users.profilePictureModificationTimes[s_serverUserData.User_ID] = Date.now();
        model.application.view.state.loading['profile_edit_submit'] = false;
    }, [m_canSubmit, s_newImageData, s_serverUserData, s_clientUserData]);

    return <>
        <PageContainer>
            <LayoutContainer>
                <Header>
                    <Title>Edit Profile</Title>
                    <SubmitButton
                        active={m_canSubmit}
                        onClick={() => {submit().then()}}
                    >Finish</SubmitButton>
                </Header>
                <FormContainer>
                    <VerticalGap gap="32px"/>
                    <EmailDisplay>
                        <LabelSpan>Email:</LabelSpan>
                        <span>{model.users.mine.authentication.login.email}</span>
                    </EmailDisplay>
                    <VerticalGap gap="24px"/>
                    <PasswordDisplay>
                        <LabelSpan>Password:</LabelSpan>
                        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.PASSWORD)}>
                            Change Password
                        </RedirectButtonWrapper>
                    </PasswordDisplay>
                    <VerticalGap gap="32px"/>
                    <Separator/>
                    <VerticalGap gap="32px"/>
                    <ProfilePictureDisplay>
                        <LabelSpan>Profile Picture:</LabelSpan>
                        <ProfilePictureContainer>
                            <div>
                            </div>
                            <div onClick={() => pushPopup({component: ProfilePictureChangingPopup, componentProps: { setImageData: setNewImageData }})}>Edit</div>
                            <ProfilePicture userId={s_serverUserData && s_serverUserData.User_ID} size={"large"}/>
                            {s_newImageData && <NewProfilePicture src={s_newImageData}/>}
                        </ProfilePictureContainer>
                    </ProfilePictureDisplay>
                    <VerticalGap gap="32px"/>
                    <Separator/>
                    <VerticalGap gap="32px"/>
                    <TextInput
                        label="First Name"
                        subLabel="What's your first name?"
                        placeHolder={""}
                        type={"text"}
                        height={"32px"}
                        width={"256px"}
                        value={s_clientUserData && s_clientUserData.first_name || ''}
                        setValue={v => setClientUserData( p => {return {...p, first_name: v}})}
                        borderColor={(() => {
                            if (s_serverUserData && s_clientUserData && s_serverUserData.first_name === s_clientUserData.first_name) return 'white';
                            return s_clientUserData && s_clientUserData.first_name && s_clientUserData.first_name.length > 1 ? 'forestgreen' : 'red'
                        })()}
                    />
                    <VerticalGap gap="24px"/>
                    <TextInput
                        label="Last Name"
                        subLabel="What's your last name?"
                        placeHolder={""}
                        type={"text"}
                        height={"32px"}
                        width={"256px"}
                        value={s_clientUserData && s_clientUserData.last_name || ''}
                        setValue={v => setClientUserData( p => {return {...p, last_name: v}})}
                        borderColor={(() => {
                            if (s_serverUserData && s_clientUserData && s_serverUserData.last_name === s_clientUserData.last_name) return 'white';
                            return s_clientUserData && s_clientUserData.last_name && s_clientUserData.last_name.length > 1 ? 'forestgreen' : 'red'
                        })()}
                    />
                    <VerticalGap gap="32px"/>
                </FormContainer>
            </LayoutContainer>
        </PageContainer>
    </>
}