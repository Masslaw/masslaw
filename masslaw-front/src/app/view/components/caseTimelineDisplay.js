import {useEffect, useMemo, useState} from "react";
import {useParams} from "react-router-dom";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "./loadingIcon";
import {model} from "../../model/model";
import {CaseTimelineRender} from "./caseTimelineRender";


export function CaseTimelineDisplay(props) {

    const {caseId} = useParams();

    const casesKnowledgeManager = model.services['casesKnowledgeManager'];

    const [s_loading, setLoading] = useState(true);

    const [s_caseKnowledge, setCaseKnowledge] = useModelValueAsReactState('$.cases.currentOpen.knowledge', {entities: [], connections: []})

    const [s_displayKnowledge, setDisplayKnowledge] = useState({});

    useEffect(() => {
        setLoading(true);
        casesKnowledgeManager.fetchCaseKnowledge().then(() => setLoading(false));
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

    const m_events = useMemo(() => {
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
            events[entity_id] = {title: entity.properties.title, date: date, dateData: entityDate};
        }
        return events;
    }, [s_displayKnowledge])

    return <>
        {s_loading ? <>
            <LoadingIcon width={'30px'} height={'30px'}/>
        </> : <>
            <CaseTimelineRender events={m_events}/>
        </>}
    </>
}


