import {model} from "../../../model/model";


export function getSearchParams() {
    const searchParams = new URLSearchParams(window.location.search);
    let params = {};
    for (let pair of searchParams.entries()) params[pair[0]] = pair[1];
    return params;
}

export function setSearchParams(params) {
    const searchParams = new URLSearchParams({...params});
    model.application.navigate(window.location.pathname + '?' + searchParams.toString(), { replace: true });
}
