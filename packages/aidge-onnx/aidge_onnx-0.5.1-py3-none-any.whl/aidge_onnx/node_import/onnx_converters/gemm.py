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
from aidge_onnx.utils import warn_unsupported_attr

@auto_register_import("gemm")
def import_gemm(onnx_node: NodeProto, input_nodes: List[Tuple[aidge_core.Node, int]], opset: Optional[int]) -> aidge_core.Node:
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
    gemm_attrs = {'transA':0, 'alpha':1.0, 'beta':1.0}

    for attr_name,attr_exp_value in gemm_attrs.items():
        if onnx_attrs[attr_name] != attr_exp_value:
            warn_unsupported_attr(attr_name,'Gemm',opset,onnx_attrs[attr_name])
            return None
        del onnx_attrs[attr_name]

    if "transB" in onnx_attrs:
        if onnx_attrs["transB"] == 0:
            weights = None
            if len(input_nodes) >= 2 and input_nodes[1] is not None:
                weights = input_nodes[1][0].get_operator().get_output(0)
                old_dims = weights.dims()
            if weights is None:
                Log.warn("Warning: no support for Gemm transB == 0 with dynamic input")
                return None
            if len(old_dims) != 2:
                raise ValueError(f"Weights of Gemm operation should have 2 dimensions (found {len(old_dims)})")
            weights.cpy_transpose(weights, [1, 0])

        elif onnx_attrs["transB"] != 1:
            # transB Should be a boolean other values than 0 or 1 raise warning
            warn_unsupported_attr("transB",'Gemm',opset,onnx_attrs["transB"])
            return None
        # Note: nothing to do if transB = 1
        del onnx_attrs["transB"]

    if opset < 7 and "broadcast" in onnx_attrs:
        warn_unsupported_attr("broadcast","Gemm",opset,onnx_attrs["broadcast"])
        return None

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'Gemm' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    bias = None
    if len(input_nodes) >= 3 and input_nodes[2] is not None:
        bias = input_nodes[2][0].get_operator().get_output(0)
        bias_dims = bias.dims()

    # In Aidge bias should be None or with 1 dims
    if bias is not None and len(bias_dims) !=1:
        if len(bias_dims) == 2 and bias_dims[0] == 1:
            # Case bias.dims = [1, N]
            bias.resize([bias_dims[1]])
        else:
            Log.warn(f"Warning: cannot import bias of dims: {bias_dims} for operator 'Gemm' with opset {opset}.\nThis node will be filled by a GenericOperator.")
            return None

    fc_node = aidge_core.Node(aidge_core.FCOp(), name=node_name)
    Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")
    return fc_node
