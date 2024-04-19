import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {mergeDeep} from "../../../functionality/object-utils/objectMerging";
import {UserStatus} from "../../../../config/userStatus";

export class CasesKnowledgeManager extends BaseService{
    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async fetchCaseKnowledge(force=false) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        if (!force && this.model.cases.currentOpen.knowledge.entities.length && this.model.cases.currentOpen.knowledge.connections.length) return;
        const caseId = this.model.cases.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_KNOWLEDGE,
            pathParameters: {case_id: caseId},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.knowledge = responseData.knowledge;
        return request;
    }

    async fetchCaseKnowledgeItem(itemType, itemId, caseId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_KNOWLEDGE_ITEM,
            pathParameters: {case_id: caseId, item_type: itemType, item_id: itemId},
        });
        const responseData = request.getResponsePayload();
        return responseData.knowledge;
    }
}