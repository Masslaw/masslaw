import {VerticalGap} from "./verticalGap";
import {UsersListProfilePictures} from "./usersListProfilePictures";
import React from "react";
import styled from "styled-components";
import {CaseUserRole} from "./caseUserRole";
import {model} from "../../model/model";

const CaseItemTitle = styled.h1`
    font-size: 20px;
    font-weight: bold;
    color: white;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin: 0;
`

const CaseItemDescription = styled.h2`
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
    height: max-content;
    max-height: 48px;
    font-size: 14px;
    line-height: 16px;
    font-weight: 500;
    color: #999999;
    margin: 0;
`

const CaseItemRole = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    color: #999999;
    margin: 0;
    font-size: 12px;
    span { margin-right: 8px; }
`

export function CaseDataDisplay(props) {
    return <>
        <CaseItemTitle>{props.caseData.title}</CaseItemTitle>
        <VerticalGap gap={'12px'} />
        <CaseItemDescription>{props.caseData.description}</CaseItemDescription>
        <VerticalGap gap={'16px'} />
        <UsersListProfilePictures
            users={Object.keys(props.caseData.users || {}).map((userId) => ({...props.caseData.users[userId], id: userId}))}
            usersToDisplay={9}
        />
        <VerticalGap gap={'16px'} />
        <CaseItemRole>
            <span>Your role:</span>
            <CaseUserRole caseId={props.caseData.case_id} userId={model.users.mine.data.User_ID}/>
        </CaseItemRole>
    </>
}