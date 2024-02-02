import {useLocation, useParams} from "react-router-dom";

import './css.css'
import {MasslawContentDisplay} from "../../../../../../modules/mlcd/mlcd";
import React, {createRef, useContext, useEffect, useState} from "react";
import {CasesManager} from "../../../../../../infrastructure/cases_management/cases_manager";
import {
    annotation_type_to_name,
    CaseFileAnnotationData,
    CaseFileAnnotationTypes,
    CaseFileData
} from "../../../../../../infrastructure/cases_management/data_structures";
import {faCopy, faHighlighter, faPencilAlt, faStickyNote, faTimes, faTrash} from "@fortawesome/free-solid-svg-icons";
import {
    GlobalPopupsInterfaceState,
    PopupComponent,
    PopupComponentProps
} from "../../../../../../infrastructure/application_base/global_functionality/global_components/application_global_layer/popups/popups";
import {InputField} from "../../../../../../shared/components/input_field/input_field";
import {MasslawButton, MasslawButtonTypes} from "../../../../../../shared/components/masslaw_button/masslaw_button";
import {LoadingButton} from "../../../../../../shared/components/loading_button/loading_button";
import {MasslawUserData} from "../../../../../../infrastructure/user_management/user_data";
import {UsersManager} from "../../../../../../infrastructure/user_management/users_manager";
import {LoadingIcon} from "../../../../../../shared/components/loading_icon/loading_icon";
import {
    ApplicationPage,
    ApplicationPageProps
} from "../../../../../../infrastructure/application_base/routing/application_page_renderer";
import {
    useGlobalState
} from "../../../../../../infrastructure/application_base/global_functionality/global_states";
import {
    QueryStringParamsState
} from "../../../../../../infrastructure/application_base/routing/application_global_routing";
import {CaseFileDataDisplay} from "../../../../../../shared/components/case_file_data_display/case_file_data_display";
import {searchResult} from "../../search/case_search";


const file_annotation_colors = [
    '#de4242',
    '#de9043',
    '#dede43',
    '#90de43',
    '#43de43',
    '#43de90',
    '#43dede',
    '#4390de',
    '#4343de',
    '#9043de',
    '#de43de',
    '#de4390',
]


export const FileDisplay: ApplicationPage = (props: ApplicationPageProps) => {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    const params = new URLSearchParams(window.location.search);

    const {caseId, fileId} = useParams();

    const [displayDirection, setDisplayDirection] = useState('h');

    const displayViewportRef = createRef<HTMLDivElement>();

    const [file_data, setFileData] = useState({} as CaseFileData);
    const [file_annotations, setFileAnnotations] = useState([] as CaseFileAnnotationData[]);

    const [sorted_annotations, setSortedAnnotations] = useState({} as { [key: string]: CaseFileAnnotationData[] });

    const [file_display_current_tab, setFileDisplayCurrentTab] = useState('FileInfoDisplay');

    const location = useLocation();
    const [search_result, setSearchResult] = useState(location.state?.search_result as searchResult | undefined);

    useEffect(() => {
        UsersManager.getInstance().updateMyCachedUserData();
    }, []);

    useEffect(() => {
    }, []);

    const reloadFileData = async () => {
        let fileData = await CasesManager.getInstance().getFileData(caseId || '', fileId || '');
        setFileData(fileData);
    }

    const reloadFileAnnotations = async () => {
        let fileAnnotations = await CasesManager.getInstance().getCaseAnnotations(caseId || '', [fileId || '']);
        setFileAnnotations(fileAnnotations);
    }

    useEffect(() => {
        reloadFileData();
        reloadFileAnnotations();
    }, []);

    useEffect(() => {
        const observer = new ResizeObserver(() => {
            if (!displayViewportRef.current) return;
            const boundingRect = displayViewportRef.current.getBoundingClientRect();
            const {width, height} = boundingRect;
            const aspectRatio = width / height
            setDisplayDirection(aspectRatio > 1 ? 'h' : 'w');
        });

        if (displayViewportRef.current)
            observer.observe(displayViewportRef.current);

        return () => {
            if (displayViewportRef.current) {
                observer.unobserve(displayViewportRef.current);
            }
        };
    }, [displayViewportRef]);

    useEffect(() => {
        let sortedAnnotations = {} as {[key: string]: CaseFileAnnotationData[]}
        let annotationsInOrder = file_annotations.sort((a, b) => a.from_char - b.from_char)
        for (let annotation of annotationsInOrder) {
            let currentTypeAnnotations = sortedAnnotations[annotation.type] || [];
            currentTypeAnnotations.push(annotation);
            sortedAnnotations[annotation.type] = currentTypeAnnotations;
        }
        setSortedAnnotations(sortedAnnotations);
    }, [file_annotations]);

    const FileDisplayTabs = {
        'FileInfoDisplay': () => {
            return (
                <>
                </>
            )
        },
        'FileStickyNotesDisplay': () => {
            return (
                <>
                </>
            )
        },
        'FileHighlightsDisplay': () => {
            return (
                <>
                </>
            )
        }
    }

    const configure_annotation = async (annotation_data: CaseFileAnnotationData) => {
        global_popups_interface.pushPopup({
            popupComponent: FileAnnotationEditConfigurationPopupComponent,
            additionalProps: {
                annotation_existing_data: annotation_data,
            },
            onClose: () => {
                reloadFileAnnotations();
            }
        });
    }
    
    const show_annotation = async (annotation_data: CaseFileAnnotationData) => {
        global_popups_interface.pushPopup({
            popupComponent: FileAnnotationShowPopupComponent,
            additionalProps: {
                annotation_data: annotation_data,
                openConfigurationPopup: () => {
                    configure_annotation(annotation_data)
                },
            },
            onClose: () => {
                reloadFileAnnotations();
            }
        });
    }

    const copyText = async (fromChar: number, toChar: number, text: string) => {
        await navigator.clipboard.writeText(text);
    }

    const selectionToolkitButtons = [
        {
            name: 'Add a sticky note',
            icon: faStickyNote,
            callback: (fromChar: number, toChar: number, text: string) => configure_annotation({
                type: CaseFileAnnotationTypes.sticky_note,
                from_char: fromChar,
                to_char: toChar,
                annotation_text: '',
                annotated_text: text,
                file_id: fileId,
                case_id: caseId,
                color: file_annotation_colors[4],
            } as CaseFileAnnotationData),
        },
        {
            name: 'Highlight selection',
            icon: faHighlighter,
            callback: (fromChar: number, toChar: number, text: string) => configure_annotation({
                type: CaseFileAnnotationTypes.highlight,
                from_char: fromChar,
                to_char: toChar,
                annotation_text: '',
                annotated_text: text,
                file_id: fileId,
                case_id: caseId,
                color: file_annotation_colors[4],
            } as CaseFileAnnotationData),
        },
        {
            name: 'Copy selection',
            icon: faCopy,
            callback: copyText,
        },
    ];

    return (
        <>
            <div
                className={`file-display direction-${displayDirection}`}
                style={{width: '100%', height: '100%'}}
                ref={displayViewportRef}
            >
                <div className={'file-content-display-area'}>
                    <MasslawContentDisplay
                        fileData={file_data}
                        fileAnnotations={file_annotations}
                        onAnnotationClicked={show_annotation}
                        scrollToChar={parseInt(query_string_params['scroll_to'])}
                        selectionToolkitButtons={selectionToolkitButtons}
                        searchResult={search_result}
                    />
                </div>
                <div className={'file-data-display-area'}>
                    <div className={'file-data-display-file-name'}>
                        {file_data.name}
                    </div>
                    <CaseFileDataDisplay
                        fileData={file_data}
                        fileAnnotations={file_annotations}
                        fileAnnotationClickedCallback={(annotationData: CaseFileAnnotationData) => {
                            setQueryStringParams((prev) => {
                                return  {
                                    ...prev,
                                    ['scroll_to']: '',
                                }
                            });
                            setQueryStringParams((prev) => {
                                return  {
                                    ...prev,
                                    ['scroll_to']: `${annotationData.from_char}`,
                                }
                            });
                        }}
                    />
                </div>
            </div>
        </>
    )
}

interface FileAnnotationEditConfigurationPopupProps extends PopupComponentProps {
    annotation_existing_data: CaseFileAnnotationData,
}

const FileAnnotationEditConfigurationPopupComponent: PopupComponent = (props: FileAnnotationEditConfigurationPopupProps) => {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [annotation_data, setAnnotationData] = useState(props.annotation_existing_data)

    const [saving, setSaving] = useState(false);

    const submit = async () => {
        setSaving(true);
        await CasesManager.getInstance().setCaseAnnotation(annotation_data);
        global_popups_interface.closeCurrentPopup();
        setSaving(false);
    }

    return (
        <>
            <div className={'annotation-configuration-popup'}>
                <div className={'annotation-popup-close-button-container'}>
                    <MasslawButton
                        buttonType={MasslawButtonTypes.CLEAR}
                        caption={''}
                        icon={faTimes}
                        size={{w: 30, h:30}}
                        fontSize={20}
                        onClick={e => global_popups_interface.closeCurrentPopup()}
                    />
                </div>
                <div className={'annotation-popup-title'}>
                    {`Configure ${annotation_type_to_name[props.annotation_existing_data?.type as string]}`}
                </div>
                <div className={'annotation-popup-section-title'}>{'Color'}</div>
                <div className={'annotation-popup-section-secondary-title'}>{'Select a marking color'}</div>
                <div className={'annotation-popup-color-selection'}>
                    {
                        file_annotation_colors.map((color, key) => {
                            return (
                                <div
                                    key={key}
                                    className={`annotation-popup-color-selectable clickable ${annotation_data.color == color && 'selected' || ''}`}
                                    style={{background: color}}
                                    onClick={() => setAnnotationData({
                                        ...annotation_data,
                                        color: color
                                    })}
                                />
                            )
                        })
                    }
                </div>
                {
                    (props.annotation_existing_data?.type == CaseFileAnnotationTypes.sticky_note) &&
                    <div className={'annotation-popup-input-text-container'}>
                        <div className={'annotation-popup-section-title'}>{'Text'}</div>
                        <div className={'annotation-popup-section-secondary-title'}>{'Input a text'}</div>
                        <InputField
                            value={annotation_data.annotation_text || ''}
                            onChange={e => setAnnotationData({
                                ...annotation_data,
                                annotation_text: e.target.value
                            })}
                            valid={'valid'}
                            isParagraph={true}
                        />
                    </div>
                    || <></>
                }
                <div style={{padding: '20px'}}>
                    <LoadingButton
                        clickable={!!annotation_data.color}
                        caption={'Finish'}
                        loading={saving}
                        onClick={submit}
                    />
                </div>
            </div>
        </>
    )
}

interface FileAnnotationShowPopupProps extends PopupComponentProps {
    annotation_data: CaseFileAnnotationData,
    openConfigurationPopup: () => void,
}

const FileAnnotationShowPopupComponent: PopupComponent = (props: FileAnnotationShowPopupProps) => {

    const [global_popups_interface, setGlobalPopupsInterface] = useGlobalState(GlobalPopupsInterfaceState);

    const [loading, setLoading] = useState(false);

    const [annotation_creator_data, setAnnotationCreatorData] = useState({} as MasslawUserData);

    const [is_creator_me, setIsCreatorMe] = useState(true);

    const [deleting, setDeleting] = useState(false);

    const getCreatorUserData = async () => {
        setLoading(true);
        setAnnotationCreatorData(await UsersManager.getInstance().getUserData(props.annotation_data.creator));
        setLoading(false);
    }

    useEffect(() => {
        const isMe = props.annotation_data.creator == UsersManager.getInstance().getMyCachedUserData().User_ID;
        setIsCreatorMe(isMe);
        if (!isMe) getCreatorUserData();
    }, [props.annotation_data]);
    
    const deleteAnnotation = async () => {
        setDeleting(true);
        await CasesManager.getInstance().deleteCaseAnnotation(props.annotation_data);
        global_popups_interface.closeCurrentPopup();
        setDeleting(false);
    }

    return (
        <>
            <div
                className={'annotation-show-popup'}
                style={{
                    borderColor: `${props.annotation_data.color}e0`
                }}
            >
                <div className={'annotation-popup-close-button-container'}>
                    <MasslawButton
                        buttonType={MasslawButtonTypes.CLEAR}
                        caption={''}
                        icon={faTimes}
                        size={{w: 30, h:30}}
                        fontSize={20}
                        onClick={e => global_popups_interface.closeCurrentPopup()}
                    />
                </div>
                <div className={'annotation-popup-title'}>
                    <span>{annotation_type_to_name[props.annotation_data?.type as string]}</span>
                </div>
                <>
                    {
                        loading &&
                        <div style={{margin: '20px'}}><LoadingIcon color={'#000000'} /></div>
                        ||
                        <>
                            {
                                is_creator_me &&
                                <>
                                    <div style={{display: 'flex', padding: '10px'}}>
                                        <div>
                                            <MasslawButton
                                                caption={`Edit ${annotation_type_to_name[props.annotation_data?.type as string]}`}
                                                icon={faPencilAlt}
                                                size={{w:150, h:30}}
                                                onClick={e => {
                                                    global_popups_interface.closeCurrentPopup();
                                                    props.openConfigurationPopup();
                                                }}
                                            />
                                        </div>
                                        <div style={{position: "absolute", right: '10px'}}>
                                            <MasslawButton
                                                clickable={true}
                                                caption={`Delete ${annotation_type_to_name[props.annotation_data?.type as string]}`}
                                                loading={deleting}
                                                icon={faTrash}
                                                size={{w:150, h:30}}
                                                buttonType={MasslawButtonTypes.DESTRUCTIVE}
                                                onClick={deleteAnnotation}
                                            />
                                        </div>
                                    </div>
                                </>
                                ||
                                <>
                                    <div className={'annotation-popup-creator-credit'}>
                                        {`By: ${annotation_creator_data.first_name} ${annotation_creator_data.last_name}`}
                                    </div>
                                </>
                            }
                            <div className={'annotation-display-annotated-text'} dir={'auto'}>
                                {`''${props.annotation_data.annotated_text}''`}
                            </div>
                            {
                                props.annotation_data.annotation_text &&
                                <div
                                    className={'annotation-display-annotation-text'}
                                    dir={'auto'}
                                    style={{
                                        background: `${props.annotation_data.color}50`
                                    }}
                                >
                                    {props.annotation_data.annotation_text}
                                </div>
                                || <></>
                            }
                        </>
                    }
                </>
            </div>
        </>
    )
}