from datetime import time


class LogProcess:
    name: str
    time_start: time
    log_level: int
    memory_recorder = None
