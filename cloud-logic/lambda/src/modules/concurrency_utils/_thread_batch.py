from concurrent.futures import ThreadPoolExecutor


def run_thread_batch(func: callable, batch_inputs: list):
    if __debug__:
        return [func(batch_input) for batch_input in batch_inputs]
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(func, batch_inputs))
    return results
