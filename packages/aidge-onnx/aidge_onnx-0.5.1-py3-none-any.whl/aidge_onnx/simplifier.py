import argparse
import onnx
import aidge_core
import aidge_backend_cpu

from typing import List, Dict
from collections import Counter
from rich.table import Table
from rich.console import Console

from .onnx_transformation import GRAPH_TRANSFORMATION
from .onnx_import import convert_onnx_to_aidge, has_native_coverage, native_coverage_report
from .onnx_export import export_onnx
from .onnx_test import check_onnx_validity


def _parse_shapes(shapes_arg: str) -> Dict[str, List[int]]:
    """Helper function to parse argument shape

    :param shapes_arg: Argument
    :type shapes_arg: str
    :return: _description_
    :rtype: Dict[str, List[List[int]]]
    """
    shapes = {}
    if shapes_arg is not None:
        for x in shapes_arg:
            if ':' not in x:
                shapes[None] = list(map(int, x.split(',')))
            else:
                pieces = x.split(':')
                # for the input name like input:0
                name, shape = ':'.join(
                    pieces[:-1]), list(map(int, pieces[-1].split(',')))
                if name in shapes:
                    shapes[name].append(shape)
                else:
                    shapes.update({name: [shape]})
    return shapes

def _forward_dims(graph_view: aidge_core.GraphView, input_shape: List[int])->bool:
    if not has_native_coverage(graph_view):
        native_coverage_report(graph_view)
        raise RuntimeError("Native coverage is not complete. Please check the coverage report above.")
    # TODO:
    # - Add support for dims with multi input
    if len(input_shape) !=1:
        raise ValueError("More than one shape given")

    graph_view.set_backend("cpu")
    graph_view.set_datatype(aidge_core.dtype.float32)

    if not graph_view.forward_dims(list(input_shape.values())[0], allow_data_dependency = False):
        aidge_core.Log.info("Could not forward dims.")

def _str_size(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def _compare_models(onnx_1, onnx_2):

    gv_1_cpt = Counter([n.op_type for n in onnx_1.graph.node])
    gv_2_cpt = Counter([n.op_type for n in onnx_2.graph.node])

    size_1 = onnx_1.ByteSize()
    size_2 = onnx_2.ByteSize()

    table = Table(show_header=True, header_style="bold")
    table.add_column("", style="bold")
    table.add_column("Original Model", justify="right")
    table.add_column("Simplified Model", justify="right")

    all_types = set(gv_1_cpt.keys()).union(gv_2_cpt.keys())
    for node_type in sorted(all_types):
        nb_nodes_1 = gv_1_cpt.get(node_type, 0)
        nb_nodes_2 = gv_2_cpt.get(node_type, 0)

        if nb_nodes_2 < nb_nodes_1:
            style = "green"
        elif nb_nodes_2 > nb_nodes_1:
            style = "red"
        else:
            style = "yellow"

        table.add_row(node_type, f"{nb_nodes_1}", f"[{style}]{nb_nodes_2}[/{style}]")

    if size_2 < size_1:
        style = "green"
    elif size_2 > size_1:
        style = "red"
    else:
        style = "yellow"

    table.add_row("Model Size",
                  _str_size(size_1),
                  f"[{style}]{_str_size(size_2)}[/{style}]")

    console = Console()
    console.print(table)

def _infer_input_shape(model: onnx.ModelProto) -> Dict[str, List[int]]:
    aidge_core.Log.notice("Inferring shape from ONNX graph")
    initializer_names = [x.name for x in model.graph.initializer]
    in_shape = {}
    graph_inputs = {
        ipt.name: [dim.dim_value for dim in ipt.type.tensor_type.shape.dim]
        for ipt in model.graph.input if ipt.name not in initializer_names
    }
    for node in model.graph.node:
        for tensor_name in node.input:
            if tensor_name in graph_inputs:
                dims = graph_inputs[tensor_name]
                if node.name not in in_shape:
                    in_shape[node.name] = []
                in_shape[node.name].append(dims)
    return in_shape

def show_available_simplification():
    print("Available graph transformations:")
    for key, value in GRAPH_TRANSFORMATION.items():
        if value[1] != "":
            print(f"\t-{key}: {value[1]}")
        else:
            print(f"\t-{key}")

def simplify_graph(graph_view: aidge_core.GraphView, input_shape: Dict[str, List[int]])->None:
    aidge_core.Log.notice("Simplifying ...")
    for key, value in GRAPH_TRANSFORMATION.items():
        aidge_core.Log.notice(f"Applying recipe: {key} ({value[1]})")
        value[0](graph_view)
        # Always forwardDims back as simplification may have removed tensor
        graph_view.forward_dims(list(input_shape.values())[0], allow_data_dependency = True)

def onnx_sim(model_path: str, output_path: str, input_shape:Dict[str, List[int]]):
    """
    Simplifies an ONNX model and saves the processed graph.

    :param model_path: Path to the input ONNX model file.
    :type model_path: str
    :param output_path: Path to save the simplified ONNX model.
    :type output_path: str
    :param input_shape: The expected input shape of the model.
    :type input_shape: List[int]
    """
    onnx_to_simplify = onnx.load(model_path)
    if input_shape == {}:
        input_shape = _infer_input_shape(onnx_to_simplify)
    aidge_core.Log.debug(f"Using the following input shape:\n")
    for key, value in input_shape.items():
        aidge_core.Log.debug(f"\t-{key}: {value}")

    graph_view = convert_onnx_to_aidge(onnx_to_simplify)
    # Transformation to have a valid Aidge graph
    aidge_core.remove_flatten(graph_view)

    _forward_dims(graph_view, input_shape)

    simplify_graph(graph_view, input_shape)

    aidge_core.Log.notice(f"Saving {output_path}")
    graph_view.save("model")
    print(graph_view.get_ordered_inputs())
    export_onnx(
        graph_view,
        output_path
    )
    if not check_onnx_validity(output_path):
        raise RuntimeError("The generated ONNX is not valid.")
    onnx_simplified = onnx.load(output_path)
    _compare_models(onnx_to_simplify, onnx_simplified)

def main():
    """Handle argument parsing and call :py:func:`aidge_onnx.onnx_sim`.
    This function is exposed as a project script by pyproject.toml.
    """
    parser = argparse.ArgumentParser()
    # Positional args
    parser.add_argument('input_model', nargs="?", help='Path to the input ONNX model.')
    parser.add_argument('output_model', nargs="?", help='Path to save the simplified ONNX model.')
    # Optional args
    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help=(
            "Set the verbosity level of the console output. "
            "Use -v to increase verbosity, with the following levels in ascending order:\n"
            "  default: WARN - Only warnings and higher (WARN, ERROR, FATAL) are displayed.\n"
            "  -v: NOTICE - Notices and higher (NOTICE, WARN, ERROR, FATAL) are displayed.\n"
            "  -vv INFO - Informational messages and higher (INFO, NOTICE, WARN, ERROR, FATAL) are displayed.\n"
            "  -vvv: DEBUG - All messages, including debug information, are displayed.\n"
            "Available levels in descending order of severity:\n"
            "  DEBUG < INFO < NOTICE < WARN < ERROR < FATAL."
        )
    )
    parser.add_argument("--show_recipes", action="store_true", help="Show available recipes and exit")
    parser.add_argument(
        "--input-shape",
        help=(
            "Overwrite the input shape.\n"
            "The format is \"input_name:dim0,dim1,...,dimN\" or simply \"dim0,dim1,...,dimN\" when there is only one input.\n"
            "For example, \"data:1,3,224,224\" or \"1,3,224,224\".\n"
            "input_name correspond to the name of the output of the input node.\n"
            "This convention is due to ONNX name being not mandatory.\n"
            "If the output name begin by a number, you need to prepend it with \"data_\".\n"
            "If one node take multiple input you can add it multiple time, the order is determined by the order of the arguments provided.\n"
            "For example, \"--input-shape data:1,3 data:1,10\".\n"
            "Here the first input will be of size \"1,3\" and the second \"1,10\".\n"
            "Note: you might want to use some visualization tools like netron to make sure what the input name and dimension ordering (NCHW or NHWC) is."),
        type=str,
        nargs="+",
    )

    args = parser.parse_args()
    if args.show_recipes:
        show_available_simplification()
        exit()

    if not args.input_model or not args.output_model:
        parser.error("the following arguments are required: input_model, output_model")

    # Setting Aidge verbose level
    if args.verbose == 0:
        aidge_core.Log.set_console_level(aidge_core.Level.Fatal)
    elif args.verbose == 1:
        aidge_core.Log.set_console_level(aidge_core.Level.Notice)
    elif args.verbose == 2:
        aidge_core.Log.set_console_level(aidge_core.Level.Info)
    elif args.verbose >= 3:
        aidge_core.Log.set_console_level(aidge_core.Level.Debug)

    input_shape: Dict[str, List[int]] = _parse_shapes(args.input_shape)

    onnx_sim(args.input_model, args.output_model, input_shape)


if __name__ == "__main__":
    main()