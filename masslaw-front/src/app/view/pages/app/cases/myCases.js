import styled from "styled-components";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import {UserStatus} from "../../../../config/userStatus";
import {model} from "../../../../model/model";
import {pushPopup} from "../../../global-view/globalLayer/_global-layer-components/popups";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {CreateCasePopup} from "./_caseCreatePopup";
import {CaseDisplayPopup} from "./_caseDisplayPopup";
import {LoadingIcon} from "../../../components/loadingIcon";
import {CaseDataDisplay} from "../../../components/caseDataDisplay";
import {SVG_PATHS} from "../../../config/svgPaths";

const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-color: #101010;
    color: white;
    border-radius: 5px;
`

const PageTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 32px 32px 16px 32px;
`

const PageSubTitle = styled.div`
    font-size: 14px;
    margin: 0 32px 16px 32px;
    color: #808080;
`

const CaseList = styled.div`
    position: relative;
    display: grid;
    grid-template-columns: repeat(auto-fill, calc(320px + 32px));
    justify-content: space-between;
    flex-grow: 1;
    border-radius: 12px;
    margin: 16px;
    padding: 16px;
    width: calc(100% - 64px);
    overflow-y: auto;
    &::-webkit-scrollbar { display: none; }
`

const ButtonsSection = styled.div`
    position: absolute;
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    top: 0;
    right: 0;
    margin: 32px;
    background: none;
    height: 48px;
`

const ButtonInButtonsSection = styled.button`
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 32px;
    width: 32px;
    margin-left: 16px;
    border-radius: 8px;
    background: none;
    border: none;
    padding: 0;
    &:hover { background: #505050; }
    svg {
        fill: white;
        width: 75%;
        height: 75%;
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

    const [s_loadingList, setLoadingList] = useState(false);

    const c_loadList = useCallback(async () => {
        if (s_userStatus < UserStatus.FULLY_APPROVED) return;
        if (s_loadingList) return;
        setLoadingList(true);
        await casesManager.fetchCases();
        setLoadingList(false);
    }, [s_loadingList, s_userStatus, s_casesList]);

    useEffect(() => {
        c_loadList();
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
            <ButtonsSection>
                <ButtonInButtonsSection onClick={() => pushPopup({component: CreateCasePopup})}>
                    <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.plusSign}/></svg>
                </ButtonInButtonsSection>
                <ButtonInButtonsSection onClick={() => c_loadList()}>
                    {s_loadingList ? <>
                        <LoadingIcon width={"32px"} height={"32px"}/>
                    </> : <>
                        <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.circleArrow}/></svg>
                    </>}
                </ButtonInButtonsSection>
            </ButtonsSection>
            <CaseList>{s_loadingList ? <LoadingIcon width={"24px"} height={"24px"}/> : m_caseItems}</CaseList>
        </PageContainer>
    </>
}

const CaseItemContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 320px;
    height: 175px;
    background-color: #202020;
    margin: 16px 0;
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
