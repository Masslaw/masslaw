import unittest

from shared_layer.concurrency_utils import run_thread_batch


def global_function(some_input):
    return some_input + 10


class TestFunctionRunThreadBatch(unittest.TestCase):
    _member_variable = 3

    def test_thread_batch_on_local_function(self):
        def local_function(some_input):
            return some_input + 1

        results = run_thread_batch(local_function, [1, 2, 3])
        self.assertEqual(results, [2, 3, 4])

    def test_thread_batch_on_global_function(self):
        results = run_thread_batch(global_function, [1, 2, 3])
        self.assertEqual(results, [11, 12, 13])

    def test_thread_batch_on_member_function(self):
        results = run_thread_batch(self.__member_function, [1, 2, 3])
        self.assertEqual(results, [4, 5, 6])

    def test_thread_batch_on_static_function(self):
        results = run_thread_batch(self.static_function, [1, 2, 3])
        self.assertEqual(results, [6, 7, 8])

    def __member_function(self, some_input):
        return some_input + self._member_variable

    @staticmethod
    def static_function(some_input):
        return some_input + 5
