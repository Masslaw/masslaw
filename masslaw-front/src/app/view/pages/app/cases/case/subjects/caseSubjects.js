import {CaseKnowledgeGraphDisplay} from "../../../../../components/caseKnowledgeGraphDisplay";
import {model} from "../../../../../../model/model";

export function CaseSubjects(props) {

    model.application.pages.currentPage.name = "CaseSubjects";

    return <>
        <CaseKnowledgeGraphDisplay labels={['PERSON']} />
    </>
}