import React, {forwardRef, useCallback, useEffect, useImperativeHandle, useRef, useState} from "react";
import {node_style} from "./style_config";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

import './css.css';
import {now} from "lodash";


interface Node {
    label: string,
    title?: string,
    position: [number, number],
    display_position: [number, number],
    velocity: [number, number],
    drag: number,
    graph_contribution: number,
    connected_nodes: [string, number][],
    state: string,
    simulated_time_since_creation: number,
}

interface Edge {
    label?: string,
    from_entity: string,
    to_entity: string,
    weight: number,
    normalized_weight: number,
    state: string,
    width: number,
}

export interface GraphInterface {
    addNode: (node_id: string, node_label: string, node_title?: string) => void,
    addEdge: (edge_id: string, from_entity: string, to_entity: string, weight: number) => void,
    reset: () => void,
    setNodeState: (node_id: string, state: string) => void,
    setEdgeState: (edge_id: string, state: string) => void,
}

export const Graph = forwardRef<
    GraphInterface,
    {
        edgeHoverCallback: (edge_id: string, hovering: boolean) => void,
        edgeClickCallback: (edge_id: string) => void,
        nodeHoverCallback: (node_id: string, hovering: boolean) => void,
        nodeClickCallback: (node_id: string) => void,
    }
    >((props, ref) => {
    
    const time_of_initial_simulation = 0;

    const MAXIMUM_NUMBER_OF_NODES_DISPLAYED = 60;
    
    const [nodes, setNodes] = useState({} as { [key: string]: Node });
    const [edges, setEdges] = useState({} as { [key: string]: Edge });
    const nodes_to_display = useRef([] as string[]);
    const [graph_updated, setGraphUpdated] = useState(false);
    const [radius, setRadius] = useState(100);

    const [viewport, setViewport] = useState([-250, -250, 500, 500]);
    const [mouse_down, setMouseDown] = useState(false);
    const [dragging_node, setDraggingNode] = useState<string | null>(null);
    const [dragging_start_position, setDraggingStartPosition] = useState([0, 0] as [number, number]);
    const [mouse_position, setMousePosition] = useState([0, 0] as [number, number]);

    const addNode = (node_id: string, node_label: string, node_title?: string) => {
        let theta = Math.random() * Math.PI * 2;
        let x = radius * Math.cos(theta);
        let y = radius * Math.sin(theta);
        setNodes(_nodes => {
            const nodes_copy = {..._nodes};
            let original_node = nodes_copy[node_id];
            if (original_node) {
                original_node.label = node_label;
                original_node.title = node_title;
                nodes_copy[node_id] = original_node;
                return nodes_copy;
            }
            nodes_copy[node_id] = {
                label: node_label,
                title: node_title,
                position: [x, y],
                display_position: [x, y],
                velocity: [0, 0],
                graph_contribution: 0,
                drag: 10,
                connected_nodes: [],
                state: 'idle',
                simulated_time_since_creation: 0
            };
            return nodes_copy;
        });
        setGraphUpdated(true);
    }

    const addEdge = (edge_id: string, from_entity: string, to_entity: string, weight: number) =>  {
        if (!edge_id || !from_entity || !to_entity || !weight) return;
        setEdges(_edges => {
            let edges_copy = {..._edges};
            let original_edge = edges_copy[edge_id];
            if (original_edge) {
                original_edge.from_entity = from_entity.toString();
                original_edge.to_entity = to_entity.toString();
                original_edge.weight = weight;
                edges_copy[edge_id] = original_edge;
                return edges_copy;
            }
            edges_copy[edge_id] = {
                from_entity: from_entity,
                to_entity: to_entity,
                weight: weight,
                normalized_weight: 0,
                state: 'idle',
                width: 0,
            }
            return edges_copy;
        });
        setGraphUpdated(true);
    }

    const setNodeState = (node_id: string, state: string) => {
        setNodes(_nodes => {
            let nodes_copy = {..._nodes};
            const node = nodes_copy[node_id];
            if (!node) return nodes_copy;
            node.state = state;
            return nodes_copy;
        });
    };

    const setEdgeState = (edge_id: string, state: string) => {
        setEdges(_edges => {
            let edges_copy = {..._edges};
            edges_copy[edge_id].state = state;
            return edges_copy;
        });
    };

    const onGraphUpdated = useCallback(() => {
        let max_weight = 0;
        let max_contribution = 0;
        let nodes_copy = {...nodes};
        let edges_copy = {...edges};
        let number_of_nodes = Object.keys(nodes_copy).length;
        setRadius(Math.sqrt(number_of_nodes));
        for (let edge_id in edges_copy) {
            let edge = edges_copy[edge_id];
            if (!nodes_copy[edge.from_entity] || !nodes_copy[edge.to_entity]) {
                delete edges_copy[edge_id];
            }
        }
        for (let node_id in nodes_copy) {
            let node = nodes_copy[node_id];
            node.graph_contribution = 0;
            node.connected_nodes = [];
        }
        for (let edge_id in edges_copy) {
            let edge = edges_copy[edge_id];
            max_weight = Math.max(max_weight, edge.weight);
            let edge_from = nodes_copy[edge.from_entity];
            let edge_to = nodes_copy[edge.to_entity];
            edge_from.graph_contribution += edge.weight;
            edge_to.graph_contribution += edge.weight;
            max_contribution = Math.max(max_contribution, edge_from.graph_contribution, edge_to.graph_contribution);
        }
        for (let node_id in nodes_copy) {
            let node = nodes_copy[node_id];
            node.graph_contribution = node.graph_contribution / max_contribution;
            node.drag = 10 + 20 * node.graph_contribution;
        }
        for (let edge_id in edges_copy) {
            let edge = edges_copy[edge_id];
            edge.normalized_weight = edge.weight / max_weight;
            edge.width = 3 * Math.sin((1 - ((edge.normalized_weight - 1) ** 2)) * Math.PI / 2);
            let edge_from = nodes_copy[edge.from_entity];
            let edge_to = nodes_copy[edge.to_entity];
            edge_from.connected_nodes.push([edge.to_entity, edge.normalized_weight]);
            edge_to.connected_nodes.push([edge.from_entity, edge.normalized_weight]);
        }
        setNodes(nodes_copy);
        setEdges(edges_copy);
        nodes_to_display.current = (
            Object.keys(nodes_copy).sort((a, b) => {
                return nodes_copy[b].graph_contribution - nodes_copy[a].graph_contribution;
            }).splice(0, Math.min(MAXIMUM_NUMBER_OF_NODES_DISPLAYED, Object.keys(nodes_copy).length))
        ) // the top <MAXIMUM_NUMBER_OF_NODES_DISPLAYED> nodes with the most contribution
    }, [nodes, edges]);

    useEffect(() => {
        if (!graph_updated) return;
        onGraphUpdated();
        setGraphUpdated(false);
    }, [graph_updated]);

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

    const physicsUpdateLoop = useCallback(() => {
        updatePhysics(0.015);
        if (!update) return;
        setTimeout(() => physicsUpdateLoop(), 0);
    }, [update]);

    const displayUpdateLoop = useCallback(() => {
        updateNodeDisplayPositions(0.015);
        if (!update) return;
        setTimeout(() => displayUpdateLoop(), 0);
    }, [update]);

    const draggingNodeRef = useRef<string | null>(null);
    const mousePositionRef = useRef<[number, number]>([0, 0]);

    useEffect(() => {
        draggingNodeRef.current = dragging_node;
    }, [dragging_node]);

    useEffect(() => {
        mousePositionRef.current = mouse_position;
    }, [mouse_position]);

    const grid = new Grid(100);

    const updatePhysics = (dt: number) => {
        setNodes(_nodes => {
            let new_nodes = {..._nodes};
            grid.clear();
            for (let node_id of nodes_to_display.current) {
                let node = new_nodes[node_id];
                if (!node) continue;
                grid.insert(node_id, node.position);
            }
            let avg_node_position = [0, 0];
            for (let node_id of nodes_to_display.current) {
                let node = new_nodes[node_id];
                if (!node) continue;
                avg_node_position[0] += 0.1 * node.position[0] / Object.keys(nodes_to_display.current).length;
                avg_node_position[1] += 0.1 * node.position[1] / Object.keys(nodes_to_display.current).length;
            }
            for (let node_id of nodes_to_display.current) {
                let node = new_nodes[node_id];
                if (!node) continue;
                let personal_dt = dt * (0.3 + (20 / (10 + (node.simulated_time_since_creation ** 2))))
                const nearbyNodes = grid.retrieve(node.position);
                for (let other_node_id of nearbyNodes) {
                    if (other_node_id === node_id) continue;
                    let other_node = new_nodes[other_node_id];
                    if (!other_node) continue;
                    let delta_vector = [node.position[0] - other_node.position[0], node.position[1] - other_node.position[1]];
                    let distance = Math.max(0.01, Math.sqrt(delta_vector[0] * delta_vector[0] + delta_vector[1] * delta_vector[1]));
                    if (distance > 100) continue;
                    let delta_vector_normalized = [delta_vector[0] / distance, delta_vector[1] / distance];
                    let repulsion = 500 * ((1 + (nodes_to_display.current.length * 2 / MAXIMUM_NUMBER_OF_NODES_DISPLAYED)) ** 2) * ((1 + node.graph_contribution * 2)) / (distance + 1);
                    node.velocity[0] += delta_vector_normalized[0] * repulsion * dt;
                    node.velocity[1] += delta_vector_normalized[1] * repulsion * dt;
                }
                let delta_from_center = node.position;
                let distance_from_center = Math.sqrt(delta_from_center[0] * delta_from_center[0] + delta_from_center[1] * delta_from_center[1]);
                let delta_from_center_normalized = [delta_from_center[0] / distance_from_center, delta_from_center[1] / distance_from_center];
                let attraction = node.graph_contribution * distance_from_center;
                node.velocity[0] -= delta_from_center_normalized[0] * attraction * personal_dt * 0.01;
                node.velocity[1] -= delta_from_center_normalized[1] * attraction * personal_dt * 0.01;
                let node_connection_length_sum = 0;
                for (let connected_node of node.connected_nodes) {
                    node_connection_length_sum += connected_node[1];
                }
                node_connection_length_sum = Math.max(0.01, node_connection_length_sum);
                for (let connected_node of node.connected_nodes) {
                    let other_node = new_nodes[connected_node[0]];
                    if (!other_node) continue;
                    let normalized_length = (1 + (5 * connected_node[1] / node_connection_length_sum));
                    other_node.velocity[0] -= (other_node.position[0] - node.position[0]) * normalized_length * personal_dt * 0.1;
                    other_node.velocity[1] -= (other_node.position[1] - node.position[1]) * normalized_length * personal_dt * 0.1;
                }
                if (draggingNodeRef.current === node_id) {
                    personal_dt = dt;
                    node.velocity[0] += (mousePositionRef.current[0] - node.position[0]) * personal_dt * 20;
                    node.velocity[1] += (mousePositionRef.current[1] - node.position[1]) * personal_dt * 20;
                }

                node.velocity[0] -= avg_node_position[0] * personal_dt;
                node.velocity[1] -= avg_node_position[1] * personal_dt;

                let drag_factor = Math.pow(1 / node.drag, personal_dt);
                node.velocity[0] *= drag_factor;
                node.velocity[1] *= drag_factor;

                node.position[0] += node.velocity[0] * personal_dt;
                node.position[1] += node.velocity[1] * personal_dt;

                node.simulated_time_since_creation += dt;
            }
            return new_nodes;
        });
    };

    const updateNodeDisplayPositions = useCallback((dt: number) => {
        setNodes(_nodes => {
            let new_nodes = {..._nodes};
            for (let node_id in new_nodes) {
                let node = new_nodes[node_id];
                if (!node) continue;
                node.display_position[0] = node.display_position[0] + (node.position[0] - node.display_position[0]) * 0.2;
                node.display_position[1] = node.display_position[1] + (node.position[1] - node.display_position[1]) * 0.2;
            }
            return new_nodes;
        });
    }, []);

    const svg_ref = React.createRef<SVGSVGElement>();

    return <>
        <svg
            ref={svg_ref}
            className="case-knowledge-graph"
            viewBox={`${viewport[0]} ${viewport[1]} ${viewport[2]} ${viewport[3]}`}
            style={{width: '100%', height: '100%'}}
            onMouseMove={(event) => {
                if (!svg_ref.current) return;
                let svgPoint = svg_ref.current.createSVGPoint();
                svgPoint.x = event.clientX;
                svgPoint.y = event.clientY;
                let screenCTM = svg_ref.current.getScreenCTM();
                if (!screenCTM) return;
                svgPoint = svgPoint.matrixTransform(screenCTM.inverse());
                if (mouse_down && !dragging_node) {
                    let new_viewport: [number, number, number, number] = [viewport[0] - event.movementX * viewport[2] / 500, viewport[1] - event.movementY * viewport[2] / 500, viewport[2], viewport[3]];
                    let new_viewport_distance_from_center = Math.sqrt(((new_viewport[0] + new_viewport[2] / 2) ** 2) + ((new_viewport[1] + new_viewport[3] / 2) ** 2));
                    if (new_viewport_distance_from_center > radius * 100) return;
                    setViewport(new_viewport);
                }
                setMousePosition([svgPoint.x, svgPoint.y]);
            }}
            onMouseUp={() => {
                setDraggingNode(null);
                setMouseDown(false);
            }}
            onWheel={(event) => {
                let delta = event.deltaY;
                if (viewport[2] + delta < 75 || viewport[3] + delta < 75) return;
                viewport[0] = viewport[0] - delta;
                viewport[1] = viewport[1] - delta;
                viewport[2] = viewport[2] + delta * 2;
                viewport[3] = viewport[3] + delta * 2;
            }}
            onMouseDown={() => {
                setMouseDown(true);
            }}
        >
            {Object.keys(edges).map((edge_id) => {
                let edge = edges[edge_id];
                if (edge == undefined) return;
                if (!nodes_to_display.current.includes(edge.from_entity.toString())) return;
                if (!nodes_to_display.current.includes(edge.to_entity.toString())) return;
                let node_from = nodes[edge.from_entity];
                let node_to = nodes[edge.to_entity];
                if (node_from == undefined || node_to == undefined) return;
                if (node_from.simulated_time_since_creation < time_of_initial_simulation) return;
                if (node_to.simulated_time_since_creation < time_of_initial_simulation) return;
                let line_width = edge.state == 'hovered' ? 5 : edge.state == 'highlighted' ? 3 * edge.normalized_weight : edge.width;
                return <g key={edge_id} className={'graph-edge'} id={edge_id}>
                    <line
                        key={edge_id + '-line'}
                        x1={node_from.display_position[0].toString()}
                        y1={node_from.display_position[1].toString()}
                        x2={node_to.display_position[0].toString()}
                        y2={node_to.display_position[1].toString()}
                        fill={'#000000f0'}
                        width={'1px'}
                        stroke={'#000000f0'}
                        style={{strokeWidth: `${line_width}px`}}
                        onMouseEnter={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(edge.from_entity, 'secondary-highlight');
                            setNodeState(edge.to_entity, 'secondary-highlight');
                            setEdgeState(edge_id, 'hovered');
                            props.edgeHoverCallback(edge_id, true);
                        }}
                        onMouseLeave={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(edge.from_entity, 'idle');
                            setNodeState(edge.to_entity, 'idle');
                            setEdgeState(edge_id, 'idle');
                            props.edgeHoverCallback(edge_id, false);
                        }}
                        onClick={e => {
                            if (draggingNodeRef.current) return;
                            props.edgeClickCallback(edge_id)
                        }}
                    />
                </g>
            })}
            {Object.keys(nodes).map((node_id) => {
                if (!nodes_to_display.current.includes(node_id)) return;
                let node = nodes[node_id];
                if (node.simulated_time_since_creation < time_of_initial_simulation) return;
                let color = ((node_style[node.label] || {}).color || {})[node.state] || 'white';
                let icon = (node_style[node.label] || {}).icon;
                let size = (5 + 5 * node.graph_contribution) + (node.state === 'highlight' ? 3 : node.state == 'secondary-highlight' ? 1.5 : 0);
                let node_title = node.title || '';
                node_title = node_title.length > 20 ? node_title.substring(0, 20) + '...' : node_title;
                return <g key={node_id} className={`graph-node ${node.label}`} id={node_id}>
                    <circle
                        key={node_id + '-circle'}
                        cx={node.display_position[0].toString()}
                        cy={node.display_position[1].toString()}
                        r={size.toString()}
                        stroke="black"
                        fill={color}
                        style={{strokeWidth: '1px'}}
                        onMouseDown={() => {
                            if (draggingNodeRef.current) return;
                            setDraggingStartPosition([node.display_position[0], node.display_position[1]]);
                            setDraggingNode(node_id)
                        }}
                        onMouseEnter={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(node_id, 'highlight')
                            for (let connected_node of node.connected_nodes)
                                setNodeState(connected_node[0], 'secondary-highlight');
                            props.nodeHoverCallback(node_id, true);
                        }}
                        onMouseLeave={() => {
                            if (draggingNodeRef.current) return;
                            setNodeState(node_id, 'idle');
                            for (let connected_node of node.connected_nodes)
                                setNodeState(connected_node[0], 'idle');
                            props.nodeHoverCallback(node_id, false);
                        }}
                        onClick={e => {
                            if (draggingNodeRef.current) return;
                            if (Math.abs(mouse_position[0] - dragging_start_position[0]) > 10) return;
                            if (Math.abs(mouse_position[1] - dragging_start_position[1]) > 10) return;
                            props.nodeClickCallback(node_id);
                        }}
                    >
                    </circle>
                    <foreignObject
                        key={node_id + '-icon'}
                        x={node.display_position[0] - 1.25 * size / 2}
                        y={node.display_position[1] - 1.25 * size / 2}
                        width={1.25 * size}
                        height={1.25 * size}
                        style={{fontSize: `${size}px`, pointerEvents: 'none', color: 'white'}}
                    >
                        <FontAwesomeIcon icon={icon} fixedWidth={true}/>
                    </foreignObject>
                    <text
                        key={node_id + '-label'}
                        x={node.display_position[0].toString()}
                        y={(node.display_position[1] + 16).toString()}
                        textAnchor="middle"
                        dominantBaseline="central"
                        fill="white"
                    >{node_title}</text>
                </g>
            })}
        </svg>
    </>
});

class Grid {
    private readonly cellSize: number;
    private cells: { [key: string]: string[] };

    constructor(cellSize: number) {
        this.cellSize = cellSize;
        this.cells = {};
    }

    clear(): void {
        this.cells = {};
    }

    insert(id: string, position: [number, number]): void {
        const column = Math.floor(position[0] / this.cellSize);
        const row = Math.floor(position[1] / this.cellSize);
        const index = `${row}-${column}`;
        let cell = this.cells[index] || [];
        cell.push(id);
        this.cells[index] = cell;
    }

    retrieve(position: [number, number]): string[] {
        const column = Math.floor(position[0] / this.cellSize);
        const row = Math.floor(position[1] / this.cellSize);
        let nodes: string[] = [];
        for (let i = -1; i <= 1; i++) {
            for (let j = -1; j <= 1; j ++) {
                const index = `${(row + i)}-${(column + j)}`;
                nodes.push(...(this.cells[index] || []));
            }
        }
        return nodes;
    }
}
