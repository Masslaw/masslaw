import styled from "styled-components";
import {useCaseData} from "../../../../../hooks/useCaseData";
import {useParams} from "react-router-dom";
import {TextInput} from "../../../../../components/textInput";
import React, {useCallback, useEffect, useMemo, useState} from "react";
import {VerticalGap} from "../../../../../components/verticalGap";
import {LongTextInput} from "../../../../../components/longTextInput";
import {ItemSelectionInput} from "../../../../../components/ItemSelectionInput";
import {CASE_LANGUAGES} from "../../../../../../config/caseLanguages";
import {model} from "../../../../../../model/model";
import {LoadingIcon} from "../../../../../components/loadingIcon";

const PageContainer = styled.div`
    width: 100%;
    height: 100%;
    background: #202020;
`

const LayoutContainer = styled.div`
    width: 512px;
    max-width: 100%;
    height: calc(100% - 64px);
    overflow: auto;
    padding: 32px;
`

const PageTitle = styled.div`
    font-size: 24px;
    color: white;
    font-weight: bold;
`;

const Label = styled.div`
    font-size: 16px;
    color: white;
`;

const SubLabel = styled.div`
    font-size: 14px;
    color: #808080;
`;

const SubmitButton = styled.button`
    position: relative;
    float: right;
    font-size: 14px;
    height: 32px;
    width: 128px;
    border-radius: 8px;
    border: ${({enabled}) => enabled === true ? '1px solid #ffffff' : '1px solid #505050'};
    color: ${({enabled}) => enabled === true ? '#ffffff' : '#505050'};
    cursor: pointer;
    background: none;
    &:hover { background: ${({enabled}) => enabled === true ? '#505050' : 'none'} }
`

export function CaseSettings(props) {

    const {casesManager} = model.services;

    const {caseId} = useParams();

    const s_caseData = useCaseData();

    const [s_caseDataState, setCaseDataState] = useState({});

    useEffect(() => {
        setCaseDataState(s_caseData);
    }, [s_caseData]);

    const convertLanguageCodesToLanguageItems = (languageCodes) => {
        const languageItems = [];
        for (const languageCode of languageCodes) {
            for (const languageItem in CASE_LANGUAGES) {
                if (CASE_LANGUAGES[languageItem] === languageCode) {
                    languageItems.push(languageItem);
                    break;
                }
            }
        }
        return languageItems;
    }

    const convertLanguageItemsToLanguageCodes = (languageItems) => {
        const languageCodes = [];
        for (const languageItem of languageItems) {
            languageCodes.push(CASE_LANGUAGES[languageItem]);
        }
        return languageCodes;
    }

    const [s_submitting, setSubmitting] = useState(false);

    const m_canChange = useMemo(() => {
        if (s_caseDataState.title !== s_caseData.title) return true;
        if (s_caseDataState.description !== s_caseData.description) return true;
        if ((s_caseDataState.languages || []).sort().join(',') !== (s_caseDataState.languages || []).sort().join(',')) return true;
        return false;
    }, [s_caseDataState, s_caseData]);

    const c_submitChanges = useCallback(async () => {
        if (s_submitting) return;
        if (!m_canChange) return;
        setSubmitting(true);
        await casesManager.postCaseData(s_caseDataState);
        setSubmitting(false);
    }, [s_caseDataState, m_canChange]);

    return <>
        <PageContainer>
            <LayoutContainer>
                <PageTitle>Case Settings</PageTitle>
                <VerticalGap gap={"32px"}/>
                <Label>{`Case Title ${s_caseDataState.title !== s_caseData.title ? '*' : ''}`}</Label>
                <VerticalGap gap={"12px"}/>
                <SubLabel>The main title the of the case</SubLabel>
                <VerticalGap gap={"12px"}/>
                <TextInput
                    id={"casename"}
                    value={s_caseDataState.title}
                    setValue={(v) => setCaseDataState({...s_caseDataState, title: v})}
                    type={"text"}
                    placeholder={"Input A Name"}
                    width={'100%'}
                    height={'32px'}
                />
                <VerticalGap gap={"32px"}/>
                <Label>{`Case Description ${s_caseDataState.description !== s_caseData.description ? '*' : ''}`}</Label>
                <VerticalGap gap={"12px"}/>
                <SubLabel>A short description of this case</SubLabel>
                <VerticalGap gap={"12px"}/>
                <LongTextInput
                    id={"casedescription"}
                    value={s_caseDataState.description}
                    setValue={(v) => setCaseDataState({...s_caseDataState, description: v})}
                    maxLength={350}
                    width={'100%'}
                    height={'64px'}
                />
                <VerticalGap gap={"32px"}/>
                <Label>Case Languages</Label>
                <VerticalGap gap={"12px"}/>
                <SubLabel>The list of languages in which the text in this case's files is written</SubLabel>
                <VerticalGap gap={"12px"}/>
                <ItemSelectionInput
                    selectedItems={convertLanguageCodesToLanguageItems(s_caseDataState.languages || [])}
                    setSelectedItems={(v) => setCaseDataState({...s_caseDataState, languages: convertLanguageItemsToLanguageCodes(v)})}
                    optionsList={Object.keys(CASE_LANGUAGES)}
                    containerWidth={'100%'}
                    containerMargin={'0'}
                />
                <VerticalGap gap={"32px"}/>
                <SubmitButton onClick={c_submitChanges} enabled={m_canChange}>
                    {s_submitting ? <>
                        <LoadingIcon width={'16px'} height={'16px'}/>
                    </> : <>
                        Submit Changes
                    </>}
                </SubmitButton>
            </LayoutContainer>
        </PageContainer>
    </>
}