import styled from "styled-components";
import {model} from "../../../../model/model";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import {VerticalGap} from "../../../components/verticalGap";
import {TextInput} from "../../../components/textInput";
import {LongTextInput} from "../../../components/longTextInput";
import {ItemSelectionInput} from "../../../components/ItemSelectionInput";
import {CASE_LANGUAGES} from "../../../../config/caseLanguages";


const CreateCasePopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 512px;
    background-color: #303030;
    color: white;
    border-radius: 12px;
    z-index: 100;
    padding: 32px;
`

const CreateCasePopupTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
`

const CreateCasePopupSubTitle = styled.div`
    font-size: 14px;
    font-weight: 500;
    color: #808080;
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
    margin-left: auto;
    margin-top: auto;
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
    const [s_selectedLanguages, setSelectedLanguages] = useState([]);

    const [s_errorMessage, setErrorMessage] = React.useState("");

    const m_canCreateCase = useMemo(() => {
        return (s_caseName.trim().length > 1) &&
            (s_caseName.trim().length < 150) &&
            (s_caseDescription.trim().length < 350) &&
            (s_selectedLanguages.length > 0);
    }, [s_caseName, s_caseDescription, s_selectedLanguages]);

    const c_createCase = useCallback(async () => {
        const caseData = {
            title: s_caseName.trim(),
            description: s_caseDescription.trim(),
            languages: s_selectedLanguages.map(language => CASE_LANGUAGES[language]),
        }
        console.log(caseData);
        const res = await casesManager.createCase(caseData);
        if (!res.getResponseSuccess()) {
            setErrorMessage("Could not create case.");
            return;
        }
        await casesManager.fetchCases();
        props.dismiss();
    }, [props.dismiss, s_caseName, s_caseDescription, s_selectedLanguages]);

    return <>
        <CreateCasePopupContainer>
            <CreateCasePopupTitle>Create A New Case</CreateCasePopupTitle>
            <VerticalGap gap={'8px'} />
            <CreateCasePopupSubTitle>Start your next project from scratch</CreateCasePopupSubTitle>
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
                    width={'512px'}
                    height={'32px'}
                />
            </CreateCaseInputWrapper>
            <VerticalGap gap={"16px"}/>
            <CreateCaseInputWrapper>
                <LongTextInput
                    id={"casedescription"}
                    label={"Case Description"}
                    subLabel={"Describe your case in a few words"}
                    value={s_caseDescription}
                    setValue={setCaseDescription}
                    maxLength={350}
                    width={'512px'}
                    height={'64px'}
                />
            </CreateCaseInputWrapper>
            <VerticalGap gap={"16px"}/>
            <ItemSelectionInput
                label={'Languages'}
                subLabel={'Select the languages in which the text of your case\'s files is written'}
                selectedItems={s_selectedLanguages}
                setSelectedItems={setSelectedLanguages}
                optionsList={Object.keys(CASE_LANGUAGES)}
                containerWidth={'100%'}
                containerMargin={'0'}
            />
            {s_errorMessage && <>
                <VerticalGap gap={"16px"}/>
                <ErrorMessage>{s_errorMessage}</ErrorMessage>
            </>}
            <VerticalGap gap={"32px"}/>
            <FinishCreateCaseButton onClick={() => c_createCase()} enabled={m_canCreateCase}>Create</FinishCreateCaseButton>
        </CreateCasePopupContainer>
    </>
}
