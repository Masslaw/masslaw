import styled from "styled-components";
import {useParams} from "react-router-dom";
import {useCallback, useEffect, useMemo, useRef, useState} from "react";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {model} from "../../../../../../model/model";
import {SVG_PATHS} from "../../../../../config/svgPaths";
import {LongTextInput} from "../../../../../components/longTextInput";
import ReactMarkdown from "react-markdown";
import {ProfilePicture} from "../../../../../components/profilePicture";
import {Icon} from "../../../../../components/icon";


const PageContainer = styled.div`
    position: relative;
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
    background: #202020;
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
    &::-webkit-scrollbar { display: none; }
`

const ConversationMessagesSeparator = styled.div`
    position: relative;
    width: 100%;
    height: 1px;
    background: #202020;
    background: linear-gradient(90deg, #202020 0%, #505050 20%, #505050 80%, #202020 100%);
    margin: 0;
`

export function CaseConversation(props) {
    const {caseId, conversationId} = useParams();

    const r_conversationRef = useRef(null);

    const {caseConversationsManager} = model.services;

    const [s_conversationsContent, setConversationsContent] = useModelValueAsReactState('cases.currentOpen.conversations.content');

    const [s_loadingConversation, setLoadingConversation] = useState(true);

    const c_scrollConversationToBottom = useCallback(() => {
        setTimeout(() => {
            if (!r_conversationRef.current) return;
            r_conversationRef.current.scrollTo({
                top: r_conversationRef.current.scrollHeight,
                behavior: "smooth"
            });
        }, 500);
    }, [r_conversationRef.current]);

    useEffect(() => {
        setLoadingConversation(true);
        caseConversationsManager.fetchCaseConversationContent(conversationId, caseId).then(() => {
            c_scrollConversationToBottom();
            setLoadingConversation(false);
        });
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
        const promise = caseConversationsManager.sendConversationMessage(s_messageInput, conversationId, caseId);
        const conversationMessages = model.cases.currentOpen.conversations.content[conversationId].messages || [];
        const newTemporaryMessage = {role: 'user', content: s_messageInput};
        const newTemporaryAssistantMessage = {role: 'assistant', content: '[[LOADING]]'};
        model.cases.currentOpen.conversations.content[conversationId].messages = [...conversationMessages, newTemporaryMessage, newTemporaryAssistantMessage];
        c_scrollConversationToBottom();
        await promise;
        c_scrollConversationToBottom();
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
                            width={'calc(100% - 70px)'}
                            color={'white'}
                            borderColor={'#505050'}
                            backgroundColor={'none'}
                            hideValidIndicator={true}
                            fontSize={'16px'}
                            padding={'16px'}
                        />
                        <ConversationMessageSubmitButton onClick={c_sendMessage}>
                            {s_submittingMessage ? <LoadingIcon width={'20px'} height={'20px'} color={'black'}/> : <Icon>{SVG_PATHS.send}</Icon>}
                        </ConversationMessageSubmitButton>
                    </ConversationInputContainer>
                    <ConversationMessagesContainer ref={r_conversationRef}>
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
    background: #202020;
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
    border: 1px solid #505050;
    background: black;
`

const ConversationMessageNameContainer = styled.div`
    margin: 8px;
    color: white;
    font-size: 16px;
    font-weight: bold;
`

const ConversationMessageContentContainer = styled.div`
    position: relative;
    margin: 8px 0;
    color: white;
    font-size: 16px;
    width: 100%;
    line-height: 24px;
    letter-spacing: 0.5px;
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
                        <ConversationMessageMassbotImageSvg viewBox={'0 0 1 1'}><path d={SVG_PATHS.logo}/></ConversationMessageMassbotImageSvg>
                    </>}
                </ConversationMessageImageContainer>
                <ConversationMessageNameContainer>
                    {props.message.role === 'user' ? 'You' : props.message.role === 'assistant' ? 'MassBot' : ''}
                </ConversationMessageNameContainer>
            </ConversationMessageHeaderContainer>
            <ConversationMessageContentContainer>
                {props.message.role === 'assistant' && props.message.content === '[[LOADING]]' ? <>
                    <LoadingIcon width={'20px'} height={'20px'} />
                </> : <>
                    <ReactMarkdown>{props.message.content}</ReactMarkdown>
                </>}
            </ConversationMessageContentContainer>
        </ConversationMessageContainer>
    </>
}
