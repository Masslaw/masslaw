import styled from "styled-components";
import {model} from "../../../../model/model";
import React, {useCallback, useMemo} from "react";
import {VerticalGap} from "../../../components/bits-and-pieces/verticalGap";
import {TextInput} from "../../../components/textInput";
import {LongTextInput} from "../../../components/longTextInput";
import {RedirectButtonWrapper} from "../../../components/redirectButtonWrapper";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";


const CaseDisplayPopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 512px;
    background-color: #1f1f1f;
    color: white;
    border-radius: 12px;
    z-index: 100;
`

const CaseDisplayPopupTitle = styled.h1`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 16px 32px 16px 32px;
`

const CaseDisplayPopupDescription = styled.h2`
    font-size: 14px;
    font-weight: 500;
    margin: 0 32px 16px 32px;
    color: #999999;
`

const OpenCaseDisplayButton = styled.button`
    position: relative;
    margin: 32px 32px 16px auto;
    background: white;
    width: 96px;
    height: 32px;
    border: 1px solid white;
    color: black;
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: .5px;
    pointer-events: all;
    
    &:hover {
        filter: drop-shadow(0 0 5px white);
    }
`

export function CaseDisplayPopup(props) {

    const c_openCase = useCallback(() => {
        model.application.navigate(constructUrl(ApplicationRoutes.CASE_DASHBOARD, {caseId: props.caseData.case_id}));
        props.dismiss();
    }, []);

    return <>
        <CaseDisplayPopupContainer>
            <CaseDisplayPopupTitle>{props.caseData.title}</CaseDisplayPopupTitle>
            <CaseDisplayPopupDescription>{props.caseData.description}</CaseDisplayPopupDescription>
            <VerticalGap gap={"16px"}/>
            <OpenCaseDisplayButton onClick={() => c_openCase()}>Open</OpenCaseDisplayButton>
        </CaseDisplayPopupContainer>
    </>
}
