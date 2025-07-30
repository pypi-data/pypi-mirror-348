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
from onnx import NodeProto

from aidge_onnx.node_import import auto_register_import
from aidge_onnx.utils import get_node_attributes

from aidge_core import Log

@auto_register_import("leakyrelu")
def import_leaky_relu(onnx_node: NodeProto, input_nodes: List[Tuple[aidge_core.Node, int]], opset: Optional[int]) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = get_node_attributes(onnx_node, opset)
    leaky_relu_attrs : dict = {"negative_slope" : 0.0, "name": node_name}#aidge default alpha/negative_slope value, different to 0.01 default for ONNX

    if opset < 6 and 'consumed_inputs' in onnx_attrs:
        #Legacy optimization attribute, ignored
        del onnx_attrs['consumed_inputs']

    if 'alpha' in onnx_attrs:
        leaky_relu_attrs['negative_slope'] = onnx_attrs['alpha']
        del onnx_attrs['alpha']

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'LeakyRelu' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    my_node = aidge_core.LeakyReLU(**leaky_relu_attrs)
    Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")
    return my_node
