import {useCallback, useEffect, useMemo, useState} from "react";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import styled from "styled-components";
import {TextInput} from "../../../../../components/textInput";
import {LoadingIcon} from "../../../../../components/loadingIcon";
import {model} from "../../../../../../model/model";
import {VerticalGap} from "../../../../../components/bits-and-pieces/verticalGap";
import {wait} from "@testing-library/user-event/dist/utils";

const SearchTextInputContainer = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    margin: 16px;
    width: calc(100% - 32px);
`

const SearchButton = styled.button`
    position: relative;
    margin-left: 16px;
    width: 96px;
    height: 34px;
    background: ${({enabled}) => enabled ? "white" : "none"};
    color: ${({enabled}) => enabled ? "black" : "white"};
    border: 1px solid white;
    border-radius: 8px;
    pointer-events: ${({enabled}) => enabled ? "all" : "none"};
    font-size: 14px;
    cursor: pointer;
    &:hover {
        ${({enabled}) => enabled ? "filter: drop-shadow(0 0 5px white)" : ""}
    }
}
`

const SearchResultsStickySection = styled.div`
    position: sticky;
    top: 0;
    display: flex;
    flex-direction: row;
    padding: 16px;
    width: calc(100% - 32px);
    background: black;
`

const SearchResultsContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 100%;
`

const NoSearchResults = styled.div`
    width: 100%;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #999999;
`

export function CaseTextSearch(props) {

    const caseSearchesManager = model.services['caseSearchesManager'];

    const [s_caseSearchData, setCaseSearchData] = useModelValueAsReactState('$.cases.currentOpen.search');
    const [s_targetSearchResultIndex, setTargetSearchResultIndex] = useModelValueAsReactState('$.cases.currentOpen.search.targetResultIndex');

    const [s_searchParams, setSearchParams] = useModelValueAsReactState('$.application.searchParams');

    const [s_searching, setSearching] = useState(false)
    const [s_searchTextInput, setSearchTextInput] = useState('');
    const [s_searchText, setSearchText] = useState('');

    const m_canSearch = useMemo(() => {
        if (s_searching) return false;
        if (!s_searchTextInput) return false;
        const trimmed = s_searchTextInput.trim();
        if (trimmed.length < 3) return false;
        return true;
    }, [s_searching, s_searchTextInput]);

    const c_performSearch = useCallback(async (inputText) => {
        if (!m_canSearch) return;
        inputText = inputText.trim();
        setSearching(true);
        setSearchParams( p => ({...p, s: inputText}));
        setTargetSearchResultIndex(-1);
        await wait(1000);
        await caseSearchesManager.searchFilesText(inputText);
        setSearchText(inputText);
        setSearching(false);
    }, [s_searching, m_canSearch]);

    useEffect(() => {
        const searchText = (s_searchParams.s || '').trim();
        setSearchTextInput(searchText);
        setSearchText(searchText);
        if (searchText.length > 2) c_performSearch(searchText);
    }, [s_searchParams]);

    const m_resultsItems = useMemo(() => {
        if (!s_searchText) return [];
        const resultItems = s_caseSearchData.results[s_searchText] || [];
        return resultItems
            .sort((a,b)=>(b.score - a.score))
            .map((result, idx) => (props.files ? props.files.includes(result.file_id) : true) ? <>
                <SearchResult
                    key={idx}
                    resultIndex={idx}
                    result={result}
                    onClick={() => {
                        setTargetSearchResultIndex(-1);
                        requestAnimationFrame(() => setTargetSearchResultIndex(idx));
                        props.onResultClicked && props.onResultClicked(s_searchText, result);
                    }}
                />
            </> : null)
            .filter(x => !!x);
    }, [s_searchText, s_caseSearchData, props.files]);

    return <>
        <SearchTextInputContainer>
            <TextInput
                id={'searchTextInput'}
                type="text"
                value={s_searchTextInput}
                setValue={setSearchTextInput}
                width={'calc(100% - 112px)'}
                height={'32px'}
                placeholder={'What would you like to find?'}
                onEnter={() => c_performSearch(s_searchTextInput)}
                options={s_caseSearchData.history}
            />
            <SearchButton
                enabled={(s_searchTextInput || '').trim().length > 2}
                onClick={() => c_performSearch(s_searchTextInput)}
            >
                {s_searching ? <LoadingIcon height={'20px'} color={'black'}/> : "Search"}
            </SearchButton>
        </SearchTextInputContainer>
        {m_resultsItems && m_resultsItems.length > 0 ? <>
            <SearchResultsStickySection>
                Search Results <span style={{marginLeft: '8px', color: '#999999'}}>({m_resultsItems.length})</span>
            </SearchResultsStickySection>
            <SearchResultsContainer>
                {m_resultsItems}
            </SearchResultsContainer>
        </> : <>
            <NoSearchResults> {s_searching ? <LoadingIcon height={'20px'} color={'white'}/> : "No search results so far..."}</NoSearchResults>
        </>}
    </>
}

const SearchResultContainer = styled.div`
    display: block;
    width: calc(100% - 32px - 32px);
    margin: 4px 16px;
    padding: 16px;
    border-radius: 8px;
    background: #404040;
    overflow-x: hidden;
    cursor: pointer;
    transition: background 0.2s;
    ${({istarget}) => istarget ? 'outline: 1px solid white' : ''};
    &:hover { 
        background: #505050; 
        transition: none;
    }
`

const SearchResultFileName = styled.div`
    font-size: 11px;
    font-weight: bold;
    color: #bbbbbb;
`

const SearchResultScore = styled.div`
    font-size: 11px;
    font-weight: bold;
    color: #999999;
`

const SearchResultTextPreview = styled.div`
    display: block;
    font-size: 14px;
    color: white;
    max-width: 100%;
    width: 100%;
    overflow: hidden;
`

const SearchResultHighlight = styled.span`
    background: rgba(255, 242, 0, 0.5);
    border-radius: 4px;
    margin: 0 2px;
    padding: 0 4px;
    min-width: 0;
`

const SearchResultPreHighlight = styled.span`
    
`

const SearchResultPostHighlight = styled.span`
    
`

function SearchResult(props) {

    const [s_targetSearchResultIndex, setTargetSearchResultIndex] = useModelValueAsReactState('$.cases.currentOpen.search.targetResultIndex');

    return <>
        <SearchResultContainer istarget={s_targetSearchResultIndex === props.resultIndex} onClick={props.onClick}>
            <SearchResultFileName>{props.result.file_name}</SearchResultFileName>
            <VerticalGap gap={'4px'}/>
            <SearchResultScore>Score: {props.result.score}</SearchResultScore>
            <VerticalGap gap={'4px'}/>
            <SearchResultTextPreview>
                <SearchResultPreHighlight>...{props.result.start_text}</SearchResultPreHighlight>
                <SearchResultHighlight>{props.result.highlighted_text}</SearchResultHighlight>
                <SearchResultPostHighlight>{props.result.end_text}...</SearchResultPostHighlight>
            </SearchResultTextPreview>
        </SearchResultContainer>
    </>
}
