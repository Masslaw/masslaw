import React, {useContext, useEffect, useState} from 'react';
import {UsersManager} from "../../../infrastructure/user_management/users_manager";
import {LoadingIcon} from "../../../shared/components/loading_icon/loading_icon";

import './css.css'
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";
import {ApplicationRoutes} from "../../../infrastructure/application_base/routing/application_routes";
import {faBook, faClock, faFileAlt, faPlus, faUserTie} from "@fortawesome/free-solid-svg-icons";
import {LoadingElement} from "../../../shared/components/loaded_element/loading_element";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {CasesManager} from "../../../infrastructure/cases_management/cases_manager";
import {unixTimeToDayDateString, unixTimeToPastTimeString} from "../../../shared/util/date_time_utiles";
import {CaseData} from "../../../infrastructure/cases_management/data_structures";
import {
    NavigationFunctionState
} from "../../../infrastructure/application_base/routing/application_global_routing";
import {
    ApplicationPage, ApplicationPageProps
} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {
    useGlobalState,
} from "../../../infrastructure/application_base/global_functionality/global_states";
import {access_level_display_names} from "../../../infrastructure/cases_management/cases_consts";


export const Dashboard: ApplicationPage = (props: ApplicationPageProps) => {

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    let [page_loaded, setPageLoaded] = useState(true);

    async function refreshUserData() {
        await UsersManager.getInstance().updateMyCachedUserData();
        setPageLoaded(true);
    }

    let [cases_list, setCasesList] = useState([] as CaseData[]);
    let [cases_list_loaded, setCasesListLoaded] = useState(false);

    async function loadCasesList() {
        setCasesListLoaded(false);
        let casesList = await CasesManager.getInstance().getMyCases() || [];
        casesList.sort((a: CaseData, b: CaseData) => parseInt((b.creation_time || '0').toString()) - parseInt((a.creation_time || '0').toString()))
        setCasesList(casesList);
        setCasesListLoaded(true);
    }

    useEffect(() => {
        (async () => {
            await refreshUserData();
            await loadCasesList();
        })().then();
    }, []);

    return (<>
            {page_loaded ? <>
                <div className={'dashboard-page-title page-title'}>Dashboard</div>
                <div className={'dashboard-my-cases-container'}>
                    <div className={'dashboard-my-cases-title'}>My Cases</div>
                    <div className={'dashboard-case-create-button-container'}>
                        <MasslawButton caption={'Create Case'}
                                       icon={faPlus}
                                       buttonType={MasslawButtonTypes.TEXTUAL}
                                       size={{w: 130, h: 35}}
                                       onClick={e => navigate_function(ApplicationRoutes.CASE_CREATE)}/>
                    </div>
                    <div className={'dashboard-my-cases-list-container'}>
                        <LoadingElement loadingElement={(cases_list.length === 0) ? <>
                            <div className={'dashboard-no-cases-text'}>
                                No cases yet...
                            </div>
                        </> : <>
                            <CasesList casesList={cases_list}/>
                        </>} loaded={cases_list_loaded}/>
                    </div>
                </div>
            </> : <>
                <LoadingIcon color={'var(--masslaw-dark-text-color)'}
                             width={100}
                             ballSize={20}/>
            </>}
        </>)
}

function CasesList(props: {
    casesList: CaseData[]
}) {

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    return (<>
            {
                props.casesList.sort(
                    (a: CaseData, b: CaseData) => parseInt((b.last_interaction || '0').toString()) - parseInt((a.last_interaction || '0').toString())
                ).map((caseData, num) => {
                    return (<>
                        <div
                            key={caseData.case_id}
                            style={{animationDelay: `${0.1 * num}s`}}
                            className={'application-dashboard-case-thumbnail-container clickable'}
                            onClick={e => {
                                navigate_function(ApplicationRoutes.CASE, {'caseId': caseData.case_id})
                            }}
                        >
                            <div className={'application-dashboard-case-thumbnail-title'}>
                                <span><FontAwesomeIcon icon={faBook} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                                <span>{` ${caseData.title}`}</span>
                            </div>
                            <div className={'application-dashboard-case-thumbnail-interaction'}>
                                <span><b>Last Modified:</b> {unixTimeToPastTimeString(parseInt((caseData.last_interaction || '0').toString()))}</span>
                                <span><FontAwesomeIcon icon={faClock} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                            </div>
                            <div className={'application-dashboard-case-thumbnail-creation'}>
                                <span><b>Created:</b> {unixTimeToDayDateString(parseInt((caseData.creation_time || '0').toString()))}</span>
                                <span><FontAwesomeIcon icon={faClock} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                            </div>
                            <div className={'application-dashboard-case-thumbnail-users'}>
                                <span><FontAwesomeIcon icon={faUserTie} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                                <span>{caseData.num_users} Participants</span>
                            </div>
                            <div className={'application-dashboard-case-thumbnail-files'}>
                                <span><FontAwesomeIcon icon={faFileAlt} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                                <span>{caseData.num_files} Files</span>
                            </div>
                            <div className={`application-dashboard-case-thumbnail-permission ${caseData.access_level}`}>
                                <span>{`${access_level_display_names[caseData.access_level]}`}</span>
                            </div>
                        </div>
                    </>)
                })
            }
        </>)
}