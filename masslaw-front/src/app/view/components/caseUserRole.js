import {accessLevelDisplayColors, accessLevelDisplayNames} from "../../config/caseConsts";
import {model} from "../../model/model";
import {useEffect, useState} from "react";
import styled from "styled-components";
import {LoadingIcon} from "./loadingIcon";
import {useCaseUserAccessLevel} from "../hooks/useCaseUserAccessLevel";
import {accessLevelDescriptions} from "../config/accessLevelDescriptions";


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

    const m_accessLevel = useCaseUserAccessLevel(props.caseId, props.userId);

    return <>
        <CaseUserDataUserRole
            title={accessLevelDescriptions[m_accessLevel] || 'Loading...'}
            width={props.width}
            height={props.height}
            color={accessLevelDisplayColors[m_accessLevel] || '#808080'}
        >
            {m_accessLevel ? accessLevelDisplayNames[m_accessLevel] : <LoadingIcon width={'20px'} height={'20px'} />}
        </CaseUserDataUserRole>
    </>
}