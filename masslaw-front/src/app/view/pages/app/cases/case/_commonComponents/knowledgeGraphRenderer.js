import React, {forwardRef, useCallback, useEffect, useImperativeHandle, useRef, useState} from "react";

import {now} from "lodash";
import styled from "styled-components";
import {setColorSV, stringToColor} from "../../../../../../controller/functionality/visual-utils/colorUtils";
import {Color} from "../../../../../../controller/functionality/visual-utils/color";

const GraphNode = styled.g`
    cursor: pointer;
    &.main-focus {
        circle {
            filter: drop-shadow(0 0 20px ${({color}) => color});
        }
    }
    &.secondary-focus {
        circle {
            filter: drop-shadow(0 0 15px ${({color}) => color});
        }
    }
    circle {
        fill: black;
        stroke-width: 2px;
        filter: drop-shadow(0 0 10px ${({color}) => color});
    }
    text {
        font-size: 7px;
        user-select: none;
        filter: drop-shadow(0 0 1px black);
        text-shadow: 0 0 7px black, 0 0 1px black, 0 0 1px black, 0 0 1px black;
    }
`

const GraphEdge = styled.g`
    line {
        cursor: pointer;
        fill: white;
        stroke: white;
        stroke-width: ${({linewidth}) => `${linewidth}px`};
    }
`

export const KnowledgeGraphRenderer = forwardRef((props, ref) => {

    const timeOfInitialSimulation = 0;

    const MAXIMUM_NUMBER_OF_NODES_DISPLAYED = 40;

    const r_nodesToDisplay = useRef([]);

    const [s_nodes, setNodes] = useState({});
    const [s_edges, setEdges] = useState({});
    const [s_graphUpdated, setGraphUpdated] = useState(false);
    const [s_radius, setRadius] = useState(100);

    const [s_viewport, setViewport] = useState([-250, -250, 500, 500]);
    const [s_mouseDown, setMouseDown] = useState(false);
    const [s_draggingNode, setDraggingNode] = useState(null);
    const [s_draggingStartPosition, setDraggingStartPosition] = useState([0, 0]);
    const [s_mousePosition, setMousePosition] = useState([0, 0]);

    const addNode = (nodeId, nodeLabel, nodeTitle) => {
        let theta = Math.random() * Math.PI * 2;
        let x = s_radius * Math.cos(theta);
        let y = s_radius * Math.sin(theta);
        setNodes(_nodes => {
            const nodesCopy = {..._nodes};
            let originalNode = nodesCopy[nodeId];
            if (originalNode) {
                originalNode.label = nodeLabel;
                originalNode.title = nodeTitle;
                nodesCopy[nodeId] = originalNode;
                return nodesCopy;
            }
            nodesCopy[nodeId] = {
                label: nodeLabel,
                title: nodeTitle,
                position: [x, y],
                displayPosition: [x, y],
                velocity: [0, 0],
                graphContribution: 0,
                drag: 10,
                connectedNodes: [],
                state: 'idle',
                simulatedTimeSinceCreation: 0,
                simulatedTimeSinceModification: 0
            };
            return nodesCopy;
        });
        setGraphUpdated(true);
    }

    const addEdge = (edgeId, fromEntity, toEntity, weight) =>  {
        if (!edgeId || !fromEntity || !toEntity || !weight) return;
        setEdges(_edges => {
            let edgesCopy = {..._edges};
            let originalEdge = edgesCopy[edgeId];
            if (originalEdge) {
                originalEdge.fromEntity = fromEntity.toString();
                originalEdge.toEntity = toEntity.toString();
                originalEdge.weight = weight;
                edgesCopy[edgeId] = originalEdge;
                return edgesCopy;
            }
            edgesCopy[edgeId] = {
                fromEntity: fromEntity,
                toEntity: toEntity,
                weight: weight,
                normalizedWeight: 0,
                state: 'idle',
                width: 0,
            }
            return edgesCopy;
        });
        setGraphUpdated(true);
    }

    const setNodeState = (nodeId, state) => {
        setNodes(_nodes => {
            let nodesCopy = {..._nodes};
            const node = nodesCopy[nodeId];
            if (!node) return nodesCopy;
            node.state = state;
            return nodesCopy;
        });
    };

    const setEdgeState = (edgeId, state) => {
        setEdges(_edges => {
            let edgesCopy = {..._edges};
            edgesCopy[edgeId].state = state;
            return edgesCopy;
        });
    };

    const c_onGraphUpdated = useCallback(() => {
        let maxWeight = 0;
        let maxContribution = 0;
        let nodesCopy = {...s_nodes};
        let edgesCopy = {...s_edges};
        let numberOfNodes = Object.keys(nodesCopy).length;
        setRadius(Math.sqrt(numberOfNodes));
        for (let edgeId in edgesCopy) {
            let edge = edgesCopy[edgeId];
            if (!nodesCopy[edge.fromEntity] || !nodesCopy[edge.toEntity]) {
                delete edgesCopy[edgeId];
            }
        }
        for (let nodeId in nodesCopy) {
            let node = nodesCopy[nodeId];
            node.graphContribution = 0;
            node.connectedNodes = [];
        }
        for (let edgeId in edgesCopy) {
            let edge = edgesCopy[edgeId];
            maxWeight = Math.max(maxWeight, edge.weight);
            let edgeFrom = nodesCopy[edge.fromEntity];
            let edgeTo = nodesCopy[edge.toEntity];
            edgeFrom.graphContribution += edge.weight;
            edgeTo.graphContribution += edge.weight;
            maxContribution = Math.max(maxContribution, edgeFrom.graphContribution, edgeTo.graphContribution);
        }
        for (let nodeId in nodesCopy) {
            let node = nodesCopy[nodeId];
            node.graphContribution = node.graphContribution / maxContribution;
            node.drag = 10 + 20 * node.graphContribution;
        }
        for (let edgeId in edgesCopy) {
            let edge = edgesCopy[edgeId];
            edge.normalizedWeight = edge.weight / maxWeight;
            edge.width = 3 * Math.sin((1 - ((edge.normalizedWeight - 1) ** 2)) * Math.PI / 2);
            let edgeFrom = nodesCopy[edge.fromEntity];
            let edgeTo = nodesCopy[edge.toEntity];
            edgeFrom.connectedNodes.push([edge.toEntity, edge.normalizedWeight, edgeId]);
            edgeTo.connectedNodes.push([edge.fromEntity, edge.normalizedWeight, edgeId]);
        }
        setNodes(nodesCopy);
        setEdges(edgesCopy);
        r_nodesToDisplay.current = (
            Object.keys(nodesCopy).sort((a, b) => {
                return nodesCopy[b].graphContribution - nodesCopy[a].graphContribution;
            }).splice(0, Math.min(MAXIMUM_NUMBER_OF_NODES_DISPLAYED, Object.keys(nodesCopy).length))
        ) // the top <MAXIMUM_NUMBER_OF_NODES_DISPLAYED> nodes with the most contribution
    }, [s_nodes, s_edges]);

    useEffect(() => {
        if (!s_graphUpdated) return;
        c_onGraphUpdated();
        setGraphUpdated(false);
    }, [s_graphUpdated]);

    const reset = () => {
        setNodes({});
        setEdges({});
    };

    useImperativeHandle(ref, () => ({
        addNode,
        addEdge,
        setNodeState,
        setEdgeState,
        reset,
    }));

    const [update, setUpdate] = useState(true);

    useEffect(() => {
        setUpdate(true);
        physicsUpdateLoop();
        displayUpdateLoop();
        return () => setUpdate(false);
    }, []);

    let previousPhysicsTime = now();
    const physicsUpdateLoop = useCallback(() => {
        let currentTime = now();
        let dt = currentTime - previousPhysicsTime;
        previousPhysicsTime = currentTime;
        updatePhysics(Math.min(0.05, dt));
        if (!update) return;
        setTimeout(() => physicsUpdateLoop(), 0);
    }, [update]);

    let previousDisplayTime = now();
    const displayUpdateLoop = useCallback(() => {
        let currentTime = now();
        let dt = currentTime - previousDisplayTime;
        previousDisplayTime = currentTime;
        updateNodeDisplayPositions(Math.min(0.05, dt));
        if (!update) return;
        setTimeout(() => displayUpdateLoop(), 0);
    }, [update]);

    const draggingNodeRef = useRef(null);
    const mousePositionRef = useRef([0, 0]);

    useEffect(() => {
        draggingNodeRef.current = s_draggingNode;
    }, [s_draggingNode]);

    useEffect(() => {
        mousePositionRef.current = s_mousePosition;
    }, [s_mousePosition]);

    const grid = new Grid(100);

    // TODO: break this into smaller functions - refactor
    const updatePhysics = (dt) => {
        setNodes(_nodes => {
            let newNodes = {..._nodes};
            grid.clear();
            for (let nodeId of r_nodesToDisplay.current) {
                let node = newNodes[nodeId];
                if (!node) continue;
                grid.insert(nodeId, node.position);
            }
            let avgNodePosition = [0, 0];
            for (let nodeId of r_nodesToDisplay.current) {
                let node = newNodes[nodeId];
                if (!node) continue;
                avgNodePosition[0] += 0.1 * node.position[0] / Object.keys(r_nodesToDisplay.current).length;
                avgNodePosition[1] += 0.1 * node.position[1] / Object.keys(r_nodesToDisplay.current).length;
            }
            for (let nodeId of r_nodesToDisplay.current) {
                let node = newNodes[nodeId];
                if (!node) continue;
                if (draggingNodeRef.current === nodeId) node.simulatedTimeSinceModification = 0;
                const transitionTime = 5; // seconds
                const slowdown = 3;
                const personalDt = (Math.tanh(transitionTime - node.simulatedTimeSinceModification) + slowdown - 1) / slowdown;
                const nearbyNodes = grid.retrieve(node.position);
                for (let otherNodeId of nearbyNodes) {
                    if (otherNodeId === nodeId) continue;
                    let otherNode = newNodes[otherNodeId];
                    if (!otherNode) continue;
                    let deltaVector = [node.position[0] - otherNode.position[0], node.position[1] - otherNode.position[1]];
                    let distance = Math.max(0.01, Math.sqrt(deltaVector[0] * deltaVector[0] + deltaVector[1] * deltaVector[1]));
                    if (distance > 100) continue;
                    let deltaVectorNormalized = [deltaVector[0] / distance, deltaVector[1] / distance];
                    let repulsion = 500 * ((1 + (r_nodesToDisplay.current.length * 2 / MAXIMUM_NUMBER_OF_NODES_DISPLAYED)) ** 2) * ((1 + node.graphContribution * 2)) / (distance + 1);
                    node.velocity[0] += deltaVectorNormalized[0] * repulsion * personalDt;
                    node.velocity[1] += deltaVectorNormalized[1] * repulsion * personalDt;
                }
                let deltaFromCenter = node.position;
                let distanceFromCenter = Math.sqrt(deltaFromCenter[0] * deltaFromCenter[0] + deltaFromCenter[1] * deltaFromCenter[1]);
                let deltaFromCenterNormalized = [deltaFromCenter[0] / distanceFromCenter, deltaFromCenter[1] / distanceFromCenter];
                let attraction = node.graphContribution * distanceFromCenter;
                node.velocity[0] -= deltaFromCenterNormalized[0] * attraction * personalDt * 0.01;
                node.velocity[1] -= deltaFromCenterNormalized[1] * attraction * personalDt * 0.01;
                let nodeConnectionLengthSum = 0;
                for (let connectedNode of node.connectedNodes) {
                    nodeConnectionLengthSum += connectedNode[1];
                }
                nodeConnectionLengthSum = Math.max(0.01, nodeConnectionLengthSum);
                for (let connectedNode of node.connectedNodes) {
                    let otherNode = newNodes[connectedNode[0]];
                    if (!otherNode) continue;
                    let normalizedLength = (1 + (5 * connectedNode[1] / nodeConnectionLengthSum));
                    otherNode.velocity[0] -= (otherNode.position[0] - node.position[0]) * normalizedLength * personalDt * 0.1;
                    otherNode.velocity[1] -= (otherNode.position[1] - node.position[1]) * normalizedLength * personalDt * 0.1;
                }
                if (draggingNodeRef.current === nodeId) {
                    node.velocity[0] += (mousePositionRef.current[0] - node.position[0]) * personalDt * 20;
                    node.velocity[1] += (mousePositionRef.current[1] - node.position[1]) * personalDt * 20;
                }

                node.velocity[0] -= avgNodePosition[0] * personalDt;
                node.velocity[1] -= avgNodePosition[1] * personalDt;

                let dragFactor = Math.pow(1 / node.drag, personalDt);
                dragFactor *= 0.01 + (0.99 / (node.simulatedTimeSinceModification + 1));
                node.velocity[0] *= dragFactor;
                node.velocity[1] *= dragFactor;

                node.position[0] += node.velocity[0] * personalDt;
                node.position[1] += node.velocity[1] * personalDt;

                node.simulatedTimeSinceCreation += dt;
                node.simulatedTimeSinceModification += dt;
            }
            return newNodes;
        });
    };

    const updateNodeDisplayPositions = useCallback((dt) => {
        setNodes(_nodes => {
            let newNodes = {..._nodes};
            for (let nodeId in newNodes) {
                let node = newNodes[nodeId];
                if (!node) continue;
                node.displayPosition[0] = node.displayPosition[0] + (node.position[0] - node.displayPosition[0]) * 0.2;
                node.displayPosition[1] = node.displayPosition[1] + (node.position[1] - node.displayPosition[1]) * 0.2;
            }
            return newNodes;
        });
    }, []);

    const svgRef = React.createRef();

    return <>
        <svg
            ref={svgRef}
            className="case-knowledge-graph"
            viewBox={`${s_viewport[0]} ${s_viewport[1]} ${s_viewport[2]} ${s_viewport[3]}`}
            style={{width: '100%', height: '100%'}}
            onMouseMove={(event) => {
                if (!svgRef.current) return;
                let svgPoint = svgRef.current.createSVGPoint();
                svgPoint.x = event.clientX;
                svgPoint.y = event.clientY;
                let screenCTM = svgRef.current.getScreenCTM();
                if (!screenCTM) return;
                svgPoint = svgPoint.matrixTransform(screenCTM.inverse());
                if (s_mouseDown && !s_draggingNode) {
                    let newViewport = [s_viewport[0] - event.movementX * s_viewport[2] / 500, s_viewport[1] - event.movementY * s_viewport[2] / 500, s_viewport[2], s_viewport[3]];
                    let newViewportDistanceFromCenter = Math.sqrt(((newViewport[0] + newViewport[2] / 2) ** 2) + ((newViewport[1] + newViewport[3] / 2) ** 2));
                    if (newViewportDistanceFromCenter > s_radius * 100) return;
                    setViewport(newViewport);
                }
                setMousePosition([svgPoint.x, svgPoint.y]);
            }}
            onMouseUp={() => {
                setDraggingNode(null);
                setMouseDown(false);
            }}
            onWheel={(event) => {
                let delta = event.deltaY;
                if (s_viewport[2] + delta < 75 || s_viewport[3] + delta < 75) return;
                s_viewport[0] = s_viewport[0] - delta;
                s_viewport[1] = s_viewport[1] - delta;
                s_viewport[2] = s_viewport[2] + delta * 2;
                s_viewport[3] = s_viewport[3] + delta * 2;
                event.stopPropagation();
            }}
            onMouseDown={() => {
                setMouseDown(true);
            }}
        >
            {Object.keys(s_edges).map((edgeId) => {
                let edge = s_edges[edgeId];
                if (edge === undefined) return;
                if (!r_nodesToDisplay.current.includes(edge.fromEntity.toString())) return;
                if (!r_nodesToDisplay.current.includes(edge.toEntity.toString())) return;
                let nodeFrom = s_nodes[edge.fromEntity];
                let nodeTo = s_nodes[edge.toEntity];
                if (nodeFrom === undefined || nodeTo === undefined) return;
                if (nodeFrom.simulatedTimeSinceCreation < timeOfInitialSimulation) return;
                if (nodeTo.simulatedTimeSinceCreation < timeOfInitialSimulation) return;
                let lineWidth = edge.state === 'hovered' ? 5 : edge.state === 'highlighted' ? 1 + edge.width : edge.width;
                return <GraphEdge
                    key={edgeId}
                    id={edgeId}
                    linewidth={lineWidth}
                >
                    <line
                        key={edgeId + '-line'}
                        x1={nodeFrom.displayPosition[0].toString()}
                        y1={nodeFrom.displayPosition[1].toString()}
                        x2={nodeTo.displayPosition[0].toString()}
                        y2={nodeTo.displayPosition[1].toString()}
                        onMouseEnter={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(edge.fromEntity, 'secondary-highlight');
                            setNodeState(edge.toEntity, 'secondary-highlight');
                            setEdgeState(edgeId, 'hovered');
                            props.edgeHoverCallback(edgeId, true);
                        }}
                        onMouseLeave={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(edge.fromEntity, 'idle');
                            setNodeState(edge.toEntity, 'idle');
                            setEdgeState(edgeId, 'idle');
                            props.edgeHoverCallback(edgeId, false);
                        }}
                        onClick={e => {
                            if (draggingNodeRef.current) return;
                            props.edgeClickCallback(edgeId)
                        }}
                    />
                </GraphEdge>
            })}
            {Object.keys(s_nodes).map((nodeId) => {
                if (!r_nodesToDisplay.current.includes(nodeId)) return;
                let node = s_nodes[nodeId];
                if (node.simulatedTimeSinceCreation < timeOfInitialSimulation) return;
                let size = (5 + 5 * node.graphContribution) + (node.state === 'highlight' ? 3 : node.state === 'secondary-highlight' ? 1.5 : 0);
                let nodeTitle = node.title || '';
                nodeTitle = nodeTitle.length > 20 ? nodeTitle.substring(0, 20) + '...' : nodeTitle;
                const nodeColor = stringToColor(node.label);
                return <GraphNode
                    key={nodeId}
                    id={nodeId}
                    color={nodeColor.getHex()}
                >
                    <circle
                        key={nodeId + '-circle'}
                        cx={node.displayPosition[0].toString()}
                        cy={node.displayPosition[1].toString()}
                        r={size.toString()}
                        stroke={setColorSV(nodeColor, 0.1, 1).getHex()}
                        onMouseDown={() => {
                            if (draggingNodeRef.current) return;
                            setDraggingStartPosition([node.displayPosition[0], node.displayPosition[1]]);
                            setDraggingNode(nodeId)
                        }}
                        onMouseEnter={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(nodeId, 'highlight')
                            for (let connectedNode of node.connectedNodes) {
                                setNodeState(connectedNode[0], 'secondary-highlight');
                                setEdgeState(connectedNode[2], 'highlighted');
                            }
                            props.nodeHoverCallback(nodeId, true);
                        }}
                        onMouseLeave={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(nodeId, 'idle');
                            for (let connectedNode of node.connectedNodes) {
                                setNodeState(connectedNode[0], 'idle');
                                setEdgeState(connectedNode[2], 'idle');
                            }
                            props.nodeHoverCallback(nodeId, false);
                        }}
                        onClick={e => {
                            if (draggingNodeRef.current) return;
                            if (Math.abs(s_mousePosition[0] - s_draggingStartPosition[0]) > 10) return;
                            if (Math.abs(s_mousePosition[1] - s_draggingStartPosition[1]) > 10) return;
                            props.nodeClickCallback(nodeId);
                        }}
                    >
                    </circle>
                    <text
                        key={nodeId + '-label'}
                        x={node.displayPosition[0].toString()}
                        y={(node.displayPosition[1] + 16).toString()}
                        textAnchor="middle"
                        dominantBaseline="central"
                        fill="white"
                    >{nodeTitle}</text>
                </GraphNode>
            })}
        </svg>
    </>
});

class Grid {
    _cellSize;
    _cells;

    constructor(cellSize) {
        this._cellSize = cellSize;
        this._cells = {};
    }

    clear() {
        this._cells = {};
    }

    insert(id, position) {
        const column = Math.floor(position[0] / this._cellSize);
        const row = Math.floor(position[1] / this._cellSize);
        const index = `${row}-${column}`;
        let cell = this._cells[index] || [];
        cell.push(id);
        this._cells[index] = cell;
    }

    retrieve(position) {
        const column = Math.floor(position[0] / this._cellSize);
        const row = Math.floor(position[1] / this._cellSize);
        let nodes = [];
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j ++) {
                const index = `${(row + i)}-${(column + j)}`;
                nodes.push(...(this._cells[index] || []));
            }
        }
        return nodes;
    }
}
