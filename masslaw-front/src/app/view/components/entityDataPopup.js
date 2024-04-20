import styled from "styled-components";
import {CaseKnowledgeEntityDataDisplay} from "./caseKnowledgeEntityDataDisplay";


const EntityDataPopupContainer = styled.div`
    width: 512px;
    height: 512px;
    background: #202020;
    border-radius: 8px;
    padding: 32px;
`

export function EntityDataPopup(props) {
    return <>
        <EntityDataPopupContainer>
            <CaseKnowledgeEntityDataDisplay entityId={props.entityId} />
        </EntityDataPopupContainer>
    </>
}
