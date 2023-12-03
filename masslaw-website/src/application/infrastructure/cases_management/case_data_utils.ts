import {LoadingIcon} from "../../shared/components/loading_icon/loading_icon";
import React from "react";
import {CaseFileData} from "./data_structures";
import {case_file_processing_stages_order, FileProcessingStages} from "./cases_consts";

export function get_file_current_ongoing_processing_stage(file_data: CaseFileData) {
    let stagesInProgress = get_file_ongoing_processing_stages_in_order(file_data);

    return stagesInProgress[0] as FileProcessingStages|undefined;
}

export function get_file_ongoing_processing_stages_in_order(file_data: CaseFileData) {
    let stagesInProgress = [];

    const processing_data = file_data.processing || {};

    const stages = Object.keys(processing_data);
    if (stages.length == 0) return [FileProcessingStages.Starting];
    for (let stage of stages) {
        const stage_data = processing_data[stage];
        const status = stage_data.status;
        if (status !== 'done') stagesInProgress.push(stage);
    }

    stagesInProgress.sort((a, b) => {
        const indexA = case_file_processing_stages_order.indexOf(a as FileProcessingStages);
        const indexB = case_file_processing_stages_order.indexOf(b as FileProcessingStages);

        if (indexA === -1 && indexB === -1) return 0;
        if (indexA === -1) return 1;
        if (indexB === -1) return -1;

        return indexA - indexB;
    });

    return stagesInProgress as FileProcessingStages[];
}
