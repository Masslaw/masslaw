import {useState} from "react";
import {model} from "../../../model/model";


export function useModelValueAsReactState(path, defaultInitialState = null) {

    const modelStateManager = model.services['modelStateManager'];

    const currentModelValue = modelStateManager.getModelValueAtPath(path);
    const initValue = [null, undefined].includes(currentModelValue) ? defaultInitialState : currentModelValue;
    modelStateManager.setModelValueAtPath(path, initValue)

    const [state, setState] = useState(initValue);

    const newSetState = v => {
        if (typeof v === 'function') v = v(modelStateManager.getModelValueAtPath(path));
        if (typeof v === 'object' && v !== null) v = {...v};
        modelStateManager.setModelValueAtPath(path, v);
        setState(typeof v === 'function' ? () => v : v);
    }

    modelStateManager.listenToModelChange(path, (c) => newSetState(typeof c === 'function' ? () => c : c));

    return [state, newSetState];
}
