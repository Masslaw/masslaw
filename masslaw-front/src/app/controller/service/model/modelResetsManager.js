import {BaseService} from "../_baseService";
import {modelInitStateCopy} from "../../../model/model";

export class ModelResetsManager extends BaseService {
    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
    }

    resetModelStateAtPath(path) {
        const initStateAtPath = this.getModelInitStateAtPath(path);
        this.modelStateManager.setModelValueAtPath(path, initStateAtPath);
    }

    getModelInitStateAtPath(path) {
        const pathParts = this._splitPath(path);
        let obj = modelInitStateCopy;
        let i = 0;
        for (i = 0; i < pathParts.length - 1; i++) obj = obj[pathParts[i]] || {};
        return obj[pathParts[i]];
    }

    _splitPath(path) {
        return path.replace('$.', '').split('.');
    }
}