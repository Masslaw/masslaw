import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {caseFileProcessingStagesOrder, fileProcessingStages} from "../../../../config/caseConsts";

export class CaseFilesManager extends BaseService {
    start() {
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async fetchFileData(fileId, caseId=null, force=false) {
        const fileData = this.model.cases.currentOpen.files.all[fileId] || {};
        if (!force && fileData.name) return;
        caseId = caseId || this.model.cases.currentOpen.id || '';
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_FILE_DATA,
            pathParameters: {file_id: fileId, case_id: caseId}
        });
        const response = request.getResponsePayload();
        const data = response.file_data || {};
        this.model.cases.currentOpen.files.all[fileId] = {...fileData, ...data};
        return request;
    }

    async setCaseFileDescription(newDescription, fileId, caseId = null) {
        caseId = caseId || this.model.cases.currentOpen.id || '';
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_CASE_FILE_DATA,
            queryStringParameters: {
                case_id: caseId,
                file_id: fileId,
            },
            body: {
                data: {
                    description: newDescription
                }
            }
        });
        return request;
    }

    async fetchFileContent(contentPaths, fileId, caseId, force=false) {
        await this.fetchFileData(fileId, caseId, force);
        caseId = caseId || this.model.cases.currentOpen.id || '';
        await this.fetchFileContentDownloadURLs(contentPaths, fileId, caseId, force);
        const fileData = this.model.cases.currentOpen.files.all[fileId] || {};
        const currentContent = (fileData.content || {});
        const contentPathsToDownload = contentPaths;
        if (!force) for (const pathIdx in contentPathsToDownload) if((currentContent[contentPathsToDownload[pathIdx]] || {}).downloadedContent) contentPathsToDownload.splice(pathIdx, 1);
        if (!contentPathsToDownload.length) return;
        await Promise.all(contentPathsToDownload.map(async path => {
            let downloadResponse = {};
            for (let i = 0; i < 3; i++) {
                const url = (currentContent[path] || {}).downloadUrl;
                downloadResponse = await fetch(url);
                if (downloadResponse.ok) break;
                await this.fetchFileContentDownloadURLs([path], fileId, caseId, true);
            }
            if (!(downloadResponse || {}).ok) return;
            const content = await downloadResponse.text();
            currentContent[path] = {...(currentContent[path] || {}), ...{downloadedContent: content}};
        }));
        this.model.cases.currentOpen.files.all[fileId] = {...fileData, ...{content: currentContent}};
    }

    async fetchFileContentDownloadURLs(contentPaths, fileId, caseId, force=false) {
        await this.fetchFileData(fileId, caseId, force);
        const fileData = this.model.cases.currentOpen.files.all[fileId] || {};
        const currentContent = fileData.content || {};
        const contentPathsToUpdate = [...contentPaths];
        if (!force) for (const pathIdx in contentPathsToUpdate) if((currentContent[contentPathsToUpdate[pathIdx]] || {}).downloadUrl) contentPathsToUpdate.splice(pathIdx, 1);
        if (!contentPathsToUpdate.length) return;
        caseId = caseId || this.model.cases.currentOpen.id || '';
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_CASE_FILE_CONTENT,
            pathParameters:  {file_id: fileId, case_id: caseId},
            queryStringParameters:  {content_paths: contentPathsToUpdate.join('|')}
        });
        const response = request.getResponsePayload();
        const downloadUrls = response.download_urls || {};
        for (const path in downloadUrls) currentContent[path] = {...(currentContent[path] || {}), downloadUrl: downloadUrls[path]};
        this.model.cases.currentOpen.files.all[fileId] = {...fileData, content: currentContent};
        return request;
    }

    getFileUnfinishedProcessingStagesInOrder(fileData) {
        let stagesInProgress = [];
        const processingData = fileData.processing || {};
        const stages = Object.keys(processingData);
        if (stages.length === 0) return [fileProcessingStages.Starting];
        for (let stage of stages) {
            const stage_data = processingData[stage];
            const status = stage_data.status;
            if (status !== 'done') stagesInProgress.push(stage);
        }
        stagesInProgress.sort((a, b) => {
            const indexA = caseFileProcessingStagesOrder.indexOf(a);
            const indexB = caseFileProcessingStagesOrder.indexOf(b);
            if (indexA === -1 && indexB === -1) return 0;
            if (indexA === -1) return 1;
            if (indexB === -1) return -1;
            return indexA - indexB;
        });
        return stagesInProgress;
    }
}