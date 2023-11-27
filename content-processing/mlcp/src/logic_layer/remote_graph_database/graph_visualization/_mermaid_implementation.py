from typing import IO

from logic_layer.remote_graph_database._graph_database_manager import GraphDatabaseManager


def visualize_graph_database_using_mermaid(graph_database_manager: GraphDatabaseManager, output_file: str, node_title_property: str = 'title'):
    def get_title(node):
        return node.get_properties().get(node_title_property, 'untitled').replace(' ', '_')

    mermaid_script = "graph LR\n"
    all_nodes = graph_database_manager.get_nodes_by_properties({})
    all_edges = graph_database_manager.get_edges_by_properties({})
    for node in all_nodes:
        mermaid_script += f"{node.get_id()}({get_title(node)})\n"
    for edge in all_edges:
        from_id = edge.get_from_node()
        to_id = edge.get_to_node()
        mermaid_script += f"{from_id} --> | {edge.get_label()} | {to_id}\n"
    with open(output_file, 'w') as f:
        f.write(mermaid_script)
