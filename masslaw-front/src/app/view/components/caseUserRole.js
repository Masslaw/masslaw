import {accessLevelDisplayColors, accessLevelDisplayNames} from "../../config/caseConsts";
import {model} from "../../model/model";
import {useEffect, useState} from "react";
import styled from "styled-components";


const CaseUserDataUserRole = styled.div`
    height: ${({height}) => height || '24px'};
    width: ${({width}) => width || '96px'};
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
    background: ${({color}) => color};
    border: 1px solid #ffffff80;
`

export function CaseUserRole(props) {

    const casesManager = model.services['casesManager'];

    const [s_caseData, setCaseData] = useState(null);

    useEffect(() => {
        if (!props.caseId) return;
        casesManager.fetchCaseData(props.caseId).then(() => {
            const caseData = model.cases.all[props.caseId];
            setCaseData(caseData);
        });
    }, [props.caseId])

    const [s_userData, setUserData] = useState({});

    useEffect(() => {
        if (!s_caseData) return;
        if (!props.userId) return;
        const caseUsers = s_caseData.users || {};
        const caseUserData = caseUsers[props.userId] || {};
        setUserData(p => ({...p, ...caseUserData}));
    }, [s_caseData, props.userId]);

    return <>
        <CaseUserDataUserRole
            width={props.width}
            height={props.height}
            color={accessLevelDisplayColors[s_userData.access_level] || '#00000000'}
        >
            {accessLevelDisplayNames[s_userData.access_level]}
        </CaseUserDataUserRole>
    </>
}