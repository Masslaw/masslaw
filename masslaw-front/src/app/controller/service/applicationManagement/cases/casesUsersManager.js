import {BaseService} from "../../_baseService";
import {caseAccessLevels} from "../../../../config/caseConsts";
import {UserStatus} from "../../../../config/userStatus";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";

export class CaseUsersManager extends BaseService{
    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.modelResetsManager = this.model.services['modelResetsManager'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    getCaseUserData(caseId = null, userId = null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        userId = userId || this.model.users.mine.data.User_ID;
        if (!caseId || !userId) return {};
        const caseData = this.model.cases.all[caseId] || {};
        const caseUsers = caseData.users || {};
        const caseUserData = caseUsers[userId];
        return caseUserData;
    }

    getUserAccessLevelInCase(caseId = null, userId = null) {
        const caseUserData = this.getCaseUserData(caseId, userId) || {};
        const accessLevel = caseUserData.access_level;
        return accessLevel || caseAccessLevels.external;
    }

    getUserFilesAccessPolicyInCase(caseId = null, userId = null) {
        const caseUserData = this.getCaseUserData(caseId, userId) || {};
        const filesAccessPolicy = caseUserData.access_policy;
        return filesAccessPolicy || {allowed: {}, denied: {}};
    }

    getUserAccessData(caseId = null, userId = null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        userId = userId || this.model.users.mine.data.User_ID;
        if (!caseId || !userId) return {};
        const caseData = this.model.cases.all[caseId];
        if (!caseData) return {};
        const caseUsers = caseData.users || {};
        const userAccessData = caseUsers[userId] || {};
        return userAccessData;
    }

    getUserAccessLevel(caseId = null, userId = null) {
        const userAccessData = this.getUserAccessData(caseId, userId);
        return userAccessData.access_level || caseAccessLevels.external;
    }

    async setUserAccessConfiguration(userId, accessLevel = null, accessPolicy = null, caseId = null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        if (!caseId || !userId) return;
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_CASE_USER,
            pathParameters: {case_id: caseId, user_id: userId},
            body: {
                ...(accessLevel ? {access_level: accessLevel} : {}),
                ...(accessPolicy ? {access_policy: accessPolicy} : {}),
            }
        });
        return request;
    }
}
