import {BaseService} from "../_baseService";
import {UserStatus} from "../../../config/userStatus";
import {ApplicationRoutes} from "../../../config/applicaitonRoutes";
import {pushNotification} from "../../../view/global-view/globalLayer/_global-layer-components/notifications";

export class PagePermissionsManager extends BaseService {

    previousStatus = -1;
    currentStatus = -1;

    minimumUserStatus = null;
    maximumUserStatus = null;

    start() {
        this.cognitoClient = this.model.services['cognitoClient'];
        this.masslawHttpApiClient = this.model.services['masslawHttpApiClient'];
        this.modelStateManager = this.model.services['modelStateManager'];
        this.usersManager = this.model.services['usersManager'];

        this.modelStateManager.listenToModelChange('$.users.mine.authentication.status', v => this._onUserStatusChanged(v));
        this.modelStateManager.listenToModelChange('$.application.pages.currentPage.minimumUserStatus', v => this._onMinimumStatusChanged(v));
        this.modelStateManager.listenToModelChange('$.application.pages.currentPage.maximumUserStatus', v => this._onMaximumStatusChanged(v));
        this.modelStateManager.listenToModelChange('$.application.pages.currentPage.name', v => this._processState());
        this._refreshStatus(); // this will essentially ensure that the user is logged in if their login attributes are saved in the local storage
    }

    _onUserStatusChanged(userStatus) {
        console.log("User status changed to:", userStatus);
        if (userStatus < 0) return;
        this.previousStatus = this.currentStatus;
        this.currentStatus = userStatus;
        this._processState().then();
    }

    _onMinimumStatusChanged(minimumUserStatus) {
        console.log("Minimum user status changed to:", minimumUserStatus);
        this.minimumUserStatus = minimumUserStatus;
        this._processState().then();
    }

    _onMaximumStatusChanged(maximumUserStatus) {
        console.log("Maximum user status changed to:", maximumUserStatus);
        this.maximumUserStatus = maximumUserStatus;
        this._processState().then();
    }

    async _processState() {
        console.log("Processing state...", "current status:", this.currentStatus, "previous status:", this.previousStatus, "minimum status:", this.minimumUserStatus, "maximum status:", this.maximumUserStatus);
        if (this.currentStatus < 0) return;

        const currentStatusTooLow = this.minimumUserStatus !== null && this.currentStatus < this.minimumUserStatus;
        const currentStatusTooHigh = this.maximumUserStatus !== null && this.currentStatus > this.maximumUserStatus;

        if (!(currentStatusTooLow || currentStatusTooHigh)) return;

        console.log("Invalid user status detected.");

        if (currentStatusTooLow) {
            console.log("Refreshing user status...");
            const statusChangedOnRefresh = await this._refreshStatus();
            if (statusChangedOnRefresh) return;
        }

        console.log("User status refreshing did not change the status.")
        console.log("Handling invalid user status...")
        if (this.currentStatus === UserStatus.GUEST) {
            this.model.application.navigate(ApplicationRoutes.LOGIN);
            if (currentStatusTooLow) pushNotification({id: 'failed_on_guest_status', title: "You have been logged out.", body: "Your session has expired. Please log back in to continue."});
            return;
        }

        if (this.currentStatus === UserStatus.UNVERIFIED) {
            this.model.application.navigate(ApplicationRoutes.VERIFICATION);
            pushNotification({id: 'failed_on_unverified_status', title: "Verification Needed", body: "Your account needs verification. Please complete the verification process to continue."});
            return;
        }

        if (this.currentStatus === UserStatus.MISSING_ATTRIBUTES) {
            this.model.application.navigate(ApplicationRoutes.EDIT_PROFILE);
            pushNotification({id: 'failed_on_missing_attributes_status', title: "Missing Information", body: "Your account is missing required information. Please fill the required account information to continue."});
            return;
        }

        if (this.currentStatus > UserStatus.MISSING_ATTRIBUTES) {
            this.model.application.navigate(ApplicationRoutes.MY_CASES);
            return;
        }
    }

    async _refreshStatus() {
        console.log("Refreshing user status...");
        this.model.application.view.state.loading['user_status'] = true;
        let loginResult = null;
        if (this.currentStatus <= UserStatus.GUEST) loginResult = await this.cognitoClient.logIn();
        if (!loginResult) await this.usersManager.fetchMyStatus();
        const newStatus = this.model.users.mine.authentication.status;
        this.model.application.view.state.loading['user_status'] = false;
        return newStatus >= 0 && newStatus !== this.currentStatus;
    }
}