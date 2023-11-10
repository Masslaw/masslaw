import {useParams} from "react-router-dom";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../../infrastructure/application_base/routing/application_page_renderer";

import './css.css'
import React, {useEffect, useState} from "react";
import {CaseData} from "../../../../../infrastructure/cases_management/data_structures";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import {LoadingIcon} from "../../../../../shared/components/loading_icon/loading_icon";
import {unixTimeToDateTimeString, unixTimeToDayDateString} from "../../../../../shared/util/date_time_utiles";
import {ParagraphEditor} from "../../../../../shared/components/pragraph_editor/paragraph_editor";
import {
    access_level_display_names,
    CaseAccessLevels
} from "../../../../../infrastructure/cases_management/cases_consts";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faClock, faFile, faUserTie} from "@fortawesome/free-solid-svg-icons";
import {UserPhoto} from "../../../../../shared/components/user_photo/user_photo";
import {UsersManager} from "../../../../../infrastructure/user_management/users_manager";


export const CaseMain: ApplicationPage = (props: ApplicationPageProps) => {

    const { caseId } = useParams();

    const [case_data, setCaseData] = useState(null as CaseData | null);

    const [can_edit, setCanEdit] = useState(false);

    const [display_quantities, setDisplayQuantities] = useState({
        num_users: 0,
        num_files: 0,
    });

    useEffect(() => {
        UsersManager.getInstance().updateMyCachedUserData();
    }, []);

    useEffect(() => {
        (async () => {
            setCaseData(null);
            setCaseData(await CasesManager.getInstance().getCaseData(caseId || ''))
        })()
    }, [caseId])

    useEffect(() => {
        setDisplayQuantities({
            num_users: 0,
            num_files: 0,
        });

        if (case_data == null) return;

        let start: number | null = null;
        const duration = 2500;

        const animate = (timestamp: number) => {
            if (!start) start = timestamp;
            const progress = timestamp - start;
            const percentage = Math.min(progress / duration, 1);
            const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3); // Ease-out cubic function

            const easedPercentage = easeOutCubic(percentage);

            const num_users = Math.round(case_data.num_users * easedPercentage);
            const num_files = Math.round(case_data.num_files * easedPercentage);

            setDisplayQuantities({ num_users, num_files });

            if (progress < duration) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);

    }, [case_data]);

    useEffect(() =>{
        setCanEdit(case_data != null && [
            CaseAccessLevels.owner,
            CaseAccessLevels.manager
        ].includes(case_data.access_level as CaseAccessLevels));
    }, [case_data]);

    return (
        <>
            {
                case_data != null &&
                <div className={'case-main-display-container'}>
                    {
                        can_edit &&
                        <>
                            <b>Title:</b>
                            <ParagraphEditor
                                text={case_data.title}
                                editable={can_edit}
                                fontSize={30}
                                maxCharacters={100}
                                size={{h: 35}}
                                onFinish={async (value) => {
                                    let new_data = {...case_data}
                                    new_data.title = value
                                    await CasesManager.getInstance().setCaseData(case_data.case_id, new_data);
                                    window.location.reload();
                                }}
                            />
                        </>
                        ||
                        <p className={'case-main-case-title'}>
                            {case_data.title}
                        </p>
                    }
                    <div style={{height: '20px'}}/>
                    <div>
                        <b>Description:</b>
                        <span>{
                            <ParagraphEditor
                                text={case_data.description}
                                editable={can_edit}
                                maxCharacters={1000}
                                onFinish={async (value) => {
                                    let new_data = {...case_data}
                                    new_data.description = value
                                    await CasesManager.getInstance().setCaseData(case_data.case_id, new_data);
                                    window.location.reload();
                                }}
                            />
                        }</span>
                    </div>
                    <div style={{height: '20px'}}/>
                    <div className={'case-main-data-items-container'} >
                        <div className={'case-main-data-item'} style={{animationDelay: '0.1s'}} >
                            <div className={'case-main-data-item-icon'}>
                                <FontAwesomeIcon icon={faClock}/>
                            </div>
                            <div className={'case-main-data-item-title'}>
                                Created At
                            </div>
                            <div className={'case-main-data-item-value'}>
                                {unixTimeToDayDateString(case_data.creation_time)}
                            </div>
                        </div>
                        <div className={'case-main-data-item'} style={{animationDelay: '0.2s'}} >
                            <div className={'case-main-data-item-icon'}>
                                <FontAwesomeIcon icon={faUserTie}/>
                            </div>
                            <div className={'case-main-data-item-title'}>
                                Participants
                            </div>
                            <div className={'case-main-data-item-value'}>
                                {display_quantities.num_users || 0}
                            </div>
                        </div>
                        <div className={'case-main-data-item'} style={{animationDelay: '0.3s'}} >
                            <div className={'case-main-data-item-icon'}>
                                <FontAwesomeIcon icon={faFile}/>
                            </div>
                            <div className={'case-main-data-item-title'}>
                                Files
                            </div>
                            <div className={'case-main-data-item-value'}>
                                {display_quantities.num_files || 0}
                            </div>
                        </div>
                    </div>
                    <div style={{height: '20px'}}/>
                    <div>
                        <b>Case Participants:</b>
                        <div className={'case-main-participants-list'}>
                            <div className={'case-main-participants-list-item'}>
                                <div className={'case-main-participants-list-item-image'}>
                                    <UserPhoto size={70} id={'masslawyer-profile-user-photo'}/>
                                </div>
                                <div className={'case-main-participants-list-item-name'}>
                                    {
                                        UsersManager.getInstance().getMyCachedUserData().first_name + ' ' +
                                        UsersManager.getInstance().getMyCachedUserData().last_name
                                    }
                                </div>
                                <div className={`case-main-participants-list-item-role ${case_data.access_level}`}>
                                    <span>{`${access_level_display_names[case_data.access_level]}`}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                ||
                <LoadingIcon color={'#000000'}/>
            }
        </>
    )
}