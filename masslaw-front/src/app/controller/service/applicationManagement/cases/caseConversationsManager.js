import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {model} from "../../../../model/model";

export class CaseConversationsManager extends BaseService {
    start() {
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async fetchCaseConversations(caseId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_CONVERSATIONS,
            pathParameters: {case_id: caseId},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.conversations.data = responseData.conversations || {};
        return request;
    }

    async fetchCaseConversationContent(conversationId, caseId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_CONVERSATION_MESSAGES,
            pathParameters: {case_id: caseId, conversation_id: conversationId},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.conversations.content[conversationId] = responseData.content || {};
        return request;
    }

    async sendConversationMessage(message, conversationId, caseId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        model.cases.currentOpen.conversations.data[conversationId].last_message = Math.floor(Date.now() / 1000).toString();
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_CASE_CONVERSATION_MESSAGE,
            pathParameters: {case_id: caseId, conversation_id: conversationId},
            body: {prompt: message},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.conversations.content[conversationId] = responseData.content || {};
        return request;
    }

    async createNewConversation(conversationName, caseId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.PUT_CASE_CONVERSATION,
            pathParameters: {case_id: caseId},
            body: {name: conversationName},
        });
        const responseData = request.getResponsePayload();
        const conversationId = responseData.id || {};
        const conversationData = responseData.data || {};
        this.model.cases.currentOpen.conversations.data[conversationId] = conversationData;
        return conversationId;
    }
}
