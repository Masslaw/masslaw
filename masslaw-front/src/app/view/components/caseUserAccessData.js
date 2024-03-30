import React, {useEffect, useMemo, useState} from "react";
import {accessLevelDisplayNames, caseAccessLevels} from "../../config/caseConsts";
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';
import styled from "styled-components";
import {VerticalGap} from "./verticalGap";
import {CaseContentPathSelection} from "./caseContentPathSelection";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {model} from "../../model/model";


const selectableAccessLevels = [
    { value: caseAccessLevels.manager, label: accessLevelDisplayNames[caseAccessLevels.manager] },
    { value: caseAccessLevels.editor, label: accessLevelDisplayNames[caseAccessLevels.editor] },
    { value: caseAccessLevels.reader, label: accessLevelDisplayNames[caseAccessLevels.reader] },
]


const accessLevelComments = {
    [caseAccessLevels.manager]: "Managers have an administrative access to the case. They are exposed to the entirety of the case and its content. They have the ability to perform any action below the owner of the case.",
    [caseAccessLevels.editor]: "Editors have the ability to make changes to the case. In the storage hierarchy configured as accessible by them, they can upload and make changes to any file or document.",
    [caseAccessLevels.reader]: "Readers can only view the content of the case. In the storage hierarchy configured as accessible by them, they can view and comment on any file or document.",
}

const SectionLabel = styled.div`
    font-size: 14px;
    color: white;
    margin: 8px 16px;
`

const SectionSubLabel = styled.div`
    font-size: 12px;
    color: #808080;
    margin: 8px 16px;
`

const AccessLevelDropDownContainer = styled.div`
    width: calc(100% - 32px);
    margin: 8px 16px;
    .Dropdown-control {
        position: relative;
        overflow: hidden;
        background-color: #404040;
        border: 1px solid #ccc;
        box-sizing: border-box;
        color: white;
        border-radius: 8px;
        cursor: pointer;
        outline: none;
        padding: 8px 52px 8px 10px;
        transition: all 200ms ease;
        font-size: 14px;
    }
    .Dropdown-menu {
        border-radius: 8px;
        margin-top: 6px;
    }
    .Dropdown-option {
        box-sizing: border-box;
        color: white;
        cursor: pointer;
        display: block;
        padding: 6px 8px;
        background: #404040;
        font-size: 13px;
    }
    .Dropdown-option:hover {
        background: #505050;
        color: white;
    }
    .Dropdown-option.is-selected {
        background: #606060;
        color: white;
    }
`

const AccessLevelComment = styled.div`
    width: calc(100% - 48px);
    margin: 8px 24px;
    color: #808080;
    font-size: 12px;
`

const CaseContentPathSelectionContainer = styled.div`
    width: calc(100% - 32px);
    margin: 8px 16px;
    background: #303030;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #808080;
`

export function CaseUserAccessData(props) {

    const caseUsersManager = model.services['caseUsersManager'];

    const [s_accessData, setAccessData] = useState({});

    const [s_cases, setCases] = useModelValueAsReactState('$.cases.all');

    useEffect(() => {
        setAccessData(caseUsersManager.getUserAccessData(props.caseId, props.userId));
    }, [s_cases, props.caseId, props.userId]);

    useEffect(() => {
        if (!props.setAccessData) return;
        props.setAccessData(s_accessData);
    }, [s_accessData]);
    
    return <>
        <VerticalGap gap={'8px'} />
        <SectionLabel>Access Level</SectionLabel>
        <SectionSubLabel>This will be the level of access the user will have to your case</SectionSubLabel>
        <AccessLevelDropDownContainer>
            <Dropdown
                options={selectableAccessLevels}
                value={s_accessData.access_level || caseAccessLevels.manager}
                onChange={o => setAccessData(p => ({...p, access_level: o.value}))}
            />
        </AccessLevelDropDownContainer>
        <AccessLevelComment>{accessLevelComments[s_accessData.access_level || caseAccessLevels.manager]}</AccessLevelComment>
        {[caseAccessLevels.editor, caseAccessLevels.reader].includes(s_accessData.access_level) ? <>
            <VerticalGap gap={'8px'} />
            <SectionLabel>Accessible Folders</SectionLabel>
            <SectionSubLabel>Within the content of the case, these folders will be the only ones accessible by the user</SectionSubLabel>
            <VerticalGap gap={'8px'} />
            <CaseContentPathSelectionContainer>
                <CaseContentPathSelection
                    caseId={props.caseId}
                    paths={((s_accessData.access_policy || {}).files || {}).allowed_paths || []}
                    setPaths={paths => setAccessData(accessData => {
                        const newAccessData = {...accessData}
                        newAccessData.access_policy = newAccessData.access_policy || {};
                        newAccessData.access_policy.files = newAccessData.access_policy.files || {};
                        newAccessData.access_policy.files.allowed_paths = paths;
                        return newAccessData
                    })}
                />
            </CaseContentPathSelectionContainer>
            <VerticalGap gap={'8px'} />
            <SectionLabel>Blocked Content</SectionLabel>
            <SectionSubLabel>Within the folders that are accessible by the user, these paths be excluded and blocked for this user</SectionSubLabel>
            <VerticalGap gap={'8px'} />
            <CaseContentPathSelectionContainer>
                <CaseContentPathSelection
                    caseId={props.caseId}
                    paths={((s_accessData.access_policy || {}).files || {}).prohibited_paths || []}
                    setPaths={paths => setAccessData(accessData => {
                        const newAccessData = {...accessData}
                        newAccessData.access_policy = newAccessData.access_policy || {};
                        newAccessData.access_policy.files = newAccessData.access_policy.files || {};
                        newAccessData.access_policy.files.prohibited_paths = paths;
                        return newAccessData
                    })}
                />
            </CaseContentPathSelectionContainer>
        </> : <></>}
        <VerticalGap gap={'16px'} />
    </>
}
