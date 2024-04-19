import {Outlet, useParams} from "react-router-dom";
import styled from "styled-components";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import {model} from "../../../../../model/model";
import {UserStatus} from "../../../../../config/userStatus";
import {useModelValueAsReactState} from "../../../../../controller/functionality/model/modelReactHooks";
import {pushPopup} from "../../../../global-view/globalLayer/_global-layer-components/popups";
import {UploadCaseFilesPopup} from "./_uploadCaseFilesPopup";
import {pushNotification} from "../../../../global-view/globalLayer/_global-layer-components/notifications";
import {SVG_PATHS} from "../../../../config/svgPaths";
import {CaseFilePopup} from "./_caseFilePopup";
import {RedirectButtonWrapper} from "../../../../components/redirectButtonWrapper";
import {constructUrl} from "../../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../../config/applicaitonRoutes";
import {VerticalGap} from "../../../../components/verticalGap";
import {LoadingIcon} from "../../../../components/loadingIcon";
import {useCaseUserAccessLevel} from "../../../../hooks/useCaseUserAccessLevel";
import {caseAccessLevels} from "../../../../../config/caseConsts";
import {CaseFilesHierarchyDisplay} from "../../../../components/CaseFilesHierarchyDisplay";
import {Icon} from "../../../../components/icon";

const CaseContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    position: relative;
`

const CaseSidePanelAlignment = styled.div`
    display: flex;
    flex-direction: row;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 100%;
    position: relative;
    width: 100%;
    height: 100%;
`

const CaseSidePanelContainer = styled.div`
    display: block;
    width: 256px;
    height: 100%;
    background-color: #151515;
    border-right: 1px solid #505050;
    color: white;
    overflow-x: hidden;
    overflow-y: auto;
    flex-basis: 256px;
    flex-shrink: 0;
    flex-grow: 0;
    &::-webkit-scrollbar { display: none; }
`

const CaseDisplayOutletWrapper = styled.div`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    min-width: 0;
    position: relative;
    height: 100%;
    max-height: 100%;
    background: #202020;
`

export function Case(props) {
    const {caseId} = useParams();

    model.application.pages.currentPage.name = "Case";
    model.application.pages.currentPage.minimumUserStatus = UserStatus.FULLY_APPROVED;
    model.application.pages.currentPage.maximumUserStatus = null;
    model.application.view.state.header.shown = true;

    const casesManager = model.services['casesManager'];

    const [s_loadingCase, setLoadingCase] = useModelValueAsReactState("$.application.view.state.loading.case_page", false);

    useEffect(() => {
        setLoadingCase(true);
        model.cases.currentOpen.id = caseId;
    }, []);

    const [s_userStatus, setUserStatus] = useModelValueAsReactState("$.users.mine.authentication.status");

    useEffect(() => {
        if (s_userStatus < UserStatus.FULLY_APPROVED) return;
        setLoadingCase(true);
        model.cases.currentOpen.id = caseId;
        casesManager.fetchCaseData().then(() => {setLoadingCase(false)});
        casesManager.fetchCaseContentHierarchy().then(() => {});
    }, [s_userStatus, caseId]);


    return <>
        <CaseContainer>
            <CaseSidePanelAlignment>
                <CaseSidePanelContainer>
                    <CaseSidePanel/>
                </CaseSidePanelContainer>
                <CaseDisplayOutletWrapper>
                    {s_loadingCase ? <><LoadingIcon width={'30px'} height={'30px'}/></> : <Outlet/>}
                </CaseDisplayOutletWrapper>
            </CaseSidePanelAlignment>
        </CaseContainer>
    </>
}

const CaseSidePanelSeparator = styled.div`
    position: relative;
    width: 100%;
    height: 1px;
    background: #151515;
    background: linear-gradient(90deg, #151515 0%, #505050 20%, #505050 80%, #151515 100%);
    margin: 0;
`

const CaseSidePanelButton = styled.button`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    color: white;
    margin: 0 8px;
    padding: 12px;
    width: calc(100% - 16px);
    border: none;
    border-radius: 8px;
    text-align: left;
    font-size: 16px;
    background: ${({open}) => open ? '#303030' : 'none'};

    &:hover {
        background: #353535;
    }
    
    svg { 
        width: 20px;
        height: 20px;
        fill: white;
        margin-right: 8px;
    }
`

const CaseSidePanelTitle = styled.div`
    position: sticky;
    display: flex;
    flex-direction: row;
    z-index: 1;
    top: 0;
    border-bottom: 1px solid #505050;
    background: #151515;
    & > span {
        color: white;
        padding: 16px;
        font-size: 22px;
        flex-grow: 1;
        flex-shrink: 0;
        flex-basis: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    button {
        position: relative;
        top: 50%;
        transform: translateY(-50%);
        cursor: pointer;
        border: none;
        outline: none;
        background: none;
        color: white;
        margin: 0 8px;
        font-size: 20px;
    }
`

function CaseSidePanel(props) {

    const [s_caseId, setCaseId] = useModelValueAsReactState("$.cases.currentOpen.id", '');
    const [s_casesData, setCaseData] = useModelValueAsReactState("$.cases.all", {});

    const [s_currentPage, setCurrentPage] = useModelValueAsReactState("$.application.pages.currentPage.name", '');

    const m_caseData = useMemo(() => (s_casesData[s_caseId] || {}), [s_caseId, s_casesData]);

    const s_myUserAccessLevel = useCaseUserAccessLevel(s_caseId);

    return <>
        <CaseSidePanelTitle>
            <span>{m_caseData.title}</span>
            {[caseAccessLevels.owner, caseAccessLevels.manager].includes(s_myUserAccessLevel) ? <>
                <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_SETTINGS, {caseId: s_caseId})}>
                    <button><Icon>{SVG_PATHS.gear}</Icon></button>
                </RedirectButtonWrapper>
            </> : <></>}
        </CaseSidePanelTitle>
        <FilesUploading/>
        <CaseSidePanelFilesSection/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_DASHBOARD, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseDashboard'}>
                <Icon>{SVG_PATHS.dashboard}</Icon>
                Dashboard
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_CONVERSATIONS, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseConversations'}>
                <Icon>{SVG_PATHS.conversations}</Icon>
                MassBot
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_SEARCH, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseSearch'}>
                <Icon>{SVG_PATHS.search}</Icon>
                Search
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_KNOWLEDGE, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseKnowledge'}>
                <Icon>{SVG_PATHS.knowledge}</Icon>
                Knowledge
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_TIMELINE, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseTimeline'}>
                <Icon>{SVG_PATHS.timeline}</Icon>
                Timeline
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_USERS, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseUsers'}>
                <Icon>{SVG_PATHS.person}</Icon>
                Participants
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        <VerticalGap gap={'256px'}/>
    </>
}

const CaseSidePanelFilesSectionContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
`

const CaseSidePanelFilesSectionUploadButton = styled.button`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 8px 8px 4px 8px;
    width: calc(100% - 16px);
    border: 1px solid #505050;
    background: none;
    color: white;
    border-radius: 12px;
    font-size: 14px;
    padding: 10px;
    letter-spacing: .5px;

    &:hover {
        background: #808080;
    }
    
    svg {
        width: 16px;
        height: 16px;
        fill: white;
        margin-right: 8px;
    }
`

function CaseSidePanelFilesSection(props) {

    const m_myUserAccessLevel = useCaseUserAccessLevel(props.caseId);

    return <>
        <CaseSidePanelFilesSectionContainer>
            {[caseAccessLevels.owner, caseAccessLevels.manager, caseAccessLevels.editor].includes(m_myUserAccessLevel) ? <>
                <CaseSidePanelFilesSectionUploadButton onClick={() => pushPopup({component: UploadCaseFilesPopup})}>
                    <Icon>{SVG_PATHS.addFile}</Icon>
                    Upload Files
                </CaseSidePanelFilesSectionUploadButton>
            </> : <></>}
            <VerticalGap gap={'8px'}/>
            <CaseFilesHierarchyDisplay/>
            <VerticalGap gap={'8px'}/>
            <CaseSidePanelSeparator/>
        </CaseSidePanelFilesSectionContainer>
    </>
}

const FilesUploadingContainer = styled.div`
    width: 100%;
    display: flex;
    flex-direction: column;
`

const FilesUploadingTitle = styled.div`
    position: relative;
    color: white;
    width: calc(100% - 16px);
    padding: 8px 8px 2px 8px;
    font-size: 14px;
`

const FilesUploadingLeftCounter = styled.div`
    position: relative;
    color: #808080;
    width: calc(100% - 16px);
    padding: 8px;
    font-size: 12px;
`

const FilesUploadingFileName = styled.div`
    position: relative;
    color: white;
    width: calc(100% - 16px);
    padding: 2px 8px 2px 8px;
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const FilesUploadingFileProgress = styled.div`
    position: relative;
    color: white;
    width: calc(100% - 18px);
    height: 4px;
    border: 1px solid #606060;
    border-radius: 2px;
    background: none;
    margin: 2px 8px 8px 8px;
    overflow: hidden;
`

const FilesUploadingFileProgressBar = styled.div`
    position: absolute;
    width: ${({progress}) => progress};
    height: 100%;
    background: white;
    top: 0;
    left: 0;
`

function FilesUploading(props) {

    const modelToLocalStorageManager = model.services['modelToLocalStorageManager'];
    const contentUploader = model.services['contentUploader'];
    const casesManager = model.services['casesManager'];

    const caseId = model.cases.currentOpen.id;

    const [s_previousNumberOfFiles, setPreviousNumberOfFiles] = useState(0);

    const [s_caseFilesToUpload, setCaseFilesToUpload] = useModelValueAsReactState(`$.cases.currentOpen.files.filesToUpload`);

    const [s_uploadingFile, setUploadingFile] = useState(null);

    useEffect(() => {
        const numberOfFiles = (s_caseFilesToUpload[caseId] || []).length;
        setPreviousNumberOfFiles(numberOfFiles);
        if (s_previousNumberOfFiles > 0) return;
        if (numberOfFiles === 0) return;
        pushNotification({title: "Files Uploading", body: "Files are being uploaded in the background. You can continue using the application."});
    }, [s_caseFilesToUpload, s_previousNumberOfFiles]);

    useEffect(() => {
        const caseFilesToUpload = s_caseFilesToUpload[caseId] || [];
        if (caseFilesToUpload.length === 0) return;
        const fileToUpload = caseFilesToUpload[0];
        contentUploader.uploadCaseFile(fileToUpload.file, fileToUpload.directory, (progress) => {
            setUploadingFile({name: fileToUpload.file.name, progress: progress});
        }).then(() => {
            setCaseFilesToUpload(p => ({...p, ...{[caseId]: caseFilesToUpload.slice(1)}}));
            casesManager.fetchCaseContentHierarchy(caseId, true).then();
        });
    }, [s_caseFilesToUpload]);

    return <>
        {((s_caseFilesToUpload[caseId] || []).length && s_uploadingFile) ? <>
            <FilesUploadingContainer>
                <FilesUploadingTitle>Uploading Files...</FilesUploadingTitle>
                <FilesUploadingLeftCounter>{`Left: ${(s_caseFilesToUpload[caseId] || []).length}`}</FilesUploadingLeftCounter>
                <FilesUploadingFileName>{s_uploadingFile.name}</FilesUploadingFileName>
                <FilesUploadingFileProgress>
                    <FilesUploadingFileProgressBar progress={`${Math.max(5, s_uploadingFile.progress * 100)}%`}/>
                </FilesUploadingFileProgress>
            </FilesUploadingContainer>
            <CaseSidePanelSeparator/>
        </> : <></>}
    </>
}
