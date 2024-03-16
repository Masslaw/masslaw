import {initView} from "./view/view";
import {initModel} from "./model/model";
import {initController} from "./controller/controller";


export class Application {
    constructor() {
    }

    start() {
        initModel();
        initController();
        initView();
    }
}
