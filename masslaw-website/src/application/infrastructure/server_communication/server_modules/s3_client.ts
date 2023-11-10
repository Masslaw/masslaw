import axios from "axios";

export class S3Manager {
    private static instance = new S3Manager();

    public static getInstance() {
        return this.instance;
    }

    constructor() {
        if (S3Manager.instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }
}

export interface MultipartUploadTemplate {
    beginuploadapicall: Function,
    finishuploadapicall: Function,
}

export abstract class MultipartFileUploader {

    protected readonly file: File;
    protected readonly progressCallback?: Function;

    private readonly CHUNK_SIZE = 1024 * 1024 * 5; // ~ 5MB

    protected num_chunks = 0;

    protected upload_urls = {} as {[key:string]:string};

    protected file_parts : { [key: string]: { [key: string]: string | number }[] } = { 'Parts': [] };

    constructor(file: File, progressCallback?: Function) {
        this.file = file
        this.progressCallback = progressCallback
    }

    public async performMultipartUpload() {

        this.num_chunks = Math.ceil(this.file.size / this.CHUNK_SIZE);

        await this.beginUpload();

        for (let i = 0; i < this.num_chunks; i++){
            if (this.progressCallback) this.progressCallback(i / this.num_chunks);

            const chunk_num = i;
            const part = chunk_num + 1;
            const chunk_blob = this.file.slice(chunk_num * this.CHUNK_SIZE, (chunk_num + 1) * this.CHUNK_SIZE);

            const part_upload_res = await axios.put(this.upload_urls[i],chunk_blob, {
                headers: {'Content-Type': chunk_blob.type}
            });
            if ('headers' in part_upload_res && 'etag' in part_upload_res['headers']) {
                this.file_parts['Parts'].push({'ETag': part_upload_res['headers']['etag'],'PartNumber': part});
            }
        }
        if (this.progressCallback) this.progressCallback(1);

        return await this.finishUpload();
    }

    protected async beginUpload() {
        this.upload_urls = {};
    }

    protected async finishUpload() {
        return true;
    }
}