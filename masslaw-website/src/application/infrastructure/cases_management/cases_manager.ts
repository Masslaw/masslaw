import {ApiManager, HTTPRequest} from "../server_communication/api/api_client";
import {MultipartFileUploader, MultipartUploadTemplate} from "../server_communication/server_modules/s3_client";
import {CaseData, CaseFileAnnotationData, CaseFileData, knowledge} from "./data_structures";
import {MasslawApiCalls} from "../server_communication/api/api_config";


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

    public async getMyCases() {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{my_cases: CaseData[]}>({
                call: MasslawApiCalls.GET_MY_CASES,
            } as HTTPRequest);
        return response.data.my_cases
    }

    public async createACase(case_data: CaseData) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{case_id: string}>({
            call: MasslawApiCalls.CREATE_CASE,
            body: {case_data: case_data} as {[key:string]: CaseData},
        } as HTTPRequest);
        return response.success ? response.data.case_id : null;
    }

    public async getCaseData(caseId: string) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{case_data: CaseData}>({
            call: MasslawApiCalls.GET_CASE_DATA,
            queryStringParameters: {case_id: caseId} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.case_data;
    }

    public async setCaseData(caseId: string, newData: CaseData) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{}>({
            call: MasslawApiCalls.SET_CASE_DATA,
            queryStringParameters: {case_id: caseId} as {[key:string]: string},
            body: {new_data: newData} as {[key:string]: any},
        } as HTTPRequest);
        return response.success;
    }

    public async getCaseFiles(caseId: string) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{case_files: {files: CaseFileData[]}}>({
            call: MasslawApiCalls.GET_CASE_FILES,
            queryStringParameters: {case_id: caseId} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.case_files?.files;
    }

    public async getFileData(caseId: string, fileId: string): Promise<CaseFileData> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{file_data: CaseFileData}>({
            call: MasslawApiCalls.GET_CASE_FILE_DATA,
            queryStringParameters: {case_id: caseId, file_id: fileId} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.file_data;
    }

    public async getCaseAnnotations(caseId: string, fileIds?: string[]): Promise<CaseFileAnnotationData[]> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{annotations: CaseFileAnnotationData[]}>({
            call: MasslawApiCalls.GET_CASE_ANNOTATIONS,
            queryStringParameters: {case_id: caseId, files: fileIds && fileIds.join('|') || ''} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.annotations;
    }

    public async setCaseAnnotation(annotation_data: CaseFileAnnotationData): Promise<CaseFileAnnotationData[]> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{annotations: CaseFileAnnotationData[]}>({
            call: MasslawApiCalls.SET_CASE_ANNOTATION,
            queryStringParameters: {
                case_id: annotation_data.case_id,
                file_id: annotation_data.file_id,
                annotation_id: annotation_data.annotation_id,
            } as {[key:string]: string},
            body: {
                type: annotation_data.type,
                from_char: annotation_data.from_char,
                to_char: annotation_data.to_char,
                annotation_text: annotation_data.annotation_text,
                annotated_text: annotation_data.annotated_text,
                color: annotation_data.color,
            } as {[key:string]: any}
        } as HTTPRequest);
        return response.data.annotations;
    }

    public async setCaseFileDescription(case_id: string, file_id: string, new_description: string) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{}>({
            call: MasslawApiCalls.SET_FILE_DESCRIPTION,
            queryStringParameters: {
                case_id: case_id,
                file_id: file_id,
            } as {[key:string]: string},
            body: {
                value: new_description
            } as {[key:string]: any}
        } as HTTPRequest);
        return response.success
    }

    public async deleteCaseAnnotation(annotation_data: CaseFileAnnotationData): Promise<boolean> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{}>({
            call: MasslawApiCalls.DELETE_CASE_ANNOTATION,
            queryStringParameters: {
                case_id: annotation_data.case_id,
                file_id: annotation_data.file_id,
                annotation_id: annotation_data.annotation_id,
            } as {[key:string]: string}
        } as HTTPRequest);
        return response.success;
    }

    public async deleteFile(caseId: string, fileId: string): Promise<boolean> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{}>({
            call: MasslawApiCalls.DELETE_CASE_FILE,
            queryStringParameters: {case_id: caseId, file_id: fileId} as {[key:string]: string},
        } as HTTPRequest);
        return response.success;
    }

    public async getFileContentDownloadURL(case_id: string, file_id: string, content_paths: string[]) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{download_urls: {[key:string]: string}}>({
            call: MasslawApiCalls.GET_CASE_FILE_CONTENT,
            queryStringParameters: {case_id: case_id, file_id: file_id, content_paths: content_paths.join('|')} as {[key:string]: string},
        } as HTTPRequest);
        return (response.data.download_urls || {}) as {[key:string]: string};
    }

    public async uploadFile(case_id: string, file: File, progressCallback?: Function) {
        let mpUploader = new MasslawCaseFilesMultipartUploader(case_id, file, ['eng'], progressCallback);
        return await mpUploader.performMultipartUpload();
    }

    public async getCaseKnowledgeForItem(case_id: string, item_id: string, item_type: string): Promise<knowledge> {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{knowledge: knowledge}>({
            call: MasslawApiCalls.GET_CASE_KNOWLEDGE_ITEM_DATA,
            queryStringParameters: {case_id: case_id, item_id: item_id, item_type: item_type} as {[key:string]: string},
        } as HTTPRequest);
        return response.data.knowledge;
    }

    public async search_text(caseId: string, text: string, fileIds?: string[], highlight_padding?: number) {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{
            results: {file_id: string, file_name: string, text_highlights: string}[]
        }>({
            call: MasslawApiCalls.SEARCH_CASE_FILES_TEXT,
            queryStringParameters: {
                case_id: caseId,
                search_query: text,
                files: (fileIds?.join('|')) || undefined,
                highlight_padding: highlight_padding || undefined
            } as {[key:string]: any},
        } as HTTPRequest);
        const results = response.data.results;
        return results;
    }
}

class MasslawCaseFilesMultipartUploader extends MultipartFileUploader {
    private case_id: string;
    private languages: string[];
    private file_id: string = ''

    constructor(case_id: string, file: File, languages: string[], progressCallback?: Function) {
        super(file, progressCallback);
        this.case_id = case_id;
        this.languages = languages;
    }

    protected async beginUpload() {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{file_id: string, upload_urls: {[key:string]: string}}>({
            call: MasslawApiCalls.START_CASE_FILE_UPLOAD,
            body: {
                case_id: this.case_id,
                file_name: this.file.name,
                num_parts: this.num_chunks.toString(),
                languages: this.languages,
            } as {[key:string]: any},
        } as HTTPRequest);
        this.upload_urls = response.data.upload_urls;
        this.file_id = response.data.file_id;
    }

    protected async finishUpload() {
        let response= await ApiManager.getInstance().MakeApiHttpRequest<{upload_urls: {[key:string]: string}}>({
            call: MasslawApiCalls.FINISH_CASE_FILE_UPLOAD,
            body: {
                case_id: this.case_id,
                file_id: this.file_id,
                parts: this.file_parts
            } as {[key:string]: any},
        } as HTTPRequest);
        this.upload_urls = response.data.upload_urls;
        return response.success;
    }
}
