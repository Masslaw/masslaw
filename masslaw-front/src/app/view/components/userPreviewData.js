import styled from "styled-components";
import {ProfilePicture} from "./profilePicture";
import {useEffect, useMemo, useState} from "react";
import {model} from "../../model/model";
import {LoadingIcon} from "./loadingIcon";

const UserPreviewDataContainer = styled.div`
    position: relative;
    width: calc(100% - 32px);
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 16px;
`

const UserPreviewDataProfilePictureContainer = styled.div`
    width: 32px;
    height: 32px;
    border-radius: 8px;
    overflow: hidden;
`

const UserPreviewDataUserName = styled.div`
    height: 100%;
    display: flex;
    align-items: center;
    margin-left: 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 14px;
    color: white;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
`

export function UserPreviewData(props) {

    const usersManager = model.services['usersManager'];

    const [s_userData, setUserData] = useState({});

    useEffect(() => {
        if (!props.userId) return;
        usersManager.fetchUserData(props.userId).then(() => {
            const userData = model.users.data[props.userId];
            console.log(userData);
            setUserData(p => ({...p, ...userData}));
        });
    }, [props.userId]);

    return <>
        <UserPreviewDataContainer>
            {s_userData ? <>
                <UserPreviewDataProfilePictureContainer>
                    <ProfilePicture userId={props.userId} size={'small'} />
                </UserPreviewDataProfilePictureContainer>
                <UserPreviewDataUserName>
                    {`${s_userData.first_name} ${s_userData.last_name}`.trim() || <LoadingIcon width={'8px'} height={'8px'} />}
                </UserPreviewDataUserName>
            </> : <>
                <LoadingIcon width={'20px'} height={'20px'} />
            </>}
        </UserPreviewDataContainer>
    </>
}