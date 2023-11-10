import React, {ReactNode, useState} from "react";

import "./css.css"
import {CaseFileAnnotationData, CaseFileData} from "../../../infrastructure/cases_management/data_structures";
import {CaseFileProcessingStage} from "../case_file_processing_stage/case_file_processing_stage";
import {CaseFileAnnotationItem} from "../case_file_annotation_item/case_file_annotation_item";
import {LoadingIcon} from "../loading_icon/loading_icon";
import {unixTimeToDateTimeString, unixTimeToPastTimeString} from "../../util/date_time_utiles";
import {ParagraphEditor} from "../pragraph_editor/paragraph_editor";
import {CasesManager} from "../../../infrastructure/cases_management/cases_manager";

export function CaseFileDataDisplay(props: {
    fileData: CaseFileData,
    fileAnnotations: CaseFileAnnotationData[] | null,
    fileAnnotationClickedCallback: (annotationData: CaseFileAnnotationData) => void
}) {
    const { fileData, fileAnnotations, fileAnnotationClickedCallback } = props;

    return (
        <div className="case-file-data-container">
            <p className="case-file-stage">
                Processing Stage:
                <span className={'case-file-data-section-value'}>{<CaseFileProcessingStage fileData={fileData} />}</span>
            </p>
            <p className="case-file-type">
                Type:
                <span className={'case-file-data-section-value'}>{fileData.type}</span>
            </p>
            <p className="case-file-upload-date">
                Uploaded:
                <span className={'case-file-data-section-value'}>{unixTimeToPastTimeString(parseInt(fileData.uploaded))}</span>
            </p>
            <p className="case-file-modified-date">
                Modified:
                <span className={'case-file-data-section-value'}>{unixTimeToPastTimeString(parseInt(fileData.modified))}</span>
            </p>
            <p className="case-file-languages">
                Languages:
                <span className={'case-file-data-section-value'}>{(fileData.languages || ['']).join(', ')}</span>
            </p>
            <p className={'case-file-description'}>
                File Description:
                <ParagraphEditor
                    text={fileData.description}
                    editable={true}
                    maxCharacters={500}
                    onFinish={async (new_description: string) => {
                        await CasesManager.getInstance().setCaseFileDescription(fileData.case_id, fileData.id, new_description);
                    }}
                />
            </p>
            <p className="case-file-annotations-title">Annotations:</p>
            <ul className="case-file-annotations-list">
                {
                    (() => {
                        if (fileAnnotations == null)
                            return <LoadingIcon color={'#000000'}/>
                        if (fileAnnotations.length == 0)
                            return <p>    No annotations in that file</p>
                        return fileAnnotations.sort(
                            (a, b) => b.last_modified - a.last_modified
                        ).map(annotation => (
                            <CaseFileAnnotationItem
                                key={annotation.annotation_id}
                                annotationData={annotation}
                                onClick={() => fileAnnotationClickedCallback(annotation)}
                            />
                        ))
                    })()
                }
            </ul>
        </div>
    );
}