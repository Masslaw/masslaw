import React, {useContext, useEffect, useState} from "react";
import {UsersManager} from "../../../infrastructure/user_management/users_manager";
import {ApplicationRoutes} from "../../../infrastructure/application_base/routing/application_routes";
import {UserPhoto} from "../../../shared/components/user_photo/user_photo";

import './css.css'
import {InputField} from "../../../shared/components/input_field/input_field";
import {MasslawButton, MasslawButtonTypes} from "../../../shared/components/masslaw_button/masslaw_button";
import {LoadingButton} from "../../../shared/components/loading_button/loading_button";
import {LoadingElement} from "../../../shared/components/loaded_element/loading_element";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../infrastructure/application_base/routing/application_page_renderer";
import {NavigationFunctionState} from "../../../infrastructure/application_base/routing/application_global_routing";
import {useGlobalState} from "../../../infrastructure/application_base/global_functionality/global_states";


export const Profile: ApplicationPage = (props: ApplicationPageProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const [changing_in_progress, setChangingInProgress] = useState(false);

    let cachedUserData = UsersManager.getInstance().getMyCachedUserData();
    const [user_data, setUserData] = useState(cachedUserData || {});

    const [first_name_valid, setFirstNameValid] = useState('');
    const [last_name_valid, setLastNameValid] = useState('');

    async function refreshUserData() {
        await UsersManager.getInstance().updateMyCachedUserData();
        cachedUserData = UsersManager.getInstance().getMyCachedUserData();
        setUserData(cachedUserData);
        onFirstNameChange(cachedUserData.first_name || '');
        onLastNameChange(cachedUserData.last_name || '');
    }

    useEffect(() => {
        refreshUserData().then();
    }, []);

    async function onUserDataChangeSubmit() {
        setChangingInProgress(true);
        await UsersManager.getInstance().setMyUserData(user_data);
        await refreshUserData();
        setChangingInProgress(false);
    }

    function onFirstNameChange(newValue: string) {
        setUserData((prevUserData) => ({
            ...prevUserData,
            first_name: newValue,
        }));

        cachedUserData = UsersManager.getInstance().getMyCachedUserData();
        if (newValue === cachedUserData.first_name) {
            setFirstNameValid('');
            return;
        }
        setFirstNameValid((/^[a-zA-Z]{2,}$/).test(newValue) ? 'valid' : 'invalid');
    }

    function onLastNameChange(newValue: string) {
        setUserData((prevUserData) => ({
            ...prevUserData,
            last_name: newValue,
        }));

        cachedUserData = UsersManager.getInstance().getMyCachedUserData();
        if (newValue === cachedUserData.last_name) {
            setLastNameValid('');
            return;
        }
        setLastNameValid((/^[a-zA-Z]{2,}$/).test(newValue) ? 'valid' : 'invalid');
    }

    let submitClickable =
        ((first_name_valid !== 'invalid' &&
            last_name_valid !== 'invalid') && (
            first_name_valid === 'valid' ||
            last_name_valid === 'valid'));

    return (
        <>
            <LoadingElement loaded={user_data.email != null}
                            loadingElement={
                <>
                    <div className={'profile-page-container'}>
                        <form className={'masslawyer-profile-form-container'}>
                            <div style={{height: '20px'}}/>
                            <div className={'masslawyer-profile-form-section-title'}>Personal Information</div>
                            <div className={'masslaw-profile-input-field-container'}>
                                <InputField value={user_data.first_name}
                                            label={'First Name'}
                                            valid={first_name_valid}
                                            onChange={e => {onFirstNameChange(e.target.value)}} />
                            </div>
                            <div className={'masslaw-profile-input-field-container'}>
                                <InputField value={user_data.last_name}
                                            label={'Last Name'}
                                            valid={last_name_valid}
                                            onChange={e => {onLastNameChange(e.target.value)}} />
                            </div>
                            <div className={'masslawyer-profile-form-section-title'}>Contact Information</div>
                            <div className={'masslaw-profile-input-field-container'}>
                                <InputField value={user_data.email}
                                            label={'Email'}
                                            locked={true}
                                            onChange={e => {}} />
                            </div>
                            <div className={'masslawyer-profile-form-section-title'}>Authentication</div>
                            <div className={'masslawyer-profile-form-button-container'} >
                                <MasslawButton caption={`Change Password`}
                                               buttonType={MasslawButtonTypes.TEXTUAL}
                                               size={{w: 140, h: 30}}
                                               onClick={e => {navigate_function(ApplicationRoutes.PASSWORD)}} />
                            </div>
                            <div className={'masslaw-profile-submit-button-container'}>
                                <LoadingButton caption={'Apply Changes'}
                                               clickable={submitClickable}
                                               loading={changing_in_progress}
                                               size={{w: 140, h: 30}}
                                               onClick={e => {onUserDataChangeSubmit().then(r => {})}}/>
                            </div>
                        </form>
                        <div className={'masslawyer-profile-user-photo-container'}>
                            <UserPhoto size={120} id={'masslawyer-profile-user-photo'}/>
                            <div className={'masslawyer-profile-upload-image-button-container'}>
                                <MasslawButton caption={'Change Image'}
                                               size={{w: 120, h: 30}}
                                               onClick={e => {}}/>
                            </div>
                        </div>
                    </div>

                </>
            } />
        </>
    )
}