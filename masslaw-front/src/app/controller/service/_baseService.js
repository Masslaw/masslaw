import {model} from "../../model/model";

export class BaseService {
    constructor() {
        this.model = model;
    }

    start() {}
}