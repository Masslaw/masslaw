import {model} from "../../../../../../model/model";
import {useCaseData} from "../../../../../hooks/useCaseData";
import {useParams} from "react-router-dom";
import styled from "styled-components";
import {useCaseUserAccessLevel} from "../../../../../hooks/useCaseUserAccessLevel";
import {accessLevelsOrder, caseAccessLevels} from "../../../../../../config/caseConsts";
import {VerticalGap} from "../../../../../components/verticalGap";
import {CaseFilesHierarchyDisplay} from "../../../../../components/CaseFilesHierarchyDisplay";
import React, {useMemo} from "react";
import {pushPopup} from "../../../../../global-view/globalLayer/_global-layer-components/popups";
import {UploadCaseFilesPopup} from "../_uploadCaseFilesPopup";
import {CaseUserData} from "../../../../../components/caseUserData";
import {SVG_PATHS} from "../../../../../config/svgPaths";
import {Icon} from "../../../../../components/icon";
import {RedirectButtonWrapper} from "../../../../../components/redirectButtonWrapper";
import {constructUrl} from "../../../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../../../config/applicaitonRoutes";
import {HorizontalGap} from "../../../../../components/horizontalGap";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {KnowledgeDisplay} from "../../../../../components/knowledgeDisplay";
import {CaseKnowledgeGraphDisplay} from "../../../../../components/caseKnowledgeGraphDisplay";
import {CaseTimelineDisplay} from "../../../../../components/caseTimelineDisplay";


const DashboardPageContainer = styled.div`
    position: relative;
    width: calc(100% - 64px);
    height: 100%;
    overflow: auto;
    padding: 32px;
    &::-webkit-scrollbar { display: none; }
`

const DashboardPageTitleSection = styled.div`
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
`

const DashboardPageCaseTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const DashboardGoToSettingsButton = styled.div`
    font-size: 14px;
    color: white;
    margin-left: 8px;
    cursor: pointer;
    border: 1px solid #505050;
    padding: 8px 16px;
    border-radius: 8px;
    background: none;
    flex-basis: max-content;
    flex-grow: 0;
    flex-shrink: 0;
    &:hover { background: #505050; }
`

const DashboardPageCaseDescription = styled.div`
    width: 100%;
    font-size: 16px;
    line-height: 24px;
    letter-spacing: .5px;
    color: white;
`

const DashboardDisplaySectionsRow = styled.div`
    width: 100%;
    height: 512px;
    display: flex;
    flex-direction: row;
    overflow: auto;
    gap: 16px;
`

const DashboardDisplaySection = styled.div`
    display: flex;
    flex-direction: column;
    padding: 16px;
    border: 1px solid #505050;
    border-radius: 8px;
    background: #151515;
    ${({width}) => width ? `width: ${width};` : ''}
`

const DashBoardDisplaySectionTitleSection = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-bottom: 8px;
    width: 100%;
    max-height: max-content;
    flex-basis: max-content;
    flex-grow: 0;
    flex-shrink: 0;
`

const DashboardDisplaySectionTitle = styled.div`
    font-size: 16px;
    margin: 4px 0;
    font-weight: bold;
    color: white;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex-basis: 0;
    flex-grow: 1;
    flex-shrink: 0;
`

const DashboardDisplaySectionTitleButton = styled.div`
    font-size: 14px;
    color: white;
    cursor: pointer;
    height: 24px;
    width: max-content;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: 8px;
    border: 1px solid #505050;
    border-radius: 8px;
    background: none;
    padding: 0 16px;
    &:hover { background: #505050; }
`

const DashboardDisplaySectionSubTitle = styled.div`
    font-size: 14px;
    color: #808080;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 100%;
    max-height: max-content;
    flex-basis: max-content;
    flex-grow: 0;
    flex-shrink: 0;
    margin-bottom: 8px;
`

const DashboardDisplaySectionContent = styled.div`
    width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: auto;
    border-radius: 8px;
    &::-webkit-scrollbar { display: none; }
`

export function CaseDashboard(props) {

    const {caseId} = useParams();

    model.application.pages.currentPage.name = 'CaseDashboard';

    const s_caseData = useCaseData(caseId);

    const s_myUserAccessLevel = useCaseUserAccessLevel(caseId);

    return <>
        <DashboardPageContainer>
            <DashboardPageTitleSection>
                <DashboardPageCaseTitle>
                    {s_caseData.title}
                </DashboardPageCaseTitle>
                {[caseAccessLevels.owner, caseAccessLevels.manager].includes(s_myUserAccessLevel) ? <>
                    <DashboardGoToSettingsButton>
                        <Icon>{SVG_PATHS.gear}</Icon>
                        <HorizontalGap gap={'4px'} />
                        Case Settings
                    </DashboardGoToSettingsButton>
                </> : <></>}
            </DashboardPageTitleSection>
            <VerticalGap gap={'16px'} />
            <DashboardPageCaseDescription>
                {s_caseData.description}
            </DashboardPageCaseDescription>
            <VerticalGap gap={'32px'} />
            <DashboardDisplaySectionsRow>
                <DashboardDisplaySection width={'calc(20% - 8px)'}>
                    <DashBoardDisplaySectionTitleSection>
                        <DashboardDisplaySectionTitle>Case Files</DashboardDisplaySectionTitle>
                        <DashboardDisplaySectionTitleButton onClick={() => pushPopup({component: UploadCaseFilesPopup})}>
                            <Icon>{SVG_PATHS.addFile}</Icon>
                            <HorizontalGap gap={'4px'} />
                            Upload Files
                        </DashboardDisplaySectionTitleButton>
                    </DashBoardDisplaySectionTitleSection>
                    <DashboardDisplaySectionSubTitle>The files this case contains</DashboardDisplaySectionSubTitle>
                    <DashboardDisplaySectionContent>
                        <CaseFilesContent />
                    </DashboardDisplaySectionContent>
                </DashboardDisplaySection>
                <DashboardDisplaySection width={'calc(80% - 8px)'}>
                    <DashBoardDisplaySectionTitleSection>
                        <DashboardDisplaySectionTitle>
                            <Icon>{SVG_PATHS.person}</Icon>
                            <HorizontalGap gap={'4px'} />
                            Case Participants
                        </DashboardDisplaySectionTitle>
                        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_USERS, {caseId})}>
                            <DashboardDisplaySectionTitleButton>
                                <Icon>{SVG_PATHS.redirect}</Icon>
                            </DashboardDisplaySectionTitleButton>
                        </RedirectButtonWrapper>
                    </DashBoardDisplaySectionTitleSection>
                    <DashboardDisplaySectionSubTitle>The people participating in this case</DashboardDisplaySectionSubTitle>
                    <DashboardDisplaySectionContent>
                        <CaseUsersContent caseData={s_caseData} />
                    </DashboardDisplaySectionContent>
                </DashboardDisplaySection>
            </DashboardDisplaySectionsRow>
            <VerticalGap gap={'16px'} />
            <DashboardDisplaySectionsRow>
                <DashboardDisplaySection width={'calc(60% - 8px)'}>
                    <DashBoardDisplaySectionTitleSection>
                        <DashboardDisplaySectionTitle>
                            <Icon>{SVG_PATHS.knowledge}</Icon>
                            <HorizontalGap gap={'4px'} />
                            Case Knowledge
                        </DashboardDisplaySectionTitle>
                        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_KNOWLEDGE, {caseId})}>
                            <DashboardDisplaySectionTitleButton>
                                <Icon>{SVG_PATHS.redirect}</Icon>
                            </DashboardDisplaySectionTitleButton>
                        </RedirectButtonWrapper>
                    </DashBoardDisplaySectionTitleSection>
                    <DashboardDisplaySectionSubTitle>Entities and Relations MassLaw managed to extract from the case's text</DashboardDisplaySectionSubTitle>
                    <DashboardDisplaySectionContent>
                        <CaseKnowledgeContent />
                    </DashboardDisplaySectionContent>
                </DashboardDisplaySection>
                <DashboardDisplaySection width={'calc(40% - 8px)'}>
                    <DashBoardDisplaySectionTitleSection>
                        <DashboardDisplaySectionTitle>
                            <Icon>{SVG_PATHS.timeline}</Icon>
                            <HorizontalGap gap={'4px'} />
                            Case Timeline
                        </DashboardDisplaySectionTitle>
                        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_TIMELINE, {caseId})}>
                            <DashboardDisplaySectionTitleButton>
                                <Icon>{SVG_PATHS.redirect}</Icon>
                            </DashboardDisplaySectionTitleButton>
                        </RedirectButtonWrapper>
                    </DashBoardDisplaySectionTitleSection>
                    <DashboardDisplaySectionSubTitle>The Dates and Tiles MassLaw managed to extract from the case's text</DashboardDisplaySectionSubTitle>
                    <DashboardDisplaySectionContent>
                        <CaseKnowledgeTimeline />
                    </DashboardDisplaySectionContent>
                </DashboardDisplaySection>
            </DashboardDisplaySectionsRow>
        </DashboardPageContainer>
    </>
}


function CaseFilesContent(props) {
    return <>
        <CaseFilesHierarchyDisplay />
    </>
}

const CaseUsersContentContainer = styled.div`
    width: 100%;
    max-width: 100%;
    height: max-content;
    position: relative;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
    justify-content: space-between;
`

const CaseUserDataContainer = styled.div`
    position: relative;
    width: calc(100% - 16px - 2px);
    margin: 8px 0;
    padding: 8px;
    background: #202020;
    border: 1px solid #505050;
    border-radius: 8px;
`

function CaseUsersContent(props) {

    const m_caseUserItems = useMemo(() => {
        const caseParticipants = props.caseData.users || {};
        const caseParticipantIds = Object.keys(caseParticipants);
        caseParticipantIds.sort((a, b) => {
            if (a === model.users.mine.data.User_ID) return -1;
            if (b === model.users.mine.data.User_ID) return 1;
            const aData = caseParticipants[a];
            const bData = caseParticipants[b];
            return accessLevelsOrder.indexOf(bData.access_level) - accessLevelsOrder.indexOf(aData.access_level);
        })
        return caseParticipantIds.map((userId) => <>
            <CaseUserDataContainer key={userId}>
                <CaseUserData userId={userId} caseId={props.caseData.case_id} />
            </CaseUserDataContainer>
        </>);
    }, [props.caseData]);

    return <>
        <CaseUsersContentContainer>
            {m_caseUserItems}
        </CaseUsersContentContainer>
    </>
}

function CaseKnowledgeContent(props) {

    return <>
        <CaseKnowledgeGraphDisplay hideInfo={true} />
    </>
}

function CaseKnowledgeTimeline(props) {

    return <>
        <CaseTimelineDisplay hideInfo={true} scale={64}/>
    </>
}
