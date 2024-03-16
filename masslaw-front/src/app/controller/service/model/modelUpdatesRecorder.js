import {BaseService} from "../_baseService";

export class ModelUpdatesRecorder extends BaseService {

    modelPathsUpdateTime = {};

    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
    }

    recordModelValueChangeTimesAtPath(path) {
        this.modelStateManager.listenToModelChange(path, _ => this._onModelValueChange(path));
    }

    getLastModelChangeTimeAtPath(path) {
        return this.modelPathsUpdateTime[path] || null;
    }

    getTimeSinceLastModelChangeAtPath(path) {
        const lastChangeTime = this.getLastModelChangeTimeAtPath(path);
        return lastChangeTime ? Date.now() - lastChangeTime : null;
    }

    _onModelValueChange(path) {
        this.modelPathsUpdateTime[path] = Date.now();
    }
}