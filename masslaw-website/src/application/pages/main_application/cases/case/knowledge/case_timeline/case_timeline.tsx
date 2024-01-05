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

    const [files_data, setFilesData] = useState([] as CaseFileData[]);
    const [knowledge, setKnowledge] = useState(null as { [file_id: string]: knowledge } | null);


    const [events, setEvents] = useState({} as {[event_id: string]: {
        title: string,
        onclick: () => void,
        date: Date,
    }});

    const graphRef = useRef<GraphInterface | null>(null);

    const getCaseKnowledge = useCallback(() => {
        (async () => {
            let case_files_response = await CasesManager.getInstance().getCaseFiles(caseId || '');
            setFilesData(case_files_response);
            let knowledge = {} as { [file_id: string]: knowledge };
            let promises = case_files_response.map((file_data) => {
                let file_knowledge_extraction_status = ((file_data.processing || {})[FileProcessingStages.KnowledgeExtraction] || {})['status'] || 'never_executed';
                if (file_knowledge_extraction_status !== 'done') return;
                let file_id = file_data.id;
                return (async () => {
                    let download_url = (await CasesManager.getInstance().getFileContentDownloadURL(caseId || '', file_id || '', ['extracted_knowledge/knowledge.json']))['extracted_knowledge/knowledge.json'];
                    if (!download_url) return;
                    let file_knowledge = await fetch(download_url).then((response) => response.json());
                    knowledge[file_id] = file_knowledge;
                })();
            });
            await Promise.all(promises);
            setKnowledge(knowledge);
        })()
    }, [caseId]);

    useEffect(() => {
        if (!knowledge) return;
        for (let file_id in knowledge) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) {
                if (!entity) continue;
                let entity_label = entity.label;
                if (!["DATE"].includes(entity_label)) continue;
                let entity_id = entity.id;
                let entity_title = entity.properties.title;
                let entity_iso = entity.properties.iso;
                let event = {
                    title: entity_title,
                    onclick: () => navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {caseId: caseId || '', entityId: entity_id || ''}),
                    date: new Date(entity_iso),
                };
                setEvents((current_events) => {
                    let new_events = {...current_events};
                    new_events[entity_id] = event;
                    return new_events;
                });
            }
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
