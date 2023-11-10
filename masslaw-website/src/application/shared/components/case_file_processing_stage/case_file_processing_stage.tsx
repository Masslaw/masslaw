import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck, faCheckCircle, faExclamationCircle, faEye, faEyeSlash} from "@fortawesome/free-solid-svg-icons";

import "./css.css"
import {CaseFileData} from "../../../infrastructure/cases_management/data_structures";
import {get_file_current_ongoing_processing_stage} from "../../../infrastructure/cases_management/case_data_utils";
import {case_file_processing_stage_display_names} from "../../../infrastructure/cases_management/cases_consts";
import {LoadingIcon} from "../loading_icon/loading_icon";

export function CaseFileProcessingStage(props: { fileData: CaseFileData }) {
    const currentStage = get_file_current_ongoing_processing_stage(props.fileData);
    if (currentStage) return (<div
            className={'case-file-processing-stage'}
        >
            <span>{case_file_processing_stage_display_names[currentStage]}</span><span/>
            <span>
                                               <LoadingIcon
                                                   width={35}
                                                   ballSize={10}
                                               />
                                           </span>
        </div>)
    else return (<div
            className={'case-file-processing-completed'}
        >
            <span>Ready</span>
            <span><FontAwesomeIcon
                icon={faCheck}/></span>
        </div>)
}