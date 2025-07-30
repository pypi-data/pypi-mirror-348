"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
from typing import List, Tuple, Optional

import aidge_core
import onnx
import numpy as np
from aidge_onnx.node_import import auto_register_import
from onnx import numpy_helper, NodeProto

from aidge_core import Log

@auto_register_import("constant")
def import_constant(onnx_node: NodeProto, input_nodes: List[Tuple[aidge_core.Node, int]], opset: Optional[int]) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]

    if len(onnx_node.attribute) == 1:
        #Only value accepted in aidge for the moment
        if onnx_node.attribute[0].name == "value":
            Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")
            values = numpy_helper.to_array(onnx_node.attribute[0].t)
            Log.info(f"val type: {values.dtype}")
            return aidge_core.Producer(aidge_core.Tensor(values) if values.shape != () else aidge_core.Tensor(np.array(values.item(), dtype=values.dtype)), node_name, True)

        if onnx_node.attribute[0].name in ("sparse_value","value_float","value_floats","value_int","value_ints","value_string","value_strings"):
            raise RuntimeError(f"The attribute {onnx_node.attribute[0].name} is not yet supported. Please create the conversion to Producer in node_converters/converters/contant.py or open an issue at: https://gitlab.eclipse.org/eclipse/aidge/aidge_onnx/-/issues")

        raise ValueError(f"The attribute name \"{onnx_node.attribute[0].name}\" does not exist, the ONNX may be ill formed, the accepted attribute names are listed at: https://github.com/onnx/onnx/blob/main/docs/Operators.md#attributes-16")

    raise ValueError("The number of attributes doesn't respect the doc https://github.com/onnx/onnx/blob/main/docs/Operators.md#Constant")
