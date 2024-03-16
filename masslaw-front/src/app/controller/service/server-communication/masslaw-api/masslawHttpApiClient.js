import {HttpRequest} from "../../../functionality/http/httpRequest";
import {BaseService} from "../../_baseService";

const MASSLAW_PRODUCTION_API = 'https://5vcihdhjs8.execute-api.us-east-1.amazonaws.com/prod';


export class MasslawHttpApiClient extends BaseService {

    aliveRequestInstances = {};

    start() {
    }

    async makeApiHttpRequest(request) {
        console.log("Making API request: ", request);
        this._modifyRequestData(request);
        const stringifiedRequest = JSON.stringify(request);
        let requestInstance = this.aliveRequestInstances[stringifiedRequest];
        if (!requestInstance) {
            requestInstance = this._constructRequestInstance(request);
            requestInstance.execute();
            this.aliveRequestInstances[stringifiedRequest] = requestInstance;
        }
        await requestInstance.getPromise();
        const response = requestInstance.getResponsePayload();
        this._handleApiResponse(response);
        this.aliveRequestInstances[stringifiedRequest] = null;
        return requestInstance;
    }

    _constructRequestInstance(request) {
        const requestUrl = this._getBaseUrlForApi() + request.call.rout;
        const requestInstance = new HttpRequest(
            requestUrl,
            request.call.method,
            request.pathParameters || {},
            request.queryStringParameters || {},
            request.headers || {},
            request.body || {}
        );
        return requestInstance
    }

    _modifyRequestData(request) {
        request.headers = request.headers || {};
        const authenticationToken = this.model.users.mine.authentication.tokens.access;
        if (authenticationToken) request.headers['Authorization'] = `Bearer ${authenticationToken}`;
        request.headers['Content-Type'] = 'application/json';
    }

    _handleApiResponse(responseData) {
        const discoveredStatus = typeof responseData.userStatus === 'number' ? responseData.userStatus : -1;
        console.log("Discovered user status: ", discoveredStatus);
        if (discoveredStatus >= 0) this.model.users.mine.authentication.status = discoveredStatus;
    }

    _getBaseUrlForApi() {
        return process.env.REACT_APP_API_BASE_URL || MASSLAW_PRODUCTION_API;
    }
}
