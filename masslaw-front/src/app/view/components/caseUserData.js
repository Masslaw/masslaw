import styled from "styled-components";
import {ProfilePicture} from "./profilePicture";
import {useEffect, useMemo, useState} from "react";
import {model} from "../../model/model";
import {LoadingIcon} from "./loadingIcon";
import {CaseUserRole} from "./caseUserRole";

const CaseUserDataContainer = styled.div`
    position: relative;
    width: calc(100% - 32px);
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 16px;
`

const CaseUserDataProfilePictureContainer = styled.div`
    width: 32px;
    height: 32px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid white;
`

const CaseUserDataTopSection = styled.div`
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
`

const CaseUserDataUserName = styled.div`
    height: 100%;
    display: flex;
    align-items: center;
    margin-left: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 16px;
    font-weight: bold;
    color: white;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
`

export function CaseUserData(props) {

    const casesManager = model.services['casesManager'];
    const usersManager = model.services['usersManager'];

    const [s_caseData, setCaseData] = useState(null);

    useEffect(() => {
        if (!props.caseId) return;
        casesManager.fetchCaseData(props.caseId).then(() => {
            const caseData = model.cases.all[props.caseId];
            setCaseData(caseData);
        });
    }, [props.caseId]);

    const [s_userData, setUserData] = useState({});

    useEffect(() => {
        console.log(s_caseData);
        console.log(props.userId);
        if (!s_caseData) return;
        if (!props.userId) return;
        const caseUsers = s_caseData.users || {};
        const caseUserData = caseUsers[props.userId] || {};
        setUserData(p => ({...p, ...caseUserData}));
    }, [s_caseData, props.userId]);

    useEffect(() => {
        if (!props.userId) return;
        usersManager.fetchUserData(props.userId).then(() => {
            const userData = model.users.data[props.userId];
            setUserData(p => ({...p, ...userData}));
        });
    }, [props.userId]);

    return <>
        <CaseUserDataContainer>
            {s_userData.first_name && s_userData.last_name ? <>
                <CaseUserDataTopSection>
                    <CaseUserDataProfilePictureContainer>
                        <ProfilePicture userId={props.userId} size={'small'}/>
                    </CaseUserDataProfilePictureContainer>
                    <CaseUserDataUserName>
                        {`${s_userData.first_name || ''} ${s_userData.last_name || ''}`.trim() || <LoadingIcon width={'8px'} height={'8px'} />}
                    </CaseUserDataUserName>
                    <CaseUserRole caseId={props.caseId} userId={props.userId} />
                </CaseUserDataTopSection>
            </> : <>
                <LoadingIcon width={'20px'} height={'20px'} />
            </>}
        </CaseUserDataContainer>
    </>
}