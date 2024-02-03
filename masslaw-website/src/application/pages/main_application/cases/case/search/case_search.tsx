import React, {useCallback, useContext, useEffect, useState} from "react";

import "./css.css";
import {InputField} from "../../../../../shared/components/input_field/input_field";
import {LoadingButton} from "../../../../../shared/components/loading_button/loading_button";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {useParams} from "react-router-dom";
import {LoadingIcon} from "../../../../../shared/components/loading_icon/loading_icon";
import {MasslawButton, MasslawButtonTypes} from "../../../../../shared/components/masslaw_button/masslaw_button";
import {faArrowRight} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutes} from "../../../../../infrastructure/application_base/routing/application_routes";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../../infrastructure/application_base/routing/application_page_renderer";
import {
    NavigationFunctionState,
    QueryStringParamsState
} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {
    useGlobalState
} from "../../../../../infrastructure/application_base/global_functionality/global_states";

export interface searchResult {
    file_id: string,
    file_name: string,
    start_text: string,
    highlighted_text: string,
    end_text: string,
    query: string,
}

const RESULT_PRE_TAG = '<search_result>';
const RESULT_POST_TAG = '</search_result>';
const RESULT_PADDING = 150;


export const CaseSearch: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const {caseId} = useParams();

    const [searchText, setSearchText] = useState('');

    const [searching, setSearching] = useState(false);

    const [searchResults, setSearchResults] = useState([] as searchResult[])

    const [showNoResultsMessage, setShowNoResultsMessage] = useState(false);

    const submitSearch = useCallback(async () => {
        setQueryStringParams({'query': searchText});
    }, [searchText]);

    const performSearch = useCallback(async () => {
        if (searchText.length < 2) return;
        if (!caseId) return;
        setSearching(true);
        setShowNoResultsMessage(false);
        const results = await CasesManager.getInstance().search_text(
            caseId, searchText, undefined, RESULT_PADDING);
        let searchResults: searchResult[] = [];
        if (results.length == 0) {
            setShowNoResultsMessage(true);
        } else {
            for (let result of results) {
                for (let highlight of result.text_highlights) {

                    highlight = highlight.replace(new RegExp(RESULT_POST_TAG + "\\s+" + RESULT_PRE_TAG, "g"), " ");

                    let preTagIndices: number[] = [];
                    let postTagIndices: number[] = [];

                    let preTagMatch;
                    let preTagRegex = new RegExp(RESULT_PRE_TAG, 'g');
                    while ((preTagMatch = preTagRegex.exec(highlight)) !== null) {
                        preTagIndices.push(preTagMatch.index);
                    }

                    let postTagMatch;
                    let postTagRegex = new RegExp(RESULT_POST_TAG, 'g');
                    while ((postTagMatch = postTagRegex.exec(highlight)) !== null) {
                        postTagIndices.push(postTagMatch.index + RESULT_POST_TAG.length);
                    }

                    for (let i = 0; i < preTagIndices.length; i++) {
                        const startIndexOfHighlight = preTagIndices[i] + RESULT_PRE_TAG.length;
                        const endIndexOfHighlight = postTagIndices[i] - RESULT_POST_TAG.length;

                        const startText = highlight.substring(Math.max(preTagIndices[i] - 150, 0), preTagIndices[i]);
                        const highlightedText = highlight.substring(startIndexOfHighlight, endIndexOfHighlight);
                        const endText = highlight.substring(postTagIndices[i], Math.min(postTagIndices[i] + 150, highlight.length));

                        const RESULT_HIGHLIGHT_TAGGING_REGEX = new RegExp(`${RESULT_PRE_TAG}(.*?)${RESULT_POST_TAG}`, 'g');
                        const cleanStartText = startText.replace(RESULT_HIGHLIGHT_TAGGING_REGEX, "$1");
                        const cleanEndText = endText.replace(RESULT_HIGHLIGHT_TAGGING_REGEX, "$1");

                        searchResults.push({
                            file_id: result.file_id,
                            file_name: result.file_name,
                            start_text: cleanStartText,
                            highlighted_text: highlightedText,
                            end_text: cleanEndText,
                            query: searchText
                        });
                    }
                }
            }
        }
        setSearchResults(searchResults);
        setSearching(false);
    }, [searchText]);

    useEffect(() => {
        setSearchText(query_string_params['query'] || '');
        performSearch();
    }, [query_string_params]);

    return(<>
        <div className={'case-search-header'}>
            <div className={'case-search-page-title page-title'}>{`Search Case`}</div>
            <div className={'case-search-text-input-container'}>
                <InputField
                    value={searchText}
                    onChange={e => setSearchText(e.target.value)}
                    valid={searchText.length > 1 && 'valid' || ''}
                    locked={searching}

                />
            </div>
            <div className={'case-search-submit-search-button-container'}>
                <LoadingButton
                    clickable={searchText.length > 1}
                    onClick={() => submitSearch()}
                    loading={searching}
                    caption={'Search'}
                    size={{w: 100, h: 40}}
                />
            </div>
        </div>
        <div className={'case-search-results-container'}>
            {
                showNoResultsMessage ?
                    <>
                        <div className={'case-search-no-results-message'}>{'No Results Found'}</div>
                    </>
                    :
                    <>
                        {
                        searching ?
                            <LoadingIcon color={'#000000'} width={100}/>
                            :
                            <>
                                {
                                    searchResults.map((result, key) => {
                                        return <SearchResult
                                            result={result}
                                            key={key}
                                        />
                                    })
                                }
                            </>
                        }
                    </>

            }
        </div>
    </>)
}


function SearchResult(props: {
    result: searchResult,
}) {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [expanded, setExpanded] = useState(false);

    // We are using an array here just to keep track of the text parts, but it could be a single string
    let displayText = [props.result.start_text, props.result.highlighted_text, props.result.end_text];

    if (!expanded) {
        const charsBeforeHighlight = 30;
        displayText[0] = displayText[0].length > charsBeforeHighlight
            ? '...' + displayText[0].slice(-charsBeforeHighlight)
            : displayText[0];
    }

    return(
        <div
            className={`search-result-container clickable ${expanded ? 'expanded' : ''}`}
            onClick={() => setExpanded((e) => !e)}
        >
            <div className={'search-result-file-name'}>
                {props.result.file_name}
            </div>
            <div className={`search-result-highlighted-text ${expanded ? '' : 'not-expanded'}`}>
                <span>{displayText[0]}</span>
                <span style={{background: 'var(--aqua-soft)'}}>{displayText[1]}</span>
                <span>{displayText[2]}</span>
                {expanded && <span>{'...'}</span>}
            </div>
            {
                expanded &&
                <div className={'search-result-go-to-file-container'}>
                    <div className={'search-result-go-to-file-wrapper'}>
                        <MasslawButton
                            caption={'Go To File'}
                            icon={faArrowRight}
                            buttonType={MasslawButtonTypes.MAIN}
                            onClick={() => {
                                navigate_function(ApplicationRoutes.FILE_DISPLAY,
                                    {
                                        'caseId': caseId || '',
                                        'fileId': props.result.file_id
                                    },
                                    {
                                        'search': props.result.query
                                    }, {
                                        state: {
                                            search_result: props.result
                                        }
                                    }
                                )
                            }}
                        />
                    </div>
                </div>
            }
        </div>
    )
}
