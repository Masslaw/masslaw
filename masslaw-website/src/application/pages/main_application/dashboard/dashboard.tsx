import React, {useEffect, useState} from 'react';
import {UsersManager} from "../../../infrastructure/user_management/users_manager";
import LoadingIcon from "../../../shared/components/loading_icon/loading_icon";

import './css.css'
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";
import {ApplicationRoutes} from "../../../infrastructure/routing/application_routes";
import {ApplicationRoutingManager} from "../../../infrastructure/routing/application_routing_manager";
import {faBook, faClock, faFileAlt, faPlus, faUserTie} from "@fortawesome/free-solid-svg-icons";
import {LoadingElement} from "../../../shared/components/loaded_element/loading_element";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {CasesManager} from "../../../infrastructure/cases_management/cases_manager";

export function Dashboard() {

    let [page_loaded, setPageLoaded] = useState(true);

    async function refreshUserData() {
        await UsersManager.getInstance().updateMyCachedUserData();
        setPageLoaded(true);
    }

    let [cases_list, setCasesList] = useState([]);
    let [cases_list_loaded, setCasesListLoaded] = useState(false);

    async function loadCasesList() {
        setCasesListLoaded(false);
        let casesList = await CasesManager.getInstance().getMyCases() || [];
        casesList.sort((a: { creationTime: any; }, b: { creationTime: any; }) => parseInt((a.creationTime || '0').toString()) > parseInt((b.creationTime || '0').toString()))
        setCasesList(casesList);
        setCasesListLoaded(true);
    }

    useEffect(() => {
        (async () => {
            await refreshUserData();
            await loadCasesList();
        })().then();
    }, []);

    return (
        <>
            {page_loaded ?
                <>
                    <div className={'dashboard-page-title'}>Dashboard</div>
                    <div className={'dashboard-my-cases-container'}>
                        <div className={'dashboard-my-cases-title'}>My Cases</div>
                        <div className={'dashboard-case-create-button-container'}>
                            <MasslawButton caption={'Create Case'}
                                           icon={faPlus}
                                           buttonType={MasslawButtonTypes.TEXTUAL}
                                           size={{w: 130, h: 35}}
                                           onClick={e => ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.CASE_CREATE)}/>
                        </div>
                        <div className={'dashboard-my-cases-list-container'}>
                            <LoadingElement loadingElement={
                                (cases_list.length === 0) ?
                                    <>
                                        <div className={'dashboard-no-cases-text'}>
                                            No cases yet...
                                        </div>
                                    </> :
                                    <>
                                        <CasesList casesList={cases_list} />
                                    </>
                            } loaded={cases_list_loaded}/>
                        </div>
                    </div>
                </> :
                <>
                    <LoadingIcon color={'var(--masslaw-dark-text-color)'}
                                 width={100}
                                 ballSize={20}/>
                </>
            }
        </>
    )
}

function CasesList(props: {
    casesList: any[]}) {

    return (
        <>
            {
                props.casesList.map((item, id) => (
                    <CaseThumbnail key={id}
                                   caseId={item.case_id}
                                   caseTitle={item.title || 'No title'}
                                   caseDescription={item.description || 'No description'}
                                   lastInteraction={item.last_interaction}
                                   creationTime={item.creation_time}
                                   numUsers={item.num_users}
                                   numFiles={item.num_files}
                                   accessLevel={item.access_level}
                    />
                ))
            }
        </>
    )
}

function CaseThumbnail(props: {
    caseId: string,
    caseTitle: string,
    caseDescription: string,
    lastInteraction?: string | number,
    creationTime?: string | number,
    numUsers: string | number,
    numFiles: string | number,
    accessLevel: string}){
    return (
        <>
            <div className={'application-dashboard-case-thumbnail-container clickable'}
                 onClick={e => {ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.CASE, {'caseId': props.caseId})}}>
                <div className={'application-dashboard-case-thumbnail-title'}>
                    <span><FontAwesomeIcon icon={faBook} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                    <span>{` ${props.caseTitle}`}</span>
                </div>
                <div className={'application-dashboard-case-thumbnail-interaction'}>
                    <span>{`last modified: ${unixTimeToDateTimeString(parseInt((props.lastInteraction || '0').toString()))}`}</span>
                    <span><FontAwesomeIcon icon={faClock} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                </div>
                <div className={'application-dashboard-case-thumbnail-creation'}>
                    <span>{`created: ${unixTimeToDateTimeString(parseInt((props.creationTime || '0').toString()))}`}</span>
                    <span><FontAwesomeIcon icon={faClock} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                </div>
                <div className={'application-dashboard-case-thumbnail-users'}>
                    <span><FontAwesomeIcon icon={faUserTie} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                    <span>{`${props.numUsers} Users`}</span>
                </div>
                <div className={'application-dashboard-case-thumbnail-files'}>
                    <span><FontAwesomeIcon icon={faFileAlt} className={`masslaw-button-icon`}></FontAwesomeIcon></span>
                    <span>{`${props.numFiles} Files`}</span>
                </div>
                <div className={`application-dashboard-case-thumbnail-permission ${props.accessLevel}`}>
                    <span>{`${props.accessLevel}`}</span>
                </div>
            </div>
        </>
    )
}

function unixTimeToDateTimeString(unixTime: number): string {
    if (unixTime < 10) return 'Unknown'
    const date = new Date(unixTime * 1000); // convert from seconds to milliseconds
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear().toString();
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}