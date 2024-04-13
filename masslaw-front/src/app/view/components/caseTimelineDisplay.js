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
        casesKnowledgeManager.fetchCaseKnowledge(caseId).then(() => setLoading(false));
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
            let entity_label = entity.label;
            if (!["DATE"].includes(entity_label)) continue;
            let entity_id = entity.id;
            let entity_date = entity.properties.datetime;
            if (!entity_date) continue;
            if (!entity_date.Y) continue;
            let date = new Date();
            date.setFullYear(parseInt(entity_date.Y));
            if (entity_date.M) date.setMonth((parseInt(entity_date.M || '') || 1) - 1);
            if (entity_date.D) date.setDate((parseInt(entity_date.D || '') || 1) - 1);
            date.setHours(0);
            date.setMinutes(0);
            date.setSeconds(0);
            events[entity_id] = { ...entity.properties, date: date};
        }
        console.log(events);
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


