import {AuthenticationDetails, CognitoUser, CognitoUserPool} from "amazon-cognito-identity-js";
import jwt_decode, {JwtPayload} from "jwt-decode";
import {UserStatusManager} from "../user_management/user_status_manager";
import {UserStatus} from "../user_management/user_status";

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

    }

    private _rememberedEmailKey = 'user-remembered-email'
    private _rememberedPasswordKey = 'user-remembered-password'
    private _accessTokenKey = 'users-access-token'
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

        let {email, password} = this.getRememberedUserLoginCredentials();

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

    public securelyRememberUserLoginCredentials(email : string, password : string) {
        sessionStorage.setItem(this._rememberedEmailKey, email);
        sessionStorage.setItem(this._rememberedPasswordKey, password);
    }

    public getRememberedUserLoginCredentials() : {email: string | null, password: string | null}{
        return {
            email: sessionStorage.getItem(this._rememberedEmailKey),
            password: sessionStorage.getItem(this._rememberedPasswordKey),
        }
    }

    public logOutUser() {
        this.securelyRememberUserLoginCredentials('', '');
        this.handleAccessToken('').then();
        this.setLoggedInUserEmail('');
        UserStatusManager.getInstance().setDiscoveredStatus(UserStatus.GUEST);
    }

    public getLoggedInUserEmail() : string {
        return sessionStorage.getItem(this._loggedUserEmailKey) || '';
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
                    this.handleAccessToken(accessToken);
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

    private async handleAccessToken(accessToken: string) {
        localStorage.setItem(this._accessTokenKey, accessToken);

        UserStatusManager.getInstance().setDiscoveredStatus(
            (this.getAccessToken()) ? UserStatus.LOGGED_IN : UserStatus.GUEST);
    }

    private setLoggedInUserEmail(email: string) {
        sessionStorage.setItem(this._loggedUserEmailKey, email);
    }
}