import React, {useCallback, useEffect, useRef, useState} from "react";

import "./css.css";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {useParams} from "react-router-dom";
import {ApplicationPage, ApplicationPageProps} from "../../../../../infrastructure/application_base/routing/application_page_renderer";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {useGlobalState} from "../../../../../infrastructure/application_base/global_functionality/global_states";
import {CaseFileData, knowledge, knowledgeConnection, knowledgeEntity} from "../../../../../infrastructure/cases_management/data_structures";
import {FileProcessingStages} from "../../../../../infrastructure/cases_management/cases_consts";
import {Graph} from "../../../../../modules/graph/graph";
import {now} from "lodash";
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

    const [graph_element, setGraphElement] = useState(<></>);

    const [graph_instance, setGraphInstance] = useState(new Graph());

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
                    applyFileKnowledge(file_knowledge);
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
                (graph_instance.getNodeById(entity.id) || {}).state = 'idle';
            }
            for (let connection of file_knowledge.connections) {
                (graph_instance.getEdgeById(connection.id) || {}).state = 'idle';
            }
        }
        for (let file_id of selected_files) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) {
                (graph_instance.getNodeById(entity.id) || {}).state = 'highlight';
            }
            for (let connection of file_knowledge.connections) {
                (graph_instance.getEdgeById(connection.id) || {}).state = 'highlighted';
            }
        }
    }, [graph_instance, selected_files]);

    useEffect(() => {
        graph_instance.setNodeClickCallback((node_id) => {
            navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {caseId: caseId || '', entityId: node_id || ''});
        });
        graph_instance.setEdgeClickCallback((edge_id) => {
        });

        graph_instance.setNodeHoverCallback((node_id, hovering) => {
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
        });

        graph_instance.setEdgeHoverCallback((edge_id, hovering) => {
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
        });
    }, [graph_instance]);

    let applyFileKnowledge = useCallback((file_knowledge: { entities: knowledgeEntity[], connections: knowledgeConnection[] }) => {
        for (let entity of file_knowledge.entities) {
            graph_instance.addNode(entity.id, entity.label, entity.properties['title']);
        }
        for (let connection of file_knowledge.connections) {
            graph_instance.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
        }
        setGraphInstance(graph_instance);
    }, [graph_instance]);

    const graphUpdateLoop = useCallback(() => {
        setGraphElement(graph_instance.getElement());
        setTimeout(graphUpdateLoop, 0);
    }, [graph_instance]);

    useEffect(() => {
        getCaseKnowledge();
    }, [caseId]);

    useEffect(() => {
        graphUpdateLoop();
    }, []);

    return (<>
        <div className={'case-annotations-header'}>
            <div className={'case-knowledge-page-title page-title'}>{`Case Knowledge`}</div>
        </div>
        <div className={'case-knowledge-graph-container'}>
            {
                knowledge && Object.keys(knowledge).length > 0 ?
                    <>
                        {graph_element}
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
