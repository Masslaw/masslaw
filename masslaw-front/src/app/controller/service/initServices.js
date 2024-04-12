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
import {CaseUsersManager} from "./applicationManagement/cases/casesUsersManager";
import {CaseConversationsManager} from "./applicationManagement/cases/caseConversationsManager";


const SERVICES = {
    modelStateManager: ModelStateManager,
    modelResetsManager: ModelResetsManager,
    modelToLocalStorageManager: ModelToLocalStorageManager,
    modelUpdatesRecorder: ModelUpdatesRecorder,
    masslawHttpApiClient: MasslawHttpApiClient,
    cognitoClient: CognitoClient,
    pagePermissionsManager: PagePermissionsManager,
    searchParamsManager: SearchParamsManager,
    usersManager: UsersManager,
    casesManager: CasesManager,
    caseFilesManager: CaseFilesManager,
    caseCommentsManager: CaseCommentsManager,
    caseSearchesManager: CaseSearchesManager,
    casesKnowledgeManager: CasesKnowledgeManager,
    caseUsersManager: CaseUsersManager,
    caseConversationsManager: CaseConversationsManager,
    contentUploader: ContentUploader,
};

export function initServices() {
    _constructServices();
    _startServices();
}

function _constructServices() {
    model.services = {};
    for (const serviceName in SERVICES) {
        let service = SERVICES[serviceName];
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
