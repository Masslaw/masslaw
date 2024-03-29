import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";

export class CaseCommentsManager extends BaseService {
    start() {
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async fetchFileComments(fileId=null) {
        const caseId = this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_FILE_COMMENTS,
            pathParameters: {case_id: caseId, file_id: fileId},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.files.all[fileId].comments = [];
        for (const comment of (responseData.comments || [])) {
            this.model.cases.currentOpen.comments.data[comment.id] = comment;
            this.model.cases.currentOpen.files.all[fileId].comments.push(comment.id);
        }
        return request;
    }

    async putFileComment(comment, fileId=null) {
        const caseId = this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.PUT_COMMENT,
            pathParameters: {case_id: caseId, file_id: fileId},
            body: comment
        });
        return request;
    }

    async editFileComment(comment, commentId, fileId=null) {
        const caseId = this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.POST_COMMENT,
            pathParameters: {case_id: caseId, file_id: fileId, comment_id: comment.id},
            body: {
                comment_text: comment.comment_text,
                color: comment.color,
            }
        });
        return request;
    }

    async fetchComment(commentId, fileId=null) {
        const caseId = this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_COMMENT,
            pathParameters: {case_id: caseId, file_id: fileId, comment_id: commentId},
        });
        const response = request.getResponsePayload();
        this.model.cases.currentOpen.comments.data[commentId] = response.comment;
        return request;;
    }

    async deleteFileComment(commentId, caseId=null, fileId=null) {
        caseId = caseId || this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.DELETE_COMMENT,
            pathParameters: {case_id: caseId, file_id: fileId, comment_id: commentId},
        });
        return request;
    }

    async fetchCommentReplies(commentId, fileId=null, force=false) {
        if (!force && this.model.cases.currentOpen.comments.data[commentId].replies) return;
        const caseId = this.model.cases.currentOpen.id;
        fileId = fileId || this.model.cases.currentOpen.files.currentOpen.id;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.GET_COMMENT_CHILDREN,
            pathParameters: {case_id: caseId, file_id: fileId, comment_id: commentId},
        });
        const responseData = request.getResponsePayload();
        this.model.cases.currentOpen.comments.data[commentId].replies = [];
        for (const reply of responseData.replies) {
            this.model.cases.currentOpen.comments.data[reply.id] = reply;
            this.model.cases.currentOpen.comments.data[commentId].replies.push(reply.id);
        }
        return request;
    }
}