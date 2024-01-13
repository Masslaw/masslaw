import unittest

import gremlin_python

from logic_layer.remote_graph_database import GraphDatabaseEdge
from logic_layer.remote_graph_database import GraphDatabaseNode
from logic_layer.remote_graph_database.neptune_manager import NeptuneDatabaseManager
from mlcp.testing.stubs.neptune_stub import NeptuneStubTestLoader


class TestClassNeptuneDatabaseManager(unittest.TestCase):
    loader = None

    @classmethod
    def setUpClass(cls):
        cls.loader = NeptuneStubTestLoader()
        cls.manager1 = NeptuneDatabaseManager(neptune_read_connection_data={"endpoint": "localhost", "port": 8182, "type": "gremlin"},
            neptune_write_connection_data={"endpoint": "localhost", "port": 8182, "type": "gremlin"}, subgraph_node_properties={"number": 1}, subgraph_edge_properties={"number": 1})
        cls.manager2 = NeptuneDatabaseManager(neptune_read_connection_data={"endpoint": "localhost", "port": 8182, "type": "gremlin"},
            neptune_write_connection_data={"endpoint": "localhost", "port": 8182, "type": "gremlin"}, subgraph_node_properties={"number": 2}, subgraph_edge_properties={"number": 2})

    def tearDown(self):
        nodes = self.manager1.get_nodes_by_properties({})
        self.manager1.delete_nodes_if_exist([node.get_id() for node in nodes])

        edges = self.manager1.get_edges_by_properties({})
        self.manager1.delete_edges_if_exist([edge.get_id() for edge in edges])

        nodes = self.manager2.get_nodes_by_properties({})
        self.manager2.delete_nodes_if_exist([node.get_id() for node in nodes])

        edges = self.manager2.get_edges_by_properties({})
        self.manager2.delete_edges_if_exist([edge.get_id() for edge in edges])

    @classmethod
    def tearDownClass(cls):
        cls.loader.stop_gremlin_server()

    def test_set_new_node(self):
        node_label = "Person"
        node_properties = {"name": "Bob", "age": 30}
        new_node = self.manager1.set_nodes([GraphDatabaseNode(label=node_label, properties=node_properties)])[0]
        node_id = new_node.get_id()

        node = self.manager1.get_nodes_by_ids([node_id])[0]
        self.assertEqual(node.get_id(), node_id)
        self.assertEqual(node.get_label(), node_label)
        self.assertEqual(node.get_properties(), {**node_properties, **self.manager1.get_subgraph_node_properties()})

    def test_replace_node(self):
        existing_node_label = "Person"
        existing_node_properties = {"name": "Bob", "age": 30}
        existing_node = self.manager1.set_nodes([GraphDatabaseNode(label=existing_node_label, properties=existing_node_properties)])[0]
        node_id = existing_node.get_id()

        node = self.manager1.get_nodes_by_ids([node_id])[0]
        self.assertEqual(node.get_id(), node_id)
        self.assertEqual(node.get_label(), existing_node_label)
        self.assertEqual(node.get_properties(), {**existing_node_properties, **self.manager1.get_subgraph_node_properties()})

        new_node_label = "Person"
        new_node_properties = {"name": "Will", "age": 31}
        with self.assertRaises(gremlin_python.driver.protocol.GremlinServerError):
            self.manager1.set_nodes([GraphDatabaseNode(node_id=node_id, label=new_node_label, properties=new_node_properties)])

        self.manager1.delete_nodes_if_exist([node_id])
        self.manager1.set_nodes([GraphDatabaseNode(node_id=node_id, label=new_node_label, properties=new_node_properties)])

        node = self.manager1.get_nodes_by_ids([node_id])[0]
        self.assertEqual(node.get_id(), node_id)
        self.assertEqual(node.get_label(), new_node_label)
        self.assertEqual(node.get_properties(), {**new_node_properties, **self.manager1.get_subgraph_node_properties()})

    def test_update_node_properties(self):
        existing_node_label = "Person"
        existing_node_properties = {"name": "Bob", "age": 30}
        existing_node = self.manager1.set_nodes([GraphDatabaseNode(label=existing_node_label, properties=existing_node_properties)])[0]
        node_id = existing_node.get_id()

        node = self.manager1.get_nodes_by_ids([node_id])[0]
        self.assertIsNotNone(node)
        self.assertEqual(node.get_id(), node_id)
        self.assertEqual(node.get_label(), existing_node_label)
        self.assertEqual(node.get_properties(), {**existing_node_properties, **self.manager1.get_subgraph_node_properties()})

        new_node_properties = {"name": "Will", "age": 31}
        self.manager1.load_properties_to_nodes(node_properties={node_id: new_node_properties})

        node = self.manager1.get_nodes_by_ids([node_id])[0]
        self.assertIsNotNone(node)
        self.assertEqual(node.get_id(), node_id)
        self.assertEqual(node.get_label(), existing_node_label)
        self.assertEqual(node.get_properties(), new_node_properties)

    def test_get_nodes_by_properties(self):
        bob1, bob2 = self.manager1.set_nodes([GraphDatabaseNode(label="Man", properties={'name': 'bob', 'age': 30}),
                                              GraphDatabaseNode(label="Man", properties={'name': 'bob', 'age': 40})])

        alice1, alice2 = self.manager1.set_nodes([GraphDatabaseNode(label="Woman", properties={'name': 'alice', 'age': 30}),
                                                  GraphDatabaseNode(label="Woman", properties={'name': 'alice', 'age': 40})])

        will1, will2 = self.manager1.set_nodes([GraphDatabaseNode(label="Man", properties={'name': 'will', 'age': 30}),
                                                GraphDatabaseNode(label="Man", properties={'name': 'will', 'age': 40})])

        bobs = self.manager1.get_nodes_by_properties(properties={'name': 'bob'})
        self.assertSetEqual(set([bob.get_id() for bob in bobs]), {bob1.get_id(), bob2.get_id()})

        alices = self.manager1.get_nodes_by_properties(properties={'name': 'alice'})
        self.assertSetEqual(set([alice.get_id() for alice in alices]), {alice1.get_id(), alice2.get_id()})

        wills = self.manager1.get_nodes_by_properties(properties={'name': 'will'})
        self.assertSetEqual(set([will.get_id() for will in wills]), {will1.get_id(), will2.get_id()})

        men = self.manager1.get_nodes_by_properties(label='Man', properties={})
        self.assertSetEqual(set([man.get_id() for man in men]), {bob1.get_id(), bob2.get_id(), will1.get_id(), will2.get_id()})

        people_aged_30 = self.manager1.get_nodes_by_properties(properties={'age': 30})
        self.assertSetEqual(set([person.get_id() for person in people_aged_30]), {bob1.get_id(), alice1.get_id(), will1.get_id()})

        men_aged_30 = self.manager1.get_nodes_by_properties(properties={'age': 30}, label='Man')
        self.assertSetEqual(set([man.get_id() for man in men_aged_30]), {bob1.get_id(), will1.get_id()})

        all = self.manager1.get_nodes_by_properties(properties={})
        self.assertSetEqual(set([node.get_id() for node in all]), {bob1.get_id(), bob2.get_id(), alice1.get_id(), alice2.get_id(), will1.get_id(), will2.get_id()})

    def test_set_new_edge(self):
        edge_label = "Knows"
        edge_properties = {"relation": "friend"}

        new_node1 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Bob'})])[0]
        node1_id = new_node1.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node1_id]))

        new_node2 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Will'})])[0]
        node2_id = new_node2.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node2_id]))

        new_edge = self.manager1.set_edges([GraphDatabaseEdge(edge_label=edge_label, from_node=node1_id, to_node=node2_id, properties=edge_properties)])[0]
        edge_id = new_edge.get_id()

        edge = self.manager1.get_edges_by_ids([edge_id])[0]
        self.assertIsNotNone(edge)
        self.assertEqual(edge.get_id(), edge_id)
        self.assertEqual(edge.get_label(), edge_label)
        self.assertEqual(edge.get_from_node(), node1_id)
        self.assertEqual(edge.get_to_node(), node2_id)
        self.assertEqual(edge.get_properties(), {**edge_properties, **self.manager1.get_subgraph_edge_properties()})

    def test_replace_edge(self):
        edge_label = "Knows"
        edge_properties = {"relation": "friend"}

        new_node1 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Bob'})])[0]
        node1_id = new_node1.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node1_id]))

        new_node2 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Will'})])[0]
        node2_id = new_node2.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node2_id]))

        existing_edge = self.manager1.set_edges([GraphDatabaseEdge(edge_label=edge_label, from_node=node1_id, to_node=node2_id, properties=edge_properties)])[0]
        edge_id = existing_edge.get_id()

        edge = self.manager1.get_edges_by_ids([edge_id])[0]
        self.assertIsNotNone(edge)
        self.assertEqual(edge.get_id(), edge_id)
        self.assertEqual(edge.get_label(), edge_label)
        self.assertEqual(edge.get_from_node(), node1_id)
        self.assertEqual(edge.get_to_node(), node2_id)
        self.assertEqual(edge.get_properties(), {**edge_properties, **self.manager1.get_subgraph_edge_properties()})

        new_edge_label = "Knows"
        new_edge_properties = {"relation": "enemy"}
        with self.assertRaises(gremlin_python.driver.protocol.GremlinServerError):
            self.manager1.set_edges([GraphDatabaseEdge(edge_id=edge_id, edge_label=new_edge_label, from_node=node1_id, to_node=node2_id, properties=new_edge_properties)])

        self.manager1.delete_edges_if_exist([edge_id])
        self.manager1.set_edges([GraphDatabaseEdge(edge_id=edge_id, edge_label=new_edge_label, from_node=node1_id, to_node=node2_id, properties=new_edge_properties)])

        edge = self.manager1.get_edges_by_ids([edge_id])[0]
        self.assertEqual(edge.get_id(), edge_id)
        self.assertEqual(edge.get_label(), new_edge_label)
        self.assertEqual(edge.get_from_node(), node1_id)
        self.assertEqual(edge.get_to_node(), node2_id)
        self.assertEqual(edge.get_properties(), {**new_edge_properties, **self.manager1.get_subgraph_edge_properties()})

    def test_update_edge_properties(self):
        edge_label = "Knows"
        edge_properties = {"relation": "friend"}

        new_node1 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Bob'})])[0]
        node1_id = new_node1.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node1_id]))

        new_node2 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Will'})])[0]
        node2_id = new_node2.get_id()
        self.assertIsNotNone(self.manager1.get_nodes_by_ids([node2_id]))

        existing_edge = self.manager1.set_edges([GraphDatabaseEdge(edge_label=edge_label, from_node=node1_id, to_node=node2_id, properties=edge_properties)])[0]
        edge_id = existing_edge.get_id()

        edge = self.manager1.get_edges_by_ids([edge_id])[0]
        self.assertIsNotNone(edge)
        self.assertEqual(edge.get_id(), edge_id)
        self.assertEqual(edge.get_label(), edge_label)
        self.assertEqual(edge.get_from_node(), node1_id)
        self.assertEqual(edge.get_to_node(), node2_id)
        self.assertEqual(edge.get_properties(), {**edge_properties, **self.manager1.get_subgraph_edge_properties()})

        new_edge_properties = {"relation": "enemy"}
        self.manager1.load_properties_to_edges({edge_id: new_edge_properties})

        edge = self.manager1.get_edges_by_ids([edge_id])[0]
        self.assertIsNotNone(edge)
        self.assertEqual(edge.get_id(), edge_id)
        self.assertEqual(edge.get_label(), edge_label)
        self.assertEqual(edge.get_from_node(), node1_id)
        self.assertEqual(edge.get_to_node(), node2_id)
        self.assertEqual(edge.get_properties(), {**new_edge_properties, **self.manager1.get_subgraph_edge_properties()})

    def test_get_edges_by_properties(self):
        node1, node2 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={'name': 'Bob'}),
                                                GraphDatabaseNode(label='Label', properties={'name': 'Will'})])
        node1_id = node1.get_id()
        node2_id = node2.get_id()

        friend_1, friend_2 = self.manager1.set_edges([GraphDatabaseEdge(edge_label='Knows', from_node=node1_id, to_node=node2_id, properties={'relation': 'friend', 'closeness': 'close'}),
                                                      GraphDatabaseEdge(edge_label='Knows', from_node=node1_id, to_node=node2_id, properties={'relation': 'friend', 'closeness': 'not close'})])

        enemy_1, enemy_2 = self.manager1.set_edges([GraphDatabaseEdge(edge_label='Knows', from_node=node1_id, to_node=node2_id, properties={'relation': 'enemy', 'closeness': 'close'}),
                                                    GraphDatabaseEdge(edge_label='Knows', from_node=node1_id, to_node=node2_id, properties={'relation': 'enemy', 'closeness': 'not close'})])

        # co_workers_1 = self.manager1.set_edge(edge_label='Co-Workers', from_node=node1_id, to_node=node2_id, properties={'relation': 'co-worker', 'closeness': 'close'})
        # co_workers_2 = self.manager1.set_edge(edge_label='Co-Workers', from_node=node1_id, to_node=node2_id, properties={'relation': 'co-worker', 'closeness': 'not close'})
        co_workers_1, co_workers_2 = self.manager1.set_edges([GraphDatabaseEdge(edge_label='Co-Workers', from_node=node1_id, to_node=node2_id, properties={'relation': 'co-worker', 'closeness': 'close'}),
                                                              GraphDatabaseEdge(edge_label='Co-Workers', from_node=node1_id, to_node=node2_id, properties={'relation': 'co-worker', 'closeness': 'not close'})])

        friends = self.manager1.get_edges_by_properties(properties={'relation': 'friend'})
        self.assertSetEqual(set([friend.get_id() for friend in friends]), {friend_1.get_id(), friend_2.get_id()})

        enemies = self.manager1.get_edges_by_properties(properties={'relation': 'enemy'})
        self.assertSetEqual(set([enemy.get_id() for enemy in enemies]), {enemy_1.get_id(), enemy_2.get_id()})

        co_workers = self.manager1.get_edges_by_properties(properties={'relation': 'co-worker'})
        self.assertSetEqual(set([co_worker.get_id() for co_worker in co_workers]), {co_workers_1.get_id(), co_workers_2.get_id()})

        close = self.manager1.get_edges_by_properties(properties={'closeness': 'close'})
        self.assertSetEqual(set([close_edge.get_id() for close_edge in close]), {friend_1.get_id(), enemy_1.get_id(), co_workers_1.get_id()})

        not_close = self.manager1.get_edges_by_properties(properties={'closeness': 'not close'})
        self.assertSetEqual(set([not_close_edge.get_id() for not_close_edge in not_close]), {friend_2.get_id(), enemy_2.get_id(), co_workers_2.get_id()})

        knows = self.manager1.get_edges_by_properties(label='Knows', properties={})
        self.assertSetEqual(set([know.get_id() for know in knows]), {friend_1.get_id(), friend_2.get_id(), enemy_1.get_id(), enemy_2.get_id()})

        knows_close = self.manager1.get_edges_by_properties(label='Knows', properties={'closeness': 'close'})
        self.assertSetEqual(set([know.get_id() for know in knows_close]), {friend_1.get_id(), enemy_1.get_id()})

        all = self.manager1.get_edges_by_properties(properties={})
        self.assertSetEqual(set([edge.get_id() for edge in all]), {friend_1.get_id(), friend_2.get_id(), enemy_1.get_id(), enemy_2.get_id(), co_workers_1.get_id(), co_workers_2.get_id()})

    def test_get_edges_by_nodes_connection(self):
        node1, node2, node3 = self.manager1.set_nodes([GraphDatabaseNode(label='Label', properties={}),
                                                         GraphDatabaseNode(label='Label', properties={}),
                                                         GraphDatabaseNode(label='Label', properties={})])
        node1_id = node1.get_id()
        node2_id = node2.get_id()
        node3_id = node3.get_id()

        connection_1, connection_2, connection_3 = self.manager1.set_edges([GraphDatabaseEdge(edge_label='Connection', from_node=node1_id, to_node=node2_id, properties={}),
                                                                            GraphDatabaseEdge(edge_label='Connection', from_node=node1_id, to_node=node3_id, properties={}),
                                                                            GraphDatabaseEdge(edge_label='Connection', from_node=node2_id, to_node=node3_id, properties={})])

        node1_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node1_id)
        self.assertSetEqual(set([connection.get_id() for connection in node1_connections]), {connection_1.get_id(), connection_2.get_id()})

        node2_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node2_id)
        self.assertSetEqual(set([connection.get_id() for connection in node2_connections]), {connection_3.get_id()})

        node3_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node3_id)
        self.assertSetEqual(set([connection.get_id() for connection in node3_connections]), set())

        node1_to_node2_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node1_id, to_node=node2_id)
        self.assertSetEqual(set([connection.get_id() for connection in node1_to_node2_connections]), {connection_1.get_id()})

        node1_to_node3_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node1_id, to_node=node3_id)
        self.assertSetEqual(set([connection.get_id() for connection in node1_to_node3_connections]), {connection_2.get_id()})

        node2_to_node3_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node2_id, to_node=node3_id)
        self.assertSetEqual(set([connection.get_id() for connection in node2_to_node3_connections]), {connection_3.get_id()})

        node2_to_node1_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node2_id, to_node=node1_id)
        self.assertSetEqual(set([connection.get_id() for connection in node2_to_node1_connections]), set())

        node3_to_node1_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node3_id, to_node=node1_id)
        self.assertSetEqual(set([connection.get_id() for connection in node3_to_node1_connections]), set())

        node3_to_node2_connections = self.manager1.get_edges_by_properties(properties={}, from_node=node3_id, to_node=node2_id)
        self.assertSetEqual(set([connection.get_id() for connection in node3_to_node2_connections]), set())

        connected_to_node2 = self.manager1.get_edges_by_properties(properties={}, to_node=node2_id)
        self.assertSetEqual(set([connection.get_id() for connection in connected_to_node2]), {connection_1.get_id()})

        connected_to_node3 = self.manager1.get_edges_by_properties(properties={}, to_node=node3_id)
        self.assertSetEqual(set([connection.get_id() for connection in connected_to_node3]), {connection_2.get_id(), connection_3.get_id()})

        connected_to_node1 = self.manager1.get_edges_by_properties(properties={}, to_node=node1_id)
        self.assertSetEqual(set([connection.get_id() for connection in connected_to_node1]), set())
