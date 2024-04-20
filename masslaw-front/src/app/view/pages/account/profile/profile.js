import React, {useCallback, useEffect, useMemo, useState} from "react";
import {model} from "../../../../model/model";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {useParams} from "react-router-dom";
import {UserStatus} from "../../../../config/userStatus";
import styled from "styled-components";
import {ProfilePicture} from "../../../components/profilePicture";
import {Icon} from "../../../components/icon";
import {SVG_PATHS} from "../../../config/svgPaths";
import {RedirectButtonWrapper} from "../../../components/redirectButtonWrapper";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {LoadingIcon} from "../../../components/loadingIcon";


const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    background: #101010;
`

const LayoutContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: 768px;
    max-width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    border-top: 0;
    border-bottom: 0;
    overflow-y: auto;
    &::-webkit-scrollbar { display: none; }
`

const UserDoesNotExistMessage = styled.div`
    width: 100%;
    font-size: 16px;
    color: #808080;
    text-align: center;
    margin-top: 128px;
`

const ProfileInfoSection = styled.div`
    position: relative;
    height: 100%;
    width: 256px;
    overflow: hidden;
    & > * { 
        position: relative;
        z-index: 5; 
    }
`

const ProfileContentSection = styled.div`
    height: 100%;
    width: calc(100% - 256px);
    overflow-x: hidden;
    overflow-y: auto;
`

const ProfileInfoBackground = styled.div`
    position: absolute;
    width: 100%;
    height: calc(100% - 96px);
    top: 96px;
    border-radius: 8px 8px 0 0;
    background: #252525;
    z-index: 0;
`

const ProfileImageArea = styled.div`
    width: 100%;
    height: 192px;
    display: flex;
    justify-content: center;
    align-items: center;
`

const ProfilePictureContainer = styled.div`
    width: 160px;
    height: 160px;
    border-radius: 24px;
    border: 2px solid #505050;
    overflow: hidden;
`

const ProfileNameAndEditButtonSection = styled.div`
    width: calc(100% - 64px);
    padding: 0 32px;
    margin: 8px 0;
    display: flex;
    flex-direction: row;
`

const ProfileName = styled.div`
    color: white;
    font-size: 16px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    letter-spacing: 0.5px;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
`

const ProfileEditButton = styled.button`
    width: 24px;
    height: 24px;
    color: white;
    font-size: 14px;
    flex-grow: 0;
    flex-shrink: 0;
    flex-basis: 24px;
    background: none;
    border: none;
    border-radius: 8px;
    &:hover { background: #404040; }
`

const ProfileEmail = styled.div`
    width: calc(100% - 64px);
    padding: 0 32px;
    margin: 8px 0;
    font-size: 14px;
    color: #808080;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    letter-spacing: 0.5px;
`


export function Profile() {

    const {userId} = useParams();

    const {usersManager} = model.services;

    model.application.view.state.header.shown = true;
    model.application.pages.currentPage.minimumUserStatus = userId ? 0 : UserStatus.FULLY_APPROVED;
    model.application.pages.currentPage.maximumUserStatus = null;
    model.application.pages.currentPage.name = "Profile";

    const [s_loading, setLoading] = useState(false);

    const [s_userData, setUserData] = useState({});

    const c_loadData = useCallback(async () => {
        if (s_loading) return;
        setLoading(true);
        if (userId) {
            await usersManager.fetchUserData(userId, true);
            setUserData(model.users.data[userId]);
        }
        else {
            await usersManager.fetchMyUserData(true);
            setUserData(model.users.mine.data);
        }
        setLoading(false);
    }, [userId]);

    useEffect(() => {
        c_loadData();
    }, [userId]);

    return <>
        <PageContainer>
            <LayoutContainer>
                {s_loading ? <>
                    <LoadingIcon width={'30px'} height={'30px'} />
                </> : !s_userData.email ? <>
                    <UserDoesNotExistMessage>This user does not exist.</UserDoesNotExistMessage>
                </> : <>
                    <ProfileInfoSection>
                        <ProfileInfoBackground />
                        <ProfileImageArea>
                            <ProfilePictureContainer>
                                <ProfilePicture userId={userId || model.users.mine.data.User_ID} size={'large'}/>
                            </ProfilePictureContainer>
                        </ProfileImageArea>
                        <ProfileNameAndEditButtonSection>
                            <ProfileName>
                                {`${s_userData.first_name} ${s_userData.last_name}`}
                            </ProfileName>
                            <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.EDIT_PROFILE)}>
                                <ProfileEditButton>
                                    <Icon>{SVG_PATHS.pen}</Icon>
                                </ProfileEditButton>
                            </RedirectButtonWrapper>
                        </ProfileNameAndEditButtonSection>
                        <ProfileEmail>
                            {s_userData.email}
                        </ProfileEmail>

                    </ProfileInfoSection>
                    <ProfileContentSection>

                    </ProfileContentSection>
                </>}
            </LayoutContainer>
        </PageContainer>
    </>
}