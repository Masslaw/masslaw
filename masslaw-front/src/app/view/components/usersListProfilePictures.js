import React, {useMemo} from "react";
import {accessLevelsOrder} from "../../config/caseConsts";
import {ProfilePicture} from "./profilePicture";
import styled from "styled-components";


const ProfilePicturesListContainer = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fill, 18px);
    height: 32px;
    width: calc(100% - 32px);
`

const ProfilePictureContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    width: 32px;
    height: 32px;
    background: #969696;
    border-radius: 50%;
    overflow: hidden;
    ${({zIndex}) => zIndex ? `z-index: ${zIndex};` : ""}
`

export function UsersListProfilePictures(props) {
    const users = [...props.users];
    users.sort((a, b) => accessLevelsOrder.indexOf(a.access_level) - accessLevelsOrder.indexOf(b.access_level));
    const usersToDisplay = users.slice(0, props.usersToDisplay);
    const restCount = users.length - usersToDisplay.length;
    return <>
        <ProfilePicturesListContainer>
            {usersToDisplay.map((user) => <>
                <ProfilePictureContainer>
                    <ProfilePicture
                        userId={user.id}
                        size={'small'}
                    />
                </ProfilePictureContainer>
            </>)}
            {restCount ? <>
                <ProfilePictureContainer zIndex={1}>
                    +{restCount}
                </ProfilePictureContainer>
            </> : <>
            </>}
        </ProfilePicturesListContainer>
    </>
}