import styled from "styled-components";
import {TextInput} from "./textInput";
import {useCallback, useEffect, useMemo, useState} from "react";
import {model} from "../../model/model";
import {LoadingIcon} from "./loadingIcon";
import {UserPreviewData} from "./userPreviewData";

const UsersSearchContainer = styled.div`
    position: relative;
    width: ${({width}) => width || '100%'};
    margin: ${({margin}) => margin || '0'};
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
`

const ResultsSection = styled.div`
    position: relative;
    width: calc(100% - 16px);
    background: #505050;
    border-radius: 8px;
    padding: 8px;
    overflow: auto;
    margin-top: 8px;
    height: 256px;
`

const ResultItemContainer = styled.div`
    width: calc(100% - 4px);
    background: #303030;
    border-radius: 8px;
    cursor: pointer;
    margin: 2px;
    &:hover { background: #404040 }
`

const NoResultsMessage = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #808080;
    font-size: 12px;
`

export function UsersSearch(props) {

    const usersManager = model.services['usersManager'];

    const [s_searchString, setSearchString] = useState('');

    const [s_searchResults, setSearchResults] = useState([]);

    const [s_isCooldown, setIsCooldown] = useState(true);

    const [s_isSearching, setIsSearching] = useState(false);

    const c_search = useCallback(() => {
        setSearchResults([]);
        if (s_isCooldown) return;
        if (s_isSearching) return;
        setIsSearching(true);
        console.log("Searching for users...", s_searchString);
        usersManager.searchUsers(s_searchString.trim()).then(results => {
            setSearchResults(results);
            setIsSearching(false);
        })
    }, [s_searchString, s_isSearching, s_isCooldown]);

    const [s_searchTrigger, setSearchTrigger] = useState(false);

    useEffect(() => {
        if (!s_searchTrigger) return;
        setSearchTrigger(false);
        c_search();
    }, [s_searchTrigger]);

    let timeoutId = null;

    useEffect(() => (() => timeoutId && clearTimeout(timeoutId)), []);

    useEffect(() => {
        if (timeoutId) clearTimeout(timeoutId);
        setIsCooldown(true);
        timeoutId = setTimeout(() => {
            setIsCooldown(false);
            setSearchTrigger(true);
        }, 1500);
    }, [s_searchString]);

    const m_results = useMemo(() => {
        return s_searchResults
            .filter(uId => !(props.filterUsers || []).includes(uId))
            .map((userId, index) => <>
            <ResultItemContainer
                key={`searchresultitem-${userId}`}
                onClick={() => {
                    props.onUserSelected(userId)
                    if (s_searchResults.filter(uId => !(props.filterUsers || []).includes(uId)).length === 0)
                        setSearchString("");
                }}
            >
                <UserPreviewData key={`searchresultitemdata-${userId}`} userId={userId}/>
            </ResultItemContainer>
        </>)
    }, [s_searchResults, props.filterUsers, props.onUserSelected]);

    return <>
        <UsersSearchContainer>
            <TextInput
                type={'text'}
                value={s_searchString}
                setValue={setSearchString}
                placeholder={"Search for a user"}
                width={'calc(100% - 2px)'}
                height={'32px'}
            />
            {s_searchString.length > 2 ? <>
                <ResultsSection>
                    {s_isSearching || s_isCooldown ? <>
                        <LoadingIcon width={'20px'} height={'20px'}/>
                    </> : <>
                        {m_results.length ? m_results : <NoResultsMessage>Didn't find anything...</NoResultsMessage>}
                    </>}
                </ResultsSection>
            </> : <></>}
        </UsersSearchContainer>
    </>
}