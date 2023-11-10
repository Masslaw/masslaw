def process_started_log_string(process_name: str):
    template = "<bold><cyan>┍━ {process_name}</cyan></bold>"
    return template.format(process_name=process_name)


def process_finished_log_string(success: bool, time_taken: float, max_memory_usage: str = None):
    template = "<cyan>┕━</cyan>{success} <cyan>took: <underline>{time_taken}</underline> <cyan>seconds</cyan> <cyan>{memory_usage}</cyan>"
    return template.format(success=('' if success else ' <mark><red>[ABORTED]</red></mark>'), time_taken=time_taken, memory_usage=(max_memory_usage and f'MMU: <underline>{max_memory_usage}</underline>' or ''))


def log_line_with_process_stack_prefix(process_stack_size: int, msg: str):
    process_stack_prefix = '<cyan>' + ('│ ' * process_stack_size)+ '</cyan>'
    return process_stack_prefix + msg


LOG_MESSAGE_FORMATTING_TEMPLATE = '%(asctime)-20s <italic>%(levelname)-10s</italic> :::: %(message)s'
LOG_DATETIME_FORMATTING_TEMPLATE = '%m-%d-%Y %H:%M:%S'
