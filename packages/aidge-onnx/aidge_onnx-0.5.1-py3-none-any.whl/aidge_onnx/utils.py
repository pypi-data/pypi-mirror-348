import onnx

from aidge_core import Log
from typing import Dict, Any
from importlib.metadata import version

_AIDGE_DOMAIN = "ai.onnx.converters.aidge"

def show_version():
    version_aidge_onnx = version("aidge_onnx")
    version_onnx = version("onnx")
    version_protobuf = version("protobuf")
    print(f"Aidge ONNX: {version_aidge_onnx}")
    print(f"ONNX version: {version_onnx}")
    print(f"Protobuf: {version_protobuf}")

def get_project_version()->str:
    return version("aidge_onnx")


def onnx_to_aidge_model_names(model: onnx.ModelProto) -> onnx.ModelProto:
    """
    Change the name of each node of the model from onnx convention to aidge's one
    args :
        model : to modify
    return :
        model : modified
    """
    for i in model.graph.initializer:
        i.name = onnx_to_aidge_name(i.name)

    for n in model.graph.node:
        if len(n.name) > 0:
            new_name = onnx_to_aidge_name(n.name)
            if n.name[0].isdigit():
                new_name = "layer_" + new_name
            n.name = new_name
        for index, i in enumerate(n.input):
            n.input[index] = onnx_to_aidge_name(i)
        for index, o in enumerate(n.output):
            n.output[index] = onnx_to_aidge_name(o)

    for i in model.graph.input:
        i.name = onnx_to_aidge_name(i.name)

    for o in model.graph.output:
        o.name = onnx_to_aidge_name(o.name)

    return model


def onnx_to_aidge_name(name: str) -> str:
    """
    Translates onnx node naming convention to aidge naming convention
    """
    name = name.replace("/", "_").replace(".", "_").replace(":", "_")
    if len(name) > 0 and name[0] == "_":
        name = name[1:]
    name = name if (len(name) == 0 or not name[0].isdigit()) else "data_" + name
    return name


def get_node_attributes(
    onnx_node: onnx.NodeProto, op_set: int = None, domain: str = ""
) -> Dict[str, Any]:
    """Given an ONNX node, return a dictionary with all attributes set to the
    provided value if any or the default value.
    """
    op_type = onnx_node.op_type
    schema = onnx.defs.get_schema(op_type, op_set, domain)
    result_attrs = {}

    provided_attrs = (
        {
            attr.name: onnx.helper.get_attribute_value(attr)
            for attr in onnx_node.attribute
        }
        if onnx_node.attribute
        else {}
    )

    for attr_name, attr in schema.attributes.items():
        if attr_name in provided_attrs:
            result_attrs[attr_name] = provided_attrs[attr_name]
            del provided_attrs[attr_name]
        elif attr.required:
            raise ValueError(f"Required attribute '{attr_name}' is missing.")
        elif attr.default_value.type != onnx.AttributeProto.AttributeType.UNDEFINED:
            # Add default attributes
            if attr.default_value.type == onnx.AttributeProto.INT:
                result_attrs[attr_name] = attr.default_value.i
            elif attr.default_value.type == onnx.AttributeProto.FLOAT:
                result_attrs[attr_name] = attr.default_value.f
            elif attr.default_value.type == onnx.AttributeProto.STRING:
                result_attrs[attr_name] = attr.default_value.s
            elif attr.default_value.type == onnx.AttributeProto.TENSOR:
                result_attrs[attr_name] = onnx.numpy_helper.to_array(
                    attr.default_value.t
                )
            elif attr.default_value.type == onnx.AttributeProto.INTS:
                result_attrs[attr_name] = list(attr.default_value.ints)
            elif attr.default_value.type == onnx.AttributeProto.FLOATS:
                result_attrs[attr_name] = list(attr.default_value.floats)
            elif attr.default_value.type == onnx.AttributeProto.STRINGS:
                result_attrs[attr_name] = list(attr.default_value.strings)
    if len(provided_attrs) > 0:
        raise ValueError(
            f"Warning: unsupported attribute(s): {provided_attrs.keys()} "
            f"for operator '{onnx_node.op_type}' with opset {op_set}."
        )
    return result_attrs


def warn_unsupported_attr(
    attr: str, operator: str, opset: int, value: Any = None
) -> None:
    """Function used to standardize warning messages for operators import

    :param attr: Name of the attribute not supported
    :type attr: str
    :param operator: name of the type of operator
    :type operator: str
    :param opset: opset of the operator used
    :type opset: int
    :param value: Value of the attribute if it has one
    :type value: Any
    """
    if value is not None:
        Log.warn(
            f"Warning: Unsupported attribute '{attr}' with value {value} for operator '{operator}' with opset {opset}. This node will be filled by a GenericOperator."
        )
    else:
        Log.warn(
            f"Warning: Unsupported attribute '{attr}' for operator '{operator}' with opset {opset}. This node will be filled by a GenericOperator."
        )
