import {modelInitState} from "./modelInitState";
import {makeAutoObservable} from "mobx";

export const modelInitStateCopy = JSON.parse(JSON.stringify(modelInitState));

export const model = modelInitState;

export function initModel() {
    // makeAutoObservable(model);
}
