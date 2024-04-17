import {Document, Page, pdfjs} from "react-pdf";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {createContext, useCallback, useContext, useEffect, useMemo, useRef, useState} from "react";
import {LoadingIcon} from "./loadingIcon";
import {model} from "../../model/model";
import styled from "styled-components";
import 'react-pdf/dist/esm/Page/TextLayer.css';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import {centerChildInParent, isElemVisibleWithinScrollableParent, smoothScroll} from "../../controller/functionality/dom-utils/domUtils";
import {CatchAndPassMouseInputs} from "./catchAndPassMouseInputs";
import {SVG_PATHS} from "../config/svgPaths";
import {CaseFileComment} from "./caseFileComment";


pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const OpticalFileDisplayContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
`

const OpticalFileDisplayToolbarContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    height: 40px;
    border-bottom: 1px solid #505050;
    background: #151515;
`

const OpticalFileDisplayToolbarButton = styled.button`
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 32px;
    height: 32px;
    margin: 4px 0 4px 4px;
    background: none;
    border-radius: 8px;
    border: none;
    cursor: ${({enabled}) => enabled ? 'pointer' : 'default'};
    pointer-events: ${({enabled}) => enabled ? 'auto' : 'none'};
    &:hover { 
        background: ${({enabled}) => enabled ? '#505050' : 'none'}; 
    }
    svg {
        width: 100%;
        height: 100%;
        fill: ${({enabled}) => enabled ? '#e0e0e0' : '#808080'};
    }
`

const OpticalFileDisplayRenderContainer = styled.div`
    width: 100%;
    height: calc(100% - 41px);
    overflow: auto;
    background: #202020;
    
    .react-pdf__Document {
        pointer-events: none !important;
        overflow: visible;
    }

    .react-pdf__Page {
        position: absolute !important;
        width: 100% !important;
        height: 100% !important;
        min-width: 0 !important;
        min-height: 0 !important;
        pointer-events: none !important;
    }

    .react-pdf__Page__canvas {
        width: 100% !important;
        height: 100% !important;
        pointer-events: none !important;
    }

    .react-pdf__message {
        display: none !important;
        pointer-events: none !important;
    }

    .react-pdf__Page__textContent {
        display: none !important;
        pointer-events: none !important;
    }
`

const OpticalFileDisplayPartsContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: 100%;
`

const OpticalFileDisplayFileRenderSection = styled.div`
    position: relative;
    display: block;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: visible;
`

const OpticalFileDisplayFileCommentsSection = styled.div`
    position: relative;
    display: block;
    width: 192px;
`

const OpticalFileDisplayRenderLayer = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    overflow: visible;
`

const OpticalFileDisplayPagesContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: visible;
`

const OpticalFileDisplayRenderDocumentPageContainer = styled.div`
    position: relative;
    width: calc(100% - 10px);
    height: 0;
    margin: 5px;
    overflow: visible;
    padding-bottom: ${({aspectratio}) => aspectratio * 100}%;
`

const OpticalFileDisplayLazyLoadingTestPage = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: none;
    background: white;
`

const OpticalFileDisplayRenderDocumentPageContent = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    overflow: hidden;
`

const OpticalFileDisplayPageInputCatcher = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: none;
    overflow: hidden;
    pointer-events: all;
    cursor: text;
    z-index: 5;
    user-select: none;
`

const OpticalFileDisplayRenderMarkings = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    background: none;
    overflow-x: visible;
    pointer-events: none;
    z-index: 10;
`

const PageMarkingSection = styled.div`
    position: absolute;
    top: calc(${({y1}) => y1 * 100}%${({highlighted}) => highlighted ? ' - 3px' : ''} - 3px);
    left: calc(${({x1}) => x1 * 100}%${({highlighted}) => highlighted ? ' - 3px' : ''} - 3px - 3px);
    width: calc(${({x2, x1}) => (x2 - x1) * 100}%${({highlighted}) => highlighted ? ' + 2px' : ''} + 6px);
    height: calc(${({y2, y1}) => (y2 - y1) * 100}%${({highlighted}) => highlighted ? ' + 2px' : ''} + 6px);
    background: #${({color}) => color.replace('#', '')}80;
    border: ${({highlighted, color}) => highlighted ? `3px solid ${color}` : 'none'};
    pointer-events: all;
    cursor: text;
`

export function OpticalFileDisplayRender(props) {

    const {fileId, caseId} = props;

    const caseFilesManager = model.services['caseFilesManager'];
    const caseCommentsManager = model.services['caseCommentsManager'];

    const [s_searchParams, setSearchParams] = useModelValueAsReactState('$.application.searchParams');

    const [s_fileData, setFileData] = useState({});

    const [s_caseFilesData, setCaseFilesData] = useModelValueAsReactState('$.cases.currentOpen.files.all', {});

    useEffect(() => setFileData(s_caseFilesData[fileId] || {}), [s_caseFilesData, fileId]);

    const [s_loading, setLoading] = useState(false);

    const r_container = useRef(null);

    const [s_currentPageIndex, setCurrentPageIndex] = useState({});

    const load = useCallback(async () => {
        setLoading(true);
        await caseFilesManager.fetchFileContentDownloadURLs(['extracted_text/text_structure', 'converted_file/pdf.pdf'], fileId, caseId);
        await caseFilesManager.fetchFileContent(['extracted_text/text_structure'], fileId, caseId);
        await caseCommentsManager.fetchFileComments(fileId);
        setLoading(false);
    }, [fileId, caseId]);

    useEffect(() => {
        load().then();
    }, [fileId, caseId]);

    const [s_loadedPages, setLoadedPages] = useState({});

    const [s_fileDisplayPdfData, setFileDisplayPdfData] = useState(undefined);
    const [s_fileDisplayTextStructure, setFileDisplayTextStructure] = useState(undefined);

    useEffect(() => {
        if (s_loading) return;
        const pdfUrl = ((s_fileData.content || {})['converted_file/pdf.pdf'] || {}).downloadUrl;
        if (!pdfUrl) return;
        setFileDisplayPdfData(pdfUrl);
    }, [s_loading, s_fileData]);

    useEffect(() => {
        if (s_loading) return;
        const textStructureContent = ((s_fileData.content || {})['extracted_text/text_structure'] || {}).downloadedContent;
        if (!textStructureContent) return;
        const parser = new DOMParser();
        const structure = parser.parseFromString(textStructureContent, "text/xml");
        OpticalFileDisplayRenderingUtils.fillHierarchyWithCharactersIfMissing(structure);
        setFileDisplayTextStructure(structure);
    }, [s_loading, s_fileData]);

    const m_pageGroups = useMemo(() => s_fileDisplayTextStructure ? Array.from(s_fileDisplayTextStructure.getElementsByTagName('gr')) : [], [s_fileDisplayTextStructure]);

    const m_pageAspectRatios = useMemo(() => {
        if (!s_fileDisplayTextStructure) return {};
        const aspectRatios = {};
        for (const groupNum in m_pageGroups) aspectRatios[groupNum] = OpticalFileDisplayRenderingUtils.getPageAspectRatio(s_fileDisplayTextStructure, groupNum);
        return aspectRatios;
    }, [m_pageGroups]);

    useEffect(() => {
        const loadedPages = {};
        for (const groupNum in m_pageGroups) loadedPages[groupNum] = false;
        setLoadedPages(loadedPages);
    }, [m_pageGroups]);

    const [s_mouseDown, setMouseDown] = useState(false);
    const [s_mouseStartData, setMouseStartData] = useState({page: 0, x: 0, y: 0});
    const [s_mouseEndData, setMouseEndData] = useState({page: 0, x: 0, y: 0});

    const [s_textMarkings, setTextMarkings] = useState({});

    const c_onMouseDownOnPage = useCallback((page, mouseEvent) => {
        mouseEvent.stopPropagation();
        const rect = mouseEvent.currentTarget.getBoundingClientRect();
        const mouseX = (mouseEvent.clientX - rect.left) / rect.width;
        const mouseY = (mouseEvent.clientY - rect.top) / rect.height;
        const positionData = {page: page, x: mouseX, y: mouseY};
        setMouseStartData(positionData);
        setMouseEndData(positionData);
        setMouseDown(true);
    }, []);

    const c_onMouseMoveOnPage = useCallback((page, mouseEvent) => {
        mouseEvent.stopPropagation();
        if (!s_mouseDown) return;
        const rect = mouseEvent.currentTarget.getBoundingClientRect();
        const mouseX = (mouseEvent.clientX - rect.left) / rect.width;
        const mouseY = (mouseEvent.clientY - rect.top) / rect.height;
        const positionData = {page: page, x: mouseX, y: mouseY};
        setMouseEndData(positionData);
    }, [s_mouseDown]);

    const c_onMouseUpOnPage = useCallback((page, mouseEvent) => {
        mouseEvent.stopPropagation();
        setMouseDown(false);
    }, []);

    const [s_scrollToMarking, setScrollToMarking] = useState(null);

    useEffect(() => {
        if (!s_scrollToMarking) return;
        if (!s_fileDisplayTextStructure) return;
        if (!r_container.current) return;
        OpticalFileDisplayRenderingUtils.scrollToMarking(s_fileDisplayTextStructure, s_scrollToMarking, r_container.current);
        setScrollToMarking(null);
    }, [s_scrollToMarking, s_fileDisplayTextStructure, r_container.current]);

    useEffect(() => {
        if (!s_fileDisplayTextStructure) return;
        let deltaX = Math.abs(s_mouseEndData.x - s_mouseStartData.x);
        let deltaY = Math.abs(s_mouseEndData.y - s_mouseStartData.y);
        if (deltaX + deltaY < 0.025) {
            setTextMarkings((m) => ({...m, userSelection: null}));
            return;
        }
        let userSelectionMarking = OpticalFileDisplayRenderingUtils.getUserSelectionMarkingDataForUserInput(s_fileDisplayTextStructure, s_mouseStartData, s_mouseEndData);
        userSelectionMarking = {...userSelectionMarking, color: '#2ecdf1'}
        setTextMarkings((m) => ({...m, userSelection: userSelectionMarking}));
    }, [s_fileDisplayTextStructure, s_mouseStartData, s_mouseEndData]);

    const [s_targetComment, setTargetComment] = useModelValueAsReactState('$.cases.currentOpen.comments.targetCommentId');

    const [s_markedComment, setMarkedComment] = useState(null);

    useEffect(() => {
        if (!s_targetComment) return;
        setMarkedComment(s_targetComment);
    }, [s_targetComment]);

    useEffect(() => {
        if (!s_fileData) return;
        const fileComments = s_fileData.comments || [];
        setTextMarkings((markings) => {
            const newMarkings = {...(markings || {})};
            for (const markingId in newMarkings) {
                const marking = newMarkings[markingId];
                if (marking && marking.comment) delete newMarkings[markingId];
            }
            for (const commentId of fileComments) {
                const comment = model.cases.currentOpen.comments.data[commentId];
                newMarkings[commentId] = {
                    comment: commentId,
                    start: {page: comment.from_page, char: comment.from_char,},
                    end: {page: comment.to_page, char: comment.to_char,},
                    color: comment.color,
                    highlighted: commentId === s_targetComment,
                };
            }
            return newMarkings;
        });
    }, [s_fileData.comments, s_targetComment]);

    useEffect(() => {
        if (!s_markedComment) return;
        const commentMarking = s_textMarkings[s_markedComment];
        if (!commentMarking) return;
        setScrollToMarking(commentMarking);
        setMarkedComment(null);
    }, [s_textMarkings, s_markedComment])

    const m_isTextSelected = useMemo(() => {
        const userSelection = s_textMarkings.userSelection;
        if (!userSelection) return false;
        if (userSelection.start.page !== userSelection.end.page) return true;
        if (Math.abs(userSelection.start.char - userSelection.end.char) > 0) return true;
        return false;
    }, [s_textMarkings]);

    const [s_copiedText, setCopiedText] = useState(false);

    const c_copy = useCallback((e) => {
        if (s_copiedText) return;
        if (!m_isTextSelected) return;
        const userSelection = s_textMarkings.userSelection;
        if (!userSelection) return;
        const selectedText = OpticalFileDisplayRenderingUtils.getMarkedText(s_fileDisplayTextStructure, userSelection);
        navigator.clipboard.writeText(selectedText);
        setCopiedText(true);
        setTimeout(() => setCopiedText(false), 3000);
    }, [s_fileDisplayTextStructure, s_textMarkings, s_copiedText, m_isTextSelected]);

    const [s_addingComment, setAddingComment] = useState(false);

    const c_addComment = useCallback(async () => {
        if (s_addingComment) return;
        if (!m_isTextSelected) return;
        if (!s_fileDisplayTextStructure) return;
        const userSelection = s_textMarkings.userSelection;
        if (!userSelection) return;
        setAddingComment(true);
        const selectedText = OpticalFileDisplayRenderingUtils.getMarkedText(s_fileDisplayTextStructure, userSelection);
        const commentData = {
            from_char: userSelection.start.char,
            to_char: userSelection.end.char,
            from_page: userSelection.start.page,
            to_page: userSelection.end.page,
            marked_text: selectedText,
            comment_text: '',
            color: '#12c258',
        }
        await caseCommentsManager.putFileComment(commentData);
        await caseCommentsManager.fetchFileComments(null, true);
        setAddingComment(false)
    }, [m_isTextSelected, s_textMarkings]);

    const [s_currentSearchText, setCurrentSearchText] = useState('');
    const [s_searchResultsData, setSearchResultsData] = useModelValueAsReactState('$.cases.currentOpen.search.results');
    const [s_targetResultIndex, setTargetResultIndex] = useModelValueAsReactState('$.cases.currentOpen.search.targetResultIndex');

    useEffect(() => {
        setCurrentSearchText(s_searchParams.s || '');
    }, [s_searchParams]);

    const c_calculateSearchResultsMarkingData = useCallback((searchResults) => {
        if (!s_fileDisplayTextStructure) return;
        searchResults.forEach((result, resultIndex) => {
            if (result.file_id !== fileId) return;
            const markingData = result.markingData || OpticalFileDisplayRenderingUtils.getMarkingDataFromSearchResult(s_fileDisplayTextStructure, result);
            if (!markingData) return;
            result.markingData = {
                ...markingData,
                searchResult: true,
                highlighted: resultIndex.toString() === s_targetResultIndex.toString(),
                color: '#0033ff'
            };
        });
    }, [s_fileDisplayTextStructure, fileId, s_targetResultIndex]);

    const c_applySearchResultsToMarkings = useCallback((searchResults) => {
        setTextMarkings((markings) => {
            const newMarkings = {...(markings || {})};
            for (const markingId in newMarkings) {
                const marking = newMarkings[markingId];
                if (marking && marking.searchResult) delete newMarkings[markingId];
            }
            let c = 0;
            for (const searchResult of searchResults) {
                if (searchResult.file_id !== fileId) continue;
                newMarkings[`sr-${c}`] = searchResult.markingData;
                c++; // :)
            }
            return newMarkings;
        });
    }, [fileId]);

    const c_searchSelected = useCallback((e) => {
        if (!m_isTextSelected) return;
        if (!s_fileDisplayTextStructure) return;
        const userSelection = s_textMarkings.userSelection;
        if (!userSelection) return;
        const selectedText = OpticalFileDisplayRenderingUtils.getMarkedText(s_fileDisplayTextStructure, userSelection);
        setSearchParams(p => ({...p, s: selectedText}));
    }, [s_fileDisplayTextStructure, s_textMarkings, m_isTextSelected]);

    useEffect(() => {
        const currentSearchResults = s_searchResultsData[s_currentSearchText] || [];
        c_calculateSearchResultsMarkingData(currentSearchResults);
        c_applySearchResultsToMarkings(currentSearchResults);
        model.cases.currentOpen.search.results[s_currentSearchText] = currentSearchResults;
    }, [s_currentSearchText, s_searchResultsData, c_applySearchResultsToMarkings, c_calculateSearchResultsMarkingData, s_targetResultIndex]);

    useEffect(() => {
        if (!s_fileDisplayTextStructure) return;
        if (s_targetResultIndex < 0) return;
        const currentSearchResults = s_searchResultsData[s_currentSearchText] || [];
        if (!currentSearchResults) return;
        const targetSearchResult = currentSearchResults[s_targetResultIndex];
        if (!targetSearchResult) return;
        const markingData = targetSearchResult.markingData;
        setScrollToMarking(markingData);
    }, [s_targetResultIndex, s_fileDisplayTextStructure, s_currentSearchText, s_searchResultsData]);

    const m_lazyLoadingTestLayer = useMemo(() => <>
        <OpticalFileDisplayPagesContainer>
            {m_pageGroups.map((group, groupNum) => <>
                <OpticalFileDisplayRenderDocumentPageContainer key={`lazyloadingpagecontainer-${groupNum}`} aspectratio={m_pageAspectRatios[groupNum] || 0}>
                    <OpticalFileDisplayLazyLoadingTestPage key={`lazyloadingtestpage-${groupNum}`} className={`lazy-loading-test-page ${groupNum}`}/>
                    <LoadingIcon key={`loadingicon-${groupNum}`} width={'20px'} height={'20px'} color={'black'}/>
                </OpticalFileDisplayRenderDocumentPageContainer>
            </>)}
        </OpticalFileDisplayPagesContainer>
    </>, [m_pageGroups]);

    const m_pagesVisualLayer = useMemo(() => <>
        <OpticalFileDisplayPagesContainer>{m_pageGroups.map((group, groupNum) => <>
                <OpticalFileDisplayRenderDocumentPageContainer key={`pagescontainer-${groupNum}`} aspectratio={m_pageAspectRatios[groupNum] || 0}>
                    {Math.abs(s_currentPageIndex - groupNum) > 2 && false ? <></> : <>
                        <OpticalFileDisplayRenderDocumentPageContent key={`content-${groupNum}`}>
                            <Page
                                key={`page-${groupNum}`}
                                pageNumber={groupNum+1}
                                onLoadSuccess={() => setLoadedPages((p) => ({...p, [groupNum]: true}))}
                                onLoadError={console.error}
                            />
                        </OpticalFileDisplayRenderDocumentPageContent>
                    </>}
                </OpticalFileDisplayRenderDocumentPageContainer>
            </>
        )}</OpticalFileDisplayPagesContainer>
    </>, [m_pageGroups, m_pageAspectRatios, s_currentPageIndex]);

    const m_pageInputsLayer = useMemo(() => <>{!s_fileDisplayTextStructure ? <></> : <>
        <OpticalFileDisplayPagesContainer>{Object.keys(s_loadedPages).map((loaded, groupNum) => <>
            <OpticalFileDisplayRenderDocumentPageContainer key={`inputscontainer-${groupNum}`} aspectratio={m_pageAspectRatios[groupNum] || 0}>
                {Math.abs(s_currentPageIndex - groupNum) > 2 && false ? <></> : <>
                    {loaded && <OpticalFileDisplayPageInputCatcher
                        key={`inputcatcher-${groupNum}`}
                        onMouseDown={(e) => c_onMouseDownOnPage(groupNum, e)}
                        onMouseMove={(e) => c_onMouseMoveOnPage(groupNum, e)}
                        onMouseUp={(e) => c_onMouseUpOnPage(groupNum, e)}
                    /> || <></>}
                </>}
            </OpticalFileDisplayRenderDocumentPageContainer>
        </>)}</OpticalFileDisplayPagesContainer>
    </>}</>, [s_fileDisplayTextStructure, s_loadedPages, m_pageAspectRatios, s_currentPageIndex, c_onMouseDownOnPage, c_onMouseMoveOnPage, c_onMouseUpOnPage]);

    const m_pageMarkingsSections = useMemo(() => {
        if (!s_fileDisplayTextStructure) return {};
        const textMarkingElementsPerPage = {};
        for (const markingName in s_textMarkings) {
            const markingData = s_textMarkings[markingName];
            if (!markingData) continue;
            const textMarkingRectangles = OpticalFileDisplayRenderingUtils.getMarkingSectionRectangles(s_fileDisplayTextStructure, markingData);
            for (const pageNum in textMarkingRectangles) {
                textMarkingElementsPerPage[pageNum] = textMarkingElementsPerPage[pageNum] || [];
                const pageRectangles = textMarkingRectangles[pageNum];
                for (const rectangle of pageRectangles) {
                    if (rectangle.reduce((a, b) => a + b, 0) === 0) continue;
                    const [x1, y1, x2, y2] = rectangle;
                    const markingSectionElement = <CatchAndPassMouseInputs key={`markingsectioninputswrapper-${pageNum}-${markingName}-${x1}-${y1}-${x2}-${y2}`}>
                        <PageMarkingSection
                            key={`markingsection-${pageNum}-${markingName}-${x1}-${y1}-${x2}-${y2}`}
                            x1={x1} y1={y1} x2={x2} y2={y2}
                            color={markingData.color || '#2ef184'}
                            highlighted={markingData.highlighted}
                            onMouseDown={() => {}}
                            onMouseMove={() => {}}
                            onMouseUp={() => {}}
                        />
                    </CatchAndPassMouseInputs>;
                    textMarkingElementsPerPage[pageNum].push(markingSectionElement);
                }
            }
            if (markingData.comment) {
                const commentMarkingSectionRectangles = textMarkingRectangles[markingData.start.page] || [];
                if (commentMarkingSectionRectangles.length > 1) {
                    const firstCharacterY = commentMarkingSectionRectangles[1][1];
                    const commentElement = <OpticalFileDisplayComment
                        key={`comment-${markingName}`}
                        y={`${firstCharacterY * 100}%`}
                        commentId={markingData.comment}
                        color={markingData.color}
                    />;
                    textMarkingElementsPerPage[markingData.start.page].push(commentElement);
                }
            }
        }
        return textMarkingElementsPerPage;
    }, [s_fileDisplayTextStructure, s_textMarkings]);

    useEffect(() => {
        if (!r_container.current) return;
        const characterElements = Array.from(r_container.current.getElementsByClassName('optical-file-display-comment-container'))
        const commentsArray = characterElements.map(comment => ({
            element: comment,
            top: comment.offsetTop,
            height: comment.offsetHeight
        }));
        commentsArray.sort((a, b) => a.top - b.top);
        for (let i = 0; i < commentsArray.length; i++) {
            for (let j = i + 1; j < commentsArray.length; j++) {
                if (commentsArray[j].top >= commentsArray[i].top + commentsArray[i].height + 8) break;
                const newTop = commentsArray[i].top + commentsArray[i].height + 8;
                commentsArray[j].element.style.top = `${newTop}px`;
                commentsArray[j].top = newTop;
            }
        }
    }, [r_container.current, m_pageMarkingsSections]);

    const m_pageMarkingsLayer = useMemo(() => <>
        <OpticalFileDisplayPagesContainer>{Object.keys(s_loadedPages).map((loaded, groupNum) => <>
            <OpticalFileDisplayRenderDocumentPageContainer key={`markingscontainer-${groupNum}`} aspectratio={m_pageAspectRatios[groupNum] || 0} >
                {Math.abs(s_currentPageIndex - groupNum) > 2 && false ? <></> : <>
                    <OpticalFileDisplayRenderMarkings key={`markings-${groupNum}`} id={`pageMarkingLayer-${groupNum}`}>{
                        loaded && m_pageMarkingsSections[groupNum] || <></>
                    }</OpticalFileDisplayRenderMarkings>
                </>}
            </OpticalFileDisplayRenderDocumentPageContainer>
        </>)}</OpticalFileDisplayPagesContainer>
    </>, [s_loadedPages, m_pageMarkingsSections, s_currentPageIndex]);

    useEffect(() => {
        if (!r_container.current) return (() => {});
        const resolveCurrentPage = () => {
            if (!r_container.current) return;
            let pageElements = Array.from(r_container.current.getElementsByClassName('lazy-loading-test-page'));
            for (let pageIndex = 0; pageIndex < pageElements.length; pageIndex++) {
                let pageElement = pageElements[pageIndex];
                if (!pageElement) continue;
                if (isElemVisibleWithinScrollableParent(pageElement, r_container.current)) {
                    setCurrentPageIndex(pageIndex);
                    return;
                }
            }
            setCurrentPageIndex(0);
        }
        resolveCurrentPage();
        r_container.current.addEventListener('scroll', resolveCurrentPage);
        return () => r_container.current && r_container.current.removeEventListener('scroll', resolveCurrentPage);
    }, [r_container.current]);

    useEffect(() => {
        document.addEventListener('copy', c_copy);
        return () => document.removeEventListener('copy', c_copy);
    }, [c_copy]);

    return <>
        <OpticalFileDisplayContainer>
            <OpticalFileDisplayToolbarContainer>
                <OpticalFileDisplayToolbarButton title={'copy'} enabled={m_isTextSelected} onClick={c_copy}>
                    <svg viewBox={'0 0 1000 1000'}><path d={s_copiedText ? SVG_PATHS.checkMark : SVG_PATHS.copy}/></svg>
                </OpticalFileDisplayToolbarButton>
                <OpticalFileDisplayToolbarButton title={'add comment'} enabled={m_isTextSelected && !s_addingComment} onClick={c_addComment}>
                    {s_addingComment ? <LoadingIcon width={'20px'} height={'20px'}/> : <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.addComment}/></svg>}
                </OpticalFileDisplayToolbarButton>
                <OpticalFileDisplayToolbarButton title={'search selected'} enabled={m_isTextSelected && !s_addingComment} onClick={c_searchSelected}>
                    <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.search}/></svg>
                </OpticalFileDisplayToolbarButton>
            </OpticalFileDisplayToolbarContainer>
            <OpticalFileDisplayRenderContainer ref={r_container}>
                {s_loading ? <>
                    <LoadingIcon width={'20px'} height={'20px'}/>
                </> : <>
                    <OpticalFileDisplayPartsContainer>
                        <OpticalFileDisplayFileRenderSection>
                            {(s_fileData && s_fileDisplayTextStructure && s_fileDisplayPdfData && m_pageGroups) ? <>
                                <Document file={s_fileDisplayPdfData} loading={''} error={''} noData={''}>
                                    <OpticalFileDisplayRenderLayer>{m_lazyLoadingTestLayer}</OpticalFileDisplayRenderLayer>
                                    <OpticalFileDisplayRenderLayer>{m_pagesVisualLayer}</OpticalFileDisplayRenderLayer>
                                    <OpticalFileDisplayRenderLayer>{m_pageInputsLayer}</OpticalFileDisplayRenderLayer>
                                    <OpticalFileDisplayRenderLayer>{m_pageMarkingsLayer}</OpticalFileDisplayRenderLayer>
                                </Document>
                            </> : <>
                                <LoadingIcon width={'20px'} height={'20px'}/>
                            </> }
                        </OpticalFileDisplayFileRenderSection>
                        <OpticalFileDisplayFileCommentsSection/>
                    </OpticalFileDisplayPartsContainer>
                </>}
            </OpticalFileDisplayRenderContainer>
        </OpticalFileDisplayContainer>
    </>
}

const OpticalFileDisplayFileCommentContainer = styled.div`
    position: absolute;
    display: flex;
    flex-direction: column;
    width: calc(196px - 32px - 4px);
    height: max-content;
    max-height: 512px;
    border-radius: 4px;
    overflow-x: visible;
    overflow-y: visible;
    background: #e0e0e0;
    margin: 8px;
    padding: 4px;
    left: 100%;
    top: ${({y}) => y};
    pointer-events: all;
    border-left: 4px solid ${({color}) => color || '#2ecdf1'}a0;
`

function OpticalFileDisplayComment(props) {
    return <>
        <OpticalFileDisplayFileCommentContainer
            y={props.y}
            color={props.color}
            className={'optical-file-display-comment-container'}
        >
            <CaseFileComment commentId={props.commentId}/>
        </OpticalFileDisplayFileCommentContainer>
    </>
}

class OpticalFileDisplayRenderingUtils {
    static getElementBoundingRectangle(characterElement) {
        const r = characterElement.getAttribute('r') || '0-0-0-0';
        const rect_values = r.split('-');
        const x1 = parseFloat(rect_values[0]);
        const y1 = parseFloat(rect_values[1]);
        const x2 = parseFloat(rect_values[2]);
        const y2 = parseFloat(rect_values[3]);
        return [x1, y1, x2, y2];
    }

    static getBoundingRectangleForRectangles(rectangles) {
        if (rectangles.length === 0) return [0, 0, 0, 0];
        const boundingRect = [...rectangles[0]];
        for (let i = 1; i < rectangles.length; i++) {
            const r = rectangles[i];
            boundingRect[0] = Math.min(boundingRect[0], r[0]);
            boundingRect[1] = Math.min(boundingRect[1], r[1]);
            boundingRect[2] = Math.max(boundingRect[2], r[2]);
            boundingRect[3] = Math.max(boundingRect[3], r[3]);
        }
        return boundingRect;
    }

    static normalizeRectangleForPageSize(rectangle, pageSize) {
        const normalizedRectangle = [...rectangle];
        normalizedRectangle[0] /= pageSize[0];
        normalizedRectangle[1] /= pageSize[1];
        normalizedRectangle[2] /= pageSize[0];
        normalizedRectangle[3] /= pageSize[1];
        return normalizedRectangle;
    }

    static getPageSize(textStructure, pageNum) {
        const sizeMetadataElements = Array.from(textStructure.getElementsByTagName("image_size"));
        const pageSizeMetadata = sizeMetadataElements[pageNum];
        const pageWidth = parseInt(pageSizeMetadata.getAttribute('w') || '0');
        const pageHeight = parseInt(pageSizeMetadata.getAttribute('h') || '0');
        return [pageWidth, pageHeight];
    }

    static getPageAspectRatio(textStructure, pageNum) {
        const pageSize = OpticalFileDisplayRenderingUtils.getPageSize(textStructure, pageNum);
        return pageSize[1] / pageSize[0];
    }

    static getMarkedText(textStructure, textMarkingData) {
        const pageGroups = Array.from(textStructure.getElementsByTagName('gr'));
        const startPage = textMarkingData.start.page;
        const startChar = textMarkingData.start.char;
        const endPage = textMarkingData.end.page;
        const endChar = textMarkingData.end.char;

        let markedText = '';
        for (let pageNum = startPage; pageNum <= endPage; pageNum++) {
            const pageGroup = pageGroups[pageNum];
            if (!pageGroup) continue;
            let pageCharacters = Array.from(pageGroup.getElementsByTagName('cr'));
            if (pageNum === startPage && pageNum === endPage) pageCharacters = pageCharacters.slice(startChar, endChar + 1);
            else if (pageNum === startPage) pageCharacters = pageCharacters.slice(startChar);
            else if (pageNum === endPage) pageCharacters = pageCharacters.slice(0, endChar + 1);

            let currentSectionLineParent = null;
            let currentSectionWordParent = null;
            for (const character of pageCharacters) {
                const characterLineParent = OpticalFileDisplayRenderingUtils.getElementParentByTagName(character, 'ln');
                const characterWordParent = OpticalFileDisplayRenderingUtils.getElementParentByTagName(character, 'wd');
                if (characterLineParent !== currentSectionLineParent) {
                    markedText += '\n';
                    currentSectionLineParent = characterLineParent;
                }
                if (characterWordParent !== currentSectionWordParent) {
                    markedText += ' ';
                    currentSectionWordParent = characterWordParent;
                }
                markedText += character.getAttribute('v') || character.textContent || '';
            }
        }
        markedText = markedText.trim();
        return markedText
    }

    static getMarkingSectionRectangles(textStructure, textMarkingData) {
        const pageGroups = Array.from(textStructure.getElementsByTagName('gr'));
        const startPage = textMarkingData.start.page;
        const startChar = textMarkingData.start.char;
        const endPage = textMarkingData.end.page;
        const endChar = textMarkingData.end.char;

        const markingSectionRectanglesPerPage = {}
        for (let pageNum = startPage; pageNum <= endPage; pageNum++) {
            const pageGroup = pageGroups[pageNum];
            if (!pageGroup) continue;
            let pageCharacters = Array.from(pageGroup.getElementsByTagName('cr'));
            if (pageNum === startPage && pageNum === endPage) pageCharacters = pageCharacters.slice(startChar, endChar + 1);
            else if (pageNum === startPage) pageCharacters = pageCharacters.slice(startChar);
            else if (pageNum === endPage) pageCharacters = pageCharacters.slice(0, endChar + 1);

            markingSectionRectanglesPerPage[pageNum] = [];
            let currentMarkingSectionCharacters = [];
            let currentSectionLineParent = null;
            const processSectionCharacters = (sectionCharacters) => {
                const sectionCharactersBoundingRectangles = sectionCharacters.map(c => OpticalFileDisplayRenderingUtils.getElementBoundingRectangle(c));
                const sectionBoundingRectangle = OpticalFileDisplayRenderingUtils.getBoundingRectangleForRectangles(sectionCharactersBoundingRectangles);
                const normalizedSectionBoundingRectangle = OpticalFileDisplayRenderingUtils.normalizeRectangleForPageSize(sectionBoundingRectangle, OpticalFileDisplayRenderingUtils.getPageSize(textStructure, pageNum));
                markingSectionRectanglesPerPage[pageNum].push(normalizedSectionBoundingRectangle);
            }

            for (const character of pageCharacters) {
                const characterLineParent = OpticalFileDisplayRenderingUtils.getElementParentByTagName(character, 'ln');
                if (characterLineParent === currentSectionLineParent) {
                    currentMarkingSectionCharacters.push(character);
                    continue;
                }
                processSectionCharacters(currentMarkingSectionCharacters);
                currentMarkingSectionCharacters = [character];
                currentSectionLineParent = characterLineParent;
            }
            processSectionCharacters(currentMarkingSectionCharacters);
        }
        return markingSectionRectanglesPerPage;
    }

    static getElementParentByTagName(element, tagName) {
        let currentElement = element;
        while (currentElement && currentElement.tagName !== tagName) currentElement = currentElement.parentElement;
        return currentElement;
    }

    static getUserSelectionMarkingDataForUserInput(textStructure, inputStart, inputEnd) {
        const pageGroups = Array.from(textStructure.getElementsByTagName('gr'));

        const calculateForOrientation = (startInput, endInput) => {
            const startPage = pageGroups[startInput.page];
            const endPage = pageGroups[endInput.page];
            if (!startPage) return {};
            if (!endPage) return {};

            const startPageCharacters = startPage.querySelectorAll('cr');
            const startPageSize = OpticalFileDisplayRenderingUtils.getPageSize(textStructure, startInput.page);
            let startCharacterIndex;
            for (startCharacterIndex = 0; startCharacterIndex < startPageCharacters.length; startCharacterIndex++) {
                const character = startPageCharacters[startCharacterIndex];
                const characterRect = OpticalFileDisplayRenderingUtils.getElementBoundingRectangle(character);
                const normalizedCharacterRect = OpticalFileDisplayRenderingUtils.normalizeRectangleForPageSize(characterRect, startPageSize);
                if (normalizedCharacterRect[1] > startInput.y || (normalizedCharacterRect[3] > startInput.y && normalizedCharacterRect[2] > startInput.x)) break;
            }

            const endPageCharacters = endPage.querySelectorAll('cr');
            const endPageSize = OpticalFileDisplayRenderingUtils.getPageSize(textStructure, endInput.page);
            let endCharacterIndex;
            for (endCharacterIndex = endPageCharacters.length - 1; endCharacterIndex >= 0; endCharacterIndex--) {
                const character = endPageCharacters[endCharacterIndex];
                const characterRect = OpticalFileDisplayRenderingUtils.getElementBoundingRectangle(character);
                const normalizedCharacterRect = OpticalFileDisplayRenderingUtils.normalizeRectangleForPageSize(characterRect, endPageSize);
                if (normalizedCharacterRect[3] < endInput.y || (normalizedCharacterRect[1] < endInput.y && normalizedCharacterRect[0] < endInput.x)) break;
            }
            endCharacterIndex = endCharacterIndex >= 0 ? endCharacterIndex : 0;

            return {
                start: {page: startInput.page, char: startCharacterIndex},
                end: {page: endInput.page, char: endCharacterIndex}
            }
        }

        const regularOrientation = calculateForOrientation(inputStart, inputEnd);
        const reversedOrientation = calculateForOrientation(inputEnd, inputStart);

        const comparison = inputStart.page === inputEnd.page ? (
            (regularOrientation.end.char - regularOrientation.start.char) - (reversedOrientation.end.char - reversedOrientation.start.char)
        ) : (
            inputEnd.page - inputStart.page
        );

        return comparison > 0 ? regularOrientation : reversedOrientation;
    }

    static getMarkingDataFromSearchResult(textStructure, searchResult) {
        const startText = searchResult.start_text.replace(/ |\n/g, '');
        const endText = searchResult.end_text.replace(/ |\n/g, '');
        const highlightedText = searchResult.highlighted_text.replace(/ |\n/g, '');
        const searchString = startText + highlightedText + endText;
        const document_characters = Array.from(textStructure.getElementsByTagName('cr'));
        for (let character_index = 0; character_index < document_characters.length; character_index++) {
            let searchResultStartIndex = undefined;
            let searchResultEndIndex = undefined;
            let searchIndex = 0;
            for (let characterIndex = character_index; characterIndex < document_characters.length; characterIndex++) {
                let character = document_characters[characterIndex];
                let characterValue = (character.textContent || character.getAttribute('v')) || character.textContent || '';
                if (['\n', ' '].includes(characterValue)) continue;
                const searchCharacter = searchString[searchIndex];
                if (searchCharacter !== characterValue) break;
                if (searchIndex === startText.length) searchResultStartIndex = characterIndex;
                if (searchIndex === startText.length + highlightedText.length) searchResultEndIndex = characterIndex;
                if (searchIndex >= searchString.length - 1) {
                    if (searchResultStartIndex !== undefined && searchResultEndIndex !== undefined) {
                        return OpticalFileDisplayRenderingUtils.getMarkingDataForAbsoluteCharacterIndices(textStructure, searchResultStartIndex, searchResultEndIndex - 1);
                    }
                }
                searchIndex++;
            }
        }
    }

    static getMarkingDataForAbsoluteCharacterIndices(textStructure, startCharAbosoluteIndex, endCharAbsoluteIndex) {
        const pageGroups = Array.from(textStructure.getElementsByTagName('gr'));
        let startChar = startCharAbosoluteIndex;
        let endChar = endCharAbsoluteIndex;
        let startPage = null;
        let endPage = null;
        for (let groupNum = 0; groupNum < pageGroups.length; groupNum++) {
            const pageGroup = pageGroups[groupNum];
            const pageCharacterCount = Array.from(pageGroup.getElementsByTagName('cr')).length;
            if (!startPage) {
                if (startChar <= pageCharacterCount) startPage = groupNum;
                else startChar -= pageCharacterCount;
            }
            if (!endPage) {
                if (endChar <= pageCharacterCount) endPage = groupNum;
                else endChar -= pageCharacterCount;
            }
            if (startPage !== null && endPage !== null) break;
        }
        if (!(startPage !== null && endPage !== null)) return;
        return {
            start: {
                page: startPage,
                char: startChar
            },
            end: {
                page: endPage,
                char: endChar
            }
        }
    }

    static async scrollToMarking(textStructure, markingData, documentScrollableParnet) {
        const markingStartPage = markingData.start.page;
        const markingStartChar = markingData.start.char;
        const pageElementId = `pageMarkingLayer-${markingStartPage}`;
        const pageElement = document.getElementById(pageElementId);
        if (!pageElement) return;
        const structureCharacterElement = textStructure.getElementsByTagName('gr')[markingStartPage].getElementsByTagName('cr')[markingStartChar];
        const structureCharacterRect = OpticalFileDisplayRenderingUtils.getElementBoundingRectangle(structureCharacterElement);
        const pageSize = OpticalFileDisplayRenderingUtils.getPageSize(textStructure, markingStartPage);
        const normalizedStructureCharacterRect = OpticalFileDisplayRenderingUtils.normalizeRectangleForPageSize(structureCharacterRect, pageSize);
        let characterElement = document.createElement('div');
        characterElement.style.position = 'absolute';
        characterElement.style.width = '1px';
        characterElement.style.height = '1px';
        characterElement.style.left = `${normalizedStructureCharacterRect[0] * 100}%`;
        characterElement.style.top = `${normalizedStructureCharacterRect[1] * 100}%`;
        characterElement = pageElement.appendChild(characterElement);
        await centerChildInParent(characterElement, documentScrollableParnet);
        pageElement.removeChild(characterElement);
    }

    static fillHierarchyWithCharactersIfMissing(textStructure) {
        const structureWords = Array.from(textStructure.getElementsByTagName('wd'));
        for (const word of structureWords) {
            const wordCharacters = Array.from(word.getElementsByTagName('cr'));
            if (wordCharacters.length > 0) continue;
            const wordRect = OpticalFileDisplayRenderingUtils.getElementBoundingRectangle(word);
            const wordValue = word.textContent;
            word.textContent = '';
            const characterRectWidth = (wordRect[2] - wordRect[0]) / wordValue.length;
            for (let i = 0; i < wordValue.length; i++) {
                const character = textStructure.createElement('cr');
                character.textContent = wordValue[i];
                const newBoundingRectangle = [...wordRect];
                newBoundingRectangle[0] += i * characterRectWidth;
                newBoundingRectangle[2] = newBoundingRectangle[0] + characterRectWidth;
                character.setAttribute('r', newBoundingRectangle.join('-'));
                word.appendChild(character);
            }
        }
    }
}
