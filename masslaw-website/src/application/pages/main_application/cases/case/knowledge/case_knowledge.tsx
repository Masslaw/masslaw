import React, {useCallback, useEffect, useRef, useState} from "react";

import "./css.css";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {useParams} from "react-router-dom";
import {ApplicationPage, ApplicationPageProps} from "../../../../../infrastructure/application_base/routing/application_page_renderer";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {useGlobalState} from "../../../../../infrastructure/application_base/global_functionality/global_states";
import {CaseFileData, knowledge, knowledgeConnection, knowledgeEntity} from "../../../../../infrastructure/cases_management/data_structures";
import {FileProcessingStages} from "../../../../../infrastructure/cases_management/cases_consts";
import {Graph, GraphInterface} from "../../../../../modules/graph/graph";
import {ApplicationRoutes} from "../../../../../infrastructure/application_base/routing/application_routes";
import {LoadingIcon} from "../../../../../shared/components/loading_icon/loading_icon";

export const CaseKnowledge: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [files_data, setFilesData] = useState([] as CaseFileData[]);
    const [knowledge, setKnowledge] = useState(null as { [file_id: string]: knowledge } | null);

    const [selected_files, setSelectedFiles] = useState([] as string[]);
    const [highlighted_files, setHighlightedFiles] = useState([] as string[]);

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

    const nodeClickCallback = (node_id: string) => {
        navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {caseId: caseId || '', entityId: node_id || ''});
    };
    const edgeClickCallback = (edge_id: string) => {
    };

    const nodeHoverCallback = (node_id: string, hovering: boolean) => {
        if (hovering) {
            let node_files: string[] = [];
            for (let file_id in knowledge) {
                let file_knowledge = knowledge[file_id];
                for (let entity of file_knowledge.entities) {
                    if (entity.id === node_id) node_files.push(file_id);
                }
            }
            setHighlightedFiles(node_files);
        } else {
            setHighlightedFiles([]);
        }
    };

    const edgeHoverCallback = (edge_id: string, hovering: boolean) => {
        if (hovering) {
            let edge_files: string[] = [];
            for (let file_id in knowledge) {
                let file_knowledge = knowledge[file_id];
                for (let connection of file_knowledge.connections) {
                    if (connection.id === edge_id) edge_files.push(file_id);
                }
            }
            setHighlightedFiles(edge_files);
        } else {
            setHighlightedFiles([]);
        }
    };

    useEffect(() => {
        if (!caseId) return;
        getCaseKnowledge();
    }, [caseId]);

    return (<>
        <div className={'case-annotations-header'}>
            <div className={'case-knowledge-page-title page-title'}>{`Case Knowledge`}</div>
        </div>
        <div className={'case-knowledge-graph-container'}>
            {
                knowledge && Object.keys(knowledge).length > 0 ?
                    <>
                        <Graph
                            ref={graphRef}
                            nodeClickCallback={nodeClickCallback}
                            edgeClickCallback={edgeClickCallback}
                            nodeHoverCallback={nodeHoverCallback}
                            edgeHoverCallback={edgeHoverCallback}
                        />
                        <div className={'case-knowledge-graph-info-text'}>{`Only the 40 most relevant items are displayed.`}</div>
                        <div className={'case-knowledge-files-list-title'}>{`Files`}</div>
                        <div className={'case-knowledge-files-list-container'}>
                            {files_data.map((file_data) => {
                                return <>
                                    <div
                                        key={file_data.id}
                                        className={`case-knowledge-file-item ${highlighted_files.includes(file_data.id) && 'highlighted' || ''}`}
                                        onMouseEnter={() => {
                                            setSelectedFiles((current_selected) => [...current_selected, file_data.id]);
                                        }}
                                        onMouseLeave={() => {
                                            setSelectedFiles((current_selected) => current_selected.filter((file_id) => file_id !== file_data.id));
                                        }}
                                    >
                                        {file_data.name}
                                    </div>
                                </>
                            })}
                        </div>
                    </>
                    :
                    <>
                        <LoadingIcon color={'#000000'} />
                    </>
            }
        </div>
    </>)
}
