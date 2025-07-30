import contextlib
import os
from shutil import rmtree
from subprocess import run

import numpy as np

import aidge_core
import aidge_backend_cpu
import aidge_export_cpp

def measure_inference_time(model: aidge_core.GraphView, input_data: list[str, np.ndarray], nb_warmup: int = 10, nb_iterations: int = 50) -> list[float]:
    # load and set up the model
    # model.set_datatype(ai.dtype.float32)
    model.set_backend("cpu")

    # create input Tensor list for the GraphView
    ordered_inputs: list[aidge_core.Tensor] = []
    # [tmp fix] manual transpositin of data for input of export BEFORE converting to Tensor
    for i in input_data:
        nb_dims = len(i[1].shape)
        if nb_dims == 3:
            ordered_inputs.append(aidge_core.Tensor(i[1].transpose(0,2,1).reshape(i[1].shape).copy()))
        if nb_dims == 4:
            ordered_inputs.append(aidge_core.Tensor(np.transpose(i[1], axes=(0,2,3,1)).reshape(i[1].shape).copy()))
        else:
            ordered_inputs.append(aidge_core.Tensor(i[1]))

    # set inputs for the export
    for i, inp in enumerate(model.get_ordered_inputs()):
        op = inp[0].get_operator()
        op.set_input(i, ordered_inputs[i])

    model.forward_dims([t.dims() for t in ordered_inputs])

    scheduler = aidge_core.SequentialScheduler(model)
    scheduler.generate_scheduling()

    # for ordered_input in ordered_inputs:
        # ordered_input.set_backend("cpu")
    operator_type: str = model.get_ordered_outputs()[0][0].get_operator().type()
    print("  ├─Generating export...", end="", flush=True)
    folder_name: str = f"{operator_type.lower()}_test_export_cpp"
    with open('/dev/null', 'w') as f, contextlib.redirect_stdout(f):
        aidge_core.export_utils.scheduler_export(
            scheduler,
            folder_name,
            aidge_export_cpp.ExportLibCpp,
            memory_manager=aidge_core.mem_info.generate_optimized_memory_info,
            memory_manager_args={"wrapping": False }
        )
        aidge_core.export_utils.generate_main_inference_time_cpp(folder_name, model, nb_iterations, nb_warmup)
    print(" ok")

    print("  ├─Compiling...", end="", flush=True)
    with open('/dev/null', 'w') as f, contextlib.redirect_stdout(f):
        run(['make'], cwd=folder_name, stdout=f)
    print(" ok")
    timings_str = run(f'./{folder_name}/bin/run_export', capture_output=True, text=True)

    folder_path = os.path.abspath(folder_name)
    if os.path.exists(folder_path):
        rmtree(folder_path, ignore_errors=True)

    timings = [float(t) for t in timings_str.stdout.split(' ') if t.strip()]
    return timings

def compute_output(model: aidge_core.GraphView, input_data: list[str, np.ndarray]) -> list[np.ndarray]:
    # load and set up the model
    model.set_backend("cpu")

    # create input Tensor list for the GraphView
    ordered_inputs: list[aidge_core.Tensor] = []
    # [tmp fix] manual transpositin of data for input of export BEFORE converting to Tensor
    for i in input_data:
        nb_dims = len(i[1].shape)
        if nb_dims == 3:
            ordered_inputs.append(aidge_core.Tensor(i[1].transpose(0,2,1).reshape(i[1].shape).copy()))
        if nb_dims == 4:
            ordered_inputs.append(aidge_core.Tensor(np.transpose(i[1], axes=(0,2,3,1)).reshape(i[1].shape).copy()))
        else:
            ordered_inputs.append(aidge_core.Tensor(i[1]))

    # set inputs for the export
    for i, inp in enumerate(model.get_ordered_inputs()):
        op = inp[0].get_operator()
        op.set_input(i, ordered_inputs[i])

    model.forward_dims([t.dims() for t in ordered_inputs])

    scheduler = aidge_core.SequentialScheduler(model)
    scheduler.generate_scheduling()


    operator_type: str = model.get_ordered_outputs()[0][0].get_operator().type()
    print("  │ Generating export...", end="", flush=True)
    folder_name: str = f"{operator_type.lower()}_test_export_cpp"
    with open('/dev/null', 'w') as f, contextlib.redirect_stdout(f):
        aidge_core.export_utils.scheduler_export(
            scheduler,
            folder_name,
            aidge_export_cpp.ExportLibCpp,
            memory_manager=aidge_core.mem_info.generate_optimized_memory_info,
            memory_manager_args={"wrapping": False }
        )
        aidge_core.export_utils.generate_main_display_output_cpp(folder_name, model)
    print(" ok")

    print("  │ Compiling...", end="", flush=True)
    with open('/dev/null', 'w') as f, contextlib.redirect_stdout(f):
        run(['make'], cwd=folder_name, stdout=f)
    print(" ok")
    output_str: str = run(f'./{folder_name}/bin/run_export', capture_output=True, text=True)
    folder_path = os.path.abspath(folder_name)
    if os.path.exists(folder_path):
        rmtree(folder_path, ignore_errors=True)

    outputs_str: list[str] = output_str.stdout.strip().split('\n')
    outputs = [np.array([float(val) for val in single_output_str.split(' ') if val.strip()]) for i, single_output_str in enumerate(outputs_str)]

    for i, pair in enumerate(model.get_ordered_outputs()):
        dims = pair[0].get_operator().get_output(pair[1]).dims()
        nb_dims = len(dims)
        dims_permutted = dims
        if nb_dims == 3:
            dims_permutted = [dims[0], dims[2], dims[1]]
        if nb_dims == 4:
            dims_permutted = [dims[0], dims[2], dims[3], dims[1]]

        if np.prod(dims) != outputs[i].size:
            aidge_core.Log.fatal("Incompatible export output size ({}) with required shape {}", outputs[i].size, dims)
        outputs[i] = outputs[i].reshape(dims_permutted)
        if nb_dims == 3:
            outputs[i] = outputs[i].transpose(0,2,1)
        if nb_dims == 4:
            outputs[i] = outputs[i].transpose(0,3,1,2)

    return outputs
