import {ApiManager} from "../server_communication/api_client";
import {MasslawApiCallData, MasslawApiCalls} from "../server_communication/api_config";
import {MultipartFileUploader, MultipartUploadTemplate} from "../server_communication/s3_client";

export class CasesManager {

    private static _instance = new CasesManager();

    public static getInstance() {
        return this._instance
    }

    constructor() {
        if (CasesManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }


    private _cachedCasesData: { [key : string] : { [key : string] : string } } = {};
    private _cachedCasesFiles: { [key : string] : [] } = {};


    public async getMyCases() {
        let callData : MasslawApiCallData = MasslawApiCalls.GET_MY_CASES;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {},
            headers: {},
            payload: {},
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let data = response.data as typeof callData.responseDataShape
        return data.my_cases
    }

    public async createACase(case_data: {[key: string] : any}) {
        let callData : MasslawApiCallData = MasslawApiCalls.CREATE_CASE;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {},
            headers: {},
            payload: {
                case_data: case_data
            },
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        return response.success ? response.data.case_id : null;
    }

    public async updateCaseData(caseId: string) {
        let callData : MasslawApiCallData = MasslawApiCalls.GET_CASE_DATA;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {
                case_id: caseId,
            },
            headers: {},
            payload: {},
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let case_data = response.data.case_data;
        this._cachedCasesData[caseId] = case_data;
        return case_data;
    }

    public async updateCaseFiles(caseId: string) {
        let callData : MasslawApiCallData = MasslawApiCalls.GET_CASE_FILES;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {
                case_id: caseId,
            },
            headers: {},
            payload: {},
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        let case_files = response.data.case_files['files'] as [];
        this._cachedCasesFiles[caseId] = case_files;
        return case_files;
    }

    public async get_file_download(caseId: string, file_id: string, file_form: string) {
        let callData : MasslawApiCallData = MasslawApiCalls.GET_CASE_FILE_DOWNLOAD;
        let callRequest : typeof callData.requestShape = {
            queryStringParameters: {
                case_id: caseId,
                file_id: file_id,
                file_form: file_form,
            },
            headers: {},
            payload: {},
        }
        let response = await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
        return response.data.download_url || '';
    }

    public getCachedCaseData(caseId: string){
        return this._cachedCasesData[caseId];
    }

    public getCachedCaseFiles(caseId: string){
        return this._cachedCasesFiles[caseId];
    }

    public async uploadFile(case_id: string, file: File, progressCallback: Function | null){

        let mpUploader = new MultipartFileUploader(file, {
            begin_upload_api_call: async (file_name: string, num_parts: number) => {
                let callData : MasslawApiCallData = MasslawApiCalls.START_CASE_FILE_UPLOAD;
                let callRequest : typeof callData.requestShape = {
                    queryStringParameters: {},
                    headers: {},
                    payload: {
                        case_id: case_id,
                        file_name: file_name,
                        num_parts: num_parts.toString(),
                        languages: ['eng', 'heb'],
                    },
                }
                return await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
            },
            finish_upload_api_call: async (file_id: string, parts: any) => {
                let callData : MasslawApiCallData = MasslawApiCalls.FINISH_CASE_FILE_UPLOAD;
                let callRequest : typeof callData.requestShape = {
                    queryStringParameters: {},
                    headers: {},
                    payload: {
                        case_id: case_id,
                        file_id: file_id,
                        parts: parts
                    },
                }
                return await ApiManager.getInstance().MasslawAPICall(callData, callRequest);
            },
        } as MultipartUploadTemplate, progressCallback);

        return await mpUploader.performMultipartUpload();
    }
}
