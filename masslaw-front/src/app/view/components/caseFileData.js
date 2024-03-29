import {LoadingIcon} from "./loadingIcon";
import {useParams} from "react-router-dom";
import {model} from "../../model/model";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {SVG_PATHS} from "../config/svgPaths";
import {LongTextInput} from "./longTextInput";
import {unixTimeToDayDateString, unixTimeToPastTimeString} from "../../controller/functionality/time-utils/dateTimeUtils";
import {VerticalGap} from "./verticalGap";
import {FileProcessingStage} from "./fileStage";
import {useCaseUserAccessLevel} from "../hooks/useCaseUserAccessLevel";
import {caseAccessLevels} from "../../config/caseConsts";

const CaseFilePopupFileName = styled.h1`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 32px 32px 16px 32px;
    width: calc(100% - 64px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseFilePopupDirectory = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    color: #999999;
    font-size: 14px;
    margin: 4px 32px;
    padding: 4px;
    width: max-content;
    max-width: calc(100% - 64px - 8px);
    overflow-y: hidden;
    overflow-x: auto;
    border: 1px solid #505050;
    border-radius: 4px;
    
`

const CaseFilePopupDirectoryLevel = styled.span`
    margin: 0 4px;
    color: #c0c0c0;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseFilePopupDirectorySeparator = styled.span`
`

const CaseFilePopupStageContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin: 16px 32px 8px 32px;
    font-size: 14px;
    height: max-content;
    width: calc(100% - 64px);
`

const CaseFilePopupStageTitle = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    font-weight: bold;
    color: #c0c0c0;
    margin-right: 8px;
    margin-bottom: 8px;
`

const CaseFileProcessingStageReloadButton = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    background: none;
    border: none;
    cursor: pointer;
    margin-left: 8px;
    border-radius: 5px;

    svg {
        width: 20px;
        height: 20px;
        fill: #c0c0c0;
    }
    
    &:hover {
        background: #c0c0c0;
    }
    
    &:hover svg {
        fill: #303030;
    }
`

const CaseFileProcessingStageReloading = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    background: none;
    border: none;
    margin-left: 8px;
`

const CaseFilePopupDescriptionSection = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 64px);
    margin: 16px 32px 8px 32px;
    color: white;
    font-size: 14px;
`

const CaseFilePopupDescriptionTitleSection = styled.h2`
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0;
    margin-bottom: 8px;
`

const CaseFilePopupDescriptionTitle = styled.h2`
    font-size: 16px;
    font-weight: bold;
    margin: 0;
    color: #c0c0c0;
`

const CaseFilePopupDescriptionEditIcon = styled.div`
    width: 20px;
    height: 20px;
    background: none;
    border: none;
    border-radius: 4px;
    margin-left: 8px;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    pointer-events: auto;
    cursor: pointer;
    &:hover {
        background: #c0c0c0;
    }
    
    svg {
        width: 100%;
        height: 100%;
        fill: #c0c0c0;
    }

    &:hover svg {
        fill: #303030;
    }
    
`

const CaseFilePopupDescriptionEditButtons = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
`

const CaseFilePopupDescriptionEditFinishButton = styled.button`
    width: 64px;
    height: 20px;
    font-size: 12px;
    background: white;
    color: black;
    border: 1px solid white;
    border-radius: 5px;
    margin: 8px;
    &:hover {
        filter: drop-shadow(0 0 4px white);
    }
`

const CaseFilePopupDescriptionEditCancelButton = styled.button`
    width: 64px;
    height: 20px;
    font-size: 12px;
    background: none;
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    margin: 8px;
    &:hover {
        background: white;
        color: #303030;
    }
`

const CaseFilePopupDescriptionEditSubmittingLoadingContainer = styled.div`
    position: relative;
    width: 20px;
    height: 20px;
    margin: 8px;
`

const CaseFilePopupDescriptionText = styled.p`
    margin: 0;
`

const CaseFilePopupNoDescriptionText = styled.p`
    margin: 0;
    color: #999999;
`

const CaseFilePopupTimeDisplay = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    
    span:nth-child(1) {
        color: #c0c0c0;
        margin-right: 8px;
        font-weight: bold;
    }
    
    span:nth-child(2) {
        color: white;
    }
`

export function CaseFileData(props) {

    const {caseId} = useParams();

    const caseFilesManager = model.services['caseFilesManager'];

    const [s_fileData, setFileData] = useModelValueAsReactState('$.cases.currentOpen.files.all.' + props.fileId, {});

    const [s_loading, setLoading] = useState(false);

    const [s_editingDescription, setEditingDescription] = useState(false);
    const [s_submittingDescription, setSubmittingDescription] = useState(false);

    const [s_descriptionInput, setDescriptionInput] = useState('');

    const [s_reloadingStage, setReloadingStage] = useState(false);

    useEffect(() => {
        if (!props.fileId) return;
        setLoading(true);
        caseFilesManager.fetchFileData(props.fileId).then(() => setLoading(false));
    }, [props.fileId]);

    const m_directory = useMemo(() => {
        if (!s_fileData) return <></>;
        let directory = (s_fileData || {}).path || [];
        const caseId = model.cases.currentOpen.id || '';
        const caseData = model.cases.all[caseId] || {};
        directory = [caseData.title, ...directory];
        return <CaseFilePopupDirectory>
            {directory.map((d, i) => <>
                <CaseFilePopupDirectoryLevel key={'level-' + i}>{d}</CaseFilePopupDirectoryLevel>
                <CaseFilePopupDirectorySeparator key={'separator-' + i}> / </CaseFilePopupDirectorySeparator>
            </>)}
            <CaseFilePopupDirectoryLevel>{s_fileData.name}</CaseFilePopupDirectoryLevel>
        </CaseFilePopupDirectory>
    }, [s_fileData]);

    useEffect(() => {
        setDescriptionInput((s_fileData || {}).description || '');
    }, [s_fileData]);

    const c_updateDescription = useCallback(async () => {
        setSubmittingDescription(true);
        await caseFilesManager.setCaseFileDescription(s_descriptionInput, props.fileId);
        await caseFilesManager.fetchFileData(props.fileId, caseId, true);
        setEditingDescription(false);
        setSubmittingDescription(false);
    }, [s_descriptionInput]);

    const c_reloadStage = useCallback(async () => {
        setReloadingStage(true);
        await caseFilesManager.fetchFileData(props.fileId, caseId, true);
        setReloadingStage(false);
    }, []);

    const m_myUserAccessLevel = useCaseUserAccessLevel(props.caseId);
    
    return <>
        {s_loading ? <LoadingIcon width={"32px"} height={"32px"}/> : <>
            <CaseFilePopupFileName>{(s_fileData || {}).name}</CaseFilePopupFileName>
            {m_directory}
            <CaseFilePopupStageContainer>
                <CaseFilePopupStageTitle>
                    <span>Processing Stage</span>
                    {s_reloadingStage ? <>
                        <CaseFileProcessingStageReloading>
                            <LoadingIcon width={"20px"} height={"20px"}/>
                        </CaseFileProcessingStageReloading>
                    </> : <>
                        <CaseFileProcessingStageReloadButton onClick={() => c_reloadStage()}>
                            <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.circleArrow}/></svg>
                        </CaseFileProcessingStageReloadButton>
                    </>}
                </CaseFilePopupStageTitle>
                <FileProcessingStage fileData={s_fileData}/>
            </CaseFilePopupStageContainer>
            <CaseFilePopupDescriptionSection>
                <CaseFilePopupDescriptionTitleSection>
                    <CaseFilePopupDescriptionTitle>Description</CaseFilePopupDescriptionTitle>
                    {[caseAccessLevels.owner, caseAccessLevels.manager, caseAccessLevels.editor].includes(m_myUserAccessLevel) && !s_editingDescription ? <>
                        <CaseFilePopupDescriptionEditIcon onClick={() => setEditingDescription(true)}><svg viewBox={'-200 -200 1400 1400'}><path d={SVG_PATHS.pen} /></svg></CaseFilePopupDescriptionEditIcon>
                    </> : <></>}
                </CaseFilePopupDescriptionTitleSection>
                {s_editingDescription ? <>
                    <LongTextInput
                        value={s_descriptionInput}
                        setValue={setDescriptionInput}
                        width={"calc(100% - 16px)"}
                        height={"128px"}
                        maxLength={1000}
                    />
                    {s_submittingDescription ? <>
                        <CaseFilePopupDescriptionEditSubmittingLoadingContainer><LoadingIcon width={'20px'} height={'20px'} /></CaseFilePopupDescriptionEditSubmittingLoadingContainer>
                    </> : <>
                        <CaseFilePopupDescriptionEditButtons>
                            <CaseFilePopupDescriptionEditFinishButton onClick={() => c_updateDescription()}>Finish</CaseFilePopupDescriptionEditFinishButton>
                            <CaseFilePopupDescriptionEditCancelButton onClick={() => {
                                setEditingDescription(false);
                                setDescriptionInput((s_fileData || {}).description || '')
                            }}>Cancel</CaseFilePopupDescriptionEditCancelButton>
                        </CaseFilePopupDescriptionEditButtons>
                    </>
                    }
                    </> : <>
                    {(s_fileData || {}).description ? <CaseFilePopupDescriptionText>{(s_fileData || {}).description}</CaseFilePopupDescriptionText> : <CaseFilePopupNoDescriptionText>No Description Yet...</CaseFilePopupNoDescriptionText>}
                </>}
                { s_fileData.uploaded && <>
                    <VerticalGap gap={'32px'}/>
                    <CaseFilePopupTimeDisplay><span>Uploaded In:</span><span>{unixTimeToDayDateString(s_fileData.uploaded)}</span></CaseFilePopupTimeDisplay>
                </>}
                { s_fileData.modified && <>
                    <VerticalGap gap={'16px'}/>
                    <CaseFilePopupTimeDisplay><span>Last Modification:</span><span>{unixTimeToPastTimeString(s_fileData.modified)}</span></CaseFilePopupTimeDisplay>
                </>}
            </CaseFilePopupDescriptionSection>
        </>}
    </>
}