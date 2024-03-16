import {CaseKnowledgeGraphDisplay} from "../_commonComponents/caseKnowledgeGraphDisplay";
import {model} from "../../../../../../model/model";

export function CaseSubjects(props) {

    model.application.pages.currentPage.name = "CaseSubjects";

    return <>
        <CaseKnowledgeGraphDisplay labels={['PERSON']} />
    </>
}