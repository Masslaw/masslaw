import axios from "axios";
import {MasslawApiCallData, MasslawApiCalls, MasslawApiRequest} from "./api_config";
import {ApiManager} from "./api_client";

export class S3Manager {
    private static _instance = new S3Manager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (S3Manager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }
}

export interface MultipartUploadTemplate {
    begin_upload_api_call: Function,
    finish_upload_api_call: Function,
}

export class MultipartFileUploader {

    private readonly _file: File | null;
    private readonly _uploadTemplate: MultipartUploadTemplate | null;
    private readonly _progressCallback: Function | null;

    private readonly CHUNK_SIZE = 1024 * 1024 * 5; // ~ 5MB

    private num_chunks = 0;

    private begin_result: { upload_id: string; upload_urls: string; file_id: string; } | null | undefined;

    private file_parts : { [key: string]: { [key: string]: string | number }[] } = { 'Parts': [] };

    constructor(file: File, template: MultipartUploadTemplate, progressCallback: Function | null) {
        this._file = file
        this._uploadTemplate = template
        this._progressCallback = progressCallback
    }

    public async performMultipartUpload() {

        if (!(this._file != null && this._uploadTemplate != null))
            return false;

        this.num_chunks = Math.ceil(this._file.size / this.CHUNK_SIZE);

        await this.begin_mp_file_upload();
        if (this.begin_result == null) return false;

        for (let i = 0; i < this.num_chunks; i++){
            if (this._progressCallback) this._progressCallback(i / this.num_chunks);

            const chunk_num = i;
            const part = chunk_num + 1;
            const chunk_blob = this._file.slice(chunk_num * this.CHUNK_SIZE, (chunk_num + 1) * this.CHUNK_SIZE);

            const upload_res = await axios.put(this.begin_result.upload_urls[i],chunk_blob, {
                headers:{
                    'Content-Type': chunk_blob.type
                }
            });
            if ('headers' in upload_res && 'etag' in upload_res['headers']) { // means part upload was successful
                this.file_parts['Parts'].push({
                    'ETag': upload_res['headers']['etag'],
                    'PartNumber': part,
                });
            }
        }
        if (this._progressCallback) this._progressCallback(1);
        return await this.finish_mp_file_upload();
    }

    private async begin_mp_file_upload() {
        let response = await this._uploadTemplate?.begin_upload_api_call(this._file?.name, this.num_chunks)
        if (!response.success) return;
        this.begin_result = {
            upload_id: response.data.upload_id,
            upload_urls: response.data.upload_urls,
            file_id: response.data.file_id,
        }
    }

    private async finish_mp_file_upload() {
        let response = await this._uploadTemplate?.finish_upload_api_call(this.begin_result?.file_id, this.file_parts)
        return response.success;
    }
}