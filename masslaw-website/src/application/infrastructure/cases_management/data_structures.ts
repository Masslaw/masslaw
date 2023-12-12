import {faHighlighter, faStickyNote} from "@fortawesome/free-solid-svg-icons";

export interface CaseData {
    case_id: string,
    access_level: string,
    creation_time: number,
    description: string,
    last_interaction: number,
    num_files: number,
    num_users: number,
    title: string,
}

export interface CaseFileData {
    case_id: string,
    id: string,
    name: string,
    type: string,
    uploaded: string,
    modified: string,
    languages: string[],
    processing: {[key: string] : {status: string}},
    num_annotations: number,
    description: string,
}

export interface CaseFileAnnotationData {
    annotation_id: string,
    type: CaseFileAnnotationTypes,
    creator: string,
    file_id: string,
    case_id: string,
    last_modified: number,
    from_char: number,
    to_char: number,
    annotation_text: string,
    annotated_text: string,
    color: string,
}

export enum CaseFileAnnotationTypes {
    sticky_note = 'sticky_note',
    highlight = 'highlight',
}

export const annotation_type_to_name = {
    [CaseFileAnnotationTypes.sticky_note]: 'Sticky Note',
    [CaseFileAnnotationTypes.highlight]: 'Highlight',
    [undefined as unknown as CaseFileAnnotationTypes]: '',
}


export const annotation_type_to_icon = {
    [CaseFileAnnotationTypes.sticky_note]: faStickyNote,
    [CaseFileAnnotationTypes.highlight]: faHighlighter,
    [undefined as unknown as CaseFileAnnotationTypes]: '',
}

export interface knowledgeEntity {
    id: string,
    label: string,
    properties: {[key: string]: any},
}

export interface knowledgeConnection {
    id: string,
    label: string,
    from: string,
    to: string,
    properties: {[key: string]: any},
}

export interface knowledge {
    [file_id: string]: {
        entities: knowledgeEntity[],
        connections: knowledgeConnection[],
    }
}
