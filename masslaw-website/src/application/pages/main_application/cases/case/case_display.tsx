import {Outlet, useParams} from "react-router-dom";
import {useEffect, useState} from "react";

import './css.css'
import {LoadingElement} from "../../../../shared/components/loaded_element/loading_element";
import {CasesManager} from "../../../../infrastructure/cases_management/cases_manager";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faFileAlt, faArrowLeft, faMagnifyingGlass, faStickyNote} from "@fortawesome/free-solid-svg-icons";
import {ApplicationRoutingManager} from "../../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../../infrastructure/routing/application_routes";


export function CaseDisplay() {

    const { caseId } = useParams();

    const [side_bar_open, setSideBarOpen] = useState(true);

    let cached_case_data = CasesManager.getInstance().getCachedCaseData(caseId || '');
    const [case_data , setCaseData] = useState(cached_case_data || {});

    useEffect(() => {
        (async () => {
            setCaseData(await CasesManager.getInstance().updateCaseData(caseId || ''));
        })().then();
    }, []);

    return (
        <>
            <LoadingElement loaded={case_data.title != null}
                            loadingElement={
                <>
                    <div className={'case-display-page'}>
                        <div className={`case-display-side-bar ${side_bar_open ? 'open' : 'closed'}`}>
                            <button className={'case-display-side-bar-close-button'}
                                    onClick={e => setSideBarOpen(!side_bar_open)}>
                                <FontAwesomeIcon icon={faArrowLeft} />
                            </button>
                            <div className={'case-display-side-bar-case-title'}>{(case_data as {[key:string]:string}).title}</div>
                            <div className={'case-display-side-bar-separator'}/>

                            <button className={'case-display-side-bar-button'}
                                    onClick={(e) => {ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.CASE_FILES, {'caseId': caseId || ''})}}>
                                <span className={'case-display-side-bar-button-icon'}>
                                    <FontAwesomeIcon icon={faFileAlt} />
                                </span>
                                <span className={'case-display-side-bar-button-caption'}>{'Case Files'}</span>
                            </button>
                            <button className={'case-display-side-bar-button'}>
                                <span className={'case-display-side-bar-button-icon'}>
                                    <FontAwesomeIcon icon={faMagnifyingGlass} />
                                </span>
                                <span className={'case-display-side-bar-button-caption'}>{'Search'}</span>
                            </button>
                            <button className={'case-display-side-bar-button'}>
                                <span className={'case-display-side-bar-button-icon'}>
                                    <FontAwesomeIcon icon={faStickyNote} />
                                </span>
                                <span className={'case-display-side-bar-button-caption'}>{'Sticky Notes'}</span>
                            </button>

                        </div>
                        <div className={'case-display-page-content'}>
                            <Outlet />
                        </div>
                    </div>
                </>
            } />

        </>
    )
}