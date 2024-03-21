import {CaseKnowledgeGraphDisplay} from "../../../../../components/caseKnowledgeGraphDisplay";
import {model} from "../../../../../../model/model";

export function CaseKnowledge(props) {

    model.application.pages.currentPage.name = "CaseKnowledge";

    return <>
        <CaseKnowledgeGraphDisplay />
    </>
}