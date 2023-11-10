import {AuthenticationDetails, CognitoRefreshToken, CognitoUser, CognitoUserPool} from "amazon-cognito-identity-js";
import jwt_decode, {JwtPayload} from "jwt-decode";

export enum LoginResult {
    SUCCEEDED,
    VERIFICATION_NEEDED,
    FAILED,
}

export enum LoginMethods {
    MASSLAW,
    GOOGLE,
}

export enum SignupResult {
    SUCCEEDED,
    FAILED,
    FAILED_INVALID_EMAIL,
    FAILED_INVALID_PASSWORD
}

export enum EmailVerificationResult {
    SUCCEEDED,
    FAILED_EXPIRED,
    FAILED
}

export class CognitoManager {
    private static _instance = new CognitoManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (CognitoManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
        if (this.getAccessToken() || localStorage.getItem(this._refreshTokenKey)) {
            this.startRefreshingCycle();
        }
    }

    private _rememberedEmailKey = 'user-remembered-email'
    private _rememberedPasswordKey = 'user-remembered-password'
    private _accessTokenKey = 'users-access-token'
    private _refreshTokenKey = 'user-refresh-token';
    private _refreshIntervalId: number | undefined;
    private _loggedUserEmailKey = 'logged-user-email'

    private COGNITO_USER_POOL_ID = "us-east-1_0eUKxygQZ";
    private COGNITO_CLIENT_ID = "7a2irjb3i7o3vgo5sf9t9nad62";
    private GOOGLE_CLIENT_ID = "198474213836-0qcaqfoi73rj33ls8tc5uefpmuml4o3s.apps.googleusercontent.com";

    private _userPool = new CognitoUserPool({ UserPoolId: this.COGNITO_USER_POOL_ID, ClientId: this.COGNITO_CLIENT_ID });

    public getLoginToolkit(callback: CallableFunction) {
        return {
            loginDefault: async (email: string, password: string) => {
                await this.logInDefault(email, password, callback);
            },
            googleLoginParams: {
                clientId: this.GOOGLE_CLIENT_ID,
                onSuccess: async (session: any) => {
                    await this.handleAccessToken(session.accessToken);
                    this.startRefreshingCycle();
                    callback(LoginResult.SUCCEEDED, LoginMethods.GOOGLE);
                },
                onFailure: () => {
                    callback(LoginResult.FAILED, LoginMethods.GOOGLE);
                },
            },
        };
    }

    public getSignupToolkit(callback: CallableFunction) {
        return {
            signupDefault: async (email: string, password: string) => {
                await this.signUpDefault(email, password, callback);
            },
        };
    }

    public getEmailVerificationToolkit(email: string, callback: CallableFunction) {
        const cognitoUser = new CognitoUser({
            Username: email,
            Pool: this._userPool,
        });
        return {
            resendCode: async () => {
                cognitoUser.resendConfirmationCode((err: any, data: any) => {
                    return !!err;
                }, {
                    ClientId: this.COGNITO_CLIENT_ID,
                    Username: email,
                });
            },
            attemptVerification: async (verificationCode: string) => {
                try {
                    await cognitoUser.confirmRegistration(verificationCode, true, (err, result) => {

                        if (!err) {
                            callback(EmailVerificationResult.SUCCEEDED);
                        } else if (err.name === 'ExpiredCodeException') {
                            callback(EmailVerificationResult.FAILED_EXPIRED);
                        } else {
                            callback(EmailVerificationResult.FAILED);
                        }
                    });
                } catch (e) {
                    callback(EmailVerificationResult.FAILED);
                }
            }
        }
    }

    public getForgotPasswordToolkit(email: string, new_password: string) {
        const cognitoUser = new CognitoUser({
            Username: email,
            Pool: this._userPool,
        });
        return {
            sendCode: async (): Promise<boolean> => {
                return new Promise((resolve, reject) => {
                    cognitoUser.forgotPassword({
                        onSuccess: () => {
                            resolve(true);
                        },
                        onFailure: (err) => {
                            resolve(false);
                        },
                    });
                });
            },
            attemptVerification: async (verificationCode: string): Promise<boolean> => {
                return new Promise((resolve, reject) => {
                    cognitoUser.confirmPassword(verificationCode, new_password, {
                        onSuccess: () => {
                            resolve(true);
                        },
                        onFailure: (err) => {
                            resolve(false);
                        },
                    });
                });
            }
        }
    }

    public async checkLoggedIn(attemptLoggingIn?: boolean) : Promise<boolean> {

        if (this.getAccessToken() != null) return true;

        if (!attemptLoggingIn) return false;

        return await this.attemptLogIn();
    }

    public async attemptLogIn() {
        let {email, password} = this.getRememberedUserLoginAttributes();

        if (email != null && password != null) {
            await this.logInDefault(email, password, () => {});
            if (this.getAccessToken() != null) return true;
        }

        return false;
    }

    public getAccessToken() : string | null {
        let accessToken = localStorage.getItem(this._accessTokenKey);
        if (!accessToken) return null;
        const decoded = jwt_decode(accessToken) as JwtPayload;
        const now = Math.floor(Date.now() / 1000);
        return (decoded && decoded.exp && decoded.exp > now) ? accessToken : null;
    }

    public securelyRememberUserLoginAttributes(email : string, password : string) {
        localStorage.setItem(this._rememberedEmailKey, email);
        localStorage.setItem(this._rememberedPasswordKey, password);
    }

    public getRememberedUserLoginAttributes() : {email: string | null, password: string | null}{
        const email = localStorage.getItem(this._rememberedEmailKey);
        const password = localStorage.getItem(this._rememberedPasswordKey);
        return {
            email: email,
            password: password,
        }
    }

    public logOutUser() {
        this.securelyRememberUserLoginAttributes('', '');
        this.handleAccessToken('').then();
        this.handleRefreshToken('').then();
        this.setLoggedInUserEmail('');
        this.endRefreshingCycle();
    }

    public getLoggedInUserEmail() : string {
        return localStorage.getItem(this._loggedUserEmailKey) || '';
    }

    private async logInDefault(email: string, password: string, callback: CallableFunction) {
        const authenticationDetails = new AuthenticationDetails({
            Username: email,
            Password: password,
        });

        const cognitoUser = new CognitoUser({
            Username: email,
            Pool: this._userPool,
        });

        try {
            await cognitoUser.authenticateUser(authenticationDetails, {
                onSuccess: (session) => {
                    this.setLoggedInUserEmail(email);
                    const accessToken = session.getAccessToken().getJwtToken();
                    const refreshToken = session.getRefreshToken().getToken();
                    this.handleAccessToken(accessToken);
                    this.handleRefreshToken(refreshToken);
                    callback(LoginResult.SUCCEEDED, LoginMethods.MASSLAW);
                },
                onFailure: (err) => {
                    if (err.name === 'UserNotConfirmedException') {
                        this.setLoggedInUserEmail(email);
                        callback(LoginResult.VERIFICATION_NEEDED, LoginMethods.MASSLAW);
                    } else {
                        callback(LoginResult.FAILED, LoginMethods.MASSLAW);
                    }
                },
            });
        } catch (e) {
            callback(LoginResult.FAILED, LoginMethods.MASSLAW);
        }
    }

    private async signUpDefault(email: string, password: string, callback: CallableFunction) {

        this._userPool.signUp(email, password, [], [], (err, result) => {
            if (err) {
                if ((err as Error).name === 'InvalidParameterException' && (err as any).InvalidParameterException.includes("email")) {
                    callback(SignupResult.FAILED_INVALID_EMAIL);
                } else if ((err as Error).name === 'InvalidPasswordException') {
                    callback(SignupResult.FAILED_INVALID_PASSWORD);
                } else if ((err as Error).name === 'UsernameExistsException') {
                    callback(SignupResult.FAILED_INVALID_EMAIL);
                } else {
                    callback(SignupResult.FAILED);
                }
                return;
            }
            callback(SignupResult.SUCCEEDED);
        });
    }

    private async handleAccessToken(accessToken: string | null) {
        if (accessToken) {
            localStorage.setItem(this._accessTokenKey, accessToken);
        } else {
            localStorage.removeItem(this._accessTokenKey);
            localStorage.removeItem(this._refreshTokenKey);
        }
    }

    private async handleRefreshToken(refreshToken: string | null) {
        if (refreshToken) {
            localStorage.setItem(this._refreshTokenKey, refreshToken);
        } else {
            localStorage.removeItem(this._refreshTokenKey);
        }
    }

    private setLoggedInUserEmail(email: string) {
        localStorage.setItem(this._loggedUserEmailKey, email);
    }

    private startRefreshingCycle() {
        this._refreshIntervalId = window.setInterval(async () => {
            const refreshToken = localStorage.getItem(this._refreshTokenKey);
            if (!refreshToken) return;

            const cognitoUser = this._userPool.getCurrentUser();
            if (!cognitoUser) return;

            cognitoUser.refreshSession(new CognitoRefreshToken({RefreshToken: refreshToken}), (err, session) => {
                if (err) {
                    this.logOutUser();
                } else {
                    const accessToken = session.getAccessToken().getJwtToken();
                    this.handleAccessToken(accessToken);
                }
            });
        }, 30 * 60 * 1000);  // Refresh every 30 minutes
    }

    private endRefreshingCycle() {
        if (this._refreshIntervalId) {
            window.clearInterval(this._refreshIntervalId);
            this._refreshIntervalId = undefined;
        }
    }
}