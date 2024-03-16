import styled from "styled-components";
import {model} from "../../../../model/model";
import React, {useCallback, useEffect, useMemo} from "react";
import {VerticalGap} from "../../../components/bits-and-pieces/verticalGap";
import {TextInput} from "../../../components/textInput";
import {LongTextInput} from "../../../components/longTextInput";


const CreateCasePopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 512px;
    background-color: #1f1f1f;
    color: white;
    border-radius: 12px;
    z-index: 100;
`

const CreateCasePopupTitle = styled.h1`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 16px 32px 16px 32px;
`

const CreateCasePopupSubTitle = styled.h2`
    font-size: 14px;
    font-weight: 500;
    margin: 0 32px 16px 32px;
    color: #999999;
`

const CreateCaseInputWrapper = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    justify-content: center;
    z-index: 110;
`

const FinishCreateCaseButton = styled.button`
    position: relative;
    margin: 32px 32px 16px auto;
    background: ${({enabled}) => enabled ? "white" : "none"};
    width: 96px;
    height: 32px;
    border: 1px solid white;
    color: ${({enabled}) => enabled ? "black" : "white"};
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: .5px;
    pointer-events: ${({enabled}) => enabled ? "all" : "none"};
    
    &:hover {
        ${({enabled}) => enabled ? "filter: drop-shadow(0 0 5px white)" : ""}
    }
`

const ErrorMessage = styled.div`
    position: relative;
    width: 100%;
    margin: 16px 0;
    text-align: center;
    color: red;
`

export function CreateCasePopup(props) {

    const casesManager = model.services['casesManager'];

    const [s_caseName, setCaseName] = React.useState("");
    const [s_caseDescription, setCaseDescription] = React.useState("");

    const [s_errorMessage, setErrorMessage] = React.useState("");

    const m_canCreateCase = useMemo(() => {
        return (s_caseName.trim().length > 1) && (s_caseName.trim().length < 150) && (s_caseDescription.trim().length < 350);
    }, [s_caseName]);

    const c_createCase = useCallback(async () => {
        const caseData = {
            title: s_caseName.trim(),
            description: s_caseDescription.trim(),
        }
        const res = await casesManager.createCase(caseData);
        if (!res.getResponseSuccess()) {
            setErrorMessage("Could not create case.");
            return;
        }
        await casesManager.fetchCases();
        props.dismiss();
    }, [props.dismiss, s_caseName, s_caseDescription]);

    return <>
        <CreateCasePopupContainer>
            <CreateCasePopupTitle>Create A New Case</CreateCasePopupTitle>
            <CreateCasePopupSubTitle>A new case will be created at your will</CreateCasePopupSubTitle>
            <VerticalGap gap={"16px"}/>
            <CreateCaseInputWrapper>
                <TextInput
                    id={"casename"}
                    label={"Case Name"}
                    subLabel={"Give your case a name"}
                    value={s_caseName}
                    setValue={setCaseName}
                    type={"text"}
                    placeholder={"My New Case Name"}
                    width={'calc(512px - 64px)'}
                    height={'32px'}
                />
            </CreateCaseInputWrapper>
            <VerticalGap gap={"32px"}/>
            <CreateCaseInputWrapper>
                <LongTextInput
                    id={"casedescription"}
                    label={"Case Description"}
                    subLabel={"Describe your case in a few words"}
                    value={s_caseDescription}
                    setValue={setCaseDescription}
                    maxLength={350}
                    width={'calc(512px - 64px)'}
                    height={'64px'}
                />
            </CreateCaseInputWrapper>
            {s_errorMessage && <ErrorMessage>{s_errorMessage}</ErrorMessage>}
            <FinishCreateCaseButton onClick={() => c_createCase()} enabled={m_canCreateCase}>Create</FinishCreateCaseButton>
        </CreateCasePopupContainer>
    </>
}
