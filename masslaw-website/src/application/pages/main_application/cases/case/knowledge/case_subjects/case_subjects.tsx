import './css.css';
import {ApplicationPage, ApplicationPageProps} from "../../../../../../infrastructure/application_base/routing/application_page_renderer";
import {useGlobalState} from "../../../../../../infrastructure/application_base/global_functionality/global_states";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../../infrastructure/application_base/routing/application_global_routing";
import {useParams} from "react-router-dom";
import React, {useCallback, useEffect, useRef, useState} from "react";
import {CaseFileData, knowledge, knowledgeEntity} from "../../../../../../infrastructure/cases_management/data_structures";
import {LoadingIcon} from "../../../../../../shared/components/loading_icon/loading_icon";
import {CasesManager} from "../../../../../../infrastructure/cases_management/cases_manager";
import {Graph, GraphInterface} from "../../../../../../modules/graph/graph";
import {faFile} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutes} from "../../../../../../infrastructure/application_base/routing/application_routes";
import {Accordion} from "../../../../../../shared/components/accordion/accordion";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {FileProcessingStages} from "../../../../../../infrastructure/cases_management/cases_consts";


export const CaseSubjects: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId, entityId} = useParams();

    const [loaded, setLoaded] = useState(false);

    const [knowledge, setKnowledge] = useState(null as { [file_id: string]: knowledge } | null);

    const [files_data, setFilesData] = useState([] as CaseFileData[]);

    const [entities_by_id, setEntitiesById] = useState({} as {[entity_id: string]: knowledgeEntity});
    const [entitiy_files_by_entity_id, setEntityFilesByEntityId] = useState({} as {[entity_id: string]: Set<string>});
    const [graph_contribution_by_entity_id, setGraphContributionByEntityId] = useState({} as {[entity_id: string]: number});

    const graphRef = useRef<GraphInterface | null>(null);

    const getCaseKnowledge = useCallback(() => {
        (async () => {
            let case_files_response = await CasesManager.getInstance().getCaseFiles(caseId || '');
            setFilesData(case_files_response);
            let _knowledge = {} as { [file_id: string]: knowledge };
            let promises = case_files_response.map((file_data) => {
                let file_knowledge_extraction_status = ((file_data.processing || {})[FileProcessingStages.KnowledgeExtraction] || {})['status'] || 'never_executed';
                if (file_knowledge_extraction_status !== 'done') return;
                let file_id = file_data.id;
                return (async () => {
                    let download_url = (await CasesManager.getInstance().getFileContentDownloadURL(caseId || '', file_id || '', ['extracted_knowledge/knowledge.json']))['extracted_knowledge/knowledge.json'];
                    if (!download_url) return;
                    let file_knowledge = await fetch(download_url).then((response) => response.json());
                    _knowledge[file_id] = file_knowledge;
                })();
            });
            await Promise.all(promises);
            setKnowledge(_knowledge);
        })()
    }, [caseId]);

    useEffect(() => {
        if (!knowledge) return;
        if (!graphRef.current) return;
        for (let file_id in knowledge) {
            let file_knowledge = knowledge[file_id];
            if (!file_knowledge) continue;
            for (let entity of file_knowledge.entities) {
                if (!["PERSON"].includes(entity?.label)) continue;
                setEntitiesById((prev) => ({...prev, [entity.id]: entity}));
                setEntityFilesByEntityId((prev) => {
                    let _prev = {...prev};
                    let _set = _prev[entity.id] || new Set();
                    _set.add(file_id);
                    _prev[entity.id] = _set;
                    return _prev;
                });
                graphRef.current.addNode(entity.id, entity.label, entity.properties['title']);
            }
            for (let connection of file_knowledge.connections) {
                const from_entity = file_knowledge.entities.find((entity) => entity.id === connection.from);
                const to_entity = file_knowledge.entities.find((entity) => entity.id === connection.to);
                if (!from_entity || !["PERSON"].includes(from_entity.label || '')) continue;
                if (!to_entity || !["PERSON"].includes(to_entity.label || '')) continue;
                setGraphContributionByEntityId((prev) => {
                    let _prev = {...prev};
                    _prev[from_entity.id] = (_prev[from_entity.id] || 0) + connection.properties['strength'];
                    _prev[to_entity.id] = (_prev[to_entity.id] || 0) + connection.properties['strength'];
                    return _prev;
                });
                graphRef.current.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
            }
        }
    }, [knowledge, graphRef.current]);

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

    return <>
        {knowledge && Object.keys(knowledge).length > 0 ?
            <div className={'node-display'}>
                <div className={'subjects-data-container'}>
                    <div className={"page_title"}>Case Subjects</div>
                    <div className={'subjects-list'}>
                        {
                            Object.keys(entities_by_id)
                                .sort((a, b) => (graph_contribution_by_entity_id[b] || 0) - (graph_contribution_by_entity_id[a] || 0))
                                .map((entity_id) => {
                                    return <>
                                        <div
                                            className={"entity_item_data_display"}
                                            onClick={e => nodeClickCallback(entity_id)}
                                        >
                                            <div
                                                className={"entity_item_entity_name"}
                                                onMouseEnter={e => {
                                                    graphRef.current?.setNodeState(entity_id, 'highlight');
                                                }}
                                                onMouseLeave={e => {
                                                    graphRef.current?.setNodeState(entity_id, 'idle');
                                                }}
                                            >
                                                {(entities_by_id[entity_id]?.properties || {}).title || ''}
                                            </div>
                                            <Accordion title={'Files'} component={
                                                <div className={'entity_item_files_list'}>
                                                    {
                                                        Array.from(entitiy_files_by_entity_id[entity_id] || new Set()).map((file_id) => {
                                                            return <div
                                                                className={'entity_item_files_list_item'}
                                                                onClick={e => {
                                                                    e.stopPropagation();
                                                                    navigate_function(ApplicationRoutes.FILE_DISPLAY, {'caseId': caseId || '', 'fileId': file_id})
                                                                }}
                                                            >
                                                                <div className={'entity_item_files_list_item_file_icon'}>
                                                                    <FontAwesomeIcon icon={faFile}/>
                                                                </div>
                                                                <div className={'entity_item_files_list_item_file_name'}>
                                                                    {files_data.find((file_data) => file_data.id === file_id)?.name}
                                                                </div>
                                                            </div>
                                                        })
                                                    }
                                                </div>
                                            }/>
                                        </div>
                                    </>
                                })
                        }
                    </div>
                </div>
                <div className={'node-knowledge-display-container'}>
                    <Graph
                        ref={graphRef}
                        nodeClickCallback={() => {
                        }}
                        edgeClickCallback={() => {
                        }}
                        nodeHoverCallback={() => {
                        }}
                        edgeHoverCallback={() => {
                        }}
                    />
                </div>
            </div>
            :
            <LoadingIcon color={'#000000'}/>
        }
    </>
}