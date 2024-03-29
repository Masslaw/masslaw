import {BaseService} from "../_baseService";

export class ModelToLocalStorageManager extends BaseService {

    _savedModelPaths = new Set([]);
    _modelStateChangeHandlers = {};

    start() {
        this._modelStateManager = this.model.services['modelStateManager'];
        this._loadSavedModelPathsFromLocalStorage();
        this._loadModelFromLocalStorage();
    }

    addPathToSavedPaths(path, listen=true) {
        this._savedModelPaths.add(path);
        this._saveModelPathsToLocalStorage();
        if (listen) this._startListeningToPathUpdates(path);
        console.log("added path to saved paths: ", path);
    }

    removePathFromSavedPaths(path) {
        this._savedModelPaths.delete(path);
        this._saveModelPathsToLocalStorage();
        this._stopListeningToPathUpdates(path);
        this._removeModelValueAtPath(path);
        console.log("removed path from saved paths: ", path);
    }

    saveModelValueAtPath(path) {
        const value = this._modelStateManager.getModelValueAtPath(path);
        if (!value) return;
        console.log("saving model value at path: ", path, " value: ", value);
        localStorage.setItem(path, JSON.stringify({v: value}));
    }

    loadModelValueAtPath(path) {
        let value;
        try { value = JSON.parse(localStorage.getItem(path)).v; }
        catch { value = localStorage.getItem(path); }
        if (!value) return;
        console.log("loading model value at path: ", path, " value: ", value);
        this._modelStateManager.setModelValueAtPath(path, value);
    }

    _loadSavedModelPathsFromLocalStorage() {
        this._savedModelPaths = new Set((JSON.parse(localStorage.getItem('saved-model-paths')) || { paths: [] }).paths);
        console.log("loaded saved model paths: ", this._savedModelPaths);
        this._listenToModelChangesAtPaths();
    }

    _saveModelPathsToLocalStorage() {
        console.log("saving model paths to local storage: ", this._savedModelPaths)
        localStorage.setItem('saved-model-paths', JSON.stringify({ paths: Array.from(this._savedModelPaths) }));
    }

    _listenToModelChangesAtPaths() {
        for (const path of this._savedModelPaths) this._startListeningToPathUpdates(path);
    }

    _startListeningToPathUpdates(path) {
        const handler = _ => this.saveModelValueAtPath(path);
        this._modelStateChangeHandlers[path] = handler;
        this._modelStateManager.listenToModelChange(path, handler);
    }

    _stopListeningToPathUpdates(path) {
        const handler = this._modelStateChangeHandlers[path];
        this._modelStateManager.stopListeningToModelChange(path, handler);
    }

    _removeModelValueAtPath(pathExpression) {
        localStorage.removeItem(pathExpression);
    }

    _loadModelFromLocalStorage() {
        for (const path of this._savedModelPaths) {
            this.loadModelValueAtPath(path);
        }
    }
}
