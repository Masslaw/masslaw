import logging
import threading
import time
from os import getpid

import psutil

pid = getpid()

logger = logging.getLogger()


class MemoryUsageRecorder:
    def __init__(self, record_history=False, recording_tick=1):
        self.__record = False

        self._record_history = record_history
        self._recording_tick = recording_tick

        self._memory_max = None
        self._memory_min = None
        self._memory_history = []

        self._recorder_thread = threading.Thread(target=self.__record_memory_usage)
        self._recorder_thread.start()

    def reset(self):
        self._memory_max = None
        self._memory_min = None
        self._memory_history = []

    def start(self):
        self.__record = True

    def stop(self):
        self.__record = False

    def get_recorded_memory_history(self):
        return self._memory_history

    def get_recorded_maximum_memory(self):
        return self._memory_max

    def get_recorded_minimum_memory(self):
        return self._memory_min

    def set_recording_tick(self, tick):
        self._recording_tick = tick

    def set_history_recording(self, record_history):
        self._record_history = record_history

    def __record_memory_usage(self):
        process = psutil.Process(pid)
        while True:
            if self.__record:
                memory_usage = process.memory_info().rss
                self._memory_max = max(self._memory_max, memory_usage) if self._memory_max is not None else memory_usage
                self._memory_min = min(self._memory_min, memory_usage) if self._memory_min is not None else memory_usage
                if self._record_history:
                    self._memory_history.append(memory_usage)
            time.sleep(self._recording_tick)
