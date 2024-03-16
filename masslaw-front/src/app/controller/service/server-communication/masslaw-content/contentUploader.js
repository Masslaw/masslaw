import {MultipartFileUpload} from "./_multipartUpload";
import {BaseService} from "../../_baseService";

export class ContentUploader extends BaseService {

    start() {
        this.casesManager = this.model.services['casesManager'];
    }

    async uploadCaseFile(file, directory, progressCallback = null) {
        const uploader = new MultipartFileUpload(file, directory, progressCallback);
        const result = await uploader.execute();
        return result;
    }
}


