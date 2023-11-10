import {useParams} from "react-router-dom";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import React, {useEffect, useRef, useState} from "react";
import {MasslawButton, MasslawButtonTypes} from "../../../../../shared/components/masslaw_button/masslaw_button";
import {faBook, faClock, faFileAlt, faPlus, faUserTie} from "@fortawesome/free-solid-svg-icons";

import './css.css'
import {MasslawApiCallData, MasslawApiCalls} from "../../../../../infrastructure/server_communication/api_config";
import {ApiManager} from "../../../../../infrastructure/server_communication/api_client";
import {ApplicationRoutingManager} from "../../../../../infrastructure/routing/application_routing_manager";
import {ApplicationRoutes} from "../../../../../infrastructure/routing/application_routes";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export function CaseFiles() {

    const { caseId } = useParams();

    const file_input_ref = useRef<HTMLInputElement>(null);

    let [case_files_data, setCaseFilesData] = useState(CasesManager.getInstance().getCachedCaseFiles(caseId || ''))


    let uploadFiles: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        if (e.target.files == null) return;
        if (caseId == null) return;
        Array.from(e.target.files).forEach((file) => {
            CasesManager.getInstance().uploadFile(caseId, file, () => {}).then();
        });
        e.target.value = "";
    }

    let getCaseFiles = async () => {
        setCaseFilesData(await CasesManager.getInstance().updateCaseFiles(caseId || ''));
    }

    useEffect(() => {
        (async () => {
            await getCaseFiles();
        })().then();
    }, []);

    return (
        <>
            <input ref={file_input_ref}
                   type={'file'}
                   style={{position: 'absolute', transform: 'scale(0)'}}
                   onChange={e => {uploadFiles(e)} }
                   multiple/>
            <div className={'case-files-list-header'}>
                <div className={'case-files-list-header-upload-button-container'}>
                    <MasslawButton caption={'Upload Files'}
                                   icon={faPlus}
                                   buttonType={MasslawButtonTypes.TEXTUAL}
                                   onClick={e => file_input_ref.current?.click()} />
                </div>
            </div>
            <div className={'case-files-list-content'}>
                {
                    case_files_data && case_files_data.length > 0 ?
                    <CaseFilesList caseFiles={case_files_data}/>
                    :
                    <></>
                }
            </div>
        </>
    )
}

function CaseFilesList(props: {caseFiles: []}) {
    return (
        <>
            <div className={'case-files-table-container'}>
                <thead>
                <tr>
                    <th>File Name</th>
                    <th>File Type</th>
                    <th>Processing Stage</th>
                </tr>
                </thead>
                <tbody>
                {
                    props.caseFiles.map((item, id) => (
                        <CaseFileItem key={id}
                                      fileId={item['id']}
                                      fileName={item['file_name'] || 'Unnamed'}
                                      fileType={item['file_type'] || '?'}
                                      processingStage={(() => {
                                          const stages = item['processing_data']['stages'] as {[key:string]:{status: string}};
                                          for (let stage in stages) {
                                              const stage_data = stages[stage];
                                              const status = stage_data['status'];
                                              if (status !== 'Done') return {stage: stage, status: status};
                                          }
                                          return undefined;
                                      })()}
                        />
                    ))
                }
                </tbody>
            </div>
        </>
    )
}

function CaseFileItem(props: {
    fileId: string,
    fileName: string,
    fileType: string,
    processingStage?: { stage:string, status:string }}){

    const { caseId } = useParams();
    return (
        <>
            <tr>
                <td className={"file-name"} onClick={e => {
                    ApplicationRoutingManager.getInstance().navigateToRoute(ApplicationRoutes.FILE_DISPLAY, {'caseId': caseId || '', 'fileId': props.fileId})
                }}>{props.fileName}</td>
                <td className={"file-type"}>{props.fileType}</td>
                <td className={"file-processing-stage"}>
                    {
                        props.processingStage ?
                        <div className={'files-list-file-processing-stage'}>
                            <span className={'stage-name'}>{props.processingStage.stage}</span>
                            <span className={'stage-status'}>{props.processingStage.status}</span>
                        </div>
                        :
                        <div className={'files-list-file-processing-completed'}>

                        </div>
                    }
                </td>
            </tr>
        </>
    )
}
