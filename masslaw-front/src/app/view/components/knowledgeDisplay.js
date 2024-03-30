import {KnowledgeGraphRenderer} from "./knowledgeGraphRenderer";
import {useEffect, useMemo, useRef, useState} from "react";
import styled from "styled-components";
import {Color} from "../../controller/functionality/visual-utils/color";
import {KnowledgeItemsConfig} from "../config/knowledgeItemsConfig";
import {setColorSV, stringToColor} from "../../controller/functionality/visual-utils/colorUtils";


const KnowledgeDisplayContainer = styled.div`
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    overflow: hidden;
    flex-direction: ${({orientation}) => orientation === 'vertical' ? 'column' : 'row'};
    
    & > div:nth-child(1) {
        width: ${({orientation}) => orientation === 'vertical' ? '100%' : '70%'};
        height: ${({orientation}) => orientation === 'vertical' ? '70%' : '100%'};
    }
    
    & > div:nth-child(2) {
        width: ${({orientation}) => orientation === 'vertical' ? '100%' : 'calc(30% - 1px)'};
        height: ${({orientation}) => orientation === 'vertical' ? 'calc(30% - 1px)' : '100%'};
        border-left: ${({orientation}) => orientation === 'vertical' ? 'none' : '1px solid #808080'};
        border-top: ${({orientation}) => orientation === 'vertical' ? '1px solid #808080' : 'none'};
    }
`

const KnowledgeGraphSection = styled.div`
    overflow: hidden;
    background: #101010;
    position: relative;
`

const KnowledgeInfoSection = styled.div`
    display: flex;
    flex-direction: column;
    overflow: hidden;
`

const KnowledgeEntitiesList = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
`

const KnowledgeEntitiesListTitle = styled.div`
    color: white;
    font-size: 20px;
    font-weight: bold;
    margin: 8px;
`

const KnowledgeEntityInfoItem = styled.div`
    display: flex;
    flex-direction: column;
    padding: 8px;
    margin: 2px 8px;
    width: calc(100% - 16px - 16px - 4px);
    background: #303030;
    border-radius: 4px;
    color: white;
    cursor: pointer;
    border-left: 4px solid ${({color}) => color}80;
    &:hover { background: #404040; }
`

const KnowledgeEntityInfoItemTitle = styled.div`
    position: relative;
    font-size: 16px;
    font-weight: bold;
    margin: 4px;
    max-width: calc(100% - 8px);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    span {
        color: #808080;
        margin-left: 8px;
    }
`

const KnowledgeEntityInfoItemInfo = styled.div`
    font-size: 14px;
    font-weight: normal;
    margin: 4px;
    max-width: calc(100% - 8px);
    color: #808080;
    span {
        color: white;
        margin-left: 4px;
    }
`

const CaseKnowledgeGraphInfoText = styled.div`
    position: absolute;
    height: 20px;
    bottom: 10px;
    left: 10px;
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: grey;
    font-size: 14px;
    line-height: 20px;
    font-weight: 500;
`


export function KnowledgeDisplay(props) {  
    
    const r_container = useRef({});

    const r_graphRef = useRef({});

    const [s_displayOrientation, setDisplayOrientation] = useState('horizontal');

    const [s_entityContributions, setEntityContributions] = useState({});

    useEffect(() => {
        if (!r_graphRef.current) return;
        if (!props.knowledge) return;
        r_graphRef.current.reset();
        for (let entity of (props.knowledge.entities || [])) r_graphRef.current.addNode(entity.id, entity.label, entity.properties['title']);
        for (let connection of (props.knowledge.connections || [])) r_graphRef.current.addEdge(connection.id, connection.from, connection.to, connection.properties['strength']);
        console.log(props.knowledge);
    }, [r_graphRef, props.knowledge, s_displayOrientation]);

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
        const entityContributions = {};
        (props.knowledge.connections || []).forEach(connectionData => {
            const fromEntity = props.knowledge.entities.find(entityData => entityData.id === connectionData.from);
            const toEntity = props.knowledge.entities.find(entityData => entityData.id === connectionData.to);
            if (!fromEntity || !toEntity) return;
            if (!entityContributions[fromEntity.id]) entityContributions[fromEntity.id] = 0;
            if (!entityContributions[toEntity.id]) entityContributions[toEntity.id] = 0;
            entityContributions[fromEntity.id] += connectionData.properties['strength'] || 0;
            entityContributions[toEntity.id] += connectionData.properties['strength'] || 0;
        });
        setEntityContributions(p => ({...p, ...entityContributions}));
    }, [props.knowledge, s_displayOrientation]);

    const m_nodesInfoList = useMemo(() => {
        return (props.knowledge.entities || [])
            .toSorted((a, b) => (s_entityContributions[b.id] || 0) - (s_entityContributions[a.id] || 0))
            .map((entityData, idx) => <>
            <KnowledgeEntityInfoItem
                key={idx}
                onMouseEnter={e =>  r_graphRef.current.setNodeState(entityData.id, 'highlight')}
                onMouseLeave={e => r_graphRef.current.setNodeState(entityData.id, 'idle')}
                color={setColorSV(stringToColor(entityData.label), 1 ,1).getHex()}
            >
                <KnowledgeEntityInfoItemTitle>{entityData.properties.title}<span>({KnowledgeItemsConfig[entityData.label].trueLabel})</span></KnowledgeEntityInfoItemTitle>
                <KnowledgeEntityInfoItemInfo>Contribution:<span>{s_entityContributions[entityData.id] || 0}</span></KnowledgeEntityInfoItemInfo>
                <KnowledgeEntityInfoItemInfo>Occurrences across files:<span>{entityData.properties.files.list.length}</span></KnowledgeEntityInfoItemInfo>
            </KnowledgeEntityInfoItem>
        </>);
    }, [r_graphRef, props.knowledge.entities, s_entityContributions]);

    return <>
        <KnowledgeDisplayContainer 
            ref={r_container}
            orientation={s_displayOrientation}
        >
            <KnowledgeGraphSection>
                <KnowledgeGraphRenderer
                    ref={r_graphRef}
                    nodeClickCallback={props.nodeClickCallback || (() => {})}
                    edgeClickCallback={props.edgeClickCallback || (() => {})}
                    nodeHoverCallback={props.nodeHoverCallback || (() => {})}
                    edgeHoverCallback={props.edgeHoverCallback || (() => {})}
                />
                <CaseKnowledgeGraphInfoText>Only the 40 most relevant items are displayed</CaseKnowledgeGraphInfoText>
            </KnowledgeGraphSection>
            <KnowledgeInfoSection>
                <KnowledgeEntitiesList>
                    <KnowledgeEntitiesListTitle>Entities:</KnowledgeEntitiesListTitle>
                    {m_nodesInfoList}
                </KnowledgeEntitiesList>
            </KnowledgeInfoSection>
        </KnowledgeDisplayContainer>
    </>
}