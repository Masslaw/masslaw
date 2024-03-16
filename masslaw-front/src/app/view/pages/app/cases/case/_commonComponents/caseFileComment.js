import styled from "styled-components";
import {model} from "../../../../../../model/model";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {useCallback, useEffect, useMemo, useState} from "react";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {LongTextInput} from "../../../../../components/longTextInput";
import {ProfilePicture} from "../../../../../components/profilePicture";
import {MeatballsMenu} from "../../../../../components/meatballsMenu";


const CaseFileCommentContainer = styled.div`
    width: 100%;
    height: max-content;
`

export function CaseFileComment(props) {
    return <>
        <CaseFileCommentContainer>
            <CaseFileSingleComment
                commentId={props.commentId}
                displayAnnotatedText={props.displayAnnotatedText}
            />
        </CaseFileCommentContainer>
    </>
}


const CaseFileSingleCommentContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: max-content;
`

const CaseFileSingleCommentActionInProgressLoading = styled.div`
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 50;
    pointer-events: all;
    background: #ffffff80;
`

const CaseFileSingleCommentHeader = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    margin: 4px 0;
`

const CaseFileSingleCommentHeaderProfilePictureContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    height: 20px;
    width: 20px;
    margin: 0 2px;
    border-radius: 4px;
    overflow: hidden;
`

const CaseFileSingleCommentHeaderNameContainer = styled.div`
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 13px;
    margin: 0 4px;
    color: #505050;
`

const CaseFileSingleCommentMeatballsMenuButtonContainer = styled.div`
    width: 16px;
    height: 16px;
`

const CaseFileSingleCommentOptionsSection = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    overflow: hidden;
    button {
        background: none;
        border: none;
        margin: 2px;
        color: cornflowerblue;
        font-size: 12px;
        text-underline: cornflowerblue;
    }
`

const CaseFileSingleCommentAnnotatedText = styled.div`
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
    height: max-content;
    max-height: 36px;
    font-size: 10px;
    line-height: 12px;
    width: calc(100% - 24px);
    padding: 8px 12px;
    margin: 4px 0;
    color: #303030;
    background: ${({color}) => color}60;
    border-radius: 4px;
    border: 1px solid ${({color}) => color};
`

const CaseFileSingleCommentText = styled.div`
    position: relative;
    overflow: hidden;
    text-wrap: normal;
    font-size: 12px;
    line-height: 14px;
    padding: 4px 8px;
    color: #101010;
`

const CaseFileSingleCommentToggleLongShortButton = styled.button`
    position: relative;
    display: flex;
    color: #999999;
    background: none;
    border: none;
    cursor: pointer;
`

const NoCommentsMessage = styled.div`
    position: relative;
    font-size: 12px;
    padding: 4px 8px;
    color: #999999;
`

const NoCommentsButton = styled.div`
    position: relative;
    font-size: 12px;
    padding: 2px 4px;
    margin: 2px 4px;
    width: calc(100% - 16px);
    color: #999999;
    pointer-events: all;
    cursor: pointer;
    background: none;
    border-radius: 2px;
    &:hover {
        background: #c0c0c0;
        color: #777777;
    }
`

const CaseFileSingleCommentShowHideRepliesButton = styled.button`
    position: relative;
    display: flex;
    color: #999999;
    background: none;
    border: none;
    cursor: pointer;
`

const CaseFileSingleCommentRepliesContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100% - 16px);
    overflow: hidden;
    height: max-content;
    padding: 4px 0 4px 16px;
`

function CaseFileSingleComment(props) {

    const caseCommentsManager = model.services['caseCommentsManager'];
    const usersManager = model.services['usersManager'];

    const [s_users, setUsers] = useModelValueAsReactState('$.users.data', {});

    const [s_comments, setComments] = useModelValueAsReactState('$.cases.currentOpen.comments.data', {});

    const m_commentData = useMemo(() => s_comments[props.commentId] || {}, [s_comments, props.commentId])

    useEffect(() => {
        if (!m_commentData) return;
        const ownerUserId = m_commentData.owner;
        if (!ownerUserId) return;
        usersManager.fetchUserData(ownerUserId);
    }, [m_commentData]);

    const m_ownerUserData = useMemo(() => {
        if (!m_commentData) return undefined;
        return s_users[m_commentData.owner];
    }, [s_users, m_commentData]);

    const m_imTheOwner = useMemo(() => {
        if (!m_commentData) return false;
        return m_commentData.owner === model.users.mine.data.User_ID;
    }, [m_commentData]);

    const [s_displayLong, setDisplayLong] = useState(false);

    const m_isTextLong = useMemo(() => {
        return ((m_commentData || {}).comment_text || '').length > 100;
    }, [m_commentData]);

    const m_textToDisplay = useMemo(() => {
        return s_displayLong || !m_isTextLong ? (m_commentData || {}).comment_text || '' : (m_commentData.comment_text.slice(0, 100) + '...');
    }, [m_commentData, m_isTextLong, s_displayLong]);


    const [s_editData, setEditData] = useState({});
    const [s_editing, setEditing] = useState(false);
    const [s_submittingEdit, setSubmittingEdit] = useState(false);

    const c_startEdit = useCallback(() => {
        if (s_editing) return;
        if (!m_imTheOwner) return;
        setEditData({...m_commentData});
        setEditing(true);
    }, [s_editing, m_imTheOwner]);

    const c_edit = useCallback(async () => {
        if (s_submittingEdit) return;
        if (!s_editing) return;
        if (!m_imTheOwner) return;
        setSubmittingEdit(true);
        const commentData = {...s_editData};
        await caseCommentsManager.editFileComment(commentData);
        await caseCommentsManager.fetchFileComments(null, true);
        setEditing(false);
        setSubmittingEdit(false);
    }, [s_editData, s_editing, m_imTheOwner, s_submittingEdit]);

    const c_cancelEdit = useCallback(() => {
        setEditData({...m_commentData});
        setEditing(false);
        setSubmittingEdit(false);
    }, [m_commentData]);

    const [s_deleteRequested, setDeleteRequested] = useState(false);
    const [s_deleting, setDeleting] = useState(false);

    const c_requestDelete = useCallback(async () => {
        if (s_deleteRequested) return;
        setDeleteRequested(true);
    }, [s_deleteRequested]);

    const c_delete = useCallback(async () => {
        if (s_deleting) return;
        if (!s_deleteRequested) return;
        setDeleting(true);
        await caseCommentsManager.deleteFileComment(m_commentData.id);
        await caseCommentsManager.fetchFileComments(null, true);
        setDeleting(false);
        setDeleteRequested(false);
    }, [s_deleting, s_deleteRequested]);

    const c_cancelDelete = useCallback(() => {
        setDeleteRequested(false);
        setDeleting(false);
    }, []);

    const [s_loadingReplies, setLoadingReplies] = useState(false);

    const [s_showingReplies, setShowingReplies] = useState(false);

    const c_loadReplies = useCallback(async () => {
        if (s_loadingReplies) return;
        setLoadingReplies(true);
        const commentReplies = m_commentData.children || [];
        const repliesToLoad = [];
        for (const replyId of commentReplies) {
            if (!s_comments[replyId]) repliesToLoad.push(replyId);
            if (repliesToLoad.length > 3) break;
        }
        await Promise.all(repliesToLoad.map((replyId) => caseCommentsManager.fetchComment(replyId)));
        setLoadingReplies(false);
    }, [s_loadingReplies, s_comments, m_commentData]);

    const m_loadedReplies = useMemo(() => {
        const commentReplies = m_commentData.children || [];
        const loadedReplies = [];
        for (const replyId of commentReplies) if (s_comments[replyId]) loadedReplies.push(replyId);
        return loadedReplies
    }, [s_comments, m_commentData]);

    const [s_submittingReply, setSubmittingReply] = useState('');
    const [s_replyMessage, setReplyMessage] = useState('');

    const m_addReply = useCallback(async () => {
        if (!s_replyMessage) return;
        if (s_submittingReply) return;
        setSubmittingReply(true);
        // maybe some day ...
        setSubmittingReply(false);
    }, [s_replyMessage, s_submittingReply]);

    const m_meatballsMenuItems = useMemo(() => {
        return m_imTheOwner ? [
            {label: 'edit', onClick: c_startEdit},
            {label: 'delete', onClick: c_requestDelete},
        ] : [

        ]
    }, [m_imTheOwner, c_startEdit, c_requestDelete]);

    return <>
        <CaseFileSingleCommentContainer>

            {s_submittingEdit || s_deleting ? <>
                <CaseFileSingleCommentActionInProgressLoading>
                    <LoadingIcon width={'20px'} height={'20px'} color={'black'}/>
                </CaseFileSingleCommentActionInProgressLoading>
            </> : <></>}

            {m_ownerUserData ? <>
                {s_editing ? <>
                    <LongTextInput
                        fontSize={'12px'}
                        value={s_editData.comment_text}
                        setValue={(v) => setEditData((e) => ({...e, comment_text: v}))}
                        height={'48px'}
                        width={'calc(100% - 16px)'}
                        color={'black'}
                        borderColor={'#999999'}
                        backgroundColor={'#e0e0e0'}
                        maxLength={500}
                    />
                    <CaseFileSingleCommentOptionsSection>
                        <button onClick={c_edit}>finish</button>
                        <button onClick={c_cancelEdit}>cancel</button>
                    </CaseFileSingleCommentOptionsSection>

                </> : s_deleteRequested ? <>

                    <CaseFileSingleCommentOptionsSection>
                        <button onClick={c_delete}>delete</button>
                        <button onClick={c_cancelDelete}>cancel</button>
                    </CaseFileSingleCommentOptionsSection>

                </> : <>
                    <CaseFileSingleCommentHeader>
                        <CaseFileSingleCommentHeaderProfilePictureContainer>
                            <ProfilePicture userId={m_ownerUserData.User_ID} size={'small'}/>
                        </CaseFileSingleCommentHeaderProfilePictureContainer>
                        <CaseFileSingleCommentHeaderNameContainer>
                            {`${m_ownerUserData.first_name} ${m_ownerUserData.last_name}`.trim()}
                        </CaseFileSingleCommentHeaderNameContainer>
                        <CaseFileSingleCommentMeatballsMenuButtonContainer>
                            <MeatballsMenu items={m_meatballsMenuItems}/>
                        </CaseFileSingleCommentMeatballsMenuButtonContainer>
                    </CaseFileSingleCommentHeader>
                    {props.displayAnnotatedText && m_commentData.marked_text && <>
                        <CaseFileSingleCommentAnnotatedText color={m_commentData.color}>"{m_commentData.marked_text}"</CaseFileSingleCommentAnnotatedText>
                    </>}
                    {m_textToDisplay ? <>
                        <CaseFileSingleCommentText>{m_textToDisplay}</CaseFileSingleCommentText>
                    </>:<>
                        {m_imTheOwner ? <>
                            <NoCommentsButton onClick={c_startEdit}>+ add a comment</NoCommentsButton>
                        </>:<>
                            <NoCommentsMessage>empty comment</NoCommentsMessage>
                        </>}
                    </>}
                    {m_isTextLong && <CaseFileSingleCommentToggleLongShortButton
                        onClick={() => setDisplayLong((l) => !l)}>
                        {s_displayLong ? 'show less' : 'show more'}
                    </CaseFileSingleCommentToggleLongShortButton>}
                </>}
                {!props.childOf && (m_commentData || {}).children && <>
                    {
                        <CaseFileSingleCommentRepliesContainer>
                            {m_loadedReplies.map((replyId) => <CaseFileSingleComment
                                key={replyId}
                                commentId={replyId}
                                childOf={props.commandId}
                            />)}
                            {((m_commentData || {}).children || []).length - (m_loadedReplies.length) && <>
                                <CaseFileSingleCommentShowHideRepliesButton>
                                    {s_loadingReplies ? <LoadingIcon
                                        width={'10px'}
                                        height={'10px'}
                                        color={'#999999'}
                                    /> : 'show more'}
                                </CaseFileSingleCommentShowHideRepliesButton>
                            </>}
                        </CaseFileSingleCommentRepliesContainer>
                    }
                    <CaseFileSingleCommentShowHideRepliesButton onClick={() => {
                        !s_showingReplies && c_loadReplies();
                        setShowingReplies((s) => !s);
                    }}>
                        {s_showingReplies ? 'hide replies' : 'show replies'}
                    </CaseFileSingleCommentShowHideRepliesButton>
                </>}
            </> : <>
                <LoadingIcon width={'20px'} height={'20px'}/>
            </>}
        </CaseFileSingleCommentContainer>
    </>
}
