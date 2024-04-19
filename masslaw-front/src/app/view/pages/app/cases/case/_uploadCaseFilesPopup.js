import styled from "styled-components";
import {useCallback, useEffect, useMemo, useRef, useState} from "react";
import {model} from "../../../../../model/model";
import {VerticalGap} from "../../../../components/verticalGap";
import {caseSupportedFileTypes} from "../../../../../config/caseConsts";
import {useModelValueAsReactState} from "../../../../../controller/functionality/model/modelReactHooks";
import {SVG_PATHS} from "../../../../config/svgPaths";
import {Icon} from "../../../../components/icon";

const UploadCaseFilesPopupContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 640px;
    background-color: #202020;
    color: white;
    border-radius: 12px;
    z-index: 100;
    padding: 32px;
`

const UploadCaseFilesPopupTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 0;
`

const UploadCaseFilesPopupSubTitle = styled.div`
    font-size: 14px;
    color: #808080;
    margin: 0;
`

const UploadCaseFilesSectionContainer = styled.div`
    border-radius: 8px;
    border: 1px solid #505050;
    padding: 16px;
    width: calc(100% - 32px);
`

const UploadCaseFilesSectionTitle = styled.div`
    font-size: 16px;
    font-weight: bold;
    color: white;
`

const UploadCaseFilesSectionSubTitle = styled.div`
    font-size: 14px;
    color: #808080;
`

const UploadCaseFilesStartUploadingButton = styled.button`
    position: relative;
    margin-left: auto;
    background: ${({clickable}) => clickable ? "white" : "none"};
    width: 128px;
    height: 32px;
    border: 1px solid white;
    color: ${({clickable}) => clickable ? "black" : "white"};
    border-radius: 12px;
    font-size: 14px;
    letter-spacing: .5px;
    pointer-events: ${({clickable}) => clickable ? "all" : "none"};
    cursor: ${({clickable}) => clickable ? "pointer" : "normal"};

    &:hover {
        ${({clickable}) => clickable ? "filter: drop-shadow(0 0 5px white)" : ""}
    }
`

export function UploadCaseFilesPopup(props) {

    const caseId = model.cases.currentOpen.id;

    const [s_selectedDirectory, setSelectedDirectory] = useState(['Case']);

    const [s_selectedFiles, setSelectedFiles] = useState([]);

    const [s_fileProgressByName, setFileProgressByName] = useState({});

    const [s_caseFilesToUpload, setCaseFilesToUpload] = useModelValueAsReactState(`$.cases.currentOpen.files.filesToUpload`);

    const c_uploadFiles = useCallback(() => {
        if (!s_selectedFiles.length) return;
        const caseFilesToUpload = [];
        for (const file of s_selectedFiles) {
            if (caseSupportedFileTypes.includes(file.name.split('.').pop()) === false) continue;
            caseFilesToUpload.push({file: file, directory: s_selectedDirectory.slice(1)});
        }
        setCaseFilesToUpload(p => ({...(p ?? {}), ...{[caseId]: caseFilesToUpload}}));
        setSelectedFiles([]);
        props.dismiss();
    }, [s_selectedDirectory, s_selectedFiles, props.dismiss]);

    const m_existingFilesInDirectory = useMemo(() => {
        const getSelectedDirectoryHierarchyLevel = (hierarchy, path) => {
            if (path.length === 0) return hierarchy;
            return getSelectedDirectoryHierarchyLevel((hierarchy || {})[path[0]], path.slice(1));
        }
        const caseId = model.cases.currentOpen.id || '';
        const selectedDirectoryHierarchyLevel = getSelectedDirectoryHierarchyLevel((model.cases.all[caseId] || {}).contentHierarchy || {}, s_selectedDirectory.slice(1));
        return Object.values(selectedDirectoryHierarchyLevel || {}).filter(v => typeof v === "string");
    }, []);

    return <>
        <UploadCaseFilesPopupContainer>
            <UploadCaseFilesPopupTitle>Upload Files</UploadCaseFilesPopupTitle>
            <VerticalGap gap={'8px'}/>
            <UploadCaseFilesPopupSubTitle>Upload files to this case</UploadCaseFilesPopupSubTitle>
            <VerticalGap gap={'16px'}/>
            <UploadCaseFilesSectionContainer>
                <UploadCaseFilesSectionTitle>Select Files</UploadCaseFilesSectionTitle>
                <VerticalGap gap={'8px'}/>
                <UploadCaseFilesSectionSubTitle>Select the files you wish to upload in your local file system</UploadCaseFilesSectionSubTitle>
                <VerticalGap gap={'8px'}/>
                <SelectFiles
                    setSelectedFiles={setSelectedFiles}
                    existingFiles={m_existingFilesInDirectory}
                    fileProgressByName={s_fileProgressByName}
                />
            </UploadCaseFilesSectionContainer>
            <VerticalGap gap={'16px'}/>
            <UploadCaseFilesSectionContainer>
                <UploadCaseFilesSectionTitle>Select Directory</UploadCaseFilesSectionTitle>
                <VerticalGap gap={'8px'}/>
                <UploadCaseFilesSectionSubTitle>Select the directory in the case storage to which the files will be uploaded</UploadCaseFilesSectionSubTitle>
                <VerticalGap gap={'8px'}/>
                <DirectorySelection setSelectedDirectory={setSelectedDirectory}/>
            </UploadCaseFilesSectionContainer>
            <VerticalGap gap={'16px'}/>
            <UploadCaseFilesStartUploadingButton
                onClick={() => c_uploadFiles()}
                clickable={!!s_selectedFiles.length}
            >Start Uploading</UploadCaseFilesStartUploadingButton>
        </UploadCaseFilesPopupContainer>
    </>
}

const DirectorySelectionContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100% - 32px);
    padding: 16px;
    background: #303030;
    border-radius: 12px;
`

const SelectedDirectoryContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: calc(100% - 16px);
    height: 16px;
    line-height: 16px;
    font-size: 14px;
    padding: 8px;
    background: #303030;
    border-radius: 12px;
`

const DirectoryHierarchyLevel = styled.span`
    color: white;
    margin: 0 4px;
`

const DirectorySeparator = styled.span`
    color: #9f9f9f;
`

const NewDirectoryContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: calc(100% - 16px);
    height: 20px;
    line-height: 20px;
    font-size: 14px;
    padding: 8px;
    background: #303030;
    border-radius: 12px;
`

const NewDirectoryTitle = styled.span`
    position: relative;
    margin: 0 4px;
    font-size: 14px;
`

const NewDirectoryInput = styled.input`
    position: relative;
    height: 20px;
    line-height: 20px;
    padding: 0 4px 0 4px;
    margin: 0 8px 0 4px;
    background: none;
    border: 0 solid white;
    border-bottom: 1px solid #505050;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    outline: none;
    color: white;
`

const NewDirectoryCreateButton = styled.button`
    position: relative;
    height: 24px;
    width: 64px;
    background: none;
    border: 1px solid white;
    outline: none;
    border-radius: 6px;
    color: white;
    margin: 0 2px;
    top: -2px;

    &:hover {
        background: white;
        color: black;
    }
`

const DirectoryAlreadyExistsError = styled.div`
    position: relative;
    width: calc(100% - 64px);
    margin: 4px 32px;
    color: red;
    font-size: 12px;
`

function DirectorySelection(props) {

    const [s_hierarchy, setHierarchy] = useState({});

    const [s_selectedDirectory, setSelectedDirectory] = useState(['Case']);

    const [s_newDirectoryName, setNewDirectoryName] = useState('');

    useEffect(() => {
        const caseId = model.cases.currentOpen.id || '';
        const hierarchy = (model.cases.all[caseId] || {}).contentHierarchy;
        const cleanHierarchyLevel = (level) => {
            for (const key in level) {
                if (typeof level[key] !== "object") {
                    delete level[key];
                    continue;
                }
                level[key] = cleanHierarchyLevel(level[key]);
            }
            return level;
        }
        setSelectedDirectory(['Case']);
        setHierarchy(cleanHierarchyLevel({...hierarchy}));
    }, []);

    useEffect(() => {
        props.setSelectedDirectory(s_selectedDirectory);
    }, [s_selectedDirectory]);

    const c_getDirectoryAtPath = (hierarchy, path) => {
        if (path.length === 0) return hierarchy;
        return c_getDirectoryAtPath((hierarchy || {})[path[0]], path.slice(1));
    }

    const c_createNewDirectory = useCallback(() => {
        const trimmed = s_newDirectoryName.trim();
        if (trimmed.length === 0) return;
        const newHierarchy = {...s_hierarchy};
        const currentSubDirectory = c_getDirectoryAtPath(newHierarchy, s_selectedDirectory.slice(1));
        currentSubDirectory[trimmed] = {};
        setHierarchy(newHierarchy);
        setSelectedDirectory([...s_selectedDirectory, trimmed]);
        setNewDirectoryName("");
    }, [s_selectedDirectory, s_hierarchy, s_newDirectoryName, c_getDirectoryAtPath]);

    return <>
        <SelectedDirectoryContainer>
            {s_selectedDirectory.map((d, i) => <>
                <DirectoryHierarchyLevel>{d}</DirectoryHierarchyLevel>
                <DirectorySeparator>/</DirectorySeparator>
            </>)}
        </SelectedDirectoryContainer>
        <VerticalGap gap={'8px'}/>
        <NewDirectoryContainer>
            <NewDirectoryTitle>New Directory:</NewDirectoryTitle>
            <NewDirectoryInput value={s_newDirectoryName} onChange={e => setNewDirectoryName(e.target.value)}/>
            <NewDirectoryCreateButton onClick={() => c_createNewDirectory()}>Create</NewDirectoryCreateButton>
        </NewDirectoryContainer>
        <VerticalGap gap={'8px'}/>
        {Object.keys(c_getDirectoryAtPath(s_hierarchy, s_selectedDirectory.slice(1)) || {}).includes(s_newDirectoryName) ? <DirectoryAlreadyExistsError>Directory already exists</DirectoryAlreadyExistsError> : <></>}
        <DirectorySelectionContainer>
            <HierarchyLevelDisplay
                name={'Case'}
                hierarchy={s_hierarchy}
                openDirectory={s_selectedDirectory}
                setOpenDirectory={h => setSelectedDirectory(h.length === 0 ? ['Case'] : h)}
            />
        </DirectorySelectionContainer>
    </>
}

const HierarchyLevelDisplayContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    border-left: 1px solid #505050;
    padding: 4px 0 4px 4px;
`

const HierarchyLevelDisplayLevelNameContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    height: 16px;
    line-height: 16px;
    font-size: 14px;
    margin: 4px;
    padding: 4px;
    cursor: pointer;
    border-radius: 4px;
    background: ${({open}) => open ? '#404040' : 'none'};

    &:hover {
        background: #505050;
    }
`

const HierarchyLevelFolderIcon = styled.div`
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    
    svg {
        width: 16px;
        height: 16px;
        fill: white;
    }
`

const HierarchyLevelDisplayLevelName = styled.div`
    margin-left: 4px;
`

const HierarchyLevelChildrenContainer = styled.div`
    position: relative;
    margin-left: 4px;
`

const NoSubdirectories = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 4px;
    font-size: 14px;
    color: #808080;
`

function HierarchyLevelDisplay(props) {

    const c_setOpenDirectory = useCallback((subDirectory) => {
        props.setOpenDirectory([props.name, ...subDirectory]);
    }, [props.setOpenDirectory, props.name]);

    const m_open = useMemo(() => props.openDirectory.length > 0 && props.openDirectory[0] === props.name, [props.openDirectory]);

    return <>
        <HierarchyLevelDisplayContainer>
            <HierarchyLevelDisplayLevelNameContainer open={m_open} onClick={() => props.setOpenDirectory(m_open ? [] : [props.name])}>
                <HierarchyLevelFolderIcon>
                    <Icon>{SVG_PATHS.folder}</Icon>
                </HierarchyLevelFolderIcon>
                <HierarchyLevelDisplayLevelName>{props.name}</HierarchyLevelDisplayLevelName>
            </HierarchyLevelDisplayLevelNameContainer>
            <HierarchyLevelChildrenContainer>
                {m_open ? Object.keys(props.hierarchy || {}).length ? Object.keys(props.hierarchy || {}).map(n => <HierarchyLevelDisplay
                    key={n}
                    name={n}
                    openDirectory={props.openDirectory.slice(1)}
                    setOpenDirectory={(subDirectory) => c_setOpenDirectory(subDirectory)}
                    hierarchy={props.hierarchy[n]}
                />) : <NoSubdirectories>No subdirectories</NoSubdirectories> : <></>}
            </HierarchyLevelChildrenContainer>
        </HierarchyLevelDisplayContainer>
    </>
}


const SelectFilesContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100%);
    background: #303030;
    border-radius: 12px;
`

const SelectedFilesHeader = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: calc(100% - 32px);
    height: 24px;
    line-height: 24px;
    font-size: 16px;
    padding: 16px;
    background: #303030;
    border-radius: 12px;
`

const SelectedFilesTitle = styled.span`
`

const SelectedFilesAddFilesButton = styled.button`
    position: relative;
    height: 24px;
    width: 96px;
    border-radius: 4px;
    border: 1px solid white;
    color: white;
    background: none;
    margin-left: auto;

    &:hover {
        background: white;
        color: black;
    }
`

const SelectedFilesList = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: calc(100% - 32px - 16px);
    height: max-content;
    max-height: 320px;
    overflow-y: auto;
    overflow-x: hidden;
    margin: 8px 16px 8px 16px;
    padding: 8px;
    border-radius: 12px;
`

const NoFilesSelectedPrompt = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #808080;
`

function SelectFiles(props) {

    const r_inputRef = useRef(null);

    const [s_selectedFiles, setSelectedFiles] = useState([]);

    useEffect(() => {
        props.setSelectedFiles(s_selectedFiles);
    }, [s_selectedFiles]);

    const m_selectedFileItems = useMemo(() => {
        return s_selectedFiles.map((f, i) => <SelectedFile
            key={i}
            file={f}
            supported={caseSupportedFileTypes.includes(f.name.split('.').pop() || '')}
            isDuplicate={props.existingFiles.includes(f.name) || s_selectedFiles.reduce((acc, v) => acc + (v.name === f.name ? 1 : 0)) > 1}
            removeFile={() => setSelectedFiles(s => s.filter(sf => sf !== f))}
        />)
    }, [s_selectedFiles, props.fileProgressByName]);

    return <>
        <SelectFilesContainer>
            <SelectedFilesHeader>
                <SelectedFilesTitle>Selected Files</SelectedFilesTitle>
                <SelectedFilesAddFilesButton onClick={() => r_inputRef.current.click()}>Add Files</SelectedFilesAddFilesButton>
                <input style={{display: "none"}} ref={r_inputRef} type={'file'} multiple={true} onChange={e => setSelectedFiles(f => [...f, ...e.target.files])}/>
            </SelectedFilesHeader>
            <SelectedFilesList>
            {m_selectedFileItems.length ? <>
                {m_selectedFileItems}
            </> : <>
                <NoFilesSelectedPrompt>No Files Are Selected...</NoFilesSelectedPrompt>
            </>}
            </SelectedFilesList>
        </SelectFilesContainer>
    </>
}

const SelectedFileItemContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: calc(100% - 16px);
    height: 24px;
    line-height: 24px;
    font-size: 14px;
    padding: 8px;
    background: #404040;
    border-radius: 12px;
    margin: 4px 0;
    border: 1px solid ${({invalidType, duplicate, finished}) => invalidType ? "red" : duplicate ? 'yellow' : finished ? 'green' : 'white'};
`

const SelectedFileName = styled.span`
    position: relative;
    color: white;
    margin: 0 8px;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
`

const SelectedFileStatusSection = styled.div`
    position: relative;
    width: 128px;
    min-width: 128px;
    height: 100%;
    margin: 0 4px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    font-size: 12px;
`

const FileNotUnsupported = styled.div`
    color: rgb(255, 128, 128);
`

const FileAlreadyExists = styled.div`
    color: yellow;
`

const RemoveFileButton = styled.button`
    position: relative;
    max-width: 256px;
    height: 24px;
    border-radius: 6px;
    border: 1px solid white;
    background: none;
    color: white;
    font-size: 12px;
    margin: 0 4px;
    cursor: pointer;

    &:hover {
        background: white;
        color: black;
    }
`

function SelectedFile(props) {

    return <>
        <SelectedFileItemContainer invalidType={!props.supported} duplicate={props.isDuplicate} finished={props.progress >= 1}>
            <SelectedFileName>{props.file.name}</SelectedFileName>
            <SelectedFileStatusSection>{
                !props.supported && <>
                    <FileNotUnsupported>File Not Supported</FileNotUnsupported>
                </> || props.isDuplicate && <>
                    <FileAlreadyExists>File Already Exists</FileAlreadyExists>
                </>
            }</SelectedFileStatusSection>
            <RemoveFileButton onClick={props.removeFile}>Remove</RemoveFileButton>
        </SelectedFileItemContainer>
    </>
}
