import {Outlet, useParams} from "react-router-dom";
import React, {useContext, useEffect, useState} from "react";

import './css.css'
import {LoadingElement} from "../../../../shared/components/loaded_element/loading_element";
import {CasesManager} from "../../../../infrastructure/cases_management/cases_manager";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faFileAlt,
    faArrowLeft,
    faMagnifyingGlass,
    faStickyNote,
    faHighlighter, faUserTie, faBook, faProjectDiagram, faUser, faRulerHorizontal, faCalendarAlt, faNetworkWired
} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutes} from "../../../../infrastructure/application_base/routing/application_routes";
import {CaseData} from "../../../../infrastructure/cases_management/data_structures";
import {
    NavigationFunctionState, RouteMatchState
} from "../../../../infrastructure/application_base/routing/application_global_routing";
import {LoadingIcon} from "../../../../shared/components/loading_icon/loading_icon";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../infrastructure/application_base/routing/application_page_renderer";
import {useGlobalState} from "../../../../infrastructure/application_base/global_functionality/global_states";


export const CaseDisplay: ApplicationPage = (props: ApplicationPageProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const { caseId } = useParams();

    const [side_bar_open, setSideBarOpen] = useState(true);

    const [case_data , setCaseData] = useState({} as CaseData|undefined);

    useEffect(() => {
        (async () => {
            setCaseData(await CasesManager.getInstance().getCaseData(caseId || ''));
        })().then();
    }, [caseId]);

    const [route_match_function, setRoutMatchFunction] = useGlobalState(RouteMatchState);

    useEffect(() => {
        if (route_match_function(ApplicationRoutes.CASE)) {
            navigate_function(ApplicationRoutes.CASE_MAIN, {'caseId': caseId || ''});
        }
    }, [navigate_function, route_match_function]);

    return (
        <>
            <LoadingElement
                loaded={!!case_data}
                loadingElement={
                    <>
                        <div className={'case-display-page'}>
                            <div className={`case-display-side-bar ${side_bar_open ? 'open' : 'closed'}`}>
                                <button className={'case-display-side-bar-close-button'}
                                        onClick={e => setSideBarOpen(!side_bar_open)}>
                                    <FontAwesomeIcon icon={faArrowLeft}/>
                                </button>
                                <div
                                    className={'case-display-side-bar-case-title clickable'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_MAIN, {'caseId': caseId || ''})
                                    }}
                                >
                                    {case_data?.title ? case_data?.title : <LoadingIcon/>}
                                </div>

                                <div className={'case-display-side-bar-separator'}/>

                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_DASHBOARD, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faNetworkWired}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Dashboard'}</span>
                                </button>

                                <div className={'case-display-side-bar-separator'}/>

                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_FILES, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faFileAlt}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Files'}</span>
                                </button>
                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_SEARCH, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faMagnifyingGlass}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Search'}</span>
                                </button>
                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_ANNOTATIONS, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faHighlighter}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Markings'}</span>
                                </button>
                                <div className={'case-display-side-bar-separator'}/>

                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_KNOWLEDGE, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faProjectDiagram}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Knowledge'}</span>
                                </button>
                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_SUBJECTS, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faUser}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Subjects'}</span>
                                </button>
                                <button
                                    className={'case-display-side-bar-button'}
                                    onClick={(e) => {
                                        navigate_function(ApplicationRoutes.CASE_TIMELINE, {'caseId': caseId || ''})
                                    }}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faCalendarAlt}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Timeline'}</span>
                                </button>
                                <div className={'case-display-side-bar-separator'}/>

                                <button
                                    className={'case-display-side-bar-button'}
                                    style={{opacity: 0.5}}
                                    // onClick={(e) => {navigate_function(ApplicationRoutes.CASE_USERS, {'caseId': caseId || ''})}}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faUserTie}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Participants'}</span>
                                </button>
                                <button
                                    className={'case-display-side-bar-button'}
                                    style={{opacity: 0.5}}
                                    // onClick={(e) => {navigate_function(ApplicationRoutes.CASE_USERS, {'caseId': caseId || ''})}}
                                >
                                    <span className={'case-display-side-bar-button-icon'}>
                                        <FontAwesomeIcon icon={faBook}/>
                                    </span>
                                    <span className={'case-display-side-bar-button-caption'}>{'Documentation'}</span>
                                </button>
                            </div>
                            <div className={'case-display-page-content'}>
                                <Outlet/>
                            </div>
                        </div>
                    </>
                }
            />
        </>
    )
}