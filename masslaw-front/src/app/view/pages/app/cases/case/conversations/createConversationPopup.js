import styled from "styled-components";
import {VerticalGap} from "../../../../../components/verticalGap";
import {TextInput} from "../../../../../components/textInput";
import {useCallback, useState} from "react";
import {useParams} from "react-router-dom";
import {model} from "../../../../../../model/model";
import {constructUrl} from "../../../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../../../config/applicaitonRoutes";
import {LoadingIcon} from "../../../../../components/loadingIcon";


const CreateConversationPopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 384px;
    background-color: #202020;
    color: white;
    border-radius: 12px;
    z-index: 100;
    padding: 32px;
`

const CreateConversationPopupTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 0;
`

const CreateConversationPopupSubTitle = styled.div`
    font-size: 14px;
    color: #808080;
    margin: 0;
`

const CreateConversationFinishButton = styled.button`
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 128px;
    height: 32px;
    flex-basis: 32px;
    flex-shrink: 0;
    margin-left: auto;
    margin-top: auto;
    background: ${({clickable}) => clickable ? 'white' : 'none'};
    color: ${({clickable}) => clickable ? 'black' : '#808080'};
    border: 1px solid white;
    border-radius: 8px;
    font-size: 16px;
    cursor: ${({clickable}) => clickable ? 'pointer' : 'default'};
    pointer-events: ${({clickable}) => clickable ? 'auto' : 'none'};
    transition: background 0.2s;

    &:hover {
        filter: ${({clickable}) => clickable ? 'drop-shadow(0 0 4px white)' : 'none'};
    }
`

export function CreateConversationPopup(props) {

    const {caseConversationsManager} = model.services;

    const [s_conversationName, setConversationName] = useState('');

    const [s_creatingConversation, setCreatingConversation] = useState(false);

    const c_createConversation = useCallback(async () => {
        if (s_creatingConversation) return;
        if (s_conversationName.trim().length < 1) return;
        setCreatingConversation(true);
        const new_conversation_id = await caseConversationsManager.createNewConversation(s_conversationName.trim(), props.caseId);
        setCreatingConversation(false);
        model.application.navigate(constructUrl(ApplicationRoutes.CASE_CONVERSATION, {caseId: props.caseId, conversationId: new_conversation_id}));
        props.dismiss();
    }, [props.dismiss, props.caseId, s_conversationName, s_creatingConversation]);

    return <>
        <CreateConversationPopupContainer>
            <CreateConversationPopupTitle>Create A New MassBot Conversation</CreateConversationPopupTitle>
            <VerticalGap gap={'8px'}/>
            <CreateConversationPopupSubTitle>Create a new conversation with Masslaw's AI chat bot</CreateConversationPopupSubTitle>
            <VerticalGap gap={'32px'}/>
            <TextInput
                type={'text'}
                label={"Conversation Name"}
                subLabel={"Give your conversation a meaningful name"}
                placeholder={"My New Conversation"}
                value={s_conversationName}
                setValue={setConversationName}
                width={'100%'}
                height={'32px'}
            />
            <VerticalGap gap={'32px'}/>
            <CreateConversationFinishButton
                clickable={s_conversationName.trim().length > 1}
                onClick={c_createConversation}
            >
                {s_creatingConversation ? <LoadingIcon width={'16px'} height={'16px'} color={'black'}/> : 'Create'}
            </CreateConversationFinishButton>
        </CreateConversationPopupContainer>
    </>
}
