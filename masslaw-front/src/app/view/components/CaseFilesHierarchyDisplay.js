import {model} from "../../model/model";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import React, {useCallback, useMemo, useState} from "react";
import {LoadingIcon} from "./loadingIcon";
import {SVG_PATHS} from "../config/svgPaths";
import styled from "styled-components";
import {VerticalGap} from "./verticalGap";
import {useParams} from "react-router-dom";
import {pushPopup} from "../global-view/globalLayer/_global-layer-components/popups";
import {CaseFilePopup} from "../pages/app/cases/case/_caseFilePopup";
import {Icon} from "./icon";


const CaseFileHierarchyContainer = styled.div`
    position: relative;
    width: 100%;
    max-height: max-content;
    background: #151515;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: max-content;
`

const CaseFileHierarchyReloadButton = styled.div`
    position: absolute;
    right: 0;
    top: 0;
    width: 18px;
    height: 18px;
    margin: 2px;
    padding: 4px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    background: #151515;
    border: 4px solid #151515;
    border-bottom: 0;
    border-top: 0;
    pointer-events: ${({reloading}) => reloading ? 'none' : 'all'};
    cursor: ${({reloading}) => reloading ? 'normal' : 'pointer'};
    &:hover {
        background: ${({reloading}) => reloading ? 'none' : '#303030'};
    }
    svg {
        width: 100%;
        height: 100%;
        fill: white;
    }
`

export function CaseFilesHierarchyDisplay(props) {

    const {casesManager} = model.services

    const [s_caseId, setCaseId] = useModelValueAsReactState("$.cases.currentOpen.id", '');
    const [s_casesData, setCaseData] = useModelValueAsReactState("$.cases.all", {});

    const m_caseData = useMemo(() => (s_casesData[s_caseId] || {}), [s_caseId, s_casesData]);

    const [s_reloadingContentHierarchy, setReloadingContentHierarchy] = useState(false);

    const c_reloadHierarchy = useCallback(() => {
        if (s_reloadingContentHierarchy) return;
        setReloadingContentHierarchy(true);
        casesManager.fetchCaseContentHierarchy(null, true).then(() => setReloadingContentHierarchy(false));
    }, [s_reloadingContentHierarchy]);

    return <>
        <CaseFileHierarchyContainer>
            <CaseFileHierarchyFolder
                name={m_caseData.title}
                hierarchy={m_caseData.contentHierarchy}
                open={true}
                loading={s_reloadingContentHierarchy}
            />
            <CaseFileHierarchyReloadButton
                reloading={s_reloadingContentHierarchy}
                onClick={c_reloadHierarchy}
            >
                {s_reloadingContentHierarchy ? <>
                    <LoadingIcon width={'16px'} height={'16px'} />
                </> : <>
                    <Icon>{SVG_PATHS.circleArrow}</Icon>
                </>}
            </CaseFileHierarchyReloadButton>
        </CaseFileHierarchyContainer>
    </>
}

const CaseFileHierarchyFolderContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 4px 0 0 4px;
`

const CaseFileHierarchyTitleContainer = styled.div`
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

const CaseFileHierarchyArrowIcon = styled.div`
    position: relative;
    width: 12px;

    svg {
        width: 100%;
        height: 100%;
        fill: #808080;
    }
`

const CaseFileHierarchyFolderIcon = styled.div`
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

const CaseFileHierarchyFolderTitle = styled.div`
    position: relative;
    margin-left: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseFileHierarchyFolderContentContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    margin: 0 0 0 8px;
    padding: 0 0 0 8px;
    border-left: 1px solid #404040;
    height: max-content;
`

const EmptyFolderContainer = styled.div`
    position: relative;
    color: #808080;
    font-size: 12px;
    padding: 4px;
`

export function CaseFileHierarchyFolder(props) {
    const [s_open, setOpen] = useState(props.open);

    const m_content = useMemo(() => {
        const folderItems = [];
        const fileItems = [];
        for (const item in props.hierarchy) {
            const itemData = props.hierarchy[item];
            if (typeof itemData === 'object') folderItems.push(item);
            else fileItems.push(item);
        }
        if (folderItems.length === 0 && fileItems.length === 0) return <EmptyFolderContainer>Empty Folder</EmptyFolderContainer>
        folderItems.sort();
        fileItems.sort();
        return <>
            {folderItems.map((folderName, index) => <CaseFileHierarchyFolder key={folderName} name={folderName} hierarchy={props.hierarchy[folderName]}/>)}
            {fileItems.map((fileName, index) => <CaseFileHierarchyFile key={fileName} name={fileName} fileId={props.hierarchy[fileName]}/>)}
        </>
    }, [props.hierarchy]);

    return <>
        <CaseFileHierarchyFolderContainer>
            <CaseFileHierarchyTitleContainer onClick={() => setOpen(_ => !_)} title={props.name}>
                <CaseFileHierarchyArrowIcon>
                    <svg viewBox={s_open ? "0 0 1 1" : "0 0 1 1"}>
                        <path d={s_open ? SVG_PATHS.arrowDown : SVG_PATHS.arrowRight}/>
                    </svg>
                </CaseFileHierarchyArrowIcon>
                <CaseFileHierarchyFolderIcon>
                    <svg viewBox={"0 0 1 1"}>
                        <path d={SVG_PATHS.folder}/>
                    </svg>
                </CaseFileHierarchyFolderIcon>
                <CaseFileHierarchyFolderTitle>
                    {props.name}
                </CaseFileHierarchyFolderTitle>
            </CaseFileHierarchyTitleContainer>
            <CaseFileHierarchyFolderContentContainer>
                {s_open ? props.loading ? <>
                    <VerticalGap gap={'24px'}/><LoadingIcon width={'20px'} height={'20px'} />
                </> : m_content : <></>}
            </CaseFileHierarchyFolderContentContainer>
        </CaseFileHierarchyFolderContainer>
    </>
}

const CaseFileHierarchyFileContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 4px;

    &:hover {
        background: #404040;
    }
`

const CaseFileHierarchyFileNameContainer = styled.div`
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

const CaseFileHierarchyFileIcon = styled.div`
    position: relative;
    width: 16px;
    min-width: 16px;
    height: 16px;
    margin-left: 16px;

    svg {
        width: 100%;
        height: 100%;
        fill: #a0a0a0;
    }
`

const CaseFileHierarchyFileTitle = styled.div`
    position: relative;
    margin-left: 8px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

export function CaseFileHierarchyFile(props) {

    const {caseId} = useParams();

    return <>
        <CaseFileHierarchyFileContainer>
            <CaseFileHierarchyFileNameContainer onClick={() => {
                pushPopup({component: CaseFilePopup, componentProps: {caseId: caseId, fileId: props.fileId}})
            }} title={props.name}>
                <CaseFileHierarchyFileIcon>
                    <svg viewBox={"0 0 1 1"}>
                        <path d={SVG_PATHS.file}/>
                    </svg>
                </CaseFileHierarchyFileIcon>
                <CaseFileHierarchyFileTitle>
                    {props.name}
                </CaseFileHierarchyFileTitle>
            </CaseFileHierarchyFileNameContainer>
        </CaseFileHierarchyFileContainer>
    </>
}
