export enum DevelopmentStages {
    PRODUCTION = 'prod',
    DEVELOPMENT = 'dev',
}

export class DevelopmentStagesManager {

    private static _instance = new DevelopmentStagesManager();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (DevelopmentStagesManager._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    };

    public getDevelopmentStage() {
        // on macOS / Linux do: ~export DEVELOPMENT_STAGE=<development_stage>
        // on Windows do: ~setx DEVELOPMENT_STAGE "<development_stage>"
        return DevelopmentStages.PRODUCTION; //TOPOOOO
        // return (process.env.REACT_APP_DEVELOPMENT_STAGE || DevelopmentStages.PRODUCTION) as DevelopmentStages;
    }
}