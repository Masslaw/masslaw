import styled, {keyframes} from "styled-components";
import {useMemo} from "react";
import {model} from "../../../../../../model/model";
import {caseFileProcessingStageDisplayNames, fileProcessingStages} from "../../../../../../config/caseConsts";
import {SVG_PATHS} from "../../../../../config/svgPaths";

const GlowingAnimation = keyframes`
    0% { filter: drop-shadow(0 0 1px yellow); }
    50% { filter: drop-shadow(0 0 5px yellow); }
    100% { filter: drop-shadow(0 0 1px yellow); }
`

const FileProcessingStageDisplay = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    position: relative;
    padding: 8px;
    font-size: 12px;
    font-weight: bold;
    border: 1px solid white;
    border-radius: 12px;
    width: max-content;
    height: max-content;
    animation: ${GlowingAnimation} 2s ease-in-out;
    color: ${({readystage}) => readystage ? 'black' : 'white'};
    background: ${({readystage}) => readystage ? 'white' : 'none'};
    ${({readystage}) => readystage ? 'animation-iteration-count: 0' : `animation-iteration-count: infinite`};
    ${({readystage}) => readystage ? 'filter: drop-shadow(0 0 3px white)' : ``};

    svg {
        width: 16px;
        height: 16px;
        fill: black;
        margin-left: 8px;
    }
`

export function FileProcessingStage(props) {

    const caseFilesManager = model.services['caseFilesManager'];

    const READY_STAGE = '[READY]';

    const m_processingStage = useMemo(() => {
        if (!props.fileData) return null;
        const unfinishedProcessingStagesInOrder = caseFilesManager.getFileUnfinishedProcessingStagesInOrder(props.fileData);
        if (unfinishedProcessingStagesInOrder.length === 0) return READY_STAGE;
        return caseFileProcessingStageDisplayNames[unfinishedProcessingStagesInOrder[0]];
    }, [props.fileData]);

    return <>
        <FileProcessingStageDisplay readystage={m_processingStage === READY_STAGE ? 'true' : ''}>{
            m_processingStage === READY_STAGE ? <>
                Ready <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.checkMark}/></svg>
            </> : <>
                {m_processingStage}
            </>
        }</FileProcessingStageDisplay>
    </>
}