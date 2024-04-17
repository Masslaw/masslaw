import {useCallback, useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {KnowledgeDisplay} from "./knowledgeDisplay";
import {LoadingIcon} from "./loadingIcon";
import {model} from "../../model/model";
import styled from "styled-components";
import {SVG_PATHS} from "../config/svgPaths";


const DisplayContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
`

const ReloadButton = styled.button`
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 16px;
    left: 16px;
    width: 32px;
    height: 32px;
    background: #202020;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    pointer-events: auto;
    padding: 0;
    z-index: 10;
    &:hover { background: #303030; }
    svg {
        width: 20px;
        height: 20px;
        fill: white;
    }
`

const NoKnowledgeToShow = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    color: #808080;
`

export function CaseKnowledgeGraphDisplay(props) {

    const {caseId} = useParams();

    const casesKnowledgeManager = model.services['casesKnowledgeManager'];

    const [s_loading, setLoading] = useState(false);

    const [s_caseKnowledge, setCaseKnowledge] = useModelValueAsReactState('$.cases.currentOpen.knowledge', {entities: [], connections: []})

    const [s_displayKnowledge, setDisplayKnowledge] = useState({});

    const c_loadKnowledge = useCallback(async (force=false) => {
        if (s_loading) return;
        setLoading(true);
        await casesKnowledgeManager.fetchCaseKnowledge(force);
        setLoading(false);
    }, [s_loading]);

    useEffect(() => {
        c_loadKnowledge();
    }, []);

    useEffect(() => {
        const displayKnowledge = {...s_caseKnowledge};
        if (props.files) {
            displayKnowledge.entities = (displayKnowledge.entities || [])
                .filter((entityData, _) => props.files.filter(fileId => entityData.properties.files.list.includes(fileId)).length);
            displayKnowledge.connections = (displayKnowledge.connections || [])
                .filter((connectionData, _) => props.files.filter(fileId => connectionData.properties.files.list.includes(fileId)).length);
        }
        if (props.labels) {
            displayKnowledge.entities = (displayKnowledge.entities || []).filter((entityData, _) => props.labels.includes(entityData.label));
        }
        setDisplayKnowledge(displayKnowledge);
    }, [s_caseKnowledge, props.files, props.labels]);

    return <>
        <ReloadButton onClick={() => c_loadKnowledge(true)}>
            {s_loading ? <>
                <LoadingIcon width={'20px'} height={'20px'}/>
            </> : <>
                <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.circleArrow}/></svg>
            </>}
        </ReloadButton>
        <DisplayContainer>
            {s_loading ? <>
                <LoadingIcon width={'30px'} height={'30px'}/>
            </> : !Object.keys(s_displayKnowledge).length ? <>
                <NoKnowledgeToShow>No Knowledge To Show</NoKnowledgeToShow>
            </> : <>
                <KnowledgeDisplay knowledge={s_displayKnowledge}/>
            </>}
        </DisplayContainer>
    </>
}


