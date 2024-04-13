import {useEffect, useMemo, useState} from "react";
import {model} from "../../../../../model/model";
import styled from "styled-components";
import {CaseFileData} from "../../../../components/caseFileData";
import {constructUrl} from "../../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../../config/applicaitonRoutes";
import {useModelValueAsReactState} from "../../../../../controller/functionality/model/modelReactHooks";
import {fileProcessingStages} from "../../../../../config/caseConsts";


const CaseFilePopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 512px;
    background-color: #202020;
    color: white;
    border-radius: 12px;
    z-index: 100;
    height: calc(100vh - 64px);
    max-height: 512px;
    overflow-y: auto;
    padding: 32px;
    &::-webkit-scrollbar { display: none; }
`

const CaseFileDataContainer = styled.div`
    width: 100%;
    height: max-content;
    flex-shrink: 0;
    flex-basis: max-content;
`

const CaseFilePopupOpenFileButton = styled.button`
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 128px;
    height: 32px;
    flex-basis: 32px;
    flex-shrink: 0;
    margin-left: auto;
    margin-top: auto;
    background: ${({clickable}) => clickable ? 'white' : 'none'};
    color: ${({clickable}) => clickable ? 'black' : '#808080'};
    border: 1px solid white;
    border-radius: 6px;
    font-size: 16px;
    cursor: ${({clickable}) => clickable ? 'pointer' : 'default'};
    pointer-events: ${({clickable}) => clickable ? 'auto' : 'none'};
    transition: background 0.2s;
    
    &:hover {
        filter: ${({clickable}) => clickable ? 'drop-shadow(0 0 4px white)' : 'none'};
    }
`

export function CaseFilePopup(props) {

    const [s_fileData, setFileData] = useModelValueAsReactState('$.cases.currentOpen.files.all.' + props.fileId, {});

    const m_openable = useMemo(() => {
        return (((s_fileData.processing || {})[fileProcessingStages.TextExtraction] || {})['status'] || '') === 'done';
    }, [s_fileData]);

    return <>
        <CaseFilePopupContainer>
            <CaseFileDataContainer>
                <CaseFileData fileId={props.fileId}/>
            </CaseFileDataContainer>
            <CaseFilePopupOpenFileButton
                clickable={m_openable}
                onClick={() => {
                    if (!m_openable) return;
                    model.application.navigate(constructUrl(ApplicationRoutes.FILE_DISPLAY, {caseId: props.caseId, fileId: props.fileId}));
                    props.dismiss();
                }}
            >View</CaseFilePopupOpenFileButton>
        </CaseFilePopupContainer>
    </>
}