import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import axios from 'axios';
import {model} from "../../../../model/model";

const CHUNK_SIZE = 1024 * 1024 * 5; // ~ 5MB

export class MultipartFileUpload {
    masslawHttpApiClient = null;
    uploadUrls = {};
    directory = [];
    caseId = null;
    fileInstance = null;
    progressCallback = null;
    fileParts = { 'Parts': [] };

    constructor(file, directory, progressCallback = null) {
        this.fileInstance = file;
        this.directory = directory;
        this.progressCallback = progressCallback || (() => {});
        this.caseId = model.cases.currentOpen.id || '';
        this.masslawHttpApiClient = model.services['masslawHttpApiClient'];
    }

    async execute() {
        const numChunks = Math.ceil(this.fileInstance.size / CHUNK_SIZE);
        await this._beginUpload(numChunks);
        for (let i = 0; i < numChunks; i++){
            if (this.progressCallback) this.progressCallback(i / numChunks);
            const chunkNum = i;
            const part = chunkNum + 1;
            const chunkBlob = this.fileInstance.slice(chunkNum * CHUNK_SIZE, (chunkNum + 1) * CHUNK_SIZE);
            const partUploadRes = await axios.put(this.uploadUrls[i],chunkBlob, {headers: {'Content-Type': chunkBlob.type}});
            ('headers' in partUploadRes && 'etag' in partUploadRes['headers']) && this.fileParts['Parts'].push({'ETag': partUploadRes['headers']['etag'],'PartNumber': part});
        }
        this.progressCallback && this.progressCallback(1);
        return await this._finishUpload();
    }

    async _beginUpload(numChunks) {
        let request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.START_CASE_FILE_UPLOAD,
            pathParameters: {case_id: this.caseId},
            body: {
                path: this.directory,
                file_name: this.fileInstance.name,
                num_parts: numChunks.toString(),
                languages: ['eng'],
            }
        });
        const response = request.getResponsePayload();
        this.uploadUrls = response.upload_urls;
        this.fileId = response.file_id;
    }

    async _finishUpload() {
        let response= await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.FINISH_CASE_FILE_UPLOAD,
            pathParameters: {case_id: this.caseId},
            body: {
                file_id: this.fileId,
                parts: this.fileParts
            }
        });
        return response.success;
    }
}