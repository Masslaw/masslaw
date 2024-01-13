import os
import unittest
from datetime import datetime

from logic_layer.remote_graph_database.graph_visualization import GraphDatabaseVisualizer
from logic_layer.remote_graph_database.neptune_manager import NeptuneDatabaseManager
from mlcp.testing.content.content_management import content_management
from mlcp.testing.mlcp_job_tests._mlcp_job_test import MLCPJobTest
from mlcp.testing.stubs.neptune_stub import NeptuneStubTestLoader
from mlcp.testing.stubs.s3_stub import S3StubTestLoader
from shared_layer.file_system_utils._file_system_utils import clear_directory
from shared_layer.file_system_utils._file_system_utils import join_paths

file_name = "A-Very-Short-Story.txt"

bucket_name = "mlcp-test-bucket"

languages = ["eng", "heb"]

case_id = 'aH7CFNTa9stf7n8anF78anADV324gnoF'

file_id = file_name

parent_output_directory = './output/knowledge_extraction_job'

reset_database = False


class MLCPKnowledgeExtractionJobTest(unittest.TestCase, MLCPJobTest):

    @classmethod
    def setUpClass(cls):
        cls.test_output_directory = join_paths(parent_output_directory, file_name)
        clear_directory(cls.test_output_directory)
        test_time = datetime.now()
        cls.s3_stub = S3StubTestLoader()
        cls.neptune_stub = NeptuneStubTestLoader()
        with open(join_paths(cls.test_output_directory, f'{test_time}'), 'w') as file: file.write('')

    def setUp(self):
        self._open_temporary_storage()
        self.s3_stub.start_s3_stub()
        self.s3_stub.create_client()
        self.s3_stub.create_bucket(bucket_name)
        self.neptune_stub.start_gremlin_server()
        self._upload_mock_file()
        self._load_mlcp_process_configuration()
        self._set_stage("test")

    def tearDown(self):
        self.s3_stub.stop_s3_stub()
        self.neptune_stub.stop_gremlin_server()
        self._close_temporary_storage()

    def _upload_mock_file(self):
        self.test_file = content_management.get_file_path("processable_files", file_name)
        self.s3_stub.upload_file(bucket_name, self.test_file, file_name)

    def _load_mlcp_process_configuration(self):
        self._set_mlcp_process_configuration({
            'actions': [{
                "name": "s3_download",
                "params": {
                    "bucket": bucket_name,
                    "files_data": [{
                        "key": file_name,
                        "save_as": self.in_temporary_storage(file_name)
                    }]
                },
                "required": "True"
            }, {
                "name": "extract_knowledge",
                "params": {
                    "files_data": [{
                        "file_name": self.in_temporary_storage(file_name),
                        "languages": languages,
                        "case_id": case_id,
                        "file_id": file_id,
                        "neptune_endpoints": {
                            "read": {
                                "endpoint": "localhost",
                                "protocol": "ws",
                                "port": "8182",
                                "type": "gremlin"
                            },
                            "write": {
                                "endpoint": "localhost",
                                "protocol": "ws",
                                "port": "8182",
                                "type": "gremlin"
                            }
                        },
                        "knowledge_record_data": {
                            "node_properties": {
                                "files": {
                                    "list": [file_id]
                                },
                            },
                            "edge_properties": {
                                "files": {
                                    "list": [file_id]
                                },
                            },
                            "subgraph_node_properties": {
                                "case_id": case_id + file_name
                            },
                            "subgraph_edge_properties": {
                                "case_id": case_id + file_name
                            },
                        }
                    }]
                },
                "required": "True"
            },
            ]
        })

    def _after_application_finished(self):
        db_manager = NeptuneDatabaseManager(neptune_write_connection_data={
            'endpoint': 'localhost',
            'port': '8182',
            'type': 'gremlin'
        }, neptune_read_connection_data={
            'endpoint': 'localhost',
            'port': '8182',
            'type': 'gremlin'
        }, )

        visualizer = GraphDatabaseVisualizer(db_manager)
        visualizer.visualize_database_content_using_mermaid(os.path.join(self.test_output_directory, "graph.mermaid"))
        visualizer.visualize_database_content_using_matplotlib(os.path.join(self.test_output_directory, "graph.png"))

        all_nodes = db_manager.get_nodes_by_properties({})
        all_edges = db_manager.get_edges_by_properties({})
        print(f"Number of nodes: {len(all_nodes)}")
        print(f"Number of edges: {len(all_edges)}")

        if reset_database:
            db_manager.delete_nodes_if_exist([node.get_id() for node in all_nodes])
            db_manager.delete_edges_if_exist([edge.get_id() for edge in all_edges])
