import React from "react";

export class Graph {

    private svg_ref = React.createRef<SVGSVGElement>();
    private radius = 100;
    private mouse_position: [number, number] = [0, 0];
    private dragging_node: string | null = null;

    private viewport: [number, number, number, number] = [-250, -250, 500, 500];

    private nodes: {[key:string]: {
        label: string,
        title?: string,
        position: [number, number],
        velocity: [number, number],
        drag: number,
        graph_contribution: number,
        connected_nodes: [string, number][],
        state: string,
    }} = {};
    private edges: {[ket:string]: {
        label?: string,
        from_entity: string,
        to_entity: string,
        weight: number,
        normalized_weight: number,
        highlighted: boolean,
    }} = {};

    private node_colors: {[key:string]: { [key:string]: string }} = {
        'PERSON': {
            'highlight': '#76bbff',
            'secondary-highlight': '#3280cc',
            'idle': '#0d579d',
        },
        'ORG': {
            'highlight': '#ff8b76',
            'secondary-highlight': '#cc5232',
            'idle': '#9d2b0d',
        },
        'GPE': {
            'highlight': '#76ff8b',
            'secondary-highlight': '#32cc52',
            'idle': '#0d9d2b',
        },
        'LOC': {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        'PRODUCT': {
            'highlight': '#ffbb76',
            'secondary-highlight': '#cc8032',
            'idle': '#9d570d',
        },
        'EVENT': {
            'highlight': '#bb76ff',
            'secondary-highlight': '#8032cc',
            'idle': '#570d9d',
        },
        'WORK_OF_ART': {
            'highlight': '#bbff76',
            'secondary-highlight': '#80cc32',
            'idle': '#579d0d',
        },
        'LAW': {
            'highlight': '#76ffbb',
            'secondary-highlight': '#32cc80',
            'idle': '#0d9d57',
        },
        'LANGUAGE': {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        'DATE': {
            'highlight': '#76bbff',
            'secondary-highlight': '#3280cc',
            'idle': '#0d579d',
        },
        'TIME': {
            'highlight': '#ff8b76',
            'secondary-highlight': '#cc5232',
            'idle': '#9d2b0d',
        },
        'PERCENT': {
            'highlight': '#76ff8b',
            'secondary-highlight': '#32cc52',
            'idle': '#0d9d2b',
        },
        'MONEY': {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
        'QUANTITY': {
            'highlight': '#ffbb76',
            'secondary-highlight': '#cc8032',
            'idle': '#9d570d',
        },
        'ORDINAL': {
            'highlight': '#bb76ff',
            'secondary-highlight': '#8032cc',
            'idle': '#570d9d',
        },
        'CARDINAL': {
            'highlight': '#bbff76',
            'secondary-highlight': '#80cc32',
            'idle': '#579d0d',
        },
        'FAC': {
            'highlight': '#76ffbb',
            'secondary-highlight': '#32cc80',
            'idle': '#0d9d57',
        },
        'NORP': {
            'highlight': '#ff76bb',
            'secondary-highlight': '#cc3280',
            'idle': '#9d0d57',
        },
    };

    public addNode(node_id: string, node_label: string, node_title?: string) {
        let theta = Math.random() * Math.PI * 2;
        let x = this.radius * Math.cos(theta);
        let y = this.radius * Math.sin(theta);
        this.nodes[node_id] = {
            label: node_label,
            title: node_title,
            position: [x, y],
            velocity: [0, 0],
            graph_contribution: 1,
            drag: 2,
            connected_nodes: [],
            state: 'idle',
        };
        this.onGraphUpdated();
    }

    public addEdge(edge_id: string, from_entity: string, to_entity: string, weight: number) {
        if (!edge_id || !from_entity || !to_entity || !weight) return;
        let edge_element = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        edge_element.setAttribute('stroke', 'black');
        edge_element.setAttribute('stroke-width', '1');
        this.edges[edge_id] = {
            from_entity: from_entity,
            to_entity: to_entity,
            weight: weight,
            normalized_weight: 0,
            highlighted: false,
        };
        this.onGraphUpdated();
    }

    private onGraphUpdated() {
        let max_weight = 0;
        let max_contribution = 0;
        let number_of_nodes = Object.keys(this.nodes).length;
        this.radius = 2 * Math.sqrt(number_of_nodes);
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
            let connection_length = 100 +  500 / edge.weight;
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
        }
    }

    public getElement() {
        return <>
            <svg
                ref={this.svg_ref}
                className="case-knowledge-graph"
                viewBox={`${this.viewport[0]} ${this.viewport[1]} ${this.viewport[2]} ${this.viewport[3]}`}
                style={{ width: '100%', height: '100%' }}
                onMouseMove={(event) => {
                    if (!this.svg_ref.current) return;
                    let svgPoint = this.svg_ref.current.createSVGPoint();
                    svgPoint.x = event.clientX;
                    svgPoint.y = event.clientY;
                    let screenCTM = this.svg_ref.current.getScreenCTM();
                    if (!screenCTM) return;
                    svgPoint = svgPoint.matrixTransform(screenCTM.inverse());
                    this.mouse_position = [svgPoint.x, svgPoint.y];
                }}
                onMouseUp={() => this.dragging_node = null}
                onWheel={(event) => {
                    let delta = event.deltaY;
                    this.viewport[0] = Math.min(this.viewport[0] - delta, -100);
                    this.viewport[1] = Math.min(this.viewport[1] - delta, -100);
                    this.viewport[2] = Math.max(this.viewport[2] + delta + delta, 200);
                    this.viewport[3] = Math.max(this.viewport[3] + delta + delta, 200);
                }}
            >
                {Object.keys(this.edges).map((edge_id) => {
                    let edge =  this.edges[edge_id];
                    let node_from = this.nodes[edge.from_entity];
                    let node_to = this.nodes[edge.to_entity];
                    return <g key={edge_id} className={'graph-edge'} id={edge_id}>
                        <line
                            x1={node_from.position[0].toString()}
                            y1={node_from.position[1].toString()}
                            x2={node_to.position[0].toString()}
                            y2={node_to.position[1].toString()}
                            stroke={"black"}
                            style={{strokeWidth: `${((edge.highlighted ? 2 : 1) * 5 * edge.normalized_weight)}px`}}
                            onMouseEnter={() => {
                                this.nodes[edge.from_entity].state = 'secondary-highlight';
                                this.nodes[edge.to_entity].state = 'secondary-highlight';
                                edge.highlighted = true;
                            }}
                            onMouseLeave={() => {
                                this.nodes[edge.from_entity].state = 'idle';
                                this.nodes[edge.to_entity].state = 'idle';
                                edge.highlighted = false;
                            }}
                        />
                    </g>
                })}
                {Object.keys(this.nodes).map((node_id) => {
                    let node = this.nodes[node_id];
                    let color = (this.node_colors[node.label] || {})[node.state] || 'white';
                    let size = (5 + 5 * node.graph_contribution) + (node.state === 'highlight' ? 3 : node.state == 'secondary-highlight' ? 1.5 : 0);
                    return <g key={node_id} className={`graph-node ${node.label}`} id={node_id} >
                        <circle
                            cx={node.position[0].toString()}
                            cy={node.position[1].toString()}
                            r={size.toString()}
                            stroke="black"
                            fill={color}
                            style={{strokeWidth: '1px'}}
                            onMouseDown={() => this.dragging_node = node_id }
                            onMouseEnter={() => {
                                this.nodes[node_id].state = 'highlight';
                                for(let connected_node of node.connected_nodes) {
                                    this.nodes[connected_node[0]].state = 'secondary-highlight';
                                }
                            }}
                            onMouseLeave={() => {
                                this.nodes[node_id].state = 'idle';
                                for(let connected_node of node.connected_nodes) {
                                    this.nodes[connected_node[0]].state = 'idle';
                                }
                            }}
                        />
                        <text
                            key={node_id + '-label'}
                            x={node.position[0].toString()}
                            y={(node.position[1] + 20).toString()}
                            textAnchor="middle"
                            dominantBaseline="central"
                            fill="black"
                            stroke="white"
                            strokeWidth="0.5"
                            style={{ fontSize: '10px', fontWeight: 'bold' }}
                        >{node.title}</text>
                    </g>
                })}
            </svg>
        </>
    }

    public update(dt: number) {
        let fdt = 0.003;
        for (let i = 0; i < 50; i++) {
            let avg_node_position = [0, 0];
            for (let node_id in this.nodes) {
                let node = this.nodes[node_id];
                avg_node_position[0] += 0.1 * node.position[0] / Object.keys(this.nodes).length;
                avg_node_position[1] += 0.1 * node.position[1] / Object.keys(this.nodes).length;
            }
            for (let node_id in this.nodes) {
                let node = this.nodes[node_id];

                for(let other_node_id in this.nodes) {
                    if (other_node_id === node_id) continue;
                    let other_node = this.nodes[other_node_id];
                    let delta_vector = [other_node.position[0] - node.position[0], other_node.position[1] - node.position[1]];
                    let distance = Math.sqrt(delta_vector[0] * delta_vector[0] + delta_vector[1] * delta_vector[1]);
                    let delta_vector_normalized = [delta_vector[0] / distance, delta_vector[1] / distance];
                    let repulsion = 1000 / (distance + 1);
                    other_node.velocity[0] += delta_vector_normalized[0] * repulsion * fdt;
                    other_node.velocity[1] += delta_vector_normalized[1] * repulsion * fdt;
                }

                let delta_from_center = node.position;
                let distance_from_center = Math.sqrt(delta_from_center[0] * delta_from_center[0] + delta_from_center[1] * delta_from_center[1]);
                let delta_from_center_normalized = [delta_from_center[0] / distance_from_center, delta_from_center[1] / distance_from_center];
                let attraction = node.graph_contribution * distance_from_center * distance_from_center;
                if (distance_from_center > this.radius) {
                    attraction += distance_from_center * distance_from_center / this.radius + this.radius;
                }
                node.velocity[0] -= delta_from_center_normalized[0] * attraction * fdt * 0.01;
                node.velocity[1] -= delta_from_center_normalized[1] * attraction * fdt * 0.01;

                let node_connection_length_sum = 0;
                for (let connected_node of node.connected_nodes) {
                    node_connection_length_sum += connected_node[1];
                }
                for(let connected_node of node.connected_nodes) {
                    let other_node = this.nodes[connected_node[0]];
                    let normalized_length = (1 + (connected_node[1] / node_connection_length_sum));
                    other_node.velocity[0] -= (other_node.position[0] - node.position[0]) * normalized_length * fdt * 0.1;
                    other_node.velocity[1] -= (other_node.position[1] - node.position[1]) * normalized_length * fdt * 0.1;
                }

                if (this.dragging_node == node_id) {
                    node.velocity[0] += (this.mouse_position[0] - node.position[0]) * fdt * 2;
                    node.velocity[1] += (this.mouse_position[1] - node.position[1]) * fdt * 2;
                }

                node.velocity[0] -= avg_node_position[0] * fdt;
                node.velocity[0] -= avg_node_position[0] * fdt;

                let drag_factor = Math.pow(1 / node.drag, fdt);
                node.velocity[0] *= drag_factor;
                node.velocity[1] *= drag_factor;

                node.position[0] += node.velocity[0] * fdt;
                node.position[1] += node.velocity[1] * fdt;
            }
        }
    }
}