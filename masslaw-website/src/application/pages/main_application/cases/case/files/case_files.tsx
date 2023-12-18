import {useParams} from "react-router-dom";
import {CasesManager} from "../../../../../infrastructure/cases_management/cases_manager";
import React, {useCallback, useEffect, useState} from "react";
import {MasslawButton, MasslawButtonTypes} from "../../../../../shared/components/masslaw_button/masslaw_button";
import {
    faArrowRight,
    faCheck,
    faClock,
    faPlus,
    faRedoAlt,
    faTimes,
    faTrash,
    faTrashAlt
} from "@fortawesome/free-solid-svg-icons";

import './css.css'
import {DataTable} from "../../../../../shared/components/data_table/data_table";
import {LoadingIcon} from "../../../../../shared/components/loading_icon/loading_icon";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {ProgressBar} from "../../../../../shared/components/progress_bar/progress_bar";
import {
    asyncSleep,
    unixTimeToDateTimeString,
    unixTimeToPastTimeString
} from "../../../../../shared/util/date_time_utiles";
import {ApplicationRoutes} from "../../../../../infrastructure/application_base/routing/application_routes";
import {
    GlobalPopupsInterfaceState,
    PopupComponent,
    PopupComponentProps
} from "../../../../../infrastructure/application_base/global_functionality/global_components/application_global_layer/popups/popups";
import {CaseFileAnnotationData, CaseFileData} from "../../../../../infrastructure/cases_management/data_structures";
import {MasslawEllipsisMenu} from "../../../../../shared/components/masslaw_ellipsis_menu/masslaw_ellipsis_menu";
import {FileTypeDisplay} from "../../../../../shared/components/file_type_display/file_type_display";
import {FileUploadRegion} from "../../../../../shared/components/file_upload_region/file_upload_region";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../../infrastructure/application_base/routing/application_page_renderer";
import {useGlobalState} from "../../../../../infrastructure/application_base/global_functionality/global_states";
import {
    NavigationFunctionState
} from "../../../../../infrastructure/application_base/routing/application_global_routing";
import {CognitoManager} from "../../../../../infrastructure/server_communication/server_modules/cognito_client";
import {
    get_file_current_ongoing_processing_stage,
} from "../../../../../infrastructure/cases_management/case_data_utils";
import {
    case_supported_file_types,
    FileProcessingStages
} from "../../../../../infrastructure/cases_management/cases_consts";
import {
    CaseFileProcessingStage
} from "../../../../../shared/components/case_file_processing_stage/case_file_processing_stage";
import {CaseFileDataDisplay} from "../../../../../shared/components/case_file_data_display/case_file_data_display";


export const CaseFiles: ApplicationPage = (props: ApplicationPageProps) => {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const {caseId} = useParams();

    const [case_files_data, setCaseFilesData] = useState([] as CaseFileData[]);
    const [uploading_files_list, setUploadingFilesList] = useState({} as {
        [key: string]: { progress: number, failed: boolean, file_name: string }
    });
    const [loading_files_list, setLoadingFilesList] = useState(false);

    let deleteCaseFile = async (fileData: CaseFileData) => {
        if (!caseId) return;
        setLoadingFilesList(true);
        let tempFilesData = [...case_files_data]
        for (let i = 0; i < tempFilesData.length; i++) {
            let _fileData = tempFilesData[i]
            if (_fileData.id !== fileData.id) continue;
            _fileData.processing = {
                'Deleting': {
                    status: 'InProgress',
                }
            }
            tempFilesData[i] = _fileData
            break;
        }
        setCaseFilesData(tempFilesData)
        await CasesManager.getInstance().deleteFile(
            caseId,
            fileData.id,
        )
        await getCaseFiles();
        setLoadingFilesList(false);
    }

    let getCaseFiles = async () => {
        setLoadingFilesList(true);
        setCaseFilesData(await CasesManager.getInstance().getCaseFiles(caseId || ''));
        setLoadingFilesList(false);
    }

    useEffect(() => {
        getCaseFiles();
    }, []);

    return (
        <>
            <div className={'case-files-header'}>
                <div className={'case-files-page-title page-title'}>{`Case Files`}</div>
                <div className={'case-files-list-header-upload-button-container'}>
                    <MasslawButton caption={'Upload'}
                                   icon={faPlus}
                                   buttonType={MasslawButtonTypes.MAIN}
                                   size={{w: 120, h: 35}}
                                   onClick={e => {
                                       global_popups_interface.pushPopup({
                                           popupComponent: FileUploadUIPopupComponent,
                                           additionalProps: {
                                               caseId: caseId,
                                           },
                                           onClose: getCaseFiles
                                       })
                                   }}/>
                </div>
                <div className={'case-files-list-header-reload-button-container'}>
                    {
                        loading_files_list ?
                            <>
                                <LoadingIcon
                                    color={'#000000'}
                                    ballSize={10}
                                    width={40}
                                />
                            </>
                            :
                            <>
                                <MasslawButton caption={''}
                                               icon={faRedoAlt}
                                               buttonType={MasslawButtonTypes.CLEAR}
                                               size={{w: 50, h: 50}}
                                               onClick={e => {
                                                   getCaseFiles()
                                               }}/>
                            </>
                    }
                </div>
            </div>
            <div className={'case-files-list-content'}>
                {
                    case_files_data && case_files_data.length > 0 ?
                    <DataTable
                        data={case_files_data}
                        keys={[['type', 'File Type'], ['name', 'File Name'], ['description', 'File Description'], ['uploaded', 'Uploaded'], ['modified', 'Last Modified'], ['processing', 'Status'], ['num_annotations', 'Annotations']]}
                        onItemClicked={(item_data) => {
                           global_popups_interface.pushPopup({
                               popupComponent: FileDataDisplayPopupComponent,
                               additionalProps: {
                                   caseId: caseId || '',
                                   fileId: item_data.id,
                                   functions: {
                                       'delete': deleteCaseFile,
                                   }
                               }
                           });
                       }}
                       elementDisplayMap={{
                           'description': (description: string) => {
                               return (
                                   <>
                                       <span style={{maxWidth: '200px'}}>{description || '--'}</span>
                                   </>
                               )
                           },
                           'uploaded': (upload_time: string) => {
                               return (
                                   <>
                                       <span>{`${upload_time && unixTimeToPastTimeString(parseInt(upload_time.toString())) || '?'}`}</span>
                                       <span style={{margin: '10px'}}><FontAwesomeIcon
                                           icon={faClock}></FontAwesomeIcon></span>
                                   </>
                               )
                           },
                           'modified': (upload_time: string) => {
                               return (
                                   <>
                                       <span>{`${upload_time && unixTimeToPastTimeString(parseInt(upload_time.toString())) || '?'}`}</span>
                                       <span style={{margin: '10px'}}><FontAwesomeIcon
                                           icon={faClock}></FontAwesomeIcon></span>
                                   </>
                               )
                           },
                           'type': (file_type: string) => {
                               return <FileTypeDisplay type={file_type} />
                           },
                           'processing': (processing_data: CaseFileData['processing']) => {
                               return <CaseFileProcessingStage fileData={{processing:processing_data} as CaseFileData} />
                           }}}
                    />
                    :
                    <>
                        <></>
                    </>}
            </div>
        </>
    )
}

interface FileDataDisplayPopupProps extends PopupComponentProps{
    fileId: string,
    caseId: string,
    functions: { [key:string]: (fileData: CaseFileData) => void},
}
const FileDataDisplayPopupComponent: PopupComponent = (props: FileDataDisplayPopupProps) => {
    
    const [navigate_function, setNavigateFunction] = useGlobalState(NavigationFunctionState);
    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [file_data, setCaseFileData] = useState({} as CaseFileData);
    const [file_annotations, setFileAnnotations] = useState(null as CaseFileAnnotationData[] | null);

    const [current_file_processing_stage, setCurrentFileProcessingStage] = useState<FileProcessingStages|undefined>(FileProcessingStages.Starting);

    const openable = useCallback(() => {
        return (((file_data.processing || {})[FileProcessingStages.TextExtraction] || {})['status'] || '') == 'done';
    }, [file_data])

    const obtainFileAnnotations = useCallback(async () => {
        setFileAnnotations(null);
        const annotations = await CasesManager.getInstance().getCaseAnnotations(
            file_data.case_id,
            [file_data.id]
        )
        setFileAnnotations(annotations)
    }, [file_data])

    useEffect(() => {
        setCaseFileData({} as CaseFileData);
        if (props.caseId === undefined) { return; }
        CasesManager.getInstance().getFileData(props.caseId, props.fileId).then(fileData => {
            setCaseFileData(fileData);
        })
    }, [props.caseId, props.fileId]);

    useEffect(() => {
        const currentProcessingStage = !file_data && FileProcessingStages.Starting || get_file_current_ongoing_processing_stage(file_data);
        setCurrentFileProcessingStage(currentProcessingStage);
        obtainFileAnnotations().then();
    }, [file_data]);

    useEffect(() => {
        setFileAnnotations(null);
    }, []);

    return (
        <div className={`file-data-display-popup`}>
        {
            file_data.name === undefined ?
                <>
                    <div className={'loading-icon-container'} >
                        <LoadingIcon
                            color={'#000000'}
                            width={70}
                        />
                    </div>
                </>
                :
                <>
                    <div className={'file-data-display-header'}>
                        <div className={'case-file-name'}>
                            {file_data.name}
                        </div>
                        <div className={'file-data-display-close-button-container'}>
                            <MasslawButton
                                caption={''}
                                icon={faTimes}
                                onClick={() => {
                                    global_popups_interface.closeCurrentPopup()
                                }}
                                size={{w: 60, h: 60}}
                                buttonType={MasslawButtonTypes.CLEAR}
                            />
                        </div>
                    </div>
                    <div className={'file-data-display-body'}>
                        <CaseFileDataDisplay
                            fileData={file_data}
                            fileAnnotations={file_annotations}
                            fileAnnotationClickedCallback={(annotationData) => {
                                if (!props.caseId) return;
                                if (!openable()) return;
                                navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                    'caseId': props.caseId,
                                    'fileId': props.fileId,
                                }, {
                                    ['scroll_to']: `${annotationData.from_char}`
                                });
                                global_popups_interface.closeCurrentPopup();
                            }}
                        />
                    </div>
                    <div className={'file-data-display-footer'}>
                        <div className={'file-data-display-open-file-button-container'}>
                            <MasslawButton
                                caption={''}
                                icon={faArrowRight}
                                buttonType={MasslawButtonTypes.MAIN}
                                size={{w: 110, h: 35}}
                                clickable={openable()}
                                onClick={() => {
                                    if (!props.caseId) return;
                                    navigate_function(ApplicationRoutes.FILE_DISPLAY, {
                                        'caseId': props.caseId,
                                        'fileId': props.fileId,
                                    });
                                    global_popups_interface.closeCurrentPopup();
                                }}
                            />
                        </div>
                    </div>
                </>
        }
    </div>
    )
}

interface FileDataDisplayPopupProps extends PopupComponentProps{
    caseId: string,
}
const FileUploadUIPopupComponent: PopupComponent = (props: FileDataDisplayPopupProps) => {

    interface selectedFileEntry {
        file: File,
        uploadingProgress: number,
        typeName: string,
        supported: false,
    }

    const [selected_files, setSelectedFiles] = useState({} as {[file: string]: selectedFileEntry});

    const [any_supported_selected, setAnySupportedSelected] = useState(false);

    const [uploading, setUploading] = useState(false);

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const onFilesSelected = (files: File[]) => {
        setSelectedFiles((prev) => {
            let entries = {...prev};
            for (let file of files) {
                let typeName = file.name.split('.').pop() || '';
                entries[file.name] = {
                    file: file,
                    uploadingProgress: 0,
                    typeName: typeName,
                    supported: case_supported_file_types.includes(typeName),
                } as selectedFileEntry
            }
            return entries;
        });
    }

    const removeEntry = (entry: selectedFileEntry) => {
        setSelectedFiles((prev) => {
            let newSelectedFiles = {...prev};
            delete newSelectedFiles[entry.file.name];
            return newSelectedFiles;
        })
    }

    useEffect(() => {
        for (let entry of Object.values(selected_files)) {
            if (entry.supported) {
                setAnySupportedSelected(true);
                return;
            }
        }
        setAnySupportedSelected(false);
        return;
    }, [selected_files])

    const uploadFiles = useCallback(async () => {
        setUploading(true);
        for (let entry of Object.values(selected_files)) {
            setEntryProgress(entry, 0.01);
        }
        for (let entry of Object.values(selected_files)) {
            if (entry.supported) await uploadFile(entry);
        }
        // await Promise.all(Object.values(selected_files).map((entry) => {
        //     if (!entry.supported) return;
        //     return uploadFile(entry);
        // }));
        global_popups_interface.closeCurrentPopup();
    }, [selected_files]);

    const setEntryProgress = (entry: selectedFileEntry, progress: number) => {
        setSelectedFiles((prev) => {
            let newSelectedFiles = {...prev};
            let newEntry = {...newSelectedFiles[entry.file.name]};
            newEntry.uploadingProgress = progress;
            newSelectedFiles[entry.file.name] = newEntry;
            return newSelectedFiles;
        });
    }

    const uploadFile = async (entry: selectedFileEntry) => {
        setEntryProgress(entry, 0.01);
        let res = await CasesManager.getInstance().uploadFile(props.caseId, entry.file, (progress: number) => {
            setEntryProgress(entry, Math.min(0.99, Math.max(progress, 0.01)));
        });
        await asyncSleep(1500);
        setEntryProgress(entry, res ? 1 : -1);
        await asyncSleep(1500);
    }

    return <>
        <div className={'file-upload-interface-popup'}>
            <div className={'file-upload-interface-popup-title'}>
                {'Upload Files'}
                <div className={'file-upload-interface-popup-close-button-container'}>
                    <MasslawButton
                        caption={''}
                        icon={faTimes}
                        onClick={() => {
                            global_popups_interface.closeCurrentPopup();
                        }}
                        size={{w: 60, h: 60}}
                        buttonType={MasslawButtonTypes.CLEAR}
                    />
                </div>
            </div>
            <div className={'file-upload-interface-popup-interface-container'}>
                <div className={'file-upload-interface-popup-section-title'}>{'To ensure an optimized file processing result, please Make Sure:'}</div>
                <div className={'file-upload-interface-popup-requirement'}>
                    <div className={'file-upload-interface-popup-requirement-number'}>
                        {'1.'}
                    </div>
                    <div className={'file-upload-interface-popup-requirement-prompt'}>
                        <span>
                            <span>{'For Documents And Images: '}</span>
                            <span>{'The documents are scanned with as high quality as possible. And the images are as sharp as possible'}</span>
                        </span>
                        {/*<span>*/}
                        {/*    <span>{'For Audio Files And Videos: '}</span>*/}
                        {/*    <span>{''}</span>*/}
                        {/*</span>*/}
                    </div>
                </div>
                <div className={'file-upload-interface-popup-requirement'}>
                    <div className={'file-upload-interface-popup-requirement-number'}>
                        {'2.'}
                    </div>
                    <div className={'file-upload-interface-popup-requirement-prompt'}>
                        <span>
                            <span>{'For Documents And Images: '}</span>
                            <span>{'All pages and images are right-side-up, text elements that are on their side will be extracted poorly.'}</span>
                        </span>
                        {/*<span>*/}
                        {/*    <span>{'For Audio Files And Videos: '}</span>*/}
                        {/*    <span>{''}</span>*/}
                        {/*</span>*/}
                    </div>
                </div>
                <div className={'file-upload-interface-popup-upload-region-container'}>
                    <FileUploadRegion
                        onGotFiles={onFilesSelected}
                    />
                </div>
                <div className={'file-upload-interface-popup-selected-files'}>
                    <b>{'Selected Files:'}</b>
                    {
                        Object.values(selected_files).length > 0 &&
                        Object.values(selected_files).map((entry, key) => {
                            return <div
                                key={key}
                                className={`file-upload-interface-popup-selected-file-item ` +
                                    `${!entry.supported && 'not-supported' || ''} ` +
                                    `${entry.uploadingProgress >= 1 && 'success' || ''} ` +
                                    `${entry.uploadingProgress < 0 && 'failed' || ''} `}
                            >
                                <span className={'selected-file-icon'}>{<FileTypeDisplay type={entry.typeName} />}</span>
                                <span className={'selected-file-name'}>{entry.file.name}</span>
                                {
                                    !entry.supported &&
                                    <span className={'selected-file-not-supported-message'}>{'This file type is not supported in our services yet'}</span>
                                }
                                {
                                    entry.uploadingProgress > 0 && entry.uploadingProgress < 1 &&
                                    <span className={'selected-file-progressbar-container'}>
                                        <ProgressBar progress={entry.uploadingProgress}/>
                                    </span>
                                }
                                {
                                    entry.uploadingProgress == 0 &&
                                    <span className={'remove-item-button'}>
                                        <MasslawButton
                                            caption={''}
                                            icon={faTrash}
                                            size={{w: 40, h: 40}}
                                            buttonType={MasslawButtonTypes.CLEAR}
                                            onClick={() => {removeEntry(entry)}}
                                        />
                                    </span>
                                }
                                {
                                    entry.uploadingProgress >= 1 &&
                                    <span className={'selected-file-upload-complete-status-icon'}>
                                        <FontAwesomeIcon
                                            icon={faCheck}
                                        />
                                    </span>
                                }
                                {
                                    entry.uploadingProgress < 0 &&
                                    <span className={'selected-file-upload-complete-status-icon'}>
                                        <FontAwesomeIcon
                                            icon={faTimes}
                                        />
                                    </span>
                                }
                            </div>
                        }) ||
                        <div className={'file-upload-interface-popup-selected-files-non-selected'}>
                            {'You haven\'t selected any files yet'}
                        </div>
                    }
                </div>
                <div className={'file-upload-interface-popup-upload-button-container'}>
                    <div className={'file-upload-interface-popup-upload-button-wrapper'}>
                        <MasslawButton
                            caption={'Upload'}
                            loading={uploading}
                            clickable={any_supported_selected}
                            buttonType={MasslawButtonTypes.MAIN}
                            onClick={uploadFiles}
                        />
                    </div>
                </div>
            </div>
        </div>
    </>
}
