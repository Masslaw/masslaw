import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {useParams} from "react-router-dom";
import {model} from "../../model/model";
import {constructUrl} from "../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../config/applicaitonRoutes";
import {LoadingIcon} from "./loadingIcon";

const NoConversationsMessage = styled.div`
    width: 100%;
    font-size: 14px;
    color: #808080;
    text-align: center;
`

export function CaseConversationsList(props) {
    const {caseConversationsManager} = model.services;

    const [s_loadingList, setLoadingList] = useState(false);

    useEffect(() => {
        if (s_loadingList) return;
        setLoadingList(true);
        caseConversationsManager.fetchCaseConversations(model.cases.currentOpen.id).then(() => setLoadingList(false));
    }, []);

    const [s_conversationsData, setConversationsData] = useModelValueAsReactState('$.cases.currentOpen.conversations.data')

    const m_conversationsList = useMemo(() => {
        if (!s_conversationsData || Object.keys(s_conversationsData).length === 0) return <NoConversationsMessage>No Conversations</NoConversationsMessage>
        const conversations = [];
        for (const conversationId in s_conversationsData) conversations.push({id: conversationId, ...s_conversationsData[conversationId]})
        conversations.sort((a, b) => (parseInt(b.last_message) || 0) - (parseInt(a.last_message) || 0))
        return conversations.map((conversaion, index) => <ConversationItem conversationData={conversaion} key={index}/>);
    }, [s_conversationsData]);

    return <>
        {s_loadingList ? <></> : m_conversationsList}
    </>
}

const ConversationItemContainer = styled.button`
    text-align: left;
    width: calc(100% - 16px);
    margin: 0 8px;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    color: #ffffff;
    border: none;
    background: ${({selected}) => selected ? '#252525' : 'none'};
    &:hover { background: #303030; }
    span {
        padding: 0 2px;
        margin-right: 8px;
        border-radius: 2px;
        background: white;
    }
`

function ConversationItem(props) {
    const {caseId, conversationId} = useParams();

    return <>
        <ConversationItemContainer
            selected={conversationId === props.conversationData.id}
            onClick={() => model.application.navigate(constructUrl(
                ApplicationRoutes.CASE_CONVERSATION,
                {caseId: caseId, conversationId: props.conversationData.id}
            ))}
        >
            <span />
            {props.conversationData.name}
        </ConversationItemContainer>
    </>
}
