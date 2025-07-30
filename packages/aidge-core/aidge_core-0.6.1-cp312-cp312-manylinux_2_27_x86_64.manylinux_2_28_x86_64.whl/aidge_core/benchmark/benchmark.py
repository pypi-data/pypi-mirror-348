"""
Operator Kernel Performance Benchmarking Script

This script benchmarks operator kernels using a specified inference module.
It supports timing measurements and (optionally) output comparisons with ONNXRuntime.
The configuration is provided via a JSON file.
"""

import argparse
import copy
from importlib import import_module
import json
import os
import sys
from typing import Any

import numpy as np
import onnx

import aidge_core as ai
import aidge_onnx
from aidge_onnx.generate_singleop_onnx import create_onnx_model
from . import tree_structure
from . import logger
from . import manage_config

COLOR_ON = True

def load_inference_module(module_name: str):
    """
    Dynamically imports and returns the inference module.
    Exits if the module is not installed.
    """
    try:
        return import_module(module_name)
    except ImportError:
        return None

def update_test_config(
    param: str,
    value,
    base_attributes: dict,
    base_input_shapes: list,
    other_parameters: dict,
    operator_attributes: list,
):
    """
    Updates the operator attributes and input shapes based on the test parameter.

    Returns:
        tuple: (updated_attributes, updated_input_shapes) or (None, None) if keys are missing.
    """
    attributes = copy.deepcopy(base_attributes)
    input_shapes = copy.deepcopy(base_input_shapes)

    # Update if the parameter is a valid operator attribute
    if param in operator_attributes:
        attributes[param] = value

    try:
        extra_attrs = other_parameters[param][str(value)]["attributes"]
    except KeyError:
        ai.Log.error(
            f"Test configuration {{'{param}': '{value}'}} no 'attribute' property found. Config file may be ill-formed."
        )
        return None, None
    attributes.update(extra_attrs)

    try:
        extra_input_shapes = other_parameters[param][str(value)]["input_shapes"]
    except KeyError:
        ai.Log.error(
            f"Test configuration {{'{param}': '{value}'}} no 'input_shapes' property found. Config file may be ill-formed."
        )
        return None, None

    for shape_update in extra_input_shapes:
        name, new_shape = shape_update
        for base_shape in input_shapes:
            if base_shape[0] == name:
                base_shape[1] = new_shape
                break

    return attributes, input_shapes


# def get_results_file_path(module_name: str, operator_aidge: str, save_directory: str) -> str:
#     """
#     Constructs and returns the file path for saving the benchmark results.
#     """
#     if module_name == "onnxruntime":
#         filename = f"{operator_aidge}_onnxruntime.json"
#     elif module_name == "pytorch":
#         filename = f"{operator_aidge}_pytorch.json"
#     else:
#         filename = f"{operator_aidge}.json"
#     return os.path.join(save_directory, filename)


def measure_inference_time(
    module_name: str, model: onnx.ModelProto, input_data, nb_warmups, nb_iterations, inference_module=None
) -> list[float]:
    """
    Measures inference time using the appropriate benchmark function.
    """
    if module_name == "onnxruntime":
        from . import benchmark_onnxruntime

        return benchmark_onnxruntime.measure_inference_time(
            model, {v[0]: v[1] for v in input_data}, nb_warmups, nb_iterations
        )
    elif module_name == "torch":
        from . import benchmark_torch

        return benchmark_torch.measure_inference_time(
            model, {v[0]: v[1] for v in input_data}, nb_warmups, nb_iterations
        )
    else:
        model = aidge_onnx.convert_onnx_to_aidge(model=model) if "aidge" in module_name else model
        return inference_module.benchmark.measure_inference_time(
            model, input_data, nb_warmups, nb_iterations
        )


def compute_output(
    module_name: str, model: onnx.ModelProto, input_data, inference_module
) -> list[np.ndarray]:
    """
    Measures inference time using the appropriate benchmark function.
    """
    if module_name == "onnxruntime":
        from . import benchmark_onnxruntime

        return benchmark_onnxruntime.compute_output(
            model, {v[0]: v[1] for v in input_data}
        )
    elif module_name == "torch":
        from . import benchmark_torch

        return benchmark_torch.compute_output(model, {v[0]: v[1] for v in input_data})
    else:
        if "aidge" in module_name:
            model = aidge_onnx.convert_onnx_to_aidge(model=model)
            # TODO: find a way to catch if an Operator is not implemented for a backend/exportLib
        return inference_module.benchmark.compute_output(model, input_data)


def prepare_input_data(
    input_shapes: list[str, list[int]], initializer_rank: int
) -> list[str, np.ndarray]:
    """
    Generates random input data for the first `initializer_rank` inputs.
    """
    data: list[str, np.ndarray] = []
    for i, conf in enumerate(input_shapes):
        name, shape = conf
        if i < initializer_rank:
            random_array = np.array(np.random.rand(*shape)).astype(np.float32)
            data.append((name, random_array))
    return data


def main():
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--show-available-config", action="store_true")
    known_args, _ = pre_parser.parse_known_args()

    # Handle --show-available-config early and exit
    if known_args.show_available_config:
        manage_config.show_available_config()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Operator Kernel Performance Benchmarking across multiple inference modules."
    )

    parser.add_argument(
        "--show-available-config",
        action="store_true",
        help="show JSON configuration files stored in the standard configuration directory."
    )
    onnx_model_group = parser.add_mutually_exclusive_group(required=True)
    onnx_model_group.add_argument(
        "--config-file",
        "-cf",
        type=str,
        help="Path to a JSON configuration file containing an ONNX operator description with reference and tested parameter values. A new ONNX model will automatically be generated for each test case. Cannot be specified with '--onnx-file' option",
    )
    onnx_model_group.add_argument(
        "--onnx-file",
        "-of",
        type=str,
        help="Path to an existing ONNX file that will be used for benchmarking. Cannot be specified with '--config-file' option.",
    )
    parser.add_argument(
        "--modules",
        "-m",
        type=str,
        nargs="+",
        required=True,
        help="List of inference module names to benchmark (e.g., 'torch', 'onnxruntime').",
    )
    parser.add_argument(
        "--time",
        "-t",
        action="store_true",
        help="Measure inference time for each module."
    )
    parser.add_argument(
        "--nb-iterations",
        type=int,
        default=50,
        help="Number of iterations to run for the 'time' test (default: 50)."
    )
    parser.add_argument(
        "--nb-warmups",
        type=int,
        default=10,
        help="Number of warmup steps to run for the 'time' test (default: 10)."
    )
    parser.add_argument(
        "--compare",
        "-c",
        action="store_true",
        help="Compare the inference outputs of each module against a reference implementation.",
    )
    parser.add_argument(
        "--ref",
        type=str,
        default="onnxruntime",
        help="Reference module used for comparing results (default: 'onnxruntime').",
    )
    parser.add_argument(
        "--results-directory",
        type=str,
        default="benchmark_results",
        help="Directory to save the benchmarking results",
    )
    parser.add_argument(
        "--results-filename",
        type=str,
        required=False,
        default="",
        help="Name of the saved result file. If not provided, it will default to the '<operator_name>_<module_to_bench>.json'. If a file with that nae and at tha location already exists, it will be overrided with elements individually replaced only if new ones are computed"
    )
    args = parser.parse_args()

    log = logger.Logger(COLOR_ON)

    COMPARE: bool = args.compare
    TIME: bool = args.time

    NB_WARMUPS: int = args.nb_warmups
    NB_ITERATIONS: int = args.nb_iterations

    tree = tree_structure.TreeStruct() # structure informations about the script execution

    modules: list[dict] = [{"name": m_name} for m_name in args.modules]
    NB_MODULES = len(args.modules)

    print("Loading modules...")
    ref_module_name: str = args.ref
    ref_module = None
    if COMPARE and (ref_module not in list(m["name"] for m in modules)):
        ref_module = load_inference_module(ref_module_name)
        print(f"{tree.grow(branch=False, leaf=False )}{ref_module_name} [ {log.to_color('ok', logger.Color.GREEN) if ref_module else log.to_color('xx', logger.Color.RED)} ]")

    # Load the inference module
    for m_id, m in enumerate(modules):
        print(f"{tree.grow(branch=False, leaf= (m_id >= NB_MODULES - 1))}{m["name"]} ", end='')
        m["module"] = load_inference_module(m["name"])
        if m["module"]:
            print(f"[ {log.to_color('ok', logger.Color.GREEN)} ]")
        else :
            print(f"[ {log.to_color('xx', logger.Color.RED)} ]")
            sys.exit(1)


    # Configure aidge logging
    ai.Log.set_console_level(ai.Level.Warn)
    ai.Log.set_precision(10)

    if args.onnx_file:
        ai.Log.fatal("ONNX single file not supported yet")
        sys.exit(1)

    # Load configuration
    config = manage_config.load_json(args.config_file)
    operator_name: str = config["operator"]
    opset_version: int = config["opset_version"]
    initializer_rank: int = config.get("initializer_rank", 1)

    test_meta_data: dict[str, Any] = config["test_meta_data"]
    if test_meta_data["multiple_batchs"] == True and "export" in list(m["name"] for m in modules):
        ai.Log.warn("The tested module seems to be an export module and your test cases contains "
            "\033[31;1;multiple\033[0m batchs inputs. This could lead to inaccurate results due to "
            "the stream-based (single batch) nature of exports implementations, or an error during "
            "export the 'export generation' step. Unless you know what you are doing, you should "
            "probably change your configuration file for single batch tests.")

    base_input_shapes: list[str, list[int]] = config["base_configuration"][
        "input_shapes"
    ]
    base_attributes: dict = config["base_configuration"].get("attributes", {})

    main_parameters: dict[str, Any] = config["test_configuration"].get(
        "main_parameters", {}
    )
    other_parameters: dict[str, dict] = config["test_configuration"].get(
        "other_parameters", {}
    )

    # Get operator attributes from the schema for filtering test parameters
    operator_schema = onnx.defs.get_schema(operator_name, opset_version)
    operator_attributes: list[str] = list(operator_schema.attributes)

    # Initialize or load existing benchmark results
    results_directory = os.path.expanduser(args.results_directory)
    if not os.path.isdir(results_directory):
        print("Creating result directory at: ", results_directory)
        os.makedirs(results_directory, exist_ok=True)
    base_result_filename: str = ((args.results_filename + '_') if args.results_filename else "") + (f"{operator_name.lower()}" if args.config_file else args.onnx_file) + '_'
    for m in modules:
        m["result_file_path"] = os.path.join(results_directory, base_result_filename + f'{m["name"]}.json')
        m["results"] = {"library": m["name"], "compare": {}, "time": {}}
        for param, test_values in main_parameters.items():
            m["results"]["time"][param] = {}
            m["results"]["compare"][param] = {}

    # we override existing file
    # if os.path.exists(results_file_path):
    #     with open(results_file_path, "r") as f:
    #         results = json.load(f)

    # Loop over each test parameter and its values
    tree.reset()
    print("\nStarting tests...")
    for param, test_values in main_parameters.items():
        for value in test_values:
            print(f"▷ {param} -- {value}")
            try:
                other_parameters[param][str(value)]
            except KeyError:
                ai.Log.error(
                    f"Test configuration {{'{param}': '{value}'}} not found. Config file may be ill-formed."
                )
                continue
            updated_attrs, updated_input_shapes = update_test_config(
                param,
                value,
                base_attributes,
                base_input_shapes,
                other_parameters,
                operator_attributes,
            )
            if updated_attrs is None or updated_input_shapes is None:
                continue  # Skip this test case if configuration is missing

            # Create the updated ONNX model
            model: onnx.ModelProto
            if args.config_file:
                model = create_onnx_model(
                    operator_name,
                    opset_version,
                    updated_input_shapes,
                    initializer_rank,
                    **updated_attrs,
                )
            elif args.onnx_file:
                model = aidge_onnx.load_onnx(args.onnx_file)
            else:
                ai.Log.fatal("No ONNX model to generate or load. Ending the script.")
                sys.exit(1)

            input_data = prepare_input_data(updated_input_shapes, initializer_rank)
            for m_id, m in enumerate(modules):
                print(f"{tree.grow(branch=True, leaf= (m_id >= NB_MODULES - 1))}{m["name"]}")
                if TIME:
                    print(f"{tree.grow(branch=False, leaf=not COMPARE)}time ", end='')
                    timing = measure_inference_time(m["name"], model, input_data, NB_WARMUPS, NB_ITERATIONS, m["module"])
                    m["results"]["time"][param][str(value)] = timing
                    time_str = f"[ {np.array(timing).mean():.2e} ± {np.array(timing).std():.2e} ] (seconds)"
                    print(time_str)

                if COMPARE:
                    print(f"{tree.grow(branch=False, leaf=True)}comp ", end='')
                    ref = compute_output(ref_module_name, model, input_data, ref_module)
                    tested = compute_output(m["name"], model, input_data, m["module"])
                    if len(ref) > 1:
                        print("Multi-output comparison not handled yet")
                        print([i.shape for i in ref])
                        sys.exit(1)
                    res = bool(np.all(np.isclose(ref, tested, rtol=1e-3, atol=1e-5)))
                    m["results"]["compare"][param][str(value)] = res
                    comp_str = f"[ {log.to_color('ok', logger.Color.GREEN) if res else log.to_color('xx', logger.Color.RED)} ]"
                    print(f"{comp_str}")
            print()

    # Save results
    tree.reset()
    print("Saving resutls to JSON files...")
    for m_id, m in enumerate(modules):
        with open(m["result_file_path"], "w") as outfile:
            print(f"{tree.grow(branch=False, leaf= (m_id >= NB_MODULES - 1))}'{m["result_file_path"]}'")
            json.dump(m['results'], outfile, indent=4)


if __name__ == "__main__":
    main()
