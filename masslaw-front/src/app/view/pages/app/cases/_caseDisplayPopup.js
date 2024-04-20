import styled from "styled-components";
import {model} from "../../../../model/model";
import React, {useCallback, useMemo} from "react";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {CaseDataDisplay} from "../../../components/caseDataDisplay";
import {VerticalGap} from "../../../components/verticalGap";
import {Icon} from "../../../components/icon";
import {SVG_PATHS} from "../../../config/svgPaths";
import {HorizontalGap} from "../../../components/horizontalGap";


const CaseDisplayPopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 384px;
    background-color: #202020;
    color: white;
    border-radius: 12px;
    z-index: 100;
    padding: 16px 32px;
`

const OpenCaseDisplayButton = styled.button`
    position: relative;
    margin: 8px 0 8px auto;
    background: white;
    width: 96px;
    height: 32px;
    border: 1px solid white;
    color: black;
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: .5px;
    pointer-events: all;
`

export function CaseDisplayPopup(props) {

    const c_openCase = useCallback(() => {
        window.location.href = constructUrl(ApplicationRoutes.CASE_DASHBOARD, {caseId: props.caseData.case_id});
        props.dismiss();
    }, []);

    return <>
        <CaseDisplayPopupContainer>
            <VerticalGap gap={'8px'} />
            <CaseDataDisplay caseData={props.caseData} />
            <OpenCaseDisplayButton onClick={() => c_openCase()}>
                <Icon>{SVG_PATHS.redirect}</Icon>
                <HorizontalGap gap={'4px'} />
                Open
            </OpenCaseDisplayButton>
        </CaseDisplayPopupContainer>
    </>
}
