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

export const CaseKnowledge: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [knowledge, setKnowledge] = useState(null as knowledge | null);

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
                    </>
                    :
                    <>
                        <LoadingIcon color={'#000000'} />
                    </>
            }
        </div>
    </>)
}
