import {MasslawHttpApiClient} from "./server-communication/masslaw-api/masslawHttpApiClient";
import {CognitoClient} from "./server-communication/masslaw-authentication/cognitoClient";
import {ModelStateManager} from "./model/modelStateManager";
import {ModelToLocalStorageManager} from "./model/modelToLocalStorageManager";
import {ContentUploader} from "./server-communication/masslaw-content/contentUploader";
import {model} from "../../model/model";
import {PagePermissionsManager} from "./navigation-management/pagePermissionsManager";
import {ModelUpdatesRecorder} from "./model/modelUpdatesRecorder";
import {UsersManager} from "./applicationManagement/users/usersManager";
import {CasesManager} from "./applicationManagement/cases/casesManager";
import {CaseFilesManager} from "./applicationManagement/cases/caseFilesManager";
import {ModelResetsManager} from "./model/modelResetsManager";
import {CaseCommentsManager} from "./applicationManagement/cases/caseCommentsManager";
import {CaseSearchesManager} from "./applicationManagement/cases/caseSearchesManager";
import {SearchParamsManager} from "./navigation-management/searchParamsManager";
import {CasesKnowledgeManager} from "./applicationManagement/cases/casesKnowledgeManager";


const SERVICES = [
    ModelStateManager,
    ModelResetsManager,
    ModelToLocalStorageManager,
    ModelUpdatesRecorder,
    MasslawHttpApiClient,
    CognitoClient,
    PagePermissionsManager,
    SearchParamsManager,
    UsersManager,
    CasesManager,
    CaseFilesManager,
    CaseCommentsManager,
    CaseSearchesManager,
    CasesKnowledgeManager,
    ContentUploader,
];

export function initServices() {
    _constructServices();
    _startServices();
}

function _constructServices() {
    model.services = {};
    for (const service of SERVICES) {
        let serviceName = service.name;
        serviceName = serviceName.charAt(0).toLowerCase() + serviceName.slice(1);
        model.services[serviceName] = new service();
        console.log("Service created: " + serviceName + ".")
    }
}

function _startServices() {
    for (const service in model.services) {
        model.services[service].start();
        console.log("Service started: " + service + ".");
    }
}
