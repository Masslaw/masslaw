import styled from "styled-components";
import {useCallback, useEffect, useMemo, useState} from "react";
import {useCaseData} from "../hooks/useCaseData";
import {VerticalGap} from "./verticalGap";
import {constructUrl} from "../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../config/applicaitonRoutes";
import {model} from "../../model/model";
import {LoadingIcon} from "./loadingIcon";
import {KnowledgeDisplay} from "./knowledgeDisplay";

const CaseKnowledgeEntityDataDisplayContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    overflow: auto;
    &::-webkit-scrollbar { display: none; }
`

const ErrorDisplayingDataMessage = styled.div`
    font-size: 16px;
    color: #808080;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
`

const EntityTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
`

const AppearanceItemContainer = styled.div`
    background: #202020;
    border: 1px solid #505050;
    padding: 8px;
    width: calc(100% - 16px - 2px);
    border-radius: 8px;
    margin: 8px 0;
`

const AppearanceItemFileTitle = styled.div`
    padding: 8px;
    width: calc(100% - 16px);
    color: #a0a0a0;
    font-size: 14px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    cursor: pointer;
    &:hover { text-decoration: underline; }
`

const AppearanceItemText = styled.div`
    font-size: 14px;
    color: white;
    padding: 8px;
    margin: 0 8px;
    overflow: hidden;
    line-height: 20px;
    letter-spacing: 0.5px;
    border-radius: 8px;
    border: 1px solid transparent;
    &:hover { border: 1px solid #404040; }
    button { opacity: 0; }
    &:hover button { opacity: 1; }
`

const AppearanceItemTextOccurrenceSpan = styled.span`
    font-weight: bold;
    padding: 2px;
    margin: 0 2px;
    background: #303030;
    border-radius: 4px;
    border: 1px solid #505050;
`

const ItemKnowledgeDisplayContainer = styled.div`
    width: calc(100% - 2px);
    height: 50%;
    position: relative;
    background: #101010;
    border-radius: 8px;
    border: 1px solid #505050;
    overflow: hidden;
`

export function CaseKnowledgeEntityDataDisplay(props) {

    const {casesKnowledgeManager} = model.services;

    const s_caseData = useCaseData();
    
    const [s_loading, setLoading] = useState(false);

    const [s_entityKnowledge, setEntityKnowledge] = useState({});

    useEffect(() => {
        c_loadEntityData();
    }, [props.entityId]);

    const c_loadEntityData = useCallback(async () => {
        if (s_loading) return;
        if (!props.entityId) return;
        setLoading(true);
        const itemKnowledge = await casesKnowledgeManager.fetchCaseKnowledgeItem('node', props.entityId);
        setEntityKnowledge(itemKnowledge);
        setLoading(false);
    }, [props.entityId, s_loading]);

    const [s_entityData, setEntityData] = useState({});

    useEffect(() => {
        for (const entityData of s_entityKnowledge.entities || [])  if (entityData.id === props.entityId) setEntityData(entityData);
    }, [props.entityId, s_entityKnowledge]);

    const m_appearances = useMemo(() => {
        if (!s_caseData) return [];
        const entityData = s_entityData || {};
        const properties = entityData.properties || {};
        const entityTextData = (properties.text) || {};
        const appearanceItems = [];
        for (const fileId in entityTextData) {
            const fileData = s_caseData.filesData[fileId];
            if (!fileData) continue;
            const entityFileTextData = entityTextData[fileId] || {};
            const fileAppearances = entityFileTextData.aprs || [];
            const fileAppearanceItems = [];
            for (const sentence in fileAppearances) {
                const sentenceOccurrences = fileAppearances[sentence] || [];
                sentenceOccurrences.sort();
                const sentenceParts = [];
                let previousPartEnd = 0;
                for (const occurrence of sentenceOccurrences) {
                    if (!(sentenceParts.length % 2)) sentenceParts.push(<span>{sentence.substring(previousPartEnd, occurrence)}</span>);
                    else sentenceParts.push(<AppearanceItemTextOccurrenceSpan>{sentence.substring(previousPartEnd, occurrence)}</AppearanceItemTextOccurrenceSpan>);
                    previousPartEnd = occurrence;
                }
                sentenceParts.push(<span>{sentence.substring(previousPartEnd)}</span>);
                fileAppearanceItems.push(<AppearanceItemText>“ {sentenceParts} ”</AppearanceItemText>);
            }
            if (!fileAppearanceItems.length) continue;
            appearanceItems.push(<AppearanceItemContainer>
                <AppearanceItemFileTitle onClick={() => model.application.navigate(constructUrl(ApplicationRoutes.FILE_DISPLAY, {caseId: s_caseData.case_id, fileId: fileId}))}>
                    {fileData.name}
                </AppearanceItemFileTitle>
                {fileAppearanceItems}
            </AppearanceItemContainer>);
        }
        return appearanceItems;
    }, [s_entityData, props.entityData, s_caseData])

    return <>
        <CaseKnowledgeEntityDataDisplayContainer>
            {s_loading ? <>
                <LoadingIcon width={'20px'} height={'20px'} />
            </> : !(s_entityData || {}).properties ? <>
                <ErrorDisplayingDataMessage>Data about this entity cannot be displayed</ErrorDisplayingDataMessage>
            </> : <>
                <EntityTitle>“{s_entityData.properties.title}”</EntityTitle>
                <VerticalGap gap={'16px'}/>
                <ItemKnowledgeDisplayContainer>
                    <KnowledgeDisplay knowledge={s_entityKnowledge} hideInfo={true} />
                </ItemKnowledgeDisplayContainer>
                <VerticalGap gap={'16px'}/>
                {m_appearances}
            </>}
        </CaseKnowledgeEntityDataDisplayContainer>
    </>
}