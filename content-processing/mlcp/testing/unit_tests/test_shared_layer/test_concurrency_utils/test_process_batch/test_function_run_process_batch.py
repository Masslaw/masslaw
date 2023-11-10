import unittest

from shared_layer.concurrency_utils import run_process_batch


def global_function(some_input):
    return some_input + 10


class TestFunctionRunProcessBatch(unittest.TestCase):

    def test_process_batch_on_global_function(self):
        results = run_process_batch(global_function, [1, 2, 3])
        self.assertEqual(results, [11, 12, 13])

    def test_process_batch_on_static_function(self):
        results = run_process_batch(self.static_function, [1, 2, 3])
        self.assertEqual(results, [6, 7, 8])

    @staticmethod
    def static_function(some_input):
        return some_input + 5
