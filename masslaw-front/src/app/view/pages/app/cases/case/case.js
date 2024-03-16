import {Outlet, useParams} from "react-router-dom";
import styled from "styled-components";
import React, {useEffect, useMemo, useState} from "react";
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
import {VerticalGap} from "../../../../components/bits-and-pieces/verticalGap";

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
    flex-basis: 0;
    position: relative;
    width: 100%;
    height: 100%;
`

const CaseSidePanelContainer = styled.div`
    display: block;
    width: 255px;
    height: 100%;
    background-color: #303030;
    border-right: 1px solid #999999;
    color: white;
    overflow-x: hidden;
    overflow-y: auto;
    &::-webkit-scrollbar { display: none; }
`

const CaseDisplayOutletWrapper = styled.div`
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    position: relative;
    height: 100%;
    max-height: 100%;
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
    }, [s_userStatus, caseId]);


    return <>
        <CaseContainer>
            <CaseSidePanelAlignment>
                <CaseSidePanelContainer>
                    <CaseSidePanel/>
                </CaseSidePanelContainer>
                <CaseDisplayOutletWrapper>
                    {s_loadingCase ? <></> : <Outlet/>}
                </CaseDisplayOutletWrapper>
            </CaseSidePanelAlignment>
        </CaseContainer>
    </>
}

const CaseSidePanelSeparator = styled.div`
    position: relative;
    width: 100%;
    height: 1px;
    background: #505050;
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
    background: ${({open}) => open ? '#404040' : 'none'};

    &:hover {
        background: #505050;
    }
    
    svg { 
        width: 20px;
        height: 20px;
        fill: white;
        margin-right: 8px;
    }
`

const CaseSidePanelOpenedSection = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100% - 5px);
    border-left: 1px solid #505050;
    margin-left: 4px;
`

const CaseSidePanelTitle = styled.div`
    position: sticky;
    top: 0;
    color: white;
    padding: 16px;
    font-size: 22px;
    width: calc(100% - 32px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-bottom: 1px solid #505050;
    background: #303030;
    z-index: 1;
`

function CaseSidePanel(props) {

    const [s_caseId, setCaseId] = useModelValueAsReactState("$.cases.currentOpen.id", '');
    const [s_casesData, setCaseData] = useModelValueAsReactState("$.cases.all", {});

    const [s_currentPage, setCurrentPage] = useModelValueAsReactState("$.application.pages.currentPage.name", '');

    const m_caseData = useMemo(() => (s_casesData[s_caseId] || {}), [s_caseId, s_casesData]);

    return <>
        <CaseSidePanelTitle>{m_caseData.title}</CaseSidePanelTitle>
        <FilesUploading/>
        <CaseSidePanelFilesSection/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_DASHBOARD, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseDashboard'}>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.dashboard}/></svg>
                Dashboard
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_SEARCH, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseSearch'}>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.search}/></svg>
                Search
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_KNOWLEDGE, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseKnowledge'}>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.knowledge}/></svg>
                Knowledge
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_TIMELINE, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseTimeline'}>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.timeline}/></svg>
                Timeline
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.CASE_SUBJECTS, {caseId: s_caseId})}>
            <CaseSidePanelButton open={s_currentPage === 'CaseSubjects'}>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.subjects}/></svg>
                Subjects
            </CaseSidePanelButton>
        </RedirectButtonWrapper>
        <VerticalGap gap={'8px'}/>
        <CaseSidePanelSeparator/>
        <VerticalGap gap={'8px'}/>
        {/*...*/}
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
    margin: 8px 10px 4px 6px;
    width: calc(100% - 16px);
    border: 1px solid #808080;
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

    return <>
        <CaseSidePanelFilesSectionContainer>
            <CaseSidePanelOpenedSection>
                <CaseSidePanelFilesSectionUploadButton onClick={() => pushPopup({component: UploadCaseFilesPopup})}>
                    <svg viewBox={'0 0 1050 1050'}><path d={SVG_PATHS.addFile}/></svg>
                    Upload Files
                </CaseSidePanelFilesSectionUploadButton>
                <VerticalGap gap={'8px'}/>
                <CaseSidePanelFileHierarchy/>
                <VerticalGap gap={'8px'}/>
            </CaseSidePanelOpenedSection>
            <CaseSidePanelSeparator/>
        </CaseSidePanelFilesSectionContainer>
    </>
}

function CaseSidePanelFileHierarchy(props) {

    const [s_caseId, setCaseId] = useModelValueAsReactState("$.cases.currentOpen.id", '');
    const [s_casesData, setCaseData] = useModelValueAsReactState("$.cases.all", {});

    const m_caseData = useMemo(() => (s_casesData[s_caseId] || {}), [s_caseId, s_casesData]);

    return <>
        <CaseSidePanelFileHierarchyFolder name={m_caseData.title} hierarchy={m_caseData.contentHierarchy}/>
    </>
}

const CaseSidePanelFileHierarchyFolderContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 4px 0 4px 4px;
`

const CaseSidePanelFileHierarchyTitleContainer = styled.div`
    position: relative;
    height: 20px;
    line-height: 20px;
    font-size: 14px;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 2px 4px;
    cursor: pointer;
`

const CaseSidePanelFileHierarchyArrowIcon = styled.div`
    position: relative;
    width: 16px;
    height: 16px;

    svg {
        width: 100%;
        height: 100%;
        fill: #999999;
    }
`

const CaseSidePanelFileHierarchyFolderIcon = styled.div`
    position: relative;
    width: 16px;
    min-width: 16px;
    height: 16px;
    margin-left: 8px;

    svg {
        width: 100%;
        height: 100%;
        fill: #a0a0a0;
    }
`

const CaseSidePanelFileHierarchyFolderTitle = styled.div`
    position: relative;
    margin-left: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseSidePanelFileHierarchyFolderContentContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    margin-left: 12px;
    padding-left: 16px;
    border-left: 1px solid #404040;
`

function CaseSidePanelFileHierarchyFolder(props) {
    const [s_open, setOpen] = useState(false);

    const m_content = useMemo(() => {

        const folderItems = [];
        const fileItems = [];
        for (const item in props.hierarchy) {
            const itemData = props.hierarchy[item];
            if (typeof itemData === 'object') {
                folderItems.push(item);
            } else {
                fileItems.push(item);
            }
        }

        folderItems.sort();
        fileItems.sort();

        return <>
            {folderItems.map((folderName, index) => <CaseSidePanelFileHierarchyFolder key={folderName} name={folderName} hierarchy={props.hierarchy[folderName]}/>)}
            {fileItems.map((fileName, index) => <CaseSidePanelFileHierarchyFile key={fileName} name={fileName} fileId={props.hierarchy[fileName]}/>)}
        </>
    }, [props.hierarchy]);

    return <>
        <CaseSidePanelFileHierarchyFolderContainer>
            <CaseSidePanelFileHierarchyTitleContainer onClick={() => setOpen(_ => !_)} title={props.name}>
                <CaseSidePanelFileHierarchyArrowIcon>
                    <svg viewBox={s_open ? "-100 -100 1000 700" : "-100 -100 700 1000"}>
                        <path d={s_open ? SVG_PATHS.arrowDown : SVG_PATHS.arrowRight}/>
                    </svg>
                </CaseSidePanelFileHierarchyArrowIcon>
                <CaseSidePanelFileHierarchyFolderIcon>
                    <svg viewBox={"0 0 1000 800"}>
                        <path d={SVG_PATHS.folder}/>
                    </svg>
                </CaseSidePanelFileHierarchyFolderIcon>
                <CaseSidePanelFileHierarchyFolderTitle>
                    {props.name}
                </CaseSidePanelFileHierarchyFolderTitle>
            </CaseSidePanelFileHierarchyTitleContainer>
            <CaseSidePanelFileHierarchyFolderContentContainer>{s_open ? m_content : <></>}</CaseSidePanelFileHierarchyFolderContentContainer>
        </CaseSidePanelFileHierarchyFolderContainer>
    </>
}

const CaseSidePanelFileHierarchyFileContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 4px;

    &:hover {
        background: #404040;
    }
`

const CaseSidePanelFileHierarchyFileNameContainer = styled.div`
    position: relative;
    height: 20px;
    line-height: 20px;
    font-size: 14px;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 2px 4px;
    cursor: pointer;
`

const CaseSidePanelFileHierarchyFileIcon = styled.div`
    position: relative;
    width: 16px;
    min-width: 16px;
    height: 16px;
    margin-left: 8px;

    svg {
        width: 100%;
        height: 100%;
        fill: #a0a0a0;
    }
`

const CaseSidePanelFileHierarchyFileTitle = styled.div`
    position: relative;
    margin-left: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

function CaseSidePanelFileHierarchyFile(props) {

    const {caseId} = useParams();

    return <>
        <CaseSidePanelFileHierarchyFileContainer>
            <CaseSidePanelFileHierarchyFileNameContainer onClick={() => {
                pushPopup({component: CaseFilePopup, componentProps: {caseId: caseId, fileId: props.fileId}})
            }} title={props.name}>
                <CaseSidePanelFileHierarchyFileIcon>
                    <svg viewBox={"0 0 1000 1000"}>
                        <path d={SVG_PATHS.file}/>
                    </svg>
                </CaseSidePanelFileHierarchyFileIcon>
                <CaseSidePanelFileHierarchyFileTitle>
                    {props.name}
                </CaseSidePanelFileHierarchyFileTitle>
            </CaseSidePanelFileHierarchyFileNameContainer>
        </CaseSidePanelFileHierarchyFileContainer>
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
    color: #999999;
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
            casesManager.fetchCaseContentHierarchy().then();
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
