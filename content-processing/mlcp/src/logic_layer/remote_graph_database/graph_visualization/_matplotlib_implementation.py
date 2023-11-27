from typing import IO

import networkx
import matplotlib.pyplot as plt

from logic_layer.remote_graph_database import GraphDatabaseManager

BACKGROUND_COLOR = 'white'
NODE_COLOR = 'lightblue'
EDGE_COLOR = 'gray'
NODE_LABEL_COLOR = 'black'
NODE_SIZE = 350
FONT_SIZE = 4


def visualize_graph_database_using_matplotlib(graph_database_manager: GraphDatabaseManager, output_file: str, node_title_property: str = 'title'):
    def get_title(node):
        return node.get_properties().get(node_title_property, node.get_id()).replace(' ', '_')

    all_nodes = graph_database_manager.get_nodes_by_properties({})
    all_edges = graph_database_manager.get_edges_by_properties({})

    node_by_id = {}
    for node in all_nodes:
        node_by_id[node.get_id()] = node

    G = networkx.Graph()
    for connenction in all_edges:
        from_entity = connenction.get_from_node()
        to_entity = connenction.get_to_node()
        from_entity_title = get_title(node_by_id[from_entity])
        to_entity_title = get_title(node_by_id[to_entity])
        G.add_edge(from_entity_title, to_entity_title)
    plt.figure(facecolor=BACKGROUND_COLOR)
    pos = networkx.spring_layout(G, seed=42)
    networkx.draw(G, pos, node_color=NODE_COLOR, edge_color=EDGE_COLOR, node_size=350)
    for label, (x, y) in pos.items():
        plt.text(x, y, label, fontsize=4, ha='center', va='center', color=NODE_LABEL_COLOR, bbox=dict(facecolor=NODE_COLOR, edgecolor=NODE_COLOR, boxstyle='round,pad=0.3'))
    plt.savefig(output_file, dpi=500, facecolor=BACKGROUND_COLOR)
