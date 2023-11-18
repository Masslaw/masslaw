from concurrent.futures import ProcessPoolExecutor


def run_process_batch(func: callable, batch_inputs: list):
    if __debug__:
        return [func(batch_input) for batch_input in batch_inputs]
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(func, batch_inputs))
    return results
