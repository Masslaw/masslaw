import sys

from shared_layer.memory_utils.controlled_data_loading._controlled_data_loader import MemoryControlledDataLoader


class MemoryControlledDataLoadingManager:
    def __init__(self, loader: MemoryControlledDataLoader, chunk_processing_function: callable, max_memory_usage: int = (8 * 1024)):
        self._loader = loader
        self._max_memory_usage = max_memory_usage
        self._chunk_processing_function = chunk_processing_function

    def load_and_process_data_chunks(self, load_inputs: list[any]) -> any:
        loaded_data_items = []
        for load_input in load_inputs:
            loaded_data_item = self._loader.load_data(load_input)
            loaded_data_items.append(loaded_data_item)
            loaded_data_memory_usage = sys.getsizeof(loaded_data_items)
            if loaded_data_memory_usage >= self._max_memory_usage:
                self._chunk_processing_function(loaded_data_items)
                del loaded_data_items
                loaded_data_items = []
        if len(loaded_data_items) > 0:
            self._chunk_processing_function(loaded_data_items)
            del loaded_data_items
