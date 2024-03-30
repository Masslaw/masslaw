import {UsersSearch} from "../../../../../components/usersSearch";
import {useCallback, useState} from "react";
import styled from "styled-components";
import {model} from "../../../../../../model/model";
import {VerticalGap} from "../../../../../components/verticalGap";
import {UserPreviewData} from "../../../../../components/userPreviewData";
import {CaseUserAccessData} from "../../../../../components/caseUserAccessData";
import {LoadingIcon} from "../../../../../components/loadingIcon";

const AddCaseUserPopupContainer = styled.div`
    width: 512px;
    padding: 16px;
    background: #303030;
    overflow: auto;
    &::-webkit-scrollbar { display: none; }
`

const AddCaseUsersPopupTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 16px;
`

const AddCaseUsersPopupSubTitle = styled.div`
    font-size: 14px;
    font-weight: 500;
    margin: 0 16px 16px 16px;
    color: #808080;
`

const AddCaseUsersPopupSectionTitle = styled.h3`
    font-size: 16px;
    font-weight: normal;
    color: white;
    margin: 16px;
`

const UsersSearchContainer = styled.div`
    width: calc(100% - 32px);
    margin: 16px;
`

const SelectedUserItemContainer = styled.div`
    width: calc(100% - 32px);
    background: #505050;
    border-radius: 8px;
    margin: 2px 16px;
    outline: 1px solid white;
`

const RemoveSelectedUserButton = styled.button`
    font-size: 12px;
    margin: 0 16px 16px 16px;
    color: cornflowerblue;
    cursor: pointer;
    background: none;
    border: none;
`

const AddUsersButton = styled.button`
    background: white;
    color: black;
    font-size: 14px;
    border: none;
    border-radius: 6px;
    height: 32px;
    outline: none;
    margin-right: 16px;
    float: right;
    padding: 8px 16px;
    &:hover { filter: drop-shadow(0 0 5px white); }
`

export function AddCaseUsersPopup(props) {

    const caseUsersManager = model.services['caseUsersManager'];

    const [s_selectedUsers, setSelectedUsers] = useState([]);

    const [s_selectedUsersAccessData, setSelectedUsersAccessData] = useState({});

    const [s_addingUsers, setAddingUsers] = useState(false);

    const c_addUsers = useCallback(async () => {
        setAddingUsers(true);
        const promises = [];
        for (const selectedUser of s_selectedUsers) {
            if (!selectedUser) continue;
            const selectedUsersAccessData = s_selectedUsersAccessData[selectedUser] || {};
            promises.push(caseUsersManager.setUserAccessConfiguration(selectedUser, selectedUsersAccessData.access_level, selectedUsersAccessData.access_policy));
        };
        await Promise.all(promises);
        setAddingUsers(false);
    }, [s_selectedUsers, s_selectedUsersAccessData]);

    return <>
        <AddCaseUserPopupContainer>
            <AddCaseUsersPopupTitle>Add Participants</AddCaseUsersPopupTitle>
            <AddCaseUsersPopupSubTitle>Add participants to this case with a role and permission boundaries of your choice</AddCaseUsersPopupSubTitle>
            <VerticalGap gap={'16px'} />
            <UsersSearchContainer>
                <UsersSearch
                    onUserSelected={uId => setSelectedUsers(p => ([...p, uId]))}
                    filterUsers={[...Object.keys((model.cases.all[props.caseId] || {}).users || {}), ...s_selectedUsers]}
                />
            </UsersSearchContainer>
            {s_selectedUsers.length ? <>
                <AddCaseUsersPopupSectionTitle>Selected Users</AddCaseUsersPopupSectionTitle>
                {s_selectedUsers.map((userId, idx) => <>
                    <SelectedUserItemContainer>
                        <UserPreviewData userId={userId} />
                        <RemoveSelectedUserButton onClick={() => setSelectedUsers(p => p.filter(u => u!== userId))}>Remove</RemoveSelectedUserButton>
                        <CaseUserAccessData
                            caseId={props.caseId}
                            userId={userId}
                            setAccessData={(c) => setSelectedUsersAccessData(p => ({...p, ...{[userId]: c}}))}
                        />
                    </SelectedUserItemContainer>
                </>)}
                <VerticalGap gap={'32px'} />
                <AddUsersButton onClick={() => c_addUsers().then(props.dismiss())}>
                    {s_addingUsers ? <>
                        <LoadingIcon width={'20px'} height={'20px'} color={'black'} />
                    </> : 'Add Participants'}
                </AddUsersButton>
                <VerticalGap gap={'64px'} />
            </> : <></>}
            <VerticalGap gap={'32px'} />
        </AddCaseUserPopupContainer>
    </>
}