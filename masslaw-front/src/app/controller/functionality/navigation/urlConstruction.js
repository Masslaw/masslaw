
export function constructUrl(route, params = null, queryStringParams = null) {
    let url = route;
    if (params) url = applyUrlParams(url, params);
    if (queryStringParams) url = applyQueryStringParams(url, queryStringParams);
    return url;
}

function applyUrlParams(url, params) {
    for (let key in params) url = url.replace(`:${key}`, params[key]);
    return url;
}

function applyQueryStringParams(url, queryStringParams) {
    url += "?";
    for (let key in queryStringParams) url += `${key}=${queryStringParams[key]}&`;
    url = url.substring(0, url.length - 1);
    return url;
}
