import {model} from "../../model/model";
import {useEffect, useMemo, useState} from "react";
import {caseAccessLevels} from "../../config/caseConsts";

export function useCaseUserAccessLevel(caseId = null, userId = null) {

    caseId = caseId || model.cases.currentOpen.id;
    userId = userId || model.users.mine.data.User_ID;

    const casesManager = model.services['casesManager'];
    const caseUsersManager = model.services['caseUsersManager'];

    const [s_caseData, setCaseData] = useState(null);

    useEffect(() => {
        if (!caseId) return;
        casesManager.fetchCaseData(caseId).then(() => {
            const caseData = model.cases.all[caseId];
            setCaseData(caseData);
        });
    }, [caseId]);

    const m_userAccessLevel = useMemo(() => {
        if (!s_caseData) return caseAccessLevels.external;
        return caseUsersManager.getUserAccessLevel(s_caseData.caseId, userId);
    }, [s_caseData]);

    return m_userAccessLevel;
}