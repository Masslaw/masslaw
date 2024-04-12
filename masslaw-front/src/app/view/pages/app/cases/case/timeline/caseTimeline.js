import {model} from "../../../../../../model/model";
import {CaseTimelineDisplay} from "../../../../../components/caseTimelineDisplay";

export function CaseTimeline(props) {

    model.application.pages.currentPage.name = "CaseTimeline";

    return <>
        <CaseTimelineDisplay />
    </>
}