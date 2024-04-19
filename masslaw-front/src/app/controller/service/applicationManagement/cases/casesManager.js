import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {UserStatus} from "../../../../config/userStatus";

export class CasesManager extends BaseService{
    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.modelResetsManager = this.model.services['modelResetsManager'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];

        this.modelStateManager.listenToModelChange('$.users.mine.data.User_ID', (c) => this.onUserId(c));
        this.modelStateManager.listenToModelChange('$.cases.currentOpen.id', (c) => this.onCaseOpen(c));
    }

    onUserId(userId) {
        this.modelResetsManager.resetModelStateAtPath('$.cases');
        if (!userId) return;
        this.fetchCases();
    }

    async fetchCases() {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.GET_CASES});
        const responsePayload = request.getResponsePayload() || {};
        const cases = responsePayload.cases || [];
        const casesCopy = {...this.model.cases.all};
        this.model.cases.all = {};
        for (const caseData of cases) this.model.cases.all[caseData.case_id] = {...(casesCopy[caseData.case_id] || {}), ...caseData};
        return request;
    }

    async onCaseOpen(caseId) {
        if (!caseId) return this.modelResetsManager.resetModelStateAtPath('$.cases.currentOpen');
        await this.fetchCaseData();
        await this.fetchCaseContentHierarchy();
    }

    async fetchCaseData(caseId = null, force=false) {
        caseId = caseId || this.model.cases.currentOpen.id;
        if (!caseId) return;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        if (!force && Object.keys(this.model.cases.all[caseId] || {}).length) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_DATA,
            pathParameters: {case_id: caseId}
        });
        const responsePayload = request.getResponsePayload() || {};
        const caseData = responsePayload.case_data || {};
        this.model.cases.all[caseId] = {...(this.model.cases.all[caseId] || {}), ...caseData};
        return request;
    }

    async fetchCaseContentHierarchy(caseId = null, force=false) {
        caseId = caseId || this.model.cases.currentOpen.id || '';
        if (!caseId) return;
        if (!force && (this.model.cases.all[caseId] || {}).contentHierarchy) return;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_CONTENT_HIERARCHY,
            pathParameters: {case_id: caseId}
        });
        const responsePayload = request.getResponsePayload() || {};
        const caseContentHierarchy = responsePayload.hierarchy || {};
        const caseFilesData = this.getCaseFilesDataFromHierarchy(caseContentHierarchy);
        this.model.cases.all[caseId] = {...(this.model.cases.all[caseId] || {}), ...{contentHierarchy: caseContentHierarchy}, ...{filesData: caseFilesData}};
        return request;
    }

    async createCase(caseData) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.PUT_CASE,
            body: {case_data: caseData}
        });
        return request;
    }

    async postCaseData(caseData, caseId=null) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        caseId = caseId || this.model.cases.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_CASE,
            pathParameters: {case_id: caseId},
            body: {case_data: caseData}
        });
        return request;
    }

    getCaseFilesDataFromHierarchy(hierarhchy, currentPath=null) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        currentPath = currentPath || [];
        let caseFilesData = {};
        for (const key in hierarhchy) {
            const value = hierarhchy[key];
            if (typeof value === 'object') {
                const newPath = [...currentPath, key];
                const newFilesData = this.getCaseFilesDataFromHierarchy(value, newPath);
                caseFilesData = {...caseFilesData, ...newFilesData};
                continue;
            }
            caseFilesData[value] = {
                'name': key,
                'path': currentPath,
            }
        }
        return caseFilesData;
    }
}