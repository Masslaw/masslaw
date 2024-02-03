import React, {useCallback, useEffect, useMemo, useRef, useState} from "react";
import {LoadingIcon} from "../../../../shared/components/loading_icon/loading_icon";
import {CasesManager} from "../../../../infrastructure/cases_management/cases_manager";

import './css.css';
import {InputManager} from "../../../../shared/util/input_manager";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {MLCDContentRenderingComponent, MLCDProps} from "../../mlcd";
import {centerChildInParent} from "../../../../shared/util/DOM_utils";
import {useGlobalState} from "../../../../infrastructure/application_base/global_functionality/global_states";
import {QueryStringParamsState} from "../../../../infrastructure/application_base/routing/application_global_routing";


interface PageDisplayData {
    structure: Element,
    imageUrl: string,
    pageNum: number,
    sizeData: Element
}

interface TextMarkingData {
    from_char: number,
    to_char: number,
    type: string,
    color: string,
    inRealCharacters?: boolean,
    onClick?: () => void,
}

interface TextMarkingVisualData {
    rects: [number, number, number, number][],
    type: string,
    color: string,
    hovered: boolean,
    onClick?: () => void,
}

export const OpticalDocumentRenderer: MLCDContentRenderingComponent = (props: MLCDProps) => {

    const documentRendererInputManager = new InputManager(null, true);
    const document_renderer_ref = useRef<HTMLDivElement>(null);

    const [query_string_params, setQueryStringParams] = useGlobalState(QueryStringParamsState);

    useEffect(() => {
        documentRendererInputManager.setTarget(document_renderer_ref.current);
        documentRendererInputManager.preventContextMenu();
    }, [document_renderer_ref]);

    const [loading_display, setLoadingDisplay] = useState(true);

    const [text_structure, setTextStructure] =
        useState(document.implementation.createDocument("", "", null));

    const [pages, setPages] = useState([] as PageDisplayData[]);

    const [page_image_download_urls, setPageImageDownloadUrls] = useState({} as { [pageNumber: string]: string });

    const [selection_text, setSelectionText] = useState('');

    const [scroll_to_char, setScrollToChar] = useState(props.scrollToChar);

    const [search_result_position, setSearchResultPosition] = useState({} as {start_char: number | undefined, end_char: number | undefined});

    const getRectFromCharacter = (characterElement: Element) => {
        let x1 = characterElement.getAttribute('x1');
        let y1 = characterElement.getAttribute('y1');
        let x2 = characterElement.getAttribute('x2');
        let y2 = characterElement.getAttribute('y2');
        if (!(x1 && x2 && y1 && y2)) {
            const r = characterElement.getAttribute('r') || '0-0-0-0';
            const rect_values = r.split('-');
            x1 = rect_values[0];
            y1 = rect_values[1];
            x2 = rect_values[2];
            y2 = rect_values[3];
        }
        const rect = [
            (x1 != null) && parseInt(x1) || -1,
            (y1 != null) && parseInt(y1) || -1,
            (x2 != null) && parseInt(x2) || -1,
            (y2 != null) && parseInt(y2) || -1,
        ]
        return rect
    }

    const updateFileStructure = async () => {
        const textStructureContentPath = `extracted_text/text_structure`;
        let structureDownloadURL = await CasesManager.getInstance().getFileContentDownloadURL(
            props.fileData.case_id,
            props.fileData.id,
            [textStructureContentPath]
        );
        const url = structureDownloadURL[textStructureContentPath]
        const response = await fetch(url);
        const xmlText = await response.text();
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xmlText, "text/xml");
        setTextStructure(xmlDoc);
    }

    const collectPageImagesDownloadURLs = async () => {
        const groupElements = Array.from(text_structure.getElementsByTagName("gr"));
        if (!groupElements.length) return;
        let urls = await CasesManager.getInstance().getFileContentDownloadURL(
            props.fileData.case_id,
            props.fileData.id,
            groupElements.map((_, pageNum) => `processed_assets/page_${pageNum}.png`)
        );
        let pageImageDownloadUrls = {} as { [key: string]: string };
        for (let pageNum in groupElements) {
            pageImageDownloadUrls[pageNum] = urls[`processed_assets/page_${pageNum}.png`]
        }
        setPageImageDownloadUrls(pageImageDownloadUrls);
    }

    useEffect(() => {
        updateFileStructure();
    }, [props.fileData]);

    useEffect(() => {
        collectPageImagesDownloadURLs();
    }, [text_structure]);

    useEffect(() => {
        let pages: PageDisplayData[] = [];
        const groupElements = Array.from(text_structure.getElementsByTagName("gr"));
        const sizeElements = Array.from(text_structure.getElementsByTagName("image_size"));
        for (let pageNum in groupElements) {
            pages.push({
                structure: groupElements[pageNum],
                imageUrl: page_image_download_urls[pageNum],
                pageNum: parseInt(pageNum),
                sizeData: sizeElements[pageNum]
            })
        }
        pages = pages.sort((a, b) => (a.pageNum - b.pageNum))
        setPages(pages);
    }, [text_structure, page_image_download_urls]);

    const [current_selection_start, setCurrentSelectionStart] = useState(-1);
    const [current_selection_end, setCurrentSelectionEnd] = useState(-1);

    const [selection_toolkit_displaying, setSelectionToolkitDisplaying] = useState(false);
    const [selection_toolkit_position, setSelectionToolkitPosition] = useState({page: 0, x: 0, y: 0});
    const [mouse_on_selection_toolkit, setMouseOnSelectionToolkit] = useState(false);

    const onCharacterHover = (characterNum: number) => {
        if (documentRendererInputManager.state.mouse.buttons[0].duration > 0) {
            setCurrentSelectionStart((current) => current > 0 && current || characterNum);
            setCurrentSelectionEnd(characterNum);
        }
    }

    const onMouseDownOnRenderer = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
        if (event.button == 0) {
            if (!mouse_on_selection_toolkit) {
                setCurrentSelectionStart(-1);
                setCurrentSelectionEnd(-1);
                setSelectionToolkitDisplaying(false);
            }
        }
    }, [mouse_on_selection_toolkit, current_selection_start, current_selection_end, selection_text, props.onSelection]);

    const onMouseUpOnRenderer = useCallback((event: React.MouseEvent<HTMLDivElement>) => {
        if (!mouse_on_selection_toolkit) {
            if (current_selection_start >= 0 && current_selection_end >= 0) setSelectionToolkitDisplaying(true);
            if (props.onSelection) props.onSelection(current_selection_start, current_selection_end, selection_text);
        }
    }, [mouse_on_selection_toolkit, current_selection_start, current_selection_end, selection_text, props.onSelection]);

    const [text_markings, setTextMarkings] = useState({} as { [key: string]: TextMarkingData });

    const [pages_marking_visual_data, setPagesMarkingVisualData] =
        useState([] as {
            [key: string]: TextMarkingVisualData
        }[]);

    useEffect(() => {
        console.log(current_selection_start, current_selection_end);
        setTextMarkings((state) => {
            let newState = {...state};
            newState['user-selection'] = {
                from_char: Math.min(current_selection_start, current_selection_end),
                to_char: Math.max(current_selection_start, current_selection_end),
                type: 'user_selection',
                color: '#0056ff'
            }
            return newState;
        });
    }, [current_selection_start, current_selection_end]);

    useEffect(() => {
        setTextMarkings((state) => {
            let newState = {...state};
            for (let annotation of props.fileAnnotations) {
                newState[annotation.annotation_id] = {
                    from_char: annotation.from_char,
                    to_char: annotation.to_char,
                    type: annotation.type,
                    color: annotation.color,
                    onClick: () => {
                        props.onAnnotationClicked(annotation);
                    }
                } as TextMarkingData;
            }
            return newState;
        });
    }, [props.fileAnnotations]);

    const getPageDimentions = (pageDisplayData: PageDisplayData) => {
        const pageWidth = parseInt(pageDisplayData.structure.getAttribute('w') ||
            (pageDisplayData.sizeData || new Element()).getAttribute('w') || '0') || 0;
        const pageHeight = parseInt(pageDisplayData.structure.getAttribute('h') ||
            (pageDisplayData.sizeData || new Element()).getAttribute('h') || '0') || 0;
        return [pageWidth, pageHeight]
    }

    useEffect(() => {
        setPagesMarkingVisualData((current) => {
            let selectionText = '';
            let _characterCount = 0;
            let _t = ""
            let pagesMarkingsVisualData = [] as {[key: string]: TextMarkingVisualData}[] ;
            for (let pageNum = 0; pageNum < pages.length; pageNum++) {
                let page = pages[pageNum];
                let pageMarkingsVisualData = {} as {[key: string]: TextMarkingVisualData};
                for (let line of Array.from(page.structure.getElementsByTagName('ln'))) {
                    for (let word of Array.from(line.getElementsByTagName('wd'))) {
                        for (let character of Array.from(word.getElementsByTagName('cr'))) {
                            for (let markingId of Object.keys(text_markings)) {
                                const markingData = text_markings[markingId];
                                let markingVisualData = pageMarkingsVisualData[markingId] ||
                                    {
                                        rects: [[-1, -1, -1, -1]],
                                        type: markingData.type,
                                        color: markingData.color,
                                        hovered: pageNum < current.length && current[pageNum][markingId]?.hovered || false,
                                        onClick: markingData.onClick,
                                    } as TextMarkingVisualData;
                                if (markingData.from_char <= _characterCount+1 &&
                                    _characterCount <= markingData.to_char) {
                                    const characterRect = getRectFromCharacter(character);
                                    const rectsList = markingVisualData.rects;
                                    let currentRect = rectsList[rectsList.length - 1];
                                    currentRect = [
                                        ((currentRect[0] >= 0 && characterRect[0] >= 0) && Math.min(currentRect[0], characterRect[0]) || Math.max(currentRect[0], characterRect[0])),
                                        ((currentRect[1] >= 0 && characterRect[1] >= 0) && Math.min(currentRect[1], characterRect[1]) || Math.max(currentRect[1], characterRect[1])),
                                        Math.max(currentRect[2], characterRect[2]),
                                        Math.max(currentRect[3], characterRect[3]),
                                    ]
                                    markingVisualData.rects[rectsList.length - 1] = currentRect;

                                    if (markingData.type == 'user_selection') {
                                        selectionText += character.textContent || character.getAttribute('v');
                                        let characterX1 = characterRect[0];
                                        let characterY2 = characterRect[3] + 10;
                                        let toolkitX = characterX1;
                                        let toolkitY = Math.min(characterY2, parseInt(page.structure.getAttribute('h') || `${characterY2}`) || characterY2);
                                        if (_characterCount == markingData.to_char) {
                                            setSelectionToolkitPosition({
                                                page: pageNum,
                                                x: toolkitX,
                                                y: toolkitY,
                                            })
                                        }
                                    }

                                    if (markingData.type == 'search_result') {
                                        console.log(character.textContent || character.getAttribute('v'));
                                    }
                                }
                                pageMarkingsVisualData[markingId] = markingVisualData;
                            }
                            _t += `${_characterCount} - ${character.textContent || character.getAttribute('v')}\n`;
                            _characterCount++;
                        }
                        selectionText += ' ';
                    }
                    for (let markingId of Object.keys(text_markings)) {
                        let markingVisualData = pageMarkingsVisualData[markingId];
                        if (markingVisualData) {
                            markingVisualData.rects.push([-1, -1, -1, -1]);
                            pageMarkingsVisualData[markingId] = markingVisualData;
                        }
                    }
                }
                pagesMarkingsVisualData.push(pageMarkingsVisualData);
            }
            setSelectionText(selectionText);
            console.log(_t);
            return pagesMarkingsVisualData;
        })
    }, [text_markings, pages]);

    useEffect(() => {
        resolveSearchResult().then();
    }, [props.searchResult, text_structure]);

    const resolveSearchResult = useCallback(async () => {
        let searchResult = props.searchResult;
        if (!searchResult) return;
        let searchString = searchResult.start_text + searchResult.highlighted_text + searchResult.end_text;
        let document_characters = Array.from(text_structure.getElementsByTagName('cr'));
        for (let character_index = 0; character_index < document_characters.length; character_index++) {
            let searchResultStartIndex = undefined;
            let searchResultEndIndex = undefined;
            let searchIndex = 0;
            for (let characterIndex = character_index; characterIndex < document_characters.length; characterIndex++) {
                let character = document_characters[characterIndex];
                let characterValue = (character.textContent || character.getAttribute('v')) || '';
                if (['\n', ' '].includes(characterValue)) continue;
                let searchCharacter = "";
                do {
                    if (searchIndex == searchResult.start_text.length) {
                        searchResultStartIndex = characterIndex;
                    }
                    if (searchIndex == searchResult.start_text.length + searchResult.highlighted_text.length) {
                        searchResultEndIndex = characterIndex;
                    }
                    searchCharacter = searchString[searchIndex];
                    searchIndex++;
                } while (['\n', ' '].includes(searchCharacter));
                if (searchIndex >= searchString.length){
                    if (searchResultStartIndex != undefined && searchResultEndIndex != undefined) {
                        setSearchResultPosition({
                            start_char: searchResultStartIndex + 1,
                            end_char: searchResultEndIndex - 1,
                        })
                        return;
                    };
                }
                if (searchCharacter != characterValue) {
                    break;
                }
            }
        }
    }, [props.searchResult, text_structure]);

    useEffect(() => {
        if (search_result_position.start_char == undefined || search_result_position.end_char == undefined) {
            setQueryStringParams((state) => {
                let new_state = {...state};
                delete new_state['search_result_start_char'];
                delete new_state['search_result_end_char'];
                return new_state
            });
            setTextMarkings((state) => {
                let newState = {...state};
                delete newState['search-result'];
                return newState;
            });
            return;
        };
        setQueryStringParams((state) => {
            let new_state = {...state};
            new_state['search_result_start_char'] = search_result_position.start_char && search_result_position.start_char.toString() || '';
            new_state['search_result_end_char'] = search_result_position.end_char && search_result_position.end_char.toString() || '';
            return new_state
        });
        setTextMarkings((state) => {
            let newState = {...state};
            newState['search-result'] = {
                from_char: search_result_position.start_char || 0,
                to_char: search_result_position.end_char || 0,
                type: 'search_result',
                inRealCharacters: true,
                color: '#ffc400'
            }
            return newState;
        });
        setScrollToChar(search_result_position.start_char || 0);
    }, [search_result_position]);

    useEffect(() => {
        documentRendererInputManager.setClipboardTarget(selection_text);
    }, [selection_text]);

    useEffect(() => {
        setScrollToChar(props.scrollToChar);
    }, [props.scrollToChar]);

    useEffect(() => {
        if (loading_display) return;
        if (!scroll_to_char) return;
        if (!document_renderer_ref.current || !scroll_to_char) return;
        const documentRendererElement = document_renderer_ref.current;
        const charElement = document.getElementById(`char-${scroll_to_char}`) as HTMLDivElement;
        if (!charElement) return;
        centerChildInParent(charElement, documentRendererElement);
        setScrollToChar(undefined);
    }, [scroll_to_char, loading_display]);

    const [visible_pages, setVisiblePages] = useState([] as boolean[]);

    const isPageVisible = (pageElement: Element) => {
        if (!document_renderer_ref.current) return false;

        const documentRect = document_renderer_ref.current.getBoundingClientRect();
        const pageRect = pageElement.getBoundingClientRect();

        return (
            pageRect.top <= documentRect.bottom &&
            pageRect.bottom >= documentRect.top &&
            pageRect.left <= documentRect.right &&
            pageRect.right >= documentRect.left
        );
    }

    const checkPagesVisibility = () => {
        if (!document_renderer_ref.current) return;
        let visiblePages = [];
        const children = document_renderer_ref.current.getElementsByClassName('optical-document-page-container');
        for(let i = 0; i < children.length; i++) {
            const child = children.item(i);
            visiblePages.push(child && isPageVisible(child) || false);
        }
        setVisiblePages(visiblePages);
    }

    useEffect(() => {
        checkPagesVisibility();
    }, [pages]);

    const renderedPages = useMemo(() => {
        setLoadingDisplay(true);
        let characterCount = 0;
        let _t = "";
        const rendered = pages.map((pageDisplayData, pageIndex) => {
            const [pageWidth, pageHeight] = getPageDimentions(pageDisplayData);
            return (
                <div
                    key={`page-${pageIndex}`}
                    className={'optical-document-page-container'}
                    style={{
                        paddingBottom: `${100 * pageHeight / pageWidth}%`
                    }}
                >
                    <div
                        className={'optical-document-page-content'}
                    >
                        <div className={'loading-image-icon-container'}>
                            <LoadingIcon color={'#000000'}/>
                        </div>
                        <img
                            className={'optical-document-page-image'}
                            src={pageDisplayData.imageUrl}
                        />
                        <div className={'optical-document-page-structure-container'}>
                            {
                                Array.from(pageDisplayData.structure.getElementsByTagName('cr')).map((character, characterNum) => {
                                    const currentCharacterNumber = characterCount;
                                    _t += `${characterCount} - ${character.textContent || character.getAttribute('v')}\n`;
                                    characterCount++;
                                    const characterRect = getRectFromCharacter(character);
                                    return <div
                                        key={`char-${currentCharacterNumber}`}
                                        id={`char-${currentCharacterNumber}`}
                                        className={`optical-document-character-element`}
                                        onMouseEnter={e => {
                                            onCharacterHover(currentCharacterNumber);
                                        }}
                                        style={{
                                            position: 'absolute',
                                            left: `${100 * characterRect[0] / pageWidth}%`,
                                            top: `${100 * characterRect[1] / pageHeight}%`,
                                            width: `${100 * (characterRect[2] - characterRect[0]) / pageWidth}%`,
                                            height: `${100 * (characterRect[3] - characterRect[1]) / pageHeight}%`,
                                            zIndex: '30',
                                        }}
                                    />
                                })
                            }
                        </div>
                    </div>
                </div>
            )
        });
        setLoadingDisplay(false);
        console.log(_t);
        return rendered;
    }, [pages, scroll_to_char]);

    const renderedHighlightsLayer = useMemo(() => {
        return pages.map((pageDisplayData, pageIndex) => {
            const [pageWidth, pageHeight] = getPageDimentions(pageDisplayData);
            return (
                <div
                    key={`page-${pageIndex}`}
                    className={'optical-document-page-container'}
                    style={{
                        paddingBottom: `${100 * pageHeight / pageWidth}%`
                    }}
                >

                    {
                        Object.keys(pages_marking_visual_data[pageIndex] || {}).map((markingKey) => {
                            const markingVisualData = pages_marking_visual_data[pageIndex][markingKey];
                            return <>{
                                markingVisualData.rects.map((rect, key) => {
                                    if (rect[0] < 0 || rect[1] < 0 || rect[2] < 0 || rect[3] < 0) return <></>
                                    return <div
                                        key={`mark-${pageIndex}-${markingKey}-${key}`}
                                        className={`optical-document-text-marking ${markingVisualData.type} ${markingVisualData.hovered && 'hovered' || ''}`}
                                        style={{
                                            background: `${markingVisualData.color}80`,
                                            border: `1px solid ${markingVisualData.color}`,
                                            position: 'absolute',
                                            left: `${100 * rect[0] / pageWidth}%`,
                                            top: `${100 * rect[1] / pageHeight}%`,
                                            width: `${100 * (rect[2] - rect[0]) / pageWidth}%`,
                                            height: `${100 * (rect[3] - rect[1]) / pageHeight}%`,
                                            zIndex: '50',
                                        }}
                                        onMouseEnter={e => setPagesMarkingVisualData((state) => {
                                            let newState = [...state];
                                            for (let i = 0; i < newState.length; i++)
                                                newState[i][markingKey].hovered = true;
                                            return newState;
                                        })}
                                        onMouseLeave={e => setPagesMarkingVisualData((state) => {
                                            let newState = [...state];
                                            for (let i = 0; i < newState.length; i++)
                                                newState[i][markingKey].hovered = false;
                                            return newState;
                                        })}
                                        onClick={e => {
                                            if (markingVisualData.onClick)
                                                markingVisualData.onClick()
                                        }}
                                    />
                                })
                            }</>
                        })
                    }
                    {
                        (selection_toolkit_displaying && selection_toolkit_position.page == pageIndex) &&
                        <div
                            onMouseEnter={e => {
                                setMouseOnSelectionToolkit(true);
                            }}
                            onMouseLeave={e => {
                                setMouseOnSelectionToolkit(false);
                            }}
                            className={'selection-toolkit'}
                            style={{
                                top: `${100 * selection_toolkit_position.y / pageHeight}%`,
                                left: `${100 * selection_toolkit_position.x / pageWidth}%`,
                                zIndex: '70'
                            }}
                        >
                            {
                                props.selectionToolkitButtons.map((buttonData, buttonKey) => {
                                    return (
                                        <button
                                            className={'clickable selection-toolkit-button'}
                                            title={buttonData.name}
                                            onClick={(e) => {
                                                buttonData.callback(
                                                    current_selection_start,
                                                    current_selection_end,
                                                    selection_text
                                                );
                                            }}
                                        >
                                            <FontAwesomeIcon icon={buttonData.icon}/>
                                        </button>
                                    )
                                })
                            }
                        </div>
                        || <></>
                    }

                </div>
            )
        })
    }, [
        pages,
        props.selectionToolkitButtons,
        pages_marking_visual_data,
        selection_toolkit_displaying,
    ]);

    return (
        <div
            className={'optical-document-render-container'}
            ref={document_renderer_ref}
            onMouseDown={(e) => onMouseDownOnRenderer(e)}
            onMouseUp={(e) => onMouseUpOnRenderer(e)}
        >
            {
                loading_display &&
                <LoadingIcon color={'#000000'} width={200}/>
                ||
                <>
                    <div className={'optical-document-layer'}>{renderedPages}</div>
                    <div className={'optical-document-layer'}>{renderedHighlightsLayer}</div>
                </>
            }
        </div>
    )
}