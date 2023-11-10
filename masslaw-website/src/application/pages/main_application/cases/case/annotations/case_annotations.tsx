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
import {CaseFileAnnotationData} from "../../../../../infrastructure/cases_management/data_structures";
import {
    CaseFileAnnotationItem
} from "../../../../../shared/components/case_file_annotation_item/case_file_annotation_item";

interface annotationsResult {
    file_id: string,
    file_name: string,
    start_text: string,
    highlighted_text: string,
    end_text: string,
    query: string,
}

const RESULT_PRE_TAG = '<annotations_result>';
const RESULT_POST_TAG = '</annotations_result>';
const RESULT_PADDING = 750;


export const CaseAnnotations: ApplicationPage = (props: ApplicationPageProps) => {

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);

    const {caseId} = useParams();

    const [case_annotations, setCaseAnnotations] = useState(null as CaseFileAnnotationData[] | null);

    useEffect(() => {
        (async () => {
            setCaseAnnotations(null);
            setCaseAnnotations(await CasesManager.getInstance().getCaseAnnotations(caseId || ''));
        })()
    }, [caseId]);

    return(<>
        <div className={'case-annotations-header'}>
            <div className={'case-annotations-page-title page-title'}>{`Case Markings`}</div>
        </div>
        <div className={'case-annotations-list-container'}>
            {
                (() => {
                    if (case_annotations == null)
                        return <LoadingIcon color={'#000000'}/>
                    if (case_annotations.length == 0)
                        return <p style={{textAlign: 'center', marginTop: '30px'}}>No annotations in this case yet.</p>
                    return case_annotations.sort(
                        (a, b) => b.last_modified - a.last_modified
                    ).map(annotation => (
                        <CaseFileAnnotationItem
                            key={annotation.annotation_id}
                            annotationData={annotation}
                            onClick={() => {
                                navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                    'caseId': annotation.case_id,
                                    'fileId': annotation.file_id,
                                }, {
                                    ['scroll_to']: `${annotation.from_char}`
                                });
                            }}
                        />
                    ))
                })()
            }
        </div>
    </>)
}


function AnnotationsResult(props: {
    result: annotationsResult,
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
            className={`annotations-result-container clickable ${expanded ? 'expanded' : ''}`}
            onClick={() => setExpanded((e) => !e)}
        >
            <div className={'annotations-result-file-name'}>
                {props.result.file_name}
            </div>
            <div className={`annotations-result-highlighted-text ${expanded ? '' : 'not-expanded'}`}>
                <span>{displayText[0]}</span>
                <span style={{background: 'var(--aqua-soft)'}}>{displayText[1]}</span>
                <span>{displayText[2]}</span>
                {expanded && <span>{'...'}</span>}
            </div>
            {
                expanded &&
                <div className={'annotations-result-go-to-file-container'}>
                    <div className={'annotations-result-go-to-file-wrapper'}>
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
                                        'annotations': props.result.query
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
