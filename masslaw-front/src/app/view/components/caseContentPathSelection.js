import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {useCallback, useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {SVG_PATHS} from "../config/svgPaths";
import {model} from "../../model/model";
import {VerticalGap} from "./verticalGap";

const CaseContentPathSelectionContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100% - 32px);
    padding: 8px 16px;
    height: 256px;
    overflow: auto;
    pointer-events: auto;
    &::-webkit-scrollbar { display: none; }
`

const Title = styled.div`
    font-size: 14px;
    color: white;
    font-weight: normal;
    margin: 8px;
`

const CaseContentPathInputContainer = styled.div`
    position: relative;
    height: max-content;
    width: calc(100% - 16px - 2px);
    margin: 8px;
    background: #303030;
    border: 1px solid #808080;
    border-radius: 4px;
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    overflow: hidden;
    flex-basis: max-content;
    flex-shrink: 0;
`

const CaseContentPathInputElementsContainer = styled.div`
    display: flex;
    flex-direction: row;
    overflow: hidden;
    align-items: center;
    flex-basis: max-content;
    flex-shrink: 0;
    padding: 6px;
    margin-right: auto;
    height: 24px;
`

const CaseContentPathInputPlaceHolder = styled.div`
    font-size: 12px;
    color: #808080
`

const CaseContentPathInputClickableArea = styled.div`
    width: calc(100% - 24px - 12px);
    height: 100%;
    position: absolute;
    z-index: 10;
    background: none;
    border: none;
    pointer-events: auto;
    top: 0;
    left: 0;
`

const CaseContentPathInputAddButton = styled.button`
    width: 24px;
    height: 24px;
    background: #505050;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin: 0 6px;
    flex-basis: 24px;
    flex-shrink: 0;
    flex-grow: 0;
    &:hover { background: #606060; }
    svg {
        width: 100%;
        height: 100%;
        fill: #808080;
    }
`

const CaseContentPathSelectedHierarchyElement = styled.div`
    background: #505050;
    color: white;
    border-radius: 4px;
    padding: 4px;
    font-size: 12px;
    cursor: pointer;
    position: relative;
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: max-content;
    white-space: nowrap;
`

const CaseContentPathSelectedHierarchySeparator = styled.svg`
    height: 100%;
    width: 12px;
    fill: #808080;
    margin: 0 6px;
    position: relative;
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 12px;
    white-space: nowrap;
`

const CaseContentPathNextFolderList = styled.div`
    position: absolute;
    top: 80px;
    width: calc(100% - 16px - 32px);
    margin: 8px;
    display: flex;
    flex-direction: column;
    background: #505050;
    height: 144px;
    overflow: auto;
    border-radius: 8px;
    z-index: 10;
    &::-webkit-scrollbar { display: none; }
`

const CaseContentPathNextFolderListItem = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 6px;
    cursor: pointer;
    &:hover { background: #606060; }
    svg {
        fill: white;
        width: 12px;
        height: 12px;
        margin-right: 6px;
        flex-grow: 0;
        flex-shrink: 0;
        flex-basis: 12px;
    }
    span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 12px;
        color: white;
        flex-grow: 1;
        flex-shrink: 0;
    }
`

const SelectedPathItem = styled.div`
    width: calc(100% - 16px - 12px - 2px);
    margin: 4px 8px;
    padding: 4px 6px;
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    background: #303030;
    border-radius: 8px;
    border: 1px solid white;
`

const SelectedPathRemoveButton = styled.button`
    width: max-content;
    font-size: 12px;
    padding: 2px 6px;
    height: 24px;
    background: none;
    border-radius: 8px;
    cursor: pointer;
    margin: 0 6px 0 10px;
    flex-basis: max-content;
    flex-shrink: 0;
    flex-grow: 0;
    color: white;
    border: 1px solid white;
    &:hover { 
        background: white; 
        color: black;
    }
`

const SelectedPathLevelsContainer = styled.div`
    display: flex;
    flex-direction: row;
    height: max-content;
    align-items: center;
    flex-basis: 0;
    flex-shrink: 0;
    flex-grow: 1;
    padding: 6px;
    margin-right: auto;
    overflow: auto;
    &::-webkit-scrollbar { display: none; }
`

const SelectedPathLevel = styled.div`
    background: #505050;
    color: white;
    border-radius: 4px;
    padding: 4px;
    font-size: 12px;
    cursor: pointer;
    position: relative;
    flex-grow: 0;
    flex-shrink: 0;
    flex-basis: max-content;
    white-space: nowrap;
`

const SelectedPathLevelsSeparator = styled.svg`
    height: 100%;
    width: 12px;
    fill: #808080;
    margin: 0 6px;
    position: relative;
    flex-grow: 0;
    flex-shrink: 0;
    flex-basis: 12px;
    white-space: nowrap;
`


export function CaseContentPathSelection(props) {

    const casesManager = model.services['casesManager']

    const [s_cases, setCases] = useModelValueAsReactState('$.cases.all');

    const [s_isFocused, setIsFocused] = useState(false);

    const m_caseData = useMemo(() => {
        return s_cases[props.caseId || ''] || {};
    }, [s_cases, props.caseId]);

    useEffect(() => {
        casesManager.fetchCaseContentHierarchy().then();
    }, []);

    const [s_currentInputtedPath, setCurrentInputtedPath] = useState([]);

    const m_availableHierarchy = useMemo(() => {
        if (!m_caseData) return {}
        let contentHierarchy = m_caseData.contentHierarchy;
        if (!contentHierarchy) return {};
        contentHierarchy = JSON.parse(JSON.stringify(contentHierarchy));
        if (!contentHierarchy) return {};
        contentHierarchy = {'Entire Case': contentHierarchy};
        for (const path of props.paths) {
            if (!path) continue;
            const modifiedPath = ['Entire Case', ...path];
            let currentLevel = contentHierarchy;
            for (const folder of modifiedPath.toSpliced(modifiedPath.length - 1)) currentLevel = currentLevel[folder] || {};
            delete currentLevel[modifiedPath[modifiedPath.length - 1]];
        }
        return contentHierarchy;
    }, [m_caseData, props.paths]);

    const m_nextLevel = useMemo(() => {
        let currentLevel = m_availableHierarchy;
        for (const folder of s_currentInputtedPath) {
            currentLevel = currentLevel[folder];
            if (typeof currentLevel !== 'object') return {};
        };
        return currentLevel;
    }, [m_availableHierarchy, s_currentInputtedPath]);

    const c_addPath = useCallback(() => {
        if (!s_currentInputtedPath.length) return;
        props.setPaths([...props.paths, [...s_currentInputtedPath.toSpliced(0, 1)]]);
        setIsFocused(false);
        setCurrentInputtedPath([]);
    }, [s_currentInputtedPath, props.paths, props.setPaths]);

    const c_removePath = useCallback((path) => {
        props.setPaths([...props.paths].filter(p => p !== path));
    }, [s_currentInputtedPath, props.paths, props.setPaths]);

    return <>
        <CaseContentPathSelectionContainer onClick={e => {setIsFocused(false);}}>
            <Title>Select paths:</Title>
            <CaseContentPathInputContainer>
                <CaseContentPathInputAddButton onClick={e => c_addPath()}>
                    <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.plusSign}/></svg>
                </CaseContentPathInputAddButton>
                {!s_isFocused ? <CaseContentPathInputClickableArea onClick={e => {
                    e.stopPropagation();
                    setIsFocused(true);
                }}/> : <></>}
                <CaseContentPathInputElementsContainer onClick={e => setIsFocused(true)}>
                    {s_currentInputtedPath.length === 0 ? <>
                        <CaseContentPathInputPlaceHolder>{Object.keys(m_nextLevel).length ? 'Click to select a path' : 'No more paths to select...'}</CaseContentPathInputPlaceHolder>
                    </> : <></>}
                    {s_currentInputtedPath.map((folderName, index) => <>
                        {index > 0 && <CaseContentPathSelectedHierarchySeparator viewBox={'0 0 1000 1000'}>
                            <path d={SVG_PATHS.arrowRight}/>
                        </CaseContentPathSelectedHierarchySeparator>}
                        <CaseContentPathSelectedHierarchyElement
                            key={index}
                            onClick={e => {
                                e.stopPropagation();
                                setIsFocused(true);
                                setCurrentInputtedPath(p => p.toSpliced(index));
                            }}
                        >{folderName}</CaseContentPathSelectedHierarchyElement>
                    </>)}
                </CaseContentPathInputElementsContainer>
            </CaseContentPathInputContainer>
            {s_isFocused && Object.keys(m_nextLevel).length ? <>
                <CaseContentPathNextFolderList>
                    {Object.keys(m_nextLevel).map((nextFolder, nextFolderIndex) => <>
                        <CaseContentPathNextFolderListItem
                            key={nextFolderIndex}
                            onClick={e => {
                                e.stopPropagation();
                                setCurrentInputtedPath(p => ([...p, nextFolder]));
                            }}
                        >
                            <svg viewBox={'0 0 1000 1000'}><path d={typeof m_nextLevel[nextFolder] === 'object' ? SVG_PATHS.folder : SVG_PATHS.file}/></svg>
                            <span>{nextFolder}</span>
                        </CaseContentPathNextFolderListItem>
                    </>)}
                </CaseContentPathNextFolderList>
            </> : <></>}
            {props.paths.map((path, index) => <>
                <SelectedPathItem key={index} >
                    <SelectedPathRemoveButton onClick={() => c_removePath(path)}>Remove</SelectedPathRemoveButton>
                    <SelectedPathLevelsContainer>
                        {(['Entire Case', ...path]).map((pathLevelName, index) => <>
                            {index > 0 && <SelectedPathLevelsSeparator viewBox={'0 0 1000 1000'}>
                                <path d={SVG_PATHS.arrowRight}/>
                            </SelectedPathLevelsSeparator>}
                            <SelectedPathLevel key={index}>{pathLevelName}</SelectedPathLevel>
                        </>)}
                    </SelectedPathLevelsContainer>
                </SelectedPathItem>
            </>)}
            <VerticalGap gap={'16px'} />
        </CaseContentPathSelectionContainer>
    </>
}
