import {AuthenticationDetails, CognitoRefreshToken, CognitoUser, CognitoUserPool} from "amazon-cognito-identity-js";
import jwt_decode, {JwtPayload} from "jwt-decode";
import {BaseService} from "../../_baseService";

const COGNITO_USER_POOL_ID = "us-east-1_0eUKxygQZ";
const COGNITO_CLIENT_ID = "7a2irjb3i7o3vgo5sf9t9nad62";
const GOOGLE_CLIENT_ID = "198474213836-0qcaqfoi73rj33ls8tc5uefpmuml4o3s.apps.googleusercontent.com";


const userPool = new CognitoUserPool({ UserPoolId: COGNITO_USER_POOL_ID, ClientId: COGNITO_CLIENT_ID });


export class CognitoClient extends BaseService {

    start() {
        this.modelStateManager = this.model.services['modelStateManager'];
        this.modelToLocalStorageManager = this.model.services['modelToLocalStorageManager'];
        this.modelToLocalStorageManager.addPathToSavedPaths('$.users.mine.authentication.login.email')
        this.logIn().then(() => this.startRefreshingCycle);
    }

    async logIn(email = null, password = null) {
        email = email || this.model.users.mine.authentication.login.email;
        password = password || this.model.users.mine.authentication.login.password;
        if (email == null && password == null) return "invalid email or password";
        const authenticationDetails = new AuthenticationDetails({Username: email, Password: password,});
        const cognitoUser = new CognitoUser({Username: email, Pool: userPool,});
        return await new Promise((resolve, reject) => {
            cognitoUser.authenticateUser(authenticationDetails,  {
                onSuccess: (session) => {
                    this.model.users.mine.authentication.tokens.access = session.getAccessToken().getJwtToken();
                    this.model.users.mine.authentication.tokens.refresh = session.getRefreshToken().getToken();
                    resolve(null);
                },
                onFailure: (err) => {
                    resolve(err && err.name || 'unknown error');
                },
            });
        });
    }

    async signUp(email, password) {
        if (email == null && password == null) return "invalid email or password";
        return await new Promise((resolve, reject) => {
            userPool.signUp(email, password, [], [], (err, result) => {
                resolve(err && err.name || 'unknown error');
            });
        });
    }

    async sendEmailConfirmationCode(email = null) {
        email = email || this.model.users.mine.authentication.login.email;
        if (!email) return "invalid email";
        const cognitoUser = new CognitoUser({Username: email, Pool: userPool,});
        return await new Promise((resolve, reject) => {
            cognitoUser.resendConfirmationCode((err, data) => resolve(err && (err.name || 'unknown error')));
        });
    }


    async attemptEmailVerification(verificationCode, email = null) {
        email = email || this.model.users.mine.authentication.login.email;
        if (!email) return "invalid email";
        const cognitoUser = new CognitoUser({Username: email, Pool: userPool,});
        return await new Promise((resolve, reject) => {
            cognitoUser.confirmRegistration(verificationCode, true, (err, result) => resolve(err && (err.name || 'unknown error')));
        });
    }

    async sendForgotPasswordCode(email = null) {
        email = email || this.model.users.mine.authentication.login.email;
        if (!email) return "invalid email";
        const cognitoUser = new CognitoUser({Username: email, Pool: userPool,});
        return await new Promise((resolve, reject) => {
            cognitoUser.forgotPassword({
                onSuccess: () =>  resolve(null),
                onFailure: (err) => resolve(err.name || 'unknown error'),
            });
        });
    }

    async attemptForgotPasswordVerification(verificationCode, newPassword, email = null) {
        email = email || this.model.users.mine.authentication.login.email;
        if (!email) return "invalid email";
        const cognitoUser = new CognitoUser({Username: email, Pool: userPool,});
        return await new Promise((resolve, reject) => {
            cognitoUser.confirmPassword(verificationCode, newPassword, {
                onSuccess: () =>  resolve(null),
                onFailure: (err) => resolve(err.name || 'unknown error'),
            });
        });
    }

    logOut() {
        this.model.users.mine.authentication.tokens.access = null;
        this.model.users.mine.authentication.login.email = null;
        this.model.users.mine.authentication.login.password = null;
        this.endRefreshingCycle();
    }

    startRefreshingCycle() {
        this._refreshIntervalId = window.setInterval(async () => {
            const refreshToken = this.model.users.mine.authentication.tokens.refresh;
            if (!refreshToken) return;
            const cognitoUser = userPool.getCurrentUser();
            if (!cognitoUser) return;
            cognitoUser.refreshSession(new CognitoRefreshToken({RefreshToken: refreshToken}), (err, session) => {
                if (err) {
                    this.logOut();
                } else {
                    const accessToken = session.getAccessToken().getJwtToken();
                    this.handleAccessToken(accessToken);
                }
            });
        }, 30 * 60 * 1000);  // Refresh every 30 minutes
    }

    endRefreshingCycle() {
        if (this._refreshIntervalId) {
            window.clearInterval(this._refreshIntervalId);
            this._refreshIntervalId = undefined;
        }
    }
}
