import {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {KnowledgeDisplay} from "./knowledgeDisplay";
import {LoadingIcon} from "./loadingIcon";
import {model} from "../../model/model";


export function CaseKnowledgeGraphDisplay(props) {

    const {caseId} = useParams();

    const casesKnowledgeManager = model.services['casesKnowledgeManager'];

    const [s_loading, setLoading] = useState(true);

    const [s_caseKnowledge, setCaseKnowledge] = useModelValueAsReactState('$.cases.currentOpen.knowledge', {entities: [], connections: []})

    const [s_displayKnowledge, setDisplayKnowledge] = useState({});

    useEffect(() => {
        setLoading(true);
        casesKnowledgeManager.fetchCaseKnowledge().then(() => setLoading(false));
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
        {s_loading ? <>
            <LoadingIcon width={'30px'} height={'30px'}/>
        </> : <>
            <KnowledgeDisplay knowledge={s_displayKnowledge}/>
        </>}
    </>
}


