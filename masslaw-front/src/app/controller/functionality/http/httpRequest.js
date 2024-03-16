import axios from "axios";

export class HttpRequest {

    url = "";
    method = "";
    queryStringParameters = {};
    headers = {};
    body = {};

    response = {};
    success = false;

    promise = new Promise(() => {});

    constructor(url, method, pathParameters, queryStringParameters, headers, body) {
        this.url = url || "";
        this.method = method || "";
        this.pathParameters = pathParameters || {};
        this.queryStringParameters = queryStringParameters || {};
        this.headers = headers || {};
        this.body = body || {};
    }

    execute() {
        this.promise = this._performRequest();
    }

    getPromise() {
        return this.promise;
    }

    getResponsePayload() {
        return this.response.data || {};
    }

    getResponseSuccess() {
        return this.success;
    }

    async _performRequest() {
        try {
            let url = this._constructUrl();
            this.response = await axios.request({
                url: url.href,
                method: this.method,
                headers: this.headers || {},
                data: this.body || {},
                validateStatus: () => true,
            });
            this.success = this.response.status < 300;
        } catch (error) {
            return {
                success: false,
                data: {},
            };
        }
    }

    _constructUrl() {
        let url = new URL(this.url);
        for (const [key, value] of Object.entries(this.pathParameters)) {
            if (key && value) url.pathname = url.pathname.replace(`%7B${key}%7D`, value.toString());
        }
        for (const [key, value] of Object.entries(this.queryStringParameters)) {
            if (key && value) url.searchParams.append(key, value);
        }
        return url;
    }
}