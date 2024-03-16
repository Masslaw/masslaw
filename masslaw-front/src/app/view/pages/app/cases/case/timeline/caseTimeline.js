import {CaseKnowledgeGraphDisplay} from "../_commonComponents/caseKnowledgeGraphDisplay";
import {model} from "../../../../../../model/model";

export function CaseTimeline(props) {

    model.application.pages.currentPage.name = "CaseTimeline";

    return <>
        <CaseKnowledgeGraphDisplay />
    </>
}