import {useParams} from "react-router-dom";
import styled from "styled-components";
import {useCallback, useEffect, useRef, useState} from "react";
import {TabbedDisplay} from "../../../../../components/tabbedDisplay";
import {CaseFileData} from "../../../../../components/caseFileData";
import {OpticalFileDisplayRender} from "../../../../../components/opticalFileDisplayRender";
import {model} from "../../../../../../model/model";
import {CaseTextSearch} from "../../../../../components/caseTextSearch";
import {useModelValueAsReactState} from "../../../../../../controller/functionality/model/modelReactHooks";
import {CaseFileComment} from "../../../../../components/caseFileComment";
import {VerticalGap} from "../../../../../components/verticalGap";
import {CaseKnowledgeGraphDisplay} from "../../../../../components/caseKnowledgeGraphDisplay";

const FileDisplayContainer = styled.div`
    position: relative;
    display: flex;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    overflow: hidden;
    ${({orientation}) => 
            (orientation === 'horizontal') ? 
            'flex-direction: row;' : 
            'flex-direction: column;'
    }
`

const FileDisplayFileContent = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 0;
    margin: 0;
    ${({orientation}) => 
            (orientation === 'horizontal') ?
            'width: 65%; height: 100%; max-width: 65%; max-height: 100%;' :
            'width: 100%; height: 50%; max-width: 100%; max-height: 50%;'
    }
`

const FileDisplayFileData = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 0;
    margin: 0;
    background: #202020;
    ${({orientation}) =>
            (orientation === 'horizontal') ?
            'width: calc(35% - 1px); height: 100%; max-width: calc(35% - 1px); max-height: 100%; border-left: 1px solid #808080;' :
            'width: 100%; height: calc(50% - 1px); max-width: 100%; max-height: calc(50% - 1px); border-top: 1px solid #808080;'
    }
`

const CaseFileDataContainer = styled.div`
    position: relative;
    width: calc(100% - 32px);
    height: max-content;
    overflow: hidden;
    padding: 32px;
`

const CaseFileSearchContainer = styled.div`
    display: flex;
    flex-direction: column;
    position: relative;
    width: 100%;
    height: 100%;
    overflow: auto;
    &::-webkit-scrollbar { display: none; }
`

export function CaseFileDisplay(props) {

    model.application.pages.currentPage.name = "CaseFile";

    const {caseId, fileId} = useParams();

    const [s_searchParams, setSearchParams] = useModelValueAsReactState('$.application.searchParams');

    const [s_selectedTab, setSelectedTab] = useState('Info');

    const r_container = useRef(null);

    const [s_displayOrientation, setDisplayOrientation] = useState('horizontal');

    useEffect(() => {
        model.cases.currentOpen.id = caseId;
        model.cases.currentOpen.files.currentOpen.id = fileId;
    }, [fileId, caseId]);

    useEffect(() => {
        if (!r_container.current) return;
        const updateOrientation = () => {
            if (!r_container.current) return;
            const {width, height} = r_container.current.getBoundingClientRect();
            if (width > height) setDisplayOrientation('horizontal');
            else setDisplayOrientation('vertical');
        };
        const observer = new ResizeObserver(updateOrientation);
        if (r_container.current) observer.observe(r_container.current);
        return () => r_container.current && observer.unobserve(r_container.current);
    }, [r_container]);

    useEffect(() => {
        if (s_searchParams.s) setSelectedTab('Search');
    }, [s_searchParams]);

    return <>
        <FileDisplayContainer ref={r_container} orientation={s_displayOrientation}>
            <FileDisplayFileContent orientation={s_displayOrientation}>
                {fileId && <OpticalFileDisplayRender fileId={fileId} caseId={caseId} />}
            </FileDisplayFileContent>
            <FileDisplayFileData orientation={s_displayOrientation}>
                <TabbedDisplay
                    tabs={{
                        'Info': <>
                            <CaseFileDataContainer>
                                <CaseFileData
                                    fileId={fileId}
                                />
                            </CaseFileDataContainer>
                        </>,
                        'Comments': <>
                            <CaseFileCommentsList />
                        </>,
                        'Search': <>
                            <CaseFileSearchContainer>
                                <CaseTextSearch
                                    files={[fileId]}
                                />
                            </CaseFileSearchContainer>
                        </>,
                        'Knowledge': <>
                            <CaseKnowledgeGraphDisplay 
                                files={[fileId]} 
                            />
                        </>
                    }}
                    selectedTab={s_selectedTab}
                />
            </FileDisplayFileData>
        </FileDisplayContainer>
    </>
}

const NoCommentsMessage = styled.div`
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: #808080;
`

function CaseFileCommentsList(props) {

    const {caseId, fileId} = useParams();

    const [s_fileData, setFileData] = useModelValueAsReactState('$.cases.currentOpen.files.all.' + fileId, {});

    const [s_commentsData, setCommentsData] = useModelValueAsReactState('$.cases.currentOpen.comments.data', {});

    return <>
        <VerticalGap gap={'16px'}/>
        {(s_fileData.comments || []).length === 0 ? <>
            <NoCommentsMessage>No comments in this file so far...</NoCommentsMessage>
        </> : <>
            {s_fileData.comments.filter(commentId => s_commentsData[commentId])
                .sort((a, b) => s_commentsData[a].from_page - s_commentsData[b].from_page || s_commentsData[a].from_char - s_commentsData[b].from_char)
                .map((comment, idx) => <>
                    <CaseFileCommentItem
                        key={idx}
                        commentId={comment}
                    />
                </>)
            }
        </>}
        <VerticalGap gap={'16px'}/>
    </>
}

const CaseFileCommentContainer = styled.div`
    display: block;
    width: calc(100% - 32px - 32px);
    margin: 4px 16px;
    padding: 16px;
    border-radius: 8px;
    background: #e0e0e0;
    overflow-x: hidden;
    cursor: pointer;
    transition: background 0.2s;
    ${({istarget}) => istarget ? 'outline: 1px solid black' : ''};
    &:hover {
        background: #d0d0d0;
        transition: none;
    }
`

function CaseFileCommentItem(props) {

    const [s_targetComment, setTargetComment] = useModelValueAsReactState('$.cases.currentOpen.comments.targetCommentId');

    return <>
        <CaseFileCommentContainer
            istarget={s_targetComment === props.commentId}
            onClick={() => {
                setTargetComment(null);
                requestAnimationFrame(() => setTargetComment(props.commentId));
            }}
        >
           <CaseFileComment
               commentId={props.commentId}
               displayAnnotatedText={true}
           />
        </CaseFileCommentContainer>
    </>
}
