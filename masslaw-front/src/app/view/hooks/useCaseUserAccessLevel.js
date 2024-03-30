import {model} from "../../model/model";
import {useEffect, useMemo, useState} from "react";
import {caseAccessLevels} from "../../config/caseConsts";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";

export function useCaseUserAccessLevel(caseId = null, userId = null) {

    caseId = caseId || model.cases.currentOpen.id;
    userId = userId || model.users.mine.data.User_ID;

    const {casesManager, caseUsersManager} = model.services;

    const [s_casesData, setCasesData] = useModelValueAsReactState('$.cases.all');

    const m_userAccessLevel = useMemo(() => {
        return caseUsersManager.getUserAccessLevel(caseId, userId);
    }, [s_casesData, caseId]);

    useEffect(() => {
        if (!caseId) return;
        casesManager.fetchCaseData(caseId);
    }, []);

    return m_userAccessLevel;
}