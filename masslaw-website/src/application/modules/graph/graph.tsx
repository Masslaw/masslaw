import React from "react";
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

export class Graph {

    private number_of_updates_per_frame = 50;

    private current_update_node_index = 0;

    private time_of_initial_simulation = 5;

    private svg_ref = React.createRef<SVGSVGElement>();
    private radius = 100;
    private mouse_position: [number, number] = [0, 0];
    private dragging_node: string | null = null;
    private mouse_down: boolean = false;
    private viewport: [number, number, number, number] = [-250, -250, 500, 500];
    private nodes: { [key: string]: Node } = {};
    private edges: { [ket: string]: Edge } = {};

    private previousPhysicsUpdateTime = now();
    private previousDisplayUpdateTime = now();

    constructor() {
        this.physicsUpdateLoop();
        this.displayUpdateLoop();
    }

    public reset() {
        this.nodes = {};
        this.edges = {};
    }

    private physicsUpdateLoop() {
        let _now = now();
        let dt = (_now - this.previousPhysicsUpdateTime) / 1000;
        this.previousPhysicsUpdateTime = _now;
        this.updatePhysics(dt);
        setTimeout(() => this.physicsUpdateLoop(), 0);
    }

    private displayUpdateLoop() {
        let _now = now();
        let dt = (_now - this.previousDisplayUpdateTime) / 1000;
        this.previousDisplayUpdateTime = _now;
        this.updateNodeDisplayPositions(dt);
        setTimeout(() => this.displayUpdateLoop(), 0);
    }

    public addNode(node_id: string, node_label: string, node_title?: string) {
        let theta = Math.random() * Math.PI * 2;
        let x = this.radius * Math.cos(theta);
        let y = this.radius * Math.sin(theta);
        this.nodes[node_id] = {
            label: node_label,
            title: node_title,
            position: [x, y],
            display_position: [x, y],
            velocity: [0, 0],
            graph_contribution: 1,
            drag: 2,
            connected_nodes: [],
            state: 'idle',
            simulated_time_since_creation: 0
        };
        this.onGraphUpdated();
    }

    public addEdge(edge_id: string, from_entity: string, to_entity: string, weight: number) {
        if (!edge_id || !from_entity || !to_entity || !weight) return;
        let edge_element = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        edge_element.setAttribute('stroke', 'black');
        edge_element.setAttribute('stroke-width', '1');
        this.edges[edge_id] = {
            from_entity: from_entity, to_entity: to_entity, weight: weight, normalized_weight: 0, state: 'idle', width: 0,
        };
        this.onGraphUpdated();
    }

    public getElement() {
        return <>
            <svg
                ref={this.svg_ref}
                className="case-knowledge-graph"
                viewBox={`${this.viewport[0]} ${this.viewport[1]} ${this.viewport[2]} ${this.viewport[3]}`}
                style={{width: '100%', height: '100%'}}
                onMouseMove={(event) => {
                    if (!this.svg_ref.current) return;
                    let svgPoint = this.svg_ref.current.createSVGPoint();
                    svgPoint.x = event.clientX;
                    svgPoint.y = event.clientY;
                    let screenCTM = this.svg_ref.current.getScreenCTM();
                    if (!screenCTM) return;
                    svgPoint = svgPoint.matrixTransform(screenCTM.inverse());
                    if (this.mouse_down && !this.dragging_node) {
                        let new_viewport: [number, number, number, number] = [this.viewport[0] - event.movementX * this.viewport[2] / 500, this.viewport[1] - event.movementY * this.viewport[2] / 500, this.viewport[2], this.viewport[3]];
                        let new_viewport_distance_from_center = Math.sqrt(((new_viewport[0] + new_viewport[2] / 2) ** 2) + ((new_viewport[1] + new_viewport[3] / 2) ** 2));
                        if (new_viewport_distance_from_center > this.radius * 100) return;
                        this.viewport = new_viewport;
                    }
                    this.mouse_position = [svgPoint.x, svgPoint.y];
                }}
                onMouseUp={() => {
                    this.dragging_node = null;
                    this.mouse_down = false;
                }}
                onWheel={(event) => {
                    let delta = event.deltaY;
                    if (this.viewport[2] + delta < 75 || this.viewport[3] + delta < 75) return;
                    this.viewport[0] = this.viewport[0] - delta;
                    this.viewport[1] = this.viewport[1] - delta;
                    this.viewport[2] = this.viewport[2] + delta * 2;
                    this.viewport[3] = this.viewport[3] + delta * 2;
                }}
                onMouseDown={() => {
                    this.mouse_down = true;
                }}
            >
                {Object.keys(this.edges).map((edge_id) => {
                    let edge = this.edges[edge_id];
                    let node_from = this.nodes[edge.from_entity];
                    if (node_from.simulated_time_since_creation < this.time_of_initial_simulation) return;
                    let node_to = this.nodes[edge.to_entity];
                    if (node_to.simulated_time_since_creation < this.time_of_initial_simulation) return;
                    let line_width = edge.state == 'hovered' ? 5 : edge.state == 'highlighted' ? 3 * edge.normalized_weight : edge.width;
                    return <g key={edge_id} className={'graph-edge'} id={edge_id}>
                        <line
                            x1={node_from.display_position[0].toString()}
                            y1={node_from.display_position[1].toString()}
                            x2={node_to.display_position[0].toString()}
                            y2={node_to.display_position[1].toString()}
                            fill={'#000000f0'}
                            width={'1px'}
                            stroke={'#000000f0'}
                            style={{strokeWidth: `${line_width}px`}}
                            onMouseEnter={() => {
                                this.nodes[edge.from_entity].state = 'secondary-highlight';
                                this.nodes[edge.to_entity].state = 'secondary-highlight';
                                edge.state = 'hovered';
                                this.onEdgeHoverCallback(edge_id, true);
                            }}
                            onMouseLeave={() => {
                                this.nodes[edge.from_entity].state = 'idle';
                                this.nodes[edge.to_entity].state = 'idle';
                                edge.state = 'idle';
                                this.onEdgeHoverCallback(edge_id, false);
                            }}
                            onClick={e => {
                                this.onEdgeClickedCallback(edge_id)
                            }}
                        />
                    </g>
                })}
                {Object.keys(this.nodes).map((node_id) => {
                    let node = this.nodes[node_id];
                    if (node.simulated_time_since_creation < this.time_of_initial_simulation) return;
                    let color = ((node_style[node.label] || {}).color || {})[node.state] || 'white';
                    let icon = (node_style[node.label] || {}).icon;
                    let size = (5 + 5 * node.graph_contribution) + (node.state === 'highlight' ? 3 : node.state == 'secondary-highlight' ? 1.5 : 0);
                    let node_title = node.title || '';
                    node_title = node_title.length > 20 ? node_title.substring(0, 20) + '...' : node_title;
                    return <g key={node_id} className={`graph-node ${node.label}`} id={node_id}>
                        <circle
                            cx={node.display_position[0].toString()}
                            cy={node.display_position[1].toString()}
                            r={size.toString()}
                            stroke="black"
                            fill={color}
                            style={{strokeWidth: '1px'}}
                            onMouseDown={() => this.dragging_node = node_id}
                            onMouseEnter={() => {
                                this.nodes[node_id].state = 'highlight';
                                for (let connected_node of node.connected_nodes) {
                                    this.nodes[connected_node[0]].state = 'secondary-highlight';
                                }
                                this.onNodeHoverCallback(node_id, true);
                            }}
                            onMouseLeave={() => {
                                this.nodes[node_id].state = 'idle';
                                for (let connected_node of node.connected_nodes) {
                                    this.nodes[connected_node[0]].state = 'idle';
                                }
                                this.onNodeHoverCallback(node_id, false);
                            }}
                            onClick={e => {
                                this.onNodeClickedCallback(node_id);
                            }}
                        >
                        </circle>
                        <foreignObject
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
    }

    public updatePhysics(dt: number) {
        this.number_of_updates_per_frame = Math.max(this.number_of_updates_per_frame, 20);
        dt = Math.min(dt, 0.016);
        dt *= 5;
        let nodes_to_update = this.getNextUpdateChunkAndIncrement();
        if (this.dragging_node && !nodes_to_update.includes(this.dragging_node)) nodes_to_update.push(this.dragging_node);
        let avg_node_position = [0, 0];
        for (let node_id in this.nodes) {
            let node = this.nodes[node_id];
            if (!node) continue;
            avg_node_position[0] += 0.1 * node.position[0] / Object.keys(this.nodes).length;
            avg_node_position[1] += 0.1 * node.position[1] / Object.keys(this.nodes).length;
        }
        for (let node_id of nodes_to_update) {
            let node = this.nodes[node_id];
            if (!node) continue;
            for (let other_node_id in this.nodes) {
                if (other_node_id === node_id) continue;
                let other_node = this.nodes[other_node_id];
                if (!other_node) continue;
                let delta_vector = [other_node.position[0] - node.position[0], other_node.position[1] - node.position[1]];
                let distance = Math.sqrt(delta_vector[0] * delta_vector[0] + delta_vector[1] * delta_vector[1]);
                let delta_vector_normalized = [delta_vector[0] / distance, delta_vector[1] / distance];
                let repulsion = 500 / (distance + 1);
                other_node.velocity[0] += delta_vector_normalized[0] * repulsion * dt;
                other_node.velocity[1] += delta_vector_normalized[1] * repulsion * dt;
            }
            let delta_from_center = node.position;
            let distance_from_center = Math.sqrt(delta_from_center[0] * delta_from_center[0] + delta_from_center[1] * delta_from_center[1]);
            let delta_from_center_normalized = [delta_from_center[0] / distance_from_center, delta_from_center[1] / distance_from_center];
            let attraction = node.graph_contribution * distance_from_center * distance_from_center;
            if (distance_from_center > this.radius) {
                attraction += distance_from_center * distance_from_center / this.radius + this.radius;
            }
            node.velocity[0] -= delta_from_center_normalized[0] * attraction * dt * 0.01;
            node.velocity[1] -= delta_from_center_normalized[1] * attraction * dt * 0.01;

            let node_connection_length_sum = 0;
            for (let connected_node of node.connected_nodes) {
                node_connection_length_sum += connected_node[1];
            }
            for (let connected_node of node.connected_nodes) {
                let other_node = this.nodes[connected_node[0]];
                if (!other_node) continue;
                let normalized_length = (1 + (connected_node[1] / node_connection_length_sum));
                other_node.velocity[0] -= (other_node.position[0] - node.position[0]) * normalized_length * dt * 0.1;
                other_node.velocity[1] -= (other_node.position[1] - node.position[1]) * normalized_length * dt * 0.1;
            }

            if (this.dragging_node == node_id) {
                node.velocity[0] += (this.mouse_position[0] - node.position[0]) * dt * 20;
                node.velocity[1] += (this.mouse_position[1] - node.position[1]) * dt * 20;
            }

            node.velocity[0] -= avg_node_position[0] * dt;
            node.velocity[0] -= avg_node_position[0] * dt;

            let drag_factor = Math.pow(1 / node.drag, dt);
            node.velocity[0] *= drag_factor;
            node.velocity[1] *= drag_factor;

            node.position[0] += node.velocity[0] * dt;
            node.position[1] += node.velocity[1] * dt;

            node.simulated_time_since_creation += dt;
        }
    }

    private getNextUpdateChunkAndIncrement() : string[] {
        const nodeKeys = Object.keys(this.nodes);
        const numNodes = nodeKeys.length;
        let number_of_updates_per_frame = Math.min(this.number_of_updates_per_frame, numNodes);
        let startIndex = this.current_update_node_index;
        let endIndex = startIndex + number_of_updates_per_frame;
        let updateNodes: string[] = [];
        for (let i = startIndex; i < endIndex; i++) {
            let wrappedIndex = i % numNodes;
            let node_key = nodeKeys[wrappedIndex];
            updateNodes.push(node_key);
        }
        this.current_update_node_index = (endIndex % numNodes) || 0;
        return updateNodes;
    }

    private updateNodeDisplayPositions(dt: number) {
        for (let node_id in this.nodes) {
            let node = this.nodes[node_id];
            if (!node) continue;
            node.display_position[0] = node.display_position[0] + (node.position[0] - node.display_position[0]) * 0.2;
            node.display_position[1] = node.display_position[1] + (node.position[1] - node.display_position[1]) * 0.2;
        }
    }

    public getNodeById(node_id: string) {
        return this.nodes[node_id];
    }

    public getEdgeById(edge_id: string) {
        return this.edges[edge_id];
    }

    public setNodeClickCallback(callback: (node_id: string) => void) {
        this.onNodeClickedCallback = callback;
    }

    public setEdgeClickCallback(callback: (edge_id: string) => void) {
        this.onEdgeClickedCallback = callback;
    }

    public setNodeHoverCallback(callback: (node_id: string, hovering: boolean) => void) {
        this.onNodeHoverCallback = callback
    }

    public setEdgeHoverCallback(callback: (edge_id: string, hovering: boolean) => void) {
        this.onEdgeHoverCallback = callback
    }

    private onNodeClickedCallback: (node_id: string) => void = (node_id: string) => {
    };

    private onNodeHoverCallback: (node_id: string, hovering: boolean) => void = (node_id: string) => {
    };

    private onEdgeClickedCallback: (edge_id: string) => void = (edge_id: string) => {
    };

    private onEdgeHoverCallback: (edge_id: string, hovering: boolean) => void = (edge_id: string) => {
    };

    private onGraphUpdated() {
        let max_weight = 0;
        let max_contribution = 0;
        let number_of_nodes = Object.keys(this.nodes).length;
        this.radius = Math.sqrt(number_of_nodes);
        for (let edge_id in this.edges) {
            let edge = this.edges[edge_id];
            if (!this.nodes[edge.from_entity] || !this.nodes[edge.to_entity]) {
                delete this.edges[edge_id];
            }
        }
        for (let node_id in this.nodes) {
            let node = this.nodes[node_id];
            node.graph_contribution = 0;
            node.connected_nodes = [];
        }
        for (let edge_id in this.edges) {
            let edge = this.edges[edge_id];
            max_weight = Math.max(max_weight, edge.weight);
            let edge_from = this.nodes[edge.from_entity];
            let edge_to = this.nodes[edge.to_entity];
            edge_from.graph_contribution += edge.weight;
            edge_to.graph_contribution += edge.weight;
            let connection_length = Math.min(50 + 200 / edge.weight, this.radius);
            edge_from.connected_nodes.push([edge.to_entity, connection_length]);
            edge_to.connected_nodes.push([edge.from_entity, connection_length]);
            max_contribution = Math.max(max_contribution, edge_from.graph_contribution, edge_to.graph_contribution);
        }
        for (let node_id in this.nodes) {
            let node = this.nodes[node_id];
            node.graph_contribution = node.graph_contribution / max_contribution;
            node.drag = 2 + 10 * node.graph_contribution;
        }
        for (let edge_id in this.edges) {
            let edge = this.edges[edge_id];
            edge.normalized_weight = edge.weight / max_weight;
            edge.width = 3 * Math.sin((1 - ((edge.normalized_weight - 1) ** 2)) * Math.PI / 2);
        }
    }
}