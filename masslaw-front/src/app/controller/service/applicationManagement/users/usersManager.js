import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";

export class UsersManager extends BaseService {

    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.modelUpdatesRecorder = this.model.services['modelUpdatesRecorder'];
        this.modelToLocalStorageManager = this.model.services['modelToLocalStorageManager'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async fetchMyStatus() {
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.GET_MY_STATUS});
        return request;
    }

    async fetchMyUserData(force = false) {
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.GET_USER_DATA, pathParameters: {user_id: 'me'}});
        const responsePayload = request.getResponsePayload() || {};
        const userData = responsePayload.user_data;
        if (!userData) return;
        this.model.users.mine.data = JSON.parse(JSON.stringify(userData));
        this.model.users.data[userData.User_ID] = JSON.parse(JSON.stringify(userData));
        return request;
    }

    async submitMyUserData(userData) {
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.SET_USER_DATA, body: {user_data: userData}});
        this.model.users.mine.data = JSON.parse(JSON.stringify(userData));
        this.model.users.data[userData.User_ID] = JSON.parse(JSON.stringify(userData));
        return request;
    }

    async fetchUserData(userId, force= false) {
        const userDataModelPath = `$.users.data.${userId}`;
        if (!force && this.model.users.data[userId] && this.modelUpdatesRecorder.getTimeSinceLastModelChangeAtPath(userDataModelPath) < 5000) return;
        this.modelUpdatesRecorder.recordModelValueChangeTimesAtPath(userDataModelPath);
        this.modelToLocalStorageManager.addPathToSavedPaths(userDataModelPath);
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.GET_USER_DATA, pathParameters: {user_id: userId}});
        const responsePayload = request.getResponsePayload() || {};
        const userData = responsePayload.user_data;
        if (!userData) return;
        this.model.users.data[userId] = {...(this.model.users.data[userId] || {}), ...JSON.parse(JSON.stringify(userData))};
        return request;
    }

    async searchUsers(query){
        if (query.length < 2) return [];
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({call: MasslawApiCalls.SEARCH_USERS, queryStringParameters: {search_query: query}});
        const responsePayload = request.getResponsePayload();
        const results = responsePayload.results || [];
        const resultUserIds = [];
        for (const result of results) {
            const resultUserId = result.User_ID;
            if (!resultUserId) continue;
            this.model.users.data[resultUserId] = {...(this.model.users.data[resultUserId] || {}), ...result};
            resultUserIds.push(resultUserId);
        }
        return resultUserIds;
    }
}