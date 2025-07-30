"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
from typing import List, Optional, Tuple

import aidge_core
import onnx
from onnx import NodeProto

from aidge_onnx.node_import import auto_register_import

from aidge_core import Log

@auto_register_import("round")
def import_round(onnx_node: NodeProto, input_nodes: List[Tuple[aidge_core.Node, int]], opset: Optional[int]) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]

    my_node = aidge_core.Round(name=node_name, rounding_mode=aidge_core.RoundingMode.HalfToEven)
    Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")
    return my_node
