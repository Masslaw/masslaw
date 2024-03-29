export const caseSupportedFileTypes = [
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
    'doc',
    'docx',
    'txt',
    'text',
    'log'
]

export const caseAccessLevels = {
    owner: 'owner',
    manager: 'manager',
    editor: 'editor',
    reader: 'reader',
    external: 'external',
}

export const accessLevelDisplayNames = {
    [caseAccessLevels.owner]: 'Case Owner',
    [caseAccessLevels.manager]: 'Case Manager',
    [caseAccessLevels.editor]: 'Case Editor',
    [caseAccessLevels.reader]: 'Case Reader',
    [caseAccessLevels.external]: 'External User',
}

export const accessLevelDisplayColors = {
    [caseAccessLevels.owner]: '#192a75',
    [caseAccessLevels.manager]: '#1f7519',
    [caseAccessLevels.editor]: '#5b1975',
    [caseAccessLevels.reader]: '#19756a',
    [caseAccessLevels.external]: '#751919',
}

export const accessLevelsOrder = [
    caseAccessLevels.owner,
    caseAccessLevels.manager,
    caseAccessLevels.editor,
    caseAccessLevels.reader,
    caseAccessLevels.external,
]

export const fileProcessingStages = {
    Starting: 'starting',
    TextExtraction: 'text_extraction',
    TextIndexing: 'text_indexing',
    KnowledgeExtraction: 'knowledge_extraction',
    ProcessingFile: 'processing_file',
}

export const caseFileProcessingStagesOrder = [
    fileProcessingStages.Starting,
    fileProcessingStages.TextExtraction,
    fileProcessingStages.TextIndexing,
    fileProcessingStages.KnowledgeExtraction,
    fileProcessingStages.ProcessingFile,
]

export const caseFileProcessingStageDisplayNames = {
    [fileProcessingStages.Starting]: 'Starting',
    [fileProcessingStages.TextExtraction]: 'Extracting Text',
    [fileProcessingStages.TextIndexing]: 'Making Text Searchable',
    [fileProcessingStages.KnowledgeExtraction]: 'Extracting Knowledge',
    [fileProcessingStages.ProcessingFile]: 'Processing File',
}