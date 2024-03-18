import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {UserStatus} from "../../../../config/userStatus";

export class CasesManager extends BaseService{
    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.modelResetsManager = this.model.services['modelResetsManager'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];

        this.modelStateManager.listenToModelChange('$.users.mine.data.id', (c) => this.onUserId(c));
        this.modelStateManager.listenToModelChange('$.cases.currentOpen.id', (c) => this.onCaseOpen(c));
    }

    onUserId(userId) {
        if (!userId) return;
        this.fetchCases();
    }

    async fetchCases() {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.GET_CASES});
        const responsePayload = request.getResponsePayload() || {};
        const cases = responsePayload.cases || [];
        this.model.cases.all = {};
        for (const caseData of cases) this.model.cases.all[caseData.case_id] = caseData;
        return request;
    }

    async onCaseOpen(caseId) {
        if (!caseId) {
            this.modelResetsManager.resetModelStateAtPath('$.cases.currentOpen');
            return;
        }
        await this.fetchCaseData();
    }

    async fetchCaseData(caseId = null) {
        caseId = caseId || this.model.cases.currentOpen.id || '';
        if (!caseId) return;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_DATA,
            pathParameters: {case_id: caseId}
        });
        const responsePayload = request.getResponsePayload() || {};
        const caseData = responsePayload.case_data || {};
        this.model.cases.all[caseId] = {...this.model.cases.all[caseId], ...caseData};
        await this.fetchCaseContentHierarchy();
        return request;
    }

    async fetchCaseContentHierarchy(caseId = null) {
        caseId = caseId || this.model.cases.currentOpen.id || '';
        if (!caseId) return;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_CONTENT_HIERARCHY,
            pathParameters: {case_id: caseId}
        });
        const responsePayload = request.getResponsePayload() || {};
        const caseContentHierarchy = responsePayload.hierarchy || {};
        this.model.cases.all[caseId] = {...(this.model.cases.all[caseId] || {}), ...{contentHierarchy: caseContentHierarchy}};
        return request;
    }

    async createCase(caseData) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_CASE,
            body: {case_data: caseData}
        });
        return request;
    }
}