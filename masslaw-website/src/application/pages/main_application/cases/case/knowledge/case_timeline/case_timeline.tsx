import React, {useCallback, useEffect, useRef, useState} from "react";

import "./css.css";
import {CasesManager} from "../../../../../../infrastructure/cases_management/cases_manager";
import {useParams} from "react-router-dom";
import {ApplicationPage, ApplicationPageProps} from "../../../../../../infrastructure/application_base/routing/application_page_renderer";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../../infrastructure/application_base/routing/application_global_routing";
import {useGlobalState} from "../../../../../../infrastructure/application_base/global_functionality/global_states";
import {CaseFileData, knowledge, knowledgeConnection, knowledgeEntity} from "../../../../../../infrastructure/cases_management/data_structures";
import {FileProcessingStages} from "../../../../../../infrastructure/cases_management/cases_consts";
import {Graph, GraphInterface} from "../../../../../../modules/graph/graph";
import {ApplicationRoutes} from "../../../../../../infrastructure/application_base/routing/application_routes";
import {LoadingIcon} from "../../../../../../shared/components/loading_icon/loading_icon";
import {Timeline} from "../../../../../../modules/timeline/timeline";

export const CaseTimeline: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [knowledge, setKnowledge] = useState(null as knowledge | null);


    const [events, setEvents] = useState({} as {[event_id: string]: {
        title: string,
        onclick: () => void,
        date: Date,
    }});

    const graphRef = useRef<GraphInterface | null>(null);

    const getCaseKnowledge = useCallback(() => {
        (async () => {
            let knowledge = await CasesManager.getInstance().getCaseKnowledge(caseId || '');
            setKnowledge(knowledge);
        })()
    }, [caseId]);

    useEffect(() => {
        if (!knowledge) return;
        if (!graphRef.current) return;
        for (let entity of knowledge.entities) {
            graphRef.current.addNode(entity.id, entity.label, entity.properties['title']);
        }
        for (let connection of knowledge.connections) {
            graphRef.current.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
        }
    }, [knowledge, graphRef.current]);

    useEffect(() => {
        if (!knowledge) return;
        for (let entity of knowledge.entities) {
            if (!entity) continue;
            let entity_label = entity.label;
            if (!["DATE"].includes(entity_label)) continue;
            let entity_id = entity.id;
            let entity_title = entity.properties.title;
            let entity_date = entity.properties.datetime as { Y: string, M: string, D: string };
            if (!entity_date) continue;
            if (!entity_date.Y) continue;
            let date = new Date();
            date.setFullYear(parseInt(entity_date.Y));
            if (entity_date.M) date.setMonth((parseInt(entity_date.M || '') || 1) - 1);
            if (entity_date.D) date.setDate((parseInt(entity_date.D || '') || 1) - 1);
            date.setHours(0);
            date.setMinutes(0);
            date.setSeconds(0);
            let event = {
                title: entity_title, onclick: () => navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {caseId: caseId || '', entityId: entity_id || ''}), date: date,
            };
            setEvents((current_events) => {
                let new_events = {...current_events};
                new_events[entity_id] = event;
                return new_events;
            });
        }
    }, [knowledge, graphRef.current]);

    useEffect(() => {
        if (!caseId) return;
        getCaseKnowledge();
    }, [caseId]);

    return (<>
        <div className={'case-annotations-header'}>
            <div className={'case-timeline-page-title page-title'}>{`Case Timeline`}</div>
        </div>
        <div className={'case-timeline-timeline-container'}>
            {
                knowledge && Object.keys(knowledge).length > 0 ?
                    <>
                        <Timeline events={events} />
                    </>
                    :
                    <>
                        <LoadingIcon color={'#000000'} />
                    </>
            }
        </div>
    </>)
}
