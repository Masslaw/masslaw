import {model} from "../../model/model";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {useEffect, useMemo} from "react";


export function useCaseData(caseId = null) {

    caseId = caseId || model.cases.currentOpen.id;

    const {casesManager} = model.services;

    const [s_casesData, setCasesData] = useModelValueAsReactState('$.cases.all');

    const m_caseData = useMemo(() => s_casesData[caseId] || {}, [s_casesData, caseId]);

    useEffect(() => {
        if (!caseId) return;
        casesManager.fetchCaseData(caseId);
    }, []);

    return m_caseData;
}
