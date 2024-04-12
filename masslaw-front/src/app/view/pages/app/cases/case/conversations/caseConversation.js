import styled from "styled-components";
import {useParams} from "react-router-dom";
import {useCallback, useEffect, useMemo, useState} from "react";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {model} from "../../../../../../model/model";
import {SVG_PATHS} from "../../../../../config/svgPaths";
import {LongTextInput} from "../../../../../components/longTextInput";
import ReactMarkdown from "react-markdown";
import {unixTimeToDateTimeString} from "../../../../../../controller/functionality/time-utils/dateTimeUtils";
import {ProfilePicture} from "../../../../../components/profilePicture";


const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
    align-items: center;
`

const ConversationContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column-reverse;
    width: 640px;
    padding: 0 16px;
    max-width: calc(100% - 32px);
    height: 100%;
    overflow: hidden;
`

const ConversationInputContainer = styled.div`
    display: flex;
    flex-direction: row;
    align-items: end;
    justify-content: center;
    width: 100%;
    background: #303030;
    padding: 16px 0;
    height: max-content;
    flex-basis: max-content;
    flex-shrink: 0;
    flex-grow: 0;
`

const ConversationMessageSubmitButton = styled.button`
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    width: 36px;
    height: 36px;
    border-radius: 8px;
    border: none;
    margin-left: auto;
    &:hover { filter: drop-shadow(0 0 4px white); }
    svg {
        fill: black;
        width: 80%;
        height: 80%;
    }
`

const ConversationMessagesContainer = styled.div`
    display: block;
    width: 640px;
    height: 100%;
    max-width: 100%;
    overflow: hidden;
    flex-basis: 0;
    flex-shrink: 0;
    flex-grow: 1;
    overflow-y: auto;
    
`

const ConversationMessagesSeparator = styled.div`
    position: relative;
    width: 100%;
    height: 1px;
    background: #303030;
    background: linear-gradient(90deg, #303030 0%, #505050 20%, #505050 80%, #303030 100%);
    margin: 0;
`

export function CaseConversation(props) {
    const {caseId, conversationId} = useParams();

    const {caseConversationsManager} = model.services;

    const [s_conversationsContent, setConversationsContent] = useModelValueAsReactState('cases.currentOpen.conversations.content');

    const [s_loadingConversation, setLoadingConversation] = useState(true);

    useEffect(() => {
        setLoadingConversation(true);
        caseConversationsManager.fetchCaseConversationContent(conversationId, caseId).then(() => setLoadingConversation(false));
    }, [caseId, conversationId]);

    const m_conversationMessages = useMemo(() => {
        const conversationContent = s_conversationsContent[conversationId] || {};
        const conversationMessages = conversationContent.messages || []
        return conversationMessages;
    }, [s_conversationsContent, conversationId]);

    const m_conversationMessageElements = useMemo(() => {
        if (!m_conversationMessages || !m_conversationMessages.length) return <></>;
        return m_conversationMessages.map((message, index) => <>
            {index > 0 ? <ConversationMessagesSeparator /> : <></>}
            <ConversationMessage key={index} message={message}/>
        </>);
    }, [m_conversationMessages]);

    const [s_submittingMessage, setSubmittingMessage] = useState(false);

    const [s_messageInput, setMessageInput] = useState('');

    const c_sendMessage = useCallback(async () => {
        if (s_submittingMessage) return;
        if (s_messageInput.trim().length < 1) return;
        setSubmittingMessage(true);
        setMessageInput('');
        await caseConversationsManager.sendConversationMessage(s_messageInput, conversationId, caseId);
        setSubmittingMessage(false);
    }, [caseId, conversationId, s_submittingMessage, s_messageInput]);

    return <>
        <PageContainer>
            {s_loadingConversation ? <>
                <LoadingIcon width={'20px'} height={'20px'} />
            </> : <>
                <ConversationContainer>
                    <ConversationInputContainer>
                        <LongTextInput
                            value={s_messageInput}
                            setValue={setMessageInput}
                            height={'48px'}
                            width={'calc(100% - 80px)'}
                            color={'white'}
                            borderColor={'white'}
                            backgroundColor={'none'}
                            hideValidIndicator={true}
                            fontSize={'16px'}
                            padding={'16px'}
                        />
                        <ConversationMessageSubmitButton onClick={c_sendMessage}>
                            {s_submittingMessage ? <LoadingIcon width={'20px'} height={'20px'} color={'black'}/> : <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.send}/></svg>}
                        </ConversationMessageSubmitButton>
                    </ConversationInputContainer>
                    <ConversationMessagesContainer>
                        {m_conversationMessageElements}
                    </ConversationMessagesContainer>
                </ConversationContainer>
            </>}
        </PageContainer>
    </>
}

const ConversationMessageContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: max-content;
    padding: 8px 0 ;
    background: #303030;
`

const ConversationMessageHeaderContainer = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
`

const ConversationMessageImageContainer = styled.div`
    width: 32px;
    height: 32px;
    margin: 8px 8px 8px 0;
    border-radius: 8px;
    overflow: hidden;
    flex-basis: 32px;
    flex-shrink: 0;
    flex-grow: 0;
    border: 1px solid #808080;
    background: black;
`

const ConversationMessageNameContainer = styled.div`
    margin: 8px;
    color: white;
    font-size: 16px;
    font-weight: bold;
`

const ConversationMessageContentContainer = styled.div`
    margin: 8px 0;
    color: white;
    font-size: 16px;
    width: 100%;
`

const ConversationMessageMassbotImageSvg = styled.svg`
    width: 80%;
    height: 80%;
    margin: 10%;
    fill: white;
`

function ConversationMessage(props) {
    return <>
        <ConversationMessageContainer>
            <ConversationMessageHeaderContainer>
                <ConversationMessageImageContainer>
                    {props.message.role === 'user' ? <>
                        <ProfilePicture userId={model.users.mine.data.User_ID} size={'small'} />
                    </> : <>
                        <ConversationMessageMassbotImageSvg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.logo}/></ConversationMessageMassbotImageSvg>
                    </>}
                </ConversationMessageImageContainer>
                <ConversationMessageNameContainer>
                    {props.message.role === 'user' ? 'You' : props.message.role === 'assistant' ? 'MassBot' : ''}
                </ConversationMessageNameContainer>
            </ConversationMessageHeaderContainer>
            <ConversationMessageContentContainer>{
                <ReactMarkdown>{props.message.content}</ReactMarkdown>
            }</ConversationMessageContentContainer>
        </ConversationMessageContainer>
    </>
}
