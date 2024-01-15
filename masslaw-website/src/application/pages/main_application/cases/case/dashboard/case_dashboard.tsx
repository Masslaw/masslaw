import {useParams} from "react-router-dom";
import {ApplicationPage, ApplicationPageProps} from "../../../../../infrastructure/application_base/routing/application_page_renderer";

import './css.css'
import React, {useCallback, useEffect, useRef, useState} from "react";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {LoadingIcon} from "../../../../../shared/components/loading_icon/loading_icon";
import {FileProcessingStages} from "../../../../../infrastructure/cases_management/cases_consts";
import {useGlobalState} from "../../../../../infrastructure/application_base/global_functionality/global_states";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {Graph, GraphInterface} from "../../../../../modules/graph/graph";
import {ApplicationRoutes} from "../../../../../infrastructure/application_base/routing/application_routes";
import {CaseFileData, knowledge} from "../../../../../infrastructure/cases_management/data_structures";
import {faFile} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Timeline} from "../../../../../modules/timeline/timeline";


export const CaseDashboard: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [files_data, setFilesData] = useState(null as CaseFileData[] | null);
    const [knowledge, setKnowledge] = useState(null as { [file_id: string]: knowledge } | null);

    const [selected_files, setSelectedFiles] = useState([] as string[]);
    const [highlighted_files, setHighlightedFiles] = useState([] as string[]);

    const graphRef = useRef<GraphInterface | null>(null);

    const [events, setEvents] = useState({} as {
        [event_id: string]: {
            title: string, onclick: () => void, date: Date,
        }
    });

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
        if (!graphRef.current) return;
        for (let file_id in knowledge) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) {
                graphRef.current.addNode(entity.id, entity.label, entity.properties['title']);
            }
            for (let connection of file_knowledge.connections) {
                graphRef.current.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
            }
        }
    }, [knowledge, graphRef.current]);

    useEffect(() => {
        if (!knowledge) return;
        if (!graphRef.current) return;
        for (let file_id in knowledge) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) graphRef.current.setNodeState(entity.id, 'idle');
            for (let connection of file_knowledge.connections) graphRef.current.setEdgeState(connection.id, 'idle');
        }
        for (let file_id of selected_files) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) graphRef.current.setNodeState(entity.id, 'highlight');
            for (let connection of file_knowledge.connections) graphRef.current.setEdgeState(connection.id, 'highlighted');
        }
    }, [selected_files]);

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
        }
    }, [knowledge, graphRef.current]);

    useEffect(() => {
        if (!caseId) return;
        getCaseKnowledge();
    }, [caseId]);

    const nodeClickCallback = (node_id: string) => {
        navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {caseId: caseId || '', entityId: node_id || ''});
    };
    const edgeClickCallback = (edge_id: string) => {
    };

    const nodeHoverCallback = (node_id: string, hovering: boolean) => {
    };

    const edgeHoverCallback = (edge_id: string, hovering: boolean) => {
    };

    useEffect(() => {
        if (!caseId) return;
        getCaseKnowledge();
    }, [caseId]);

    return (<>
        <div className={'case-dashboard-page-container'}>
            <div className={'case-dashboard-header'}>
                <div className={'case-dashboard-page-title page-title'}>{`Dashboard`}</div>
            </div>
            <div className={'case-dashboard-container'}>
                <div className={"case-dashboard-sub-display case-dashboard-files"} onWheel={e => e.stopPropagation()}>
                    <div className={'case-dashboard-sub-display-title'}>{`Case Files (${(files_data || []).length})`}</div>
                    <div className={'case-dashboard-files-list'}>
                        {files_data ? files_data.length > 0 ? files_data.map((file_data) => {
                            let file_id = file_data.id;
                            let file_title = file_data.name;
                            return (<div
                                key={file_id}
                                className={'case-dashboard-files-list-item'}
                            >
                                <span className={'case-dashboard-file-icon'}>
                                    <FontAwesomeIcon icon={faFile}/>
                                </span>
                                <span className={'case-dashboard-file-title'}>{file_title}</span>
                            </div>)
                        }) : <div style={{width: '100%', height: '100%', textAlign: 'center', verticalAlign: 'middle'}}>{'No Files Yet...'}</div> : <LoadingIcon color={'#000000'}/>}
                    </div>
                </div>
                <div className={"case-dashboard-sub-display case-dashboard-users"} onWheel={e => e.stopPropagation()}>
                    <div className={'case-dashboard-sub-display-title'}>{'Case Participants'}</div>

                </div>
                <div className={"case-dashboard-sub-display long-display case-dashboard-graph"} onWheel={e => e.stopPropagation()}>
                    <div className={'case-dashboard-sub-display-title'}>{'Case Knowledge'}</div>
                    {knowledge && Object.keys(knowledge).length > 0 ? <>
                        <Graph
                            ref={graphRef}
                            nodeClickCallback={nodeClickCallback}
                            edgeClickCallback={edgeClickCallback}
                            nodeHoverCallback={nodeHoverCallback}
                            edgeHoverCallback={edgeHoverCallback}
                        />
                    </> : <>
                        <LoadingIcon color={'#000000'}/>
                    </>}
                </div>
                <div className={"case-dashboard-sub-display long-display case-dashboard-timeline"} onWheel={e => e.stopPropagation()}>
                    <div className={'case-dashboard-sub-display-title'}>{'Case Timeline'}</div>
                    {knowledge ? Object.keys(events).length > 0 ? <>
                        <div className={'case-dashboard-timeline-container'}>
                            <Timeline events={events}/>
                        </div>
                    </> : <>
                        <div style={{width: '100%', top: '50%', textAlign: 'center', verticalAlign: 'middle', transform: 'translateY(-50%)'}}>{'No Events Yet...'}</div>
                    </> : <>
                        <LoadingIcon color={'#000000'}/>
                    </>}
                </div>
            </div>
        </div>
    </>)
}