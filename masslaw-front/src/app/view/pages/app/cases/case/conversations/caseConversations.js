import styled from "styled-components";
import {model} from "../../../../../../model/model";
import {Outlet, useParams} from "react-router-dom";
import {useEffect, useMemo} from "react";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {ApplicationRoutes} from "../../../../../../config/applicaitonRoutes";
import {constructUrl} from "../../../../../../controller/functionality/navigation/urlConstruction";
import {VerticalGap} from "../../../../../components/verticalGap";
import {pushPopup} from "../../../../../global-view/globalLayer/_global-layer-components/popups";
import {CreateConversationPopup} from "./createConversationPopup";

const PageContainer = styled.div`
    display: flex;
    flex-direction: row-reverse;
    width: 100%;
    height: 100%;
    overflow: hidden;
`

const ConversationsListContainer = styled.div`
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 255px;
    background: #202020;
    flex-basis: 255px;
    border-left: 1px solid #808080;
    flex-shrink: 0;
    flex-grow: 0;
`

const ConversationContainer = styled.div`
    width: 100%;
    height: 100%;
    background: #303030;
    flex-basis: 100%;
    flex-shrink: 1;
    flex-grow: 1;
`

const NoConversationsMessage = styled.div`
    width: 100%;
    font-size: 14px;
    color: #808080;
    text-align: center;
`

const CreateConversationButton = styled.button`
    width: calc(100% - 16px - 2px);
    margin: 0 8px;
    padding: 8px;
    border-radius: 8px;
    cursor: pointer;
    color: #ffffff;
    background: none;
    border: 1px solid white;
    &:hover { background: white; color: black; }
`

export function CaseConversations(props) {
    const {caseId, conversationId} = useParams();

    model.application.pages.currentPage.name = "CaseConversations";

    const {caseConversationsManager} = model.services;

    const [s_loadingList, setLoadingList] = useModelValueAsReactState('$.cases.currentOpen.conversations.loadingList')

    useEffect(() => {
        setLoadingList(true);
        caseConversationsManager.fetchCaseConversations(caseId).then(() => setLoadingList(false));
    }, []);

    const [s_conversationsData, setConversationsData] = useModelValueAsReactState('$.cases.currentOpen.conversations.data')

    const m_conversationsList = useMemo(() => {
        if (!s_conversationsData || Object.keys(s_conversationsData).length === 0) return <NoConversationsMessage>No Conversations</NoConversationsMessage>
        const conversations = [];
        for (const conversationId in s_conversationsData) conversations.push({id: conversationId, ...s_conversationsData[conversationId]})
        conversations.sort((a, b) => (parseInt(b.last_message) || 0) - (parseInt(a.last_message) || 0))
        return conversations.map((conversaion, index) => <ConversationItem conversationData={conversaion} key={index}/>);
    }, [s_conversationsData])

    return <>
        <PageContainer>
            {s_loadingList ? <>
                <LoadingIcon width={'20px'} height={'20px'}/>
            </> : <>
                <ConversationsListContainer>
                    <VerticalGap gap={'16px'}/>
                    <CreateConversationButton onClick={() => pushPopup({component: CreateConversationPopup, componentProps: {caseId: caseId}})}>
                        Create A New Conversation
                    </CreateConversationButton>
                    <VerticalGap gap={'16px'}/>
                    {m_conversationsList}
                </ConversationsListContainer>
                <ConversationContainer>
                    {conversationId ? <Outlet/> : <NoConversationContent />}
                </ConversationContainer>
            </>}
        </PageContainer>
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
    background: ${({selected}) => selected ? '#404040' : 'none'};
    &:hover { background: #505050; }
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
            {props.conversationData.name}
        </ConversationItemContainer>
    </>
}

const NoConversationContentContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    font-size: 14px;
    color: #808080;
`

const NoConversationPromptContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 224px;
    overflow: hidden;
    background: none;
    border: none;
    padding: 16px;
`

const NoConversationPromptSection1 = styled.div`
    width: 100%;
    font-size: 16px;
    overflow: hidden;
    text-align: center;
    color: #c0c0c0;
`

const NoConversationPromptSection2 = styled.div`
    width: 100%;
    font-size: 14px;
    overflow: hidden;
    color: white;
    text-align: center;
    text-decoration: underline;
`

const NoConversationPromptSection3 = styled.div`
    width: 100%;
    font-size: 12px;
    font-weight: bold;
    overflow: hidden;
    color: #808080;
    text-align: center;
`

const NoConversationPromptCreateConversationButton = styled.button`
    font-size: 14px;
    font-weight: bold;
    overflow: hidden;
    background: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    height: 32px;
    width: 100%;
    &:hover { filter: drop-shadow(0 0 5px white); }
`

function NoConversationContent(props) {
    return <>
        <NoConversationContentContainer>
            <NoConversationPromptContainer>
                <NoConversationPromptSection1>
                    No conversation selected.
                </NoConversationPromptSection1>
                <VerticalGap gap={'32px'}/>
                <NoConversationPromptSection2>
                    Select a conversation from the list.
                </NoConversationPromptSection2>
                <VerticalGap gap={'16px'}/>
                <NoConversationPromptSection3>
                    OR
                </NoConversationPromptSection3>
                <VerticalGap gap={'16px'}/>
                <NoConversationPromptCreateConversationButton onClick={() => pushPopup({component: CreateConversationPopup})}>
                    Create A New Conversation
                </NoConversationPromptCreateConversationButton>
            </NoConversationPromptContainer>
        </NoConversationContentContainer>
    </>
}
