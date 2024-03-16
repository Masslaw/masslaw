import {modelInitState} from "./modelInitState";

export const modelInitStateCopy = JSON.parse(JSON.stringify(modelInitState));

export const model = modelInitState;

export function initModel() {}
