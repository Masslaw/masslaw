import {BaseService} from "../_baseService";

export class ModelStateManager extends BaseService {

    _registeredCallbacks = {};

    start() {
        this._startCheckLoop();
    }

    listenToModelChange(path, callback) {
        const current = this.getModelValueAtPath(path);
        this._registeredCallbacks[path] = this._registeredCallbacks[path] || {callbacks: [], previousValue: current};
        this._registeredCallbacks[path].callbacks.push(callback);
    }

    stopListeningToModelChange(path, callback) {
        this._registeredCallbacks[path].callbacks = this._registeredCallbacks[path].callbacks.filter(cb => cb !== callback);
        if (this._registeredCallbacks[path].callbacks.length === 0) delete this._registeredCallbacks[path];
    }

    getModelValueAtPath(path) {
        const pathParts = this._splitPath(path);
        let obj = this.model;
        let i = 0;
        for (i = 0; i < pathParts.length - 1; i++) obj = obj[pathParts[i]] || {};
        return obj[pathParts[i]];
    }

    setModelValueAtPath(path, value) {
        const pathParts = this._splitPath(path);
        let obj = this.model;
        let i = 0;
        for (i = 0; i < pathParts.length - 1; i++) obj = obj[pathParts[i]] || {};
        obj[pathParts[i]] = value;
    }

    _startCheckLoop() {
        this._checkLoop = this._checkLoop.bind(this)
        requestAnimationFrame(this._checkLoop);
    }

    _checkLoop() {
        this._checkRegisteredModelChanges();
        requestAnimationFrame(this._checkLoop);
    }

    _checkRegisteredModelChanges() {
        for (const path in this._registeredCallbacks) this._checkForChangesAtPath(path);
    }

    _checkForChangesAtPath(path) {
        const currentValue = this.getModelValueAtPath(path);
        const stringifiedCurrenValue = JSON.stringify({v: currentValue});
        const previousValue = this._registeredCallbacks[path].previousValue;
        if (previousValue !== stringifiedCurrenValue) {
            console.log(`Model state change detected at path:`, path);
            this._handleModelChange(path, currentValue);
            this._registeredCallbacks[path].previousValue = stringifiedCurrenValue;
        }
    }

    _handleModelChange(path, value) {
        const registeredCallbacks = this._registeredCallbacks[path] || {};
        for (const callback of registeredCallbacks.callbacks || []) callback(value);
    }

    _splitPath(path) {
        return path.replace('$.', '').split('.');
    }
}
