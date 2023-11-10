export const case_supported_file_types: string[] = [
    'pdf',
    'bmp',
    'pbm',
    'pgm',
    'ppm',
    'sr',
    'ras',
    'jpeg',
    'jpg',
    'jpe',
    'jp2',
    'tiff',
    'tif',
    'png',
    'exr',
    'hdr',
    'pic',
    'webp',
]

export enum CaseAccessLevels {
    owner = 'owner',
    manager = 'manager',
    editor = 'editor',
    reader = 'reader',
    external = 'external',
}

export const access_level_display_names: { [key: string]: string } = {
    [CaseAccessLevels.owner]: 'Case Owner',
    [CaseAccessLevels.manager]: 'Case Manager',
    [CaseAccessLevels.editor]: 'Case Editor',
    [CaseAccessLevels.reader]: 'Case Reader',
    [CaseAccessLevels.external]: 'External User',
}

export enum FileProcessingStages {
    Starting = 'Starting',
    TextExtraction = 'TextExtraction',
    TextIndexing = 'TextIndexing',
    ProcessingFile = 'ProcessingFile',
} 

export const case_file_processing_stages_order = [
    FileProcessingStages.Starting,
    FileProcessingStages.TextExtraction,
    FileProcessingStages.TextIndexing,
    FileProcessingStages.ProcessingFile,
]

export const case_file_processing_stage_display_names: { [key: string]: string } = {
    [FileProcessingStages.Starting]: 'Starting',
    [FileProcessingStages.TextExtraction]: 'Extracting Text',
    [FileProcessingStages.TextIndexing]: 'Making Text Searchable',
    [FileProcessingStages.ProcessingFile]: 'Processing File',
}
