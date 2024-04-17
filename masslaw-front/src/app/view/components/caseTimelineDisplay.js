import {useCallback, useEffect, useMemo, useState} from "react";
import {useParams} from "react-router-dom";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "./loadingIcon";
import {model} from "../../model/model";
import {CaseTimelineRender} from "./caseTimelineRender";
import styled from "styled-components";
import {SVG_PATHS} from "../config/svgPaths";
import {CaseKnowledgeEntityDataDisplay} from "./caseKnowledgeEntityDataDisplay";

const DisplayContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
    background: #101010;
`

const CaseTimelineContainer = styled.div`
    position: relative;
    width: max-content;
    height: 100%;
    margin-left: 64px;
    overflow-y: auto;
    overflow-x: visible;
    &::-webkit-scrollbar { display: none; }
`

const ReloadButton = styled.button`
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 16px;
    left: 16px;
    width: 32px;
    height: 32px;
    background: #101010;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    pointer-events: auto;
    padding: 0;
    z-index: 10;
    &:hover { background: #303030; }
    svg {
        width: 20px;
        height: 20px;
        fill: white;
    }
`

const ItemDataContainer = styled.div`
    position: absolute;
    top: 32px;
    right: 32px;
    bottom: 32px;
    width: 512px;
    max-width: calc(100% - 384px - 64px);
    padding: 32px;
    border: 1px solid #505050;
    background: #151515;
    border-radius: 8px;
`

const NoEventsToShow = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    color: #808080;
`


export function CaseTimelineDisplay(props) {

    const {caseId} = useParams();

    const casesKnowledgeManager = model.services['casesKnowledgeManager'];

    const [s_loading, setLoading] = useState(false);

    const [s_caseKnowledge, setCaseKnowledge] = useModelValueAsReactState('$.cases.currentOpen.knowledge', {entities: [], connections: []})

    const [s_displayKnowledge, setDisplayKnowledge] = useState({});

    const [s_events, setEvents] = useState({});

    const [s_entityDataTarget, setEntityDataTarget] = useState(null);

    const c_loadKnowledge = useCallback(async (force=false) => {
        if (s_loading) return;
        setLoading(true);
        setEntityDataTarget(null);
        await casesKnowledgeManager.fetchCaseKnowledge(force);
        setLoading(false);
    }, [s_loading]);

    useEffect(() => {
        c_loadKnowledge();
    }, []);

    useEffect(() => {
        const displayKnowledge = {...s_caseKnowledge};
        if (props.files) {
            displayKnowledge.entities = (displayKnowledge.entities || [])
                .filter((entityData, _) => props.files.filter(fileId => entityData.properties.files.list.includes(fileId)).length);
            displayKnowledge.connections = (displayKnowledge.connections || [])
                .filter((connectionData, _) => props.files.filter(fileId => connectionData.properties.files.list.includes(fileId)).length);
        }
        if (props.labels) {
            displayKnowledge.entities = (displayKnowledge.entities || []).filter((entityData, _) => props.labels.includes(entityData.label));
        }
        setDisplayKnowledge(displayKnowledge);
    }, [s_caseKnowledge, props.files, props.labels]);

    const c_onEventClicked = useCallback((eventId) => {
        setEntityDataTarget(eventId);
        setEvents(_events => {
            const newEvents = {..._events};
            Object.values(newEvents).forEach((event, index) => event.highlighted = false);
            newEvents[eventId].highlighted = true;
            return newEvents;
        });
    }, [s_displayKnowledge]);

    const m_eventEntities = useMemo(() => {
        const events = {};
        if (!(s_displayKnowledge || {}).entities) return;
        for (let entity of s_displayKnowledge.entities) {
            if (!entity) continue;
            let entityLabel = entity.label;
            if (!["DATE", "TIME"].includes(entityLabel)) continue;
            let entity_id = entity.id;
            let entityDate = entity.properties.datetime;
            if (!entityDate) continue;
            if (!(entityDate.Y && entityDate.M && entityDate.D)) continue;
            let date = new Date();
            date.setFullYear(parseInt(entityDate.Y));
            date.setMonth((parseInt(entityDate.M || '') || 1) - 1);
            date.setDate((parseInt(entityDate.D || '') || 1));
            date.setHours((parseInt(entityDate.h || '') || 0));
            date.setMinutes((parseInt(entityDate.m || '') || 0));
            date.setSeconds((parseInt(entityDate.s || '') || 0));
            events[entity_id] = {
                title: entity.properties.title,
                date: date, dateData: entityDate,
                onClick: () => c_onEventClicked(entity_id),
                highlighted: false,
            };
        }
        return events;
    }, [s_displayKnowledge]);

    useEffect(() => {
        setEvents(m_eventEntities);
    }, [m_eventEntities]);

    return <>
        <DisplayContainer>
            {s_loading ? <>
                <LoadingIcon width={'30px'} height={'30px'}/>
            </> : <>
                <ReloadButton onClick={() => c_loadKnowledge(true)}>
                    <svg viewBox={'0 0 1000 1000'}>
                        <path d={SVG_PATHS.circleArrow}/>
                    </svg>
                </ReloadButton>
                {!(s_events && s_events.length) ? <>
                    <NoEventsToShow>No Events To Show</NoEventsToShow>
                </> : <>
                    <CaseTimelineContainer>
                        <CaseTimelineRender events={s_events}/>
                    </CaseTimelineContainer>
                </>}
            </>}
            {s_entityDataTarget && <ItemDataContainer>
                <CaseKnowledgeEntityDataDisplay entityId={s_entityDataTarget}/>
            </ItemDataContainer>}
        </DisplayContainer>
    </>
}
