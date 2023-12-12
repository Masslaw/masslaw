import React, {useCallback, useContext, useEffect, useRef, useState} from "react";

import "./css.css";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {useParams} from "react-router-dom";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../../infrastructure/application_base/routing/application_page_renderer";
import {
    NavigationFunctionState,
    QueryStringParamsState
} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {
    useGlobalState
} from "../../../../../infrastructure/application_base/global_functionality/global_states";
import {CaseFileAnnotationData, CaseFileData, knowledge, knowledgeConnection, knowledgeEntity} from "../../../../../infrastructure/cases_management/data_structures";
import {FileProcessingStages} from "../../../../../infrastructure/cases_management/cases_consts";
import {Graph} from "./graph/graph";
import {now, random} from "lodash";

export const CaseKnowledge: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [files_data, setFilesData] = useState([] as CaseFileData[]);
    const [knowledge, setKnowledge] = useState(null as knowledge | null);

    const [graph_element, setGraphElement] = useState(<></>);

    const graph = new Graph();

    const getCaseKnowledge = useCallback(() => {
        (async () => {
            let case_files_response = await CasesManager.getInstance().getCaseFiles(caseId || '');
            setFilesData(case_files_response);
            let knowledge = {} as knowledge;
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

    let applyFileKnowledge = (file_knowledge: {entities: knowledgeEntity[], connections: knowledgeConnection[]}) => {
        for (let entity of file_knowledge.entities) {
            graph.addNode(entity.id, entity.label, entity.properties['title']);
        }
        for (let connection of file_knowledge.connections) {
            graph.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
        }
    }

    let previousUpdateTime = now();
    const graphUpdateLoop = useCallback(() => {
        requestAnimationFrame(graphUpdateLoop);
        let _now = now();
        let dt = (_now - previousUpdateTime) / 1000;
        previousUpdateTime = _now;
        graph.update(dt);
        setGraphElement(graph.getElement());
    }, []);

    let animationFrameRequest = useRef();
    useEffect(() => {
        getCaseKnowledge();
        requestAnimationFrame(graphUpdateLoop);
    }, [caseId])

    return(<>
        <div className={'case-annotations-header'}>
            <div className={'case-knowledge-page-title page-title'}>{`Case Knowledge`}</div>
        </div>
        <div className={'case-knowledge-graph-container'}>
            {graph_element}
        </div>
    </>)
}
