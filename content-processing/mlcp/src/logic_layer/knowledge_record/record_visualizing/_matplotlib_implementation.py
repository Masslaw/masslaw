from typing import Callable
import networkx
import matplotlib.pyplot as plt
from logic_layer.knowledge_record import KnowledgeRecordEntity
from logic_layer.knowledge_record._record import KnowledgeRecord


BACKGROUND_COLOR = 'white'
NODE_COLOR = 'lightblue'
EDGE_COLOR = 'gray'
NODE_LABEL_COLOR = 'black'
NODE_SIZE = 350
FONT_SIZE = 4


def knowledge_record_to_graph_image(record: KnowledgeRecord, filename: str = 'record.png', entity_title_generator: Callable[[KnowledgeRecordEntity], str] = None):
    G = networkx.Graph()
    print(len(record.get_connections()))
    for connenction in record.get_connections():
        from_entity = connenction.get_from_entity()
        to_entity = connenction.get_to_entity()
        from_entity_title = entity_title_generator and entity_title_generator(from_entity) or from_entity.get_id()
        to_entity_title = entity_title_generator and entity_title_generator(to_entity) or to_entity.get_id()
        G.add_edge(from_entity_title, to_entity_title)
    plt.figure(facecolor=BACKGROUND_COLOR)
    pos = networkx.spring_layout(G, seed=42)
    networkx.draw(G, pos, node_color=NODE_COLOR, edge_color=EDGE_COLOR, node_size=350)
    for label, (x, y) in pos.items():
        plt.text(x, y, label, fontsize=4, ha='center', va='center', color=NODE_LABEL_COLOR, bbox=dict(facecolor=NODE_COLOR, edgecolor=NODE_COLOR, boxstyle='round,pad=0.3'))
    plt.savefig(filename, dpi=500, facecolor=BACKGROUND_COLOR)

