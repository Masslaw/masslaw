import './css.css';
import {ApplicationPage, ApplicationPageProps} from "../../../../../../infrastructure/application_base/routing/application_page_renderer";
import {useGlobalState} from "../../../../../../infrastructure/application_base/global_functionality/global_states";
import {NavigationFunctionState, QueryStringParamsState} from "../../../../../../infrastructure/application_base/routing/application_global_routing";
import {useParams} from "react-router-dom";
import React, {useCallback, useEffect, useRef, useState} from "react";
import {CaseFileData, knowledge, knowledgeConnection, knowledgeEntity} from "../../../../../../infrastructure/cases_management/data_structures";
import {LoadingIcon} from "../../../../../../shared/components/loading_icon/loading_icon";
import {CasesManager} from "../../../../../../infrastructure/cases_management/cases_manager";
import {Graph} from "../../../../../../modules/graph/graph";
import {now} from "lodash";
import {faArrowRight, faFile} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutes} from "../../../../../../infrastructure/application_base/routing/application_routes";
import {Accordion} from "../../../../../../shared/components/accordion/accordion";
import {node_style} from "../../../../../../modules/graph/style_config";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


export const NodeDisplay: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId, entityId} = useParams();

    const [loaded, setLoaded] = useState(false);

    const [entity_data, setEntityData] = useState(null as knowledgeEntity | null);

    const [knowledge, setKnowledge] = useState(null as knowledge | null);

    const [entities_by_id, setEntitiesById] = useState({} as { [entity_id: string]: knowledgeEntity } | null);

    const [connections_by_id, setConnectionsById] = useState({} as { [connection_id: string]: knowledgeConnection } | null);

    const [graph_element, setGraphElement] = useState(<></>);

    const [graph_instance, setGraphInstance] = useState(new Graph());

    const [files_data, setFilesData] = useState({} as { [file_id: string]: CaseFileData });

    useEffect(() => {
        (async () => {
            setLoaded(false);
            await getEntityData();
            setLoaded(true);
        })()
    }, [caseId, entityId]);

    useEffect(() => {
        (async () => {
            let files_data_list = await CasesManager.getInstance().getCaseFiles(caseId || '');
            let files_data_map = {} as { [file_id: string]: CaseFileData };
            files_data_list.forEach((file_data) => {
                files_data_map[file_data.id || ''] = file_data;
            })
            setFilesData(files_data_map);
        })();
    }, [caseId]);

    const getEntityData = useCallback(async () => {
        let item_knowledge = await CasesManager.getInstance().getCaseKnowledgeForItem(caseId || '', entityId || '', 'node');
        setKnowledge(item_knowledge);
        let entity = item_knowledge.entities.find(node => node.id === entityId) || null;
        setEntityData(entity);
        let entities_by_id_map = {} as { [entity_id: string]: knowledgeEntity };
        item_knowledge.entities.forEach((entity) => {
            entities_by_id_map[entity.id] = entity;
        })
        setEntitiesById(entities_by_id_map);
        let connections_by_id_map = {} as { [connection_id: string]: knowledgeConnection };
        item_knowledge.connections.forEach((connection) => {
            connections_by_id_map[connection.id] = connection;
        })
        setConnectionsById(connections_by_id_map);
    }, [entityId]);

    let previousUpdateTime = now();
    const graphUpdateLoop = useCallback(() => {
        requestAnimationFrame(graphUpdateLoop);
        let _now = now();
        let dt = (_now - previousUpdateTime) / 1000;
        previousUpdateTime = _now;
        graph_instance.update(dt);
        setGraphElement(graph_instance.getElement());
    }, [graph_instance]);

    let requestAnimationFrameId = useRef(0);
    useEffect(() => {
        graph_instance.reset();
        for (let entity of (knowledge || {}).entities || []) {
            graph_instance.addNode(entity.id, entity.label, entity.properties['title'] || '');
        }
        for (let connection of (knowledge || {}).connections || []) {
            graph_instance.addEdge(connection.id, connection.from, connection.to, connection.properties['strength'] || 1);
        }
        cancelAnimationFrame(requestAnimationFrameId.current);
        requestAnimationFrameId.current = requestAnimationFrame(graphUpdateLoop);
        return () => {
            cancelAnimationFrame(requestAnimationFrameId.current);
        }
    }, [knowledge]);

    return <>
        {!loaded || !entity_data || !knowledge ? <>
            <LoadingIcon color={'#000000'}/>
        </> : <>
            <div className={'node-display'}>
                <div className={'node-data-container'}>
                    <div className={'node-display-title'}>
                        {entity_data && entity_data.properties.title || ''}
                    </div>
                    <div className={'node-knowledge-quotes-list'}>
                        <div className={'node-knowledge-quotes-list-title'}>{'Insightful Quotes:'}</div>
                        <div className={'node-knowledge-quotes-list-scrollable-region'}>
                            {Object.keys(entity_data.properties['information_items'] || {}).map((file_id: string) => {
                                let file_information_items: {[key:string]:string}[] = entity_data.properties['information_items'][file_id];
                                return file_information_items.map(information_item => <div className={'node-knowledge-quotes-list-item'}>
                                    ""{information_item['t']}""
                                    <div className={'node-knowledge-quotes-list-item-file'} onClick={
                                        e => navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                            'caseId': caseId || '', 'fileId': file_id
                                        },{
                                            'scroll_to': information_item['s'] || '',
                                            'mark': `${information_item['s']}|${information_item['e']}`,
                                        })
                                    }>
                                        {files_data[file_id].name}
                                    </div>
                                </div>)
                            })}
                        </div>
                    </div>
                    <div className={'node-connections-list'}>
                        <div className={'nodes-connections-list-title'}>{`${entity_data.properties['title']} is connected to:`}</div>
                        <div className={'node-connections-list-scrollable-region'}>
                            {Object.values(knowledge.connections).map((connection_data: knowledgeConnection) => {
                                let connected_node_id = connection_data.from !== entityId ? connection_data.from : connection_data.to;
                                let node_data = entities_by_id && entities_by_id[connected_node_id] || {} as knowledgeEntity;
                                let node_color = node_style[node_data.label].color['idle'] || 'grey';
                                let node_icon = node_style[node_data.label].icon;
                                return <>
                                    <div
                                        key={connection_data.id}
                                        className={'node-connections-list-item'}
                                        style={{
                                            borderLeft: `5px solid ${node_color}`,
                                        }}
                                        onClick={() => {
                                            navigate_function(ApplicationRoutes.CASE_KNOWLEDGE_ENTITY, {
                                                'caseId': caseId || '', 'entityId': connected_node_id
                                            },)
                                        }}
                                    >
                                        <div className={'node-connections-list-item-title'}>
                                            <span><FontAwesomeIcon icon={node_icon} /></span>
                                            <span style={{marginLeft: '10px'}}> {node_data && node_data.properties['title'] || ''}</span>
                                        </div>
                                        <Accordion
                                            title={'Connection Evidence'}
                                            component={<div className={'connection-evidence-list'}>
                                                {Object.keys(connection_data.properties['evidence'] || {}).map((file_id: string) => {
                                                    let evidence_data: {[key:string]:string}[] = connection_data.properties['evidence'][file_id];
                                                    return evidence_data.map(evidence_item => <div key={evidence_item['t']} className={'connection-evidence-list-item'}>
                                                        ""{evidence_item['t'] || ''}""
                                                        <div className={'connection-evidence-list-item-file'} onClick={
                                                            e => {
                                                                navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                                                    'caseId': caseId || '', 'fileId': file_id
                                                                }, {
                                                                    'scroll_to': evidence_item['s'] || '',
                                                                    'mark': `${evidence_item['s']}|${evidence_item['e']}`,
                                                                })
                                                                e.stopPropagation();
                                                            }
                                                        }>
                                                            {files_data[file_id].name}
                                                        </div>
                                                    </div>)
                                                })}
                                            </div>}
                                        />
                                    </div>
                                </>
                            })}
                        </div>
                    </div>
                    <div className={'node-display-files-list'}>
                        <div className={'node-display-files-list-title'}>{`${entity_data.properties['title']} appears in:`}</div>
                        <div className={'node-display-files-list-scrollable-region'}>
                            {((entity_data.properties['files'] || {})['list'] || []).map((file_id: string) => {
                                let file_data = files_data[file_id];
                                if (!file_data) return <></>;
                                return <>
                                    <div
                                        key={file_id}
                                        className={'node-display-file-item'}
                                        onClick={() => {
                                            navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                                'caseId': caseId || '', 'fileId': file_id
                                            },)
                                        }}
                                    >
                                        <div className={'node-display-file-title'}>
                                            <span><FontAwesomeIcon icon={faFile} /></span>
                                            <span style={{marginLeft: '10px'}}>{file_data.name}</span>
                                        </div>
                                    </div>
                                </>
                            })}
                        </div>
                    </div>
                </div>
                <div className={'node-knowledge-display-container'}>
                    {graph_element}
                </div>
            </div>
        </>}
    </>
}