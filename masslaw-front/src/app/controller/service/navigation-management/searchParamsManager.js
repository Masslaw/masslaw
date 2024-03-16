import {BaseService} from "../_baseService";
import {getSearchParams, setSearchParams} from "../../functionality/navigation/searchParams";

export class SearchParamsManager extends BaseService {

    start() {
        this.modelStateManager = this.model.services['modelStateManager'];

        this.modelStateManager.listenToModelChange('$.application.searchParams', v => this.onSearchParamsChanged(v));
        this.modelStateManager.listenToModelChange('$.application.pages.currentPage', v => this.onPageChanged(v));
    }

    onSearchParamsChanged(searchParams) {
        setSearchParams(searchParams);
    }

    onPageChanged() {
        this.model.application.searchParams = getSearchParams();
    }
}