import {ApplicationRoutes} from "../routing/application_routes";

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
    }

    private _stageDomains : Map<DevelopmentStages, string[]> = new Map([
        [DevelopmentStages.PRODUCTION, [
            'https://masslaw.ai',
            'https://www.masslaw.ai',
        ]],
        [DevelopmentStages.DEVELOPMENT, [
            'https://dev.masslaw.ai',
            'https://localhost:3000',
            'http://localhost:3000',
        ]]
    ]);

    public getDevelopmentStage() {
        for (let [_, stage] of Object.entries(DevelopmentStages)) {
            let stageDomains = this._stageDomains.get(stage);
            if (stageDomains != null && stageDomains.includes(origin)) return stage;
        }

        return DevelopmentStages.PRODUCTION;
    }
}