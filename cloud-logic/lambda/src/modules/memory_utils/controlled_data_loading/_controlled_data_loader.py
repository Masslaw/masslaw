from abc import abstractmethod


class MemoryControlledDataLoader:
    @abstractmethod
    def load_data(self, load_input: any) -> any:
        pass
