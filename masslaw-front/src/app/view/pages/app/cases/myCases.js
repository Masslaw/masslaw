import styled from "styled-components";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import {UserStatus} from "../../../../config/userStatus";
import {model} from "../../../../model/model";
import {pushPopup} from "../../../global-view/globalLayer/_global-layer-components/popups";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {CreateCasePopup} from "./_caseCreatePopup";
import {CaseDisplayPopup} from "./_caseDisplayPopup";
import {accessLevelsOrder} from "../../../../config/caseConsts";
import {ProfilePicture} from "../../../components/profilePicture";
import {LoadingIcon} from "../../../components/loadingIcon";
import {UsersListProfilePictures} from "../../../components/usersListProfilePictures";
import {VerticalGap} from "../../../components/verticalGap";
import {CaseDataDisplay} from "../../../components/caseDataDisplay";

const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-color: #1f1f1f;
    color: white;
    border-radius: 5px;
`

const PageTitle = styled.h1`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 32px 32px 16px 32px;
`

const PageSubTitle = styled.h2`
    font-size: 14px;
    font-weight: 500;
    margin: 0 32px 16px 32px;
    color: #999999;
`

const CaseList = styled.div`
    position: relative;
    display: grid;
    grid-template-columns: repeat(auto-fill, calc(256px + 32px + 16px));
    justify-content: space-between;
    flex-grow: 1;
    border-radius: 12px;
    margin: 16px;
    padding: 16px;
    width: calc(100% - 64px);
    overflow-y: auto;
`

const CreateCaseButton = styled.button`
    position: absolute;
    top: 0;
    right: 0;
    margin: 32px;
    background: none;
    width: 128px;
    height: 48px;
    border: 1px solid white;
    color: white;
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: .5px;
    
    &:hover {
        background: white;
        color: black;
    }
`


export function MyCases(props) {

    const casesManager = model.services['casesManager'];

    model.application.pages.currentPage.name = "My Cases";
    model.application.pages.currentPage.minimumUserStatus = UserStatus.FULLY_APPROVED;
    model.application.pages.currentPage.maximumUserStatus = null;
    model.application.view.state.header.shown = true;
    
    const [s_userStatus, setUserStatus] = useModelValueAsReactState("$.users.mine.authentication.status");

    const [s_casesList, setCases] = useModelValueAsReactState("$.cases.all");

    const [s_loadingList, setLoadingList] = useState(true);

    useEffect(() => {
        if (s_userStatus < UserStatus.FULLY_APPROVED) return;
        if (Object.keys(s_casesList || {}).length > 0) return;
        casesManager.fetchCases().then(() => setLoadingList(false));
    }, [s_userStatus, s_casesList]);
    
    const m_caseItems = useMemo(() => {
        const cases = Object.keys(s_casesList).map((caseId) => {return {...s_casesList[caseId], id: caseId};});
        cases.sort((a, b) => b.last_interaction - a.last_interaction );
        return <>{cases.map((caseData) => <CaseItem caseData={caseData}/>)}</>
    }, [s_casesList]);

    return <>
        <PageContainer>
            <PageTitle>Your Cases</PageTitle>
            <PageSubTitle>The Cases You Participate In</PageSubTitle>
            <CreateCaseButton onClick={() => pushPopup({component: CreateCasePopup})}>New Case</CreateCaseButton>
            <CaseList>{s_loadingList ? <LoadingIcon width={"32px"} height={"32px"}/> : m_caseItems}</CaseList>
        </PageContainer>
    </>
}

const CaseItemContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 256px;
    height: max-content;
    background-color: #2f2f2f;
    margin: 16px 8px;
    padding: 16px;
    border-radius: 12px;
    transition: 0.5s linear;
    pointer-events: all;
    cursor: pointer;
    &:hover {
        filter: drop-shadow(0 0 2px white);
        transform: translateY(-5px);
        transition: 0.1s linear;
    }
`

export function CaseItem(props) {

    return <>
        <CaseItemContainer onClick={() => pushPopup({component: CaseDisplayPopup, componentProps: {caseData: props.caseData}})}>
            <CaseDataDisplay caseData={props.caseData}/>
        </CaseItemContainer>
    </>
}
