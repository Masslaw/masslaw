import styled from "styled-components";
import {useEffect, useMemo, useState} from "react";
import {model} from "../../../../../../model/model";
import {CaseUserData} from "../../../../../components/caseUserData";
import {accessLevelsOrder, caseAccessLevels} from "../../../../../../config/caseConsts";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {pushPopup} from "../../../../../global-view/globalLayer/_global-layer-components/popups";
import {AddCaseUsersPopup} from "./_addCaseUsersPopup";
import {useParams} from "react-router-dom";
import {SVG_PATHS} from "../../../../../config/svgPaths";
import {CaseUserAccessData} from "../../../../../components/caseUserAccessData";
import {VerticalGap} from "../../../../../components/verticalGap";
import {useCaseUserAccessLevel} from "../../../../../hooks/useCaseUserAccessLevel";

const CaseUsersPageContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    overflow: auto;
    background: #202020;
`

const CaseUsersTopSection = styled.div`
    width: calc(100% - 64px);
    margin: 32px;
    color: white;
    display: flex;
    flex-direction: row;
    align-items: center;
`

const CaseUsersTitleSubTitleSection = styled.div`
    display: flex;
    flex-direction: column;
    
    span:nth-child(1) {
        font-size: 24px;
        color: white;
        font-weight: bold;
        margin-bottom: 16px;
    }
    
    span:nth-child(2) {
        font-size: 14px;
        color: #808080;
    }
`

const CaseUsersAddUsersButton = styled.button`
    width: 160px;
    height: 42px;
    font-size: 12px;
    color: white;
    border: 1px solid white;
    background: none;
    outline: none;
    border-radius: 12px;
    cursor: pointer;
    margin-left: auto;
    font-weight: bold;
    &:hover { 
        background: white;
        color: black;
    }
`

const CaseUsersItemsContainer = styled.div`
    position: relative;
    display: grid;
    grid-template-columns: repeat(auto-fill, calc(512px + 32px + 16px));
    justify-content: space-between;
    flex-grow: 1;
    border-radius: 12px;
    padding: 8px 32px;
    width: calc(100% - 64px);
    height: max-content;
`

export function CaseUsers(props) {

    const {caseId} = useParams();

    model.application.pages.currentPage.name = 'CaseUsers'

    const casesManager = model.services['casesManager'];

    const [s_caseData, setCaseData] = useState(null);

    useEffect(() => {
        if (!caseId) return;
        casesManager.fetchCaseData(caseId).then(() => {
            const caseData = model.cases.all[caseId];
            setCaseData(caseData);
        });
    }, [caseId]);

    const m_myUserAccessLevel = useCaseUserAccessLevel();

    const m_caseUserItems = useMemo(() => {
        if (!caseId) return <></>
        const caseUsers = (s_caseData || {}).users || {};
        return Object.keys(caseUsers)
            .sort((u1, u2) => accessLevelsOrder.indexOf(caseUsers[u1].access_level) - accessLevelsOrder.indexOf(caseUsers[u2].access_level))
            .map((userId) => <>
            <CaseUserItemDisplay
                key={userId}
                caseId={caseId}
                userId={userId}
            />
        </>)
    }, [caseId, s_caseData])

    return <>
        <CaseUsersPageContainer>
            {!s_caseData ? <>
                <LoadingIcon width={'30px'} height={'30px'} />
            </> : <>
                <CaseUsersTopSection>
                    <CaseUsersTitleSubTitleSection>
                        <span>Case Participants</span>
                        <span>People who participate in this case</span>
                    </CaseUsersTitleSubTitleSection>
                    { [caseAccessLevels.owner, caseAccessLevels.manager].includes(m_myUserAccessLevel) ? <>
                        <CaseUsersAddUsersButton onClick={() => pushPopup({component: AddCaseUsersPopup, componentProps: {caseId: caseId}})}>
                            Add Participants
                        </CaseUsersAddUsersButton>
                    </> : <></>}
                </CaseUsersTopSection>
            </>}
            <CaseUsersItemsContainer>{m_caseUserItems}</CaseUsersItemsContainer>
        </CaseUsersPageContainer>
    </>
}

const CaseUserItemDisplayContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 512px;
    height: max-content;
    background: #282828;
    border: 1px solid #505050;
    margin: 16px 8px;
    padding: 8px;
    border-radius: 12px;
    transition: 0.5s linear;
`

const CaseUserPermissionsContainer = styled.div`
    width: calc(100% - 32px);
    padding: 4px 16px;
`

const CaseUserPermissionsShowHideButton = styled.button`
    color: #808080;
    border: none;
    background: none;
    outline: none;
    cursor: pointer;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    svg {
        width: 12px;
        height: 12px;
        transform: scaleY(${({open}) => open ? '-1' : '1'});
        margin-right: 8px;
        fill: #808080;
    }
`

function CaseUserItemDisplay(props) {

    const caseUsersManager = model.services['caseUsersManager'];

    const m_myUserAccessLevel = useCaseUserAccessLevel(props.caseId);

    const m_targetUserAccessLevel = useCaseUserAccessLevel(props.caseId, props.userId);

    const [s_permissionsShown, setPermissionsShown] = useState(false);

    return <>
        <CaseUserItemDisplayContainer>
            <CaseUserData caseId={props.caseId} userId={props.userId} />
            { [caseAccessLevels.owner, caseAccessLevels.manager].includes(m_myUserAccessLevel) && ![caseAccessLevels.owner].includes(m_targetUserAccessLevel) ? <>
                <CaseUserPermissionsContainer>
                    <CaseUserPermissionsShowHideButton
                        open={s_permissionsShown}
                        onClick={() => setPermissionsShown(p => !p)}
                    >
                        <svg viewBox={'0 0 1000 1000'}>
                            <path d={SVG_PATHS.arrowDown}/>
                        </svg>
                        {s_permissionsShown ? 'Hide Permissions' : 'Show Permissions'}
                    </CaseUserPermissionsShowHideButton>
                    {s_permissionsShown ? <>
                        <CaseUserAccessData userId={props.userId} caseId={props.caseId}/>
                    </> : <></>}
                </CaseUserPermissionsContainer>
                <VerticalGap gap={'8px'} />
            </> : <></>}
        </CaseUserItemDisplayContainer>
    </>
}
