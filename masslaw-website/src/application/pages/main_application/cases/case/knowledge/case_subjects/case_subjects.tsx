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
import {faFile, faUser} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutes} from "../../../../../../infrastructure/application_base/routing/application_routes";
import {Accordion} from "../../../../../../shared/components/accordion/accordion";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {FileProcessingStages} from "../../../../../../infrastructure/cases_management/cases_consts";


export const CaseSubjects: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId, entityId} = useParams();


    const [knowledge, setKnowledge] = useState(null as knowledge | null);

    const [entities_by_id, setEntitiesById] = useState({} as {[entity_id: string]: knowledgeEntity});
    const [graph_contribution_by_entity_id, setGraphContributionByEntityId] = useState({} as {[entity_id: string]: number});

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
            if (!["PERSON"].includes(entity?.label)) continue;
            setEntitiesById((prev) => ({...prev, [entity.id]: entity}));
            graphRef.current.addNode(entity.id, entity.label, entity.properties['title']);
        }
        for (let connection of knowledge.connections) {
            const from_entity = knowledge.entities.find((entity) => entity.id === connection.from);
            const to_entity = knowledge.entities.find((entity) => entity.id === connection.to);
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
                            (() => {
                                const totalContribution = [...Object.values(graph_contribution_by_entity_id)].reduce((a, b) => a + b, 0);
                                return Object.keys(entities_by_id)
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
                                                    <span><FontAwesomeIcon icon={faUser} /></span>
                                                    <span style={{marginLeft: "5px"}}>{(entities_by_id[entity_id]?.properties || {}).title || ''}</span>
                                                </div>
                                                <div className={"entity_item_data_display_info"}>
                                                    {`Contribution: ${Math.round(100 * (graph_contribution_by_entity_id[entity_id] || 0) / totalContribution)}%`}
                                                    <br/>
                                                    {`Appears in: ${(((entities_by_id[entity_id]?.properties || {})["files"] || {})["list"] || []).length} files`}
                                                </div>
                                            </div>
                                        </>
                                    })
                            })()
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