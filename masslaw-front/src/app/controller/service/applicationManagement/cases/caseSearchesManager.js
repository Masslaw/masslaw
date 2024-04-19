import {BaseService} from "../../_baseService";
import {MasslawApiCalls} from "../../../../config/masslawAPICalls";
import {UserStatus} from "../../../../config/userStatus";

const RESULT_PRE_TAG = '<search_result>';
const ESCAPED_PRE_TAG = RESULT_PRE_TAG.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
const RESULT_POST_TAG = '</search_result>';
const ESCAPED_POST_TAG = RESULT_POST_TAG.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
const RESULT_PADDING = 150;

export class CaseSearchesManager extends BaseService {
    start() {
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
    }

    async searchFilesText(searchText, files=null, force=false) {
        if (this.model.users.mine.authentication.status < UserStatus.FULLY_APPROVED) return;
        searchText = searchText.trim();
        const caseId = this.model.cases.currentOpen.id || '';
        if (!force && (this.model.cases.currentOpen.search.results[searchText] || []).length) return;
        const request = await this.masslawHttpApiClient.makeApiHttpRequest({
            call: MasslawApiCalls.SEARCH_CASE_FILES_TEXT,
            pathParameters: {case_id: caseId},
            queryStringParameters: {search_query: searchText, ...( files ? {files: files.join('&')} : {}), highlight_padding: RESULT_PADDING}
        });
        const response = request.getResponsePayload();
        const responseResults = response.results || {};
        const searchResults = [];
        for (let result of responseResults) {
            const items = this.parseSearchResultData(result);
            searchResults.push(...items);
        }
        this.model.cases.currentOpen.search.history.push(searchText);
        if (JSON.stringify(this.model.cases.currentOpen.search.results).length > 1_000_000) delete this.model.cases.currentOpen.search.results[this.model.cases.currentOpen.search.history.shift()];
        this.model.cases.currentOpen.search.results[searchText] = searchResults;
        return request;
    }

    parseSearchResultData(searchResultData) {
        const searchResults = [];
        for (let highlight of searchResultData.text_highlights || []) {
            highlight = highlight.replace(new RegExp(`${ESCAPED_POST_TAG}((\\s*.{0,10}?)\\s*)${ESCAPED_PRE_TAG}`, "g"), "$1");
            const preTagIndices = [];
            const postTagIndices = [];
            let preTagRegex = new RegExp(RESULT_PRE_TAG, 'g');
            let preTagMatch;
            while ((preTagMatch = preTagRegex.exec(highlight)) !== null) preTagIndices.push(preTagMatch.index);
            let postTagMatch;
            let postTagRegex = new RegExp(RESULT_POST_TAG, 'g');
            while ((postTagMatch = postTagRegex.exec(highlight)) !== null) postTagIndices.push(postTagMatch.index + RESULT_POST_TAG.length);
            for (let i = 0; i < preTagIndices.length; i++) {
                const startIndexOfHighlight = preTagIndices[i] + RESULT_PRE_TAG.length;
                const endIndexOfHighlight = postTagIndices[i] - RESULT_POST_TAG.length;
                const highlightedText = highlight.substring(startIndexOfHighlight, endIndexOfHighlight);
                let startText = highlight
                    .substring(0, preTagIndices[i])
                    .replace(new RegExp(RESULT_PRE_TAG, 'g'), '')
                    .replace(new RegExp(RESULT_POST_TAG, 'g'), '');
                startText = startText.substring(startText.length - RESULT_PADDING, startText.length);
                let endText = highlight
                    .substring(postTagIndices[i], highlight.length)
                    .replace(new RegExp(RESULT_PRE_TAG, 'g'), '')
                    .replace(new RegExp(RESULT_POST_TAG, 'g'), '');
                endText = endText.substring(0, RESULT_PADDING);
                const itemData = {
                    ...searchResultData,
                    start_text: startText,
                    highlighted_text: highlightedText,
                    end_text: endText
                };
                delete itemData.text_highlights;
                searchResults.push(itemData);
            }
        }
        return searchResults;
    }
}