import React, {ChangeEvent, useContext, useState} from "react";
import {InputField} from "../../../../shared/components/input_field/input_field";
import {LoadingButton} from "../../../../shared/components/loading_button/loading_button";
import {CasesManager} from "../../../../infrastructure/cases_management/cases_manager";
import {ApplicationRoutes} from "../../../../infrastructure/application_base/routing/application_routes";
import {CaseData} from "../../../../infrastructure/cases_management/data_structures";
import {
    NavigationFunctionState
} from "../../../../infrastructure/application_base/routing/application_global_routing";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../infrastructure/application_base/routing/application_page_renderer";
import {
    useGlobalState,
} from "../../../../infrastructure/application_base/global_functionality/global_states";


export const CreateCase: ApplicationPage = (props: ApplicationPageProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const [case_title, setCaseTitle] = useState('');
    const [case_title_valid, setCaseTitleValid] = useState('');
    const [case_description, setCaseDescription] = useState('');
    const [case_description_valid, setCaseDescriptionValid] = useState('');

    function onTitleChange(e: ChangeEvent<HTMLInputElement>) {
        let raw_name = e.target.value;
        let formatted_name : string = raw_name.replace(/\b\w/g, match => match.toUpperCase());
        setCaseTitle(formatted_name);
        setCaseTitleValid(formatted_name.length > 2 ? 'valid' : 'invalid');
    }

    function onDescriptionChange(e: ChangeEvent<HTMLInputElement>) {
        let description = e.target.value;
        setCaseDescription(description);
        setCaseDescriptionValid((description.length > 2 && description.length < 200) ? 'valid' : 'invalid');
    }

    const [submit_button_loading, submitButtonLoading] = useState(false);
    const [submit_button_message, submitButtonMessage] = useState('');

    async function onSubmit() {
        submitButtonLoading(true);
        let case_id = await CasesManager.getInstance().createACase({
            title: case_title,
            description: case_description,
        } as CaseData);
        if (case_id != null) {
            navigate_function(ApplicationRoutes.CASE, {'caseId': case_id})
        }
        submitButtonLoading(false);
    }

    return (
        <>
            <div style={{
                width: '500px',
                left: '50%',
                margin: '20px'
            }}>
                <h2>Create Case</h2>
                <InputField value={case_title}
                            onChange={e => onTitleChange(e)}
                            label={'Title'}
                            valid={case_title_valid}
                />
                <InputField value={case_description}
                            onChange={e => onDescriptionChange(e)}
                            valid={case_description_valid}
                            label={'Description'}
                            isParagraph={true}
                />
                <LoadingButton clickable={(
                    case_title_valid === 'valid' &&
                    case_description_valid === 'valid')}
                               caption={'Create'}
                               loading={submit_button_loading}
                               onClick={e => onSubmit()} />
            </div>
        </>
    )
}