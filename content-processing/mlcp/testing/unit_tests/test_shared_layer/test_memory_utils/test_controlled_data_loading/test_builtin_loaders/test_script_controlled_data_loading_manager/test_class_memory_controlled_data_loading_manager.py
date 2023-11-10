import unittest
from unittest.mock import Mock
from unittest.mock import patch

from shared_layer.memory_utils.controlled_data_loading import MemoryControlledDataLoadingManager
from shared_layer.memory_utils.controlled_data_loading._controlled_data_loader import MemoryControlledDataLoader


# for the sake of clarity and testability, in this test, the memory consumption of the loaded data is
# the sum of the data items
@patch('sys.getsizeof', side_effect=lambda data: sum(data))
class TestClassMemoryControlledDataLoadingManager(unittest.TestCase):
    def setUp(self):
        self.mock_loader = Mock(spec=MemoryControlledDataLoader)

        def mock_data_loading_function(data):
            return data + 10

        self.mock_loader.load_data = mock_data_loading_function

    def test_load_and_process_data_chunks_grouped(self, mock_getsizeof):
        loaded_chunks = []

        def mock_chunk_process_function(chunk):
            loaded_chunks.append(chunk)

        load_inputs = [10, 20, 30]  # loaded it will be [20, 30, 40]
        max_memory_usage = 50

        loading_manager = MemoryControlledDataLoadingManager(self.mock_loader, mock_chunk_process_function, max_memory_usage=max_memory_usage)

        loading_manager.load_and_process_data_chunks(load_inputs)

        self.assertEqual(loaded_chunks, [[20, 30], [40]])

    def test_load_and_process_data_chunks_whole(self, mock_getsizeof):
        loaded_chunks = []

        def mock_chunk_process_function(chunk):
            loaded_chunks.append(chunk)

        load_inputs = [10, 20, 30]  # loaded it will be [20, 30, 40]
        max_memory_usage = 100

        loading_manager = MemoryControlledDataLoadingManager(self.mock_loader, mock_chunk_process_function, max_memory_usage=max_memory_usage)

        loading_manager.load_and_process_data_chunks(load_inputs)

        self.assertEqual(loaded_chunks, [[20, 30, 40]])

    def test_load_and_process_data_chunks_split(self, mock_getsizeof):
        loaded_chunks = []

        def mock_chunk_process_function(chunk):
            loaded_chunks.append(chunk)

        load_inputs = [10, 20, 30]  # loaded it will be [20, 30, 40]
        max_memory_usage = 20

        loading_manager = MemoryControlledDataLoadingManager(self.mock_loader, mock_chunk_process_function, max_memory_usage=max_memory_usage)

        loading_manager.load_and_process_data_chunks(load_inputs)

        self.assertEqual(loaded_chunks, [[20], [30], [40]])
