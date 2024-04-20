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
import {Icon} from "./icon";

const CaseFileDataFileName = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 0;
    width: calc(100% - 64px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseFileDataDirectory = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    color: #808080;
    font-size: 14px;
    margin: 0;
    padding: 4px;
    width: max-content;
    max-width: calc(100% - 64px - 8px);
    overflow-y: hidden;
    overflow-x: auto;
    border: 1px solid #505050;
    border-radius: 4px;
    
`

const CaseFileDataDirectoryLevel = styled.span`
    margin: 0 4px;
    color: #c0c0c0;
    font-weight: bold;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const CaseFileDataDirectorySeparator = styled.span`
`

const CaseFileDataStageContainer = styled.div`
    display: flex;
    flex-direction: column;
    margin: 0;
    font-size: 14px;
    height: max-content;
    width: calc(100% - 64px);
`

const CaseFileDataStageTitle = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    font-weight: bold;
    color: #c0c0c0;
    margin-right: 8px;
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
    color: #c0c0c0;
    &:hover { background: #505050; }
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

const CaseFileDataDescriptionSection = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 64px);
    color: white;
    font-size: 14px;
`

const CaseFileDataDescriptionTitleSection = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0;
    margin-bottom: 8px;
`

const CaseFileDataDescriptionTitle = styled.div`
    font-weight: bold;
    margin: 0;
    color: #c0c0c0;
`

const CaseFileDataDescriptionEditIcon = styled.div`
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
    color: #c0c0c0;
    &:hover { background: #505050; }
`

const CaseFileDataDescriptionEditButtons = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
`

const CaseFileDataDescriptionEditFinishButton = styled.button`
    width: 64px;
    height: 20px;
    font-size: 12px;
    background: white;
    color: black;
    border: 1px solid white;
    border-radius: 5px;
    margin: 8px;
`

const CaseFileDataDescriptionEditCancelButton = styled.button`
    width: 64px;
    height: 20px;
    font-size: 12px;
    background: none;
    color: white;
    border: 1px solid white;
    border-radius: 5px;
    margin: 8px;
`

const CaseFileDataDescriptionEditSubmittingLoadingContainer = styled.div`
    position: relative;
    width: 20px;
    height: 20px;
    margin: 8px;
`

const CaseFileDataDescriptionText = styled.div`
    margin: 0;
`

const CaseFileDataNoDescriptionText = styled.div`
    margin: 0;
    color: #808080;
`

const CaseFileDataTimeDisplay = styled.div`
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
        return <CaseFileDataDirectory>
            {directory.map((d, i) => <>
                <CaseFileDataDirectoryLevel key={'level-' + i}>{d}</CaseFileDataDirectoryLevel>
                <CaseFileDataDirectorySeparator key={'separator-' + i}> / </CaseFileDataDirectorySeparator>
            </>)}
            <CaseFileDataDirectoryLevel>{s_fileData.name}</CaseFileDataDirectoryLevel>
        </CaseFileDataDirectory>
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
            <CaseFileDataFileName>{(s_fileData || {}).name}</CaseFileDataFileName>
            <VerticalGap gap={'16px'} />
            {m_directory}
            <VerticalGap gap={'16px'} />
            <CaseFileDataStageContainer>
                <CaseFileDataStageTitle>
                    <span>Processing Stage</span>
                    {s_reloadingStage ? <>
                        <CaseFileProcessingStageReloading>
                            <LoadingIcon width={"20px"} height={"20px"}/>
                        </CaseFileProcessingStageReloading>
                    </> : <>
                        <CaseFileProcessingStageReloadButton onClick={() => c_reloadStage()}>
                            <Icon>{SVG_PATHS.circleArrow}</Icon>
                        </CaseFileProcessingStageReloadButton>
                    </>}
                </CaseFileDataStageTitle>
                <VerticalGap gap={'8px'} />
                <FileProcessingStage fileData={s_fileData}/>
            </CaseFileDataStageContainer>
            <VerticalGap gap={'16px'} />
            <CaseFileDataDescriptionSection>
                <CaseFileDataDescriptionTitleSection>
                    <CaseFileDataDescriptionTitle>Description</CaseFileDataDescriptionTitle>
                    {[caseAccessLevels.owner, caseAccessLevels.manager, caseAccessLevels.editor].includes(m_myUserAccessLevel) && !s_editingDescription ? <>
                        <CaseFileDataDescriptionEditIcon onClick={() => setEditingDescription(true)}>
                            <Icon>{SVG_PATHS.pen}</Icon>
                        </CaseFileDataDescriptionEditIcon>
                    </> : <></>}
                </CaseFileDataDescriptionTitleSection>
                <VerticalGap gap={'8px'} />
                {s_editingDescription ? <>
                    <LongTextInput
                        value={s_descriptionInput}
                        setValue={setDescriptionInput}
                        width={"calc(100% - 16px)"}
                        height={"128px"}
                        maxLength={1000}
                    />
                    {s_submittingDescription ? <>
                        <CaseFileDataDescriptionEditSubmittingLoadingContainer><LoadingIcon width={'20px'} height={'20px'} /></CaseFileDataDescriptionEditSubmittingLoadingContainer>
                    </> : <>
                        <CaseFileDataDescriptionEditButtons>
                            <CaseFileDataDescriptionEditFinishButton onClick={() => c_updateDescription()}>Finish</CaseFileDataDescriptionEditFinishButton>
                            <CaseFileDataDescriptionEditCancelButton onClick={() => {
                                setEditingDescription(false);
                                setDescriptionInput((s_fileData || {}).description || '')
                            }}>
                                Cancel
                            </CaseFileDataDescriptionEditCancelButton>
                        </CaseFileDataDescriptionEditButtons>
                    </>
                    }
                    </> : <>
                    {(s_fileData || {}).description ? <CaseFileDataDescriptionText>{(s_fileData || {}).description}</CaseFileDataDescriptionText> : <CaseFileDataNoDescriptionText>No Description Yet...</CaseFileDataNoDescriptionText>}
                </>}
                { s_fileData.uploaded && <>
                    <VerticalGap gap={'32px'}/>
                    <CaseFileDataTimeDisplay><span>Uploaded In:</span><span>{unixTimeToDayDateString(s_fileData.uploaded)}</span></CaseFileDataTimeDisplay>
                </>}
                { s_fileData.modified && <>
                    <VerticalGap gap={'16px'}/>
                    <CaseFileDataTimeDisplay><span>Last Modification:</span><span>{unixTimeToPastTimeString(s_fileData.modified)}</span></CaseFileDataTimeDisplay>
                </>}
            </CaseFileDataDescriptionSection>
        </>}
    </>
}