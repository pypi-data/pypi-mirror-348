import time

import numpy as np

import aidge_core
import aidge_backend_cuda

def measure_inference_time(model: aidge_core.GraphView, input_data: list[str, np.ndarray], nb_warmup: int = 10, nb_iterations: int = 50) -> list[float]:
    # update model and inputs backend
    model.set_backend("cuda")
    ordered_inputs = [aidge_core.Tensor(i[1]) for i in input_data]
    for ordered_input in ordered_inputs:
        ordered_input.set_backend("cuda")

    scheduler = aidge_core.SequentialScheduler(model)
    scheduler.generate_scheduling()

    timings = []
    # Warm-up runs.
    for i in range(nb_warmup + nb_iterations):
        if i < nb_warmup:
            scheduler.forward(forward_dims=False, data=ordered_inputs)
        else:
            start = time.process_time()
            scheduler.forward(forward_dims=False, data=ordered_inputs)
            end = time.process_time()
            timings.append((end - start))
    return timings

def compute_output(model: aidge_core.GraphView, input_data: list[str, np.ndarray]) -> list[np.ndarray]:
    # update model and inputs backend
    model.set_backend("cuda", device = 1)
    ordered_inputs = [aidge_core.Tensor(i[1]) for i in input_data]
    for ordered_input in ordered_inputs:
        ordered_input.set_backend("cuda", device = 1)

    scheduler = aidge_core.SequentialScheduler(model)
    scheduler.generate_scheduling()

    scheduler.forward(forward_dims=False, data=ordered_inputs)
    outs = []
    for pair in model.get_ordered_outputs():
        t = pair[0].get_operator().get_output(pair[1])
        t.set_backend("cpu")
        outs.append(t)

    return [np.array(out) for out in outs]