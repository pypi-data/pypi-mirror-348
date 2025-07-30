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

@auto_register_import("quantizelinear")
def import_quantizelinear(onnx_node: NodeProto, input_nodes: List[Tuple[aidge_core.Node, int]], opset: Optional[int]) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    #QuantizeLinear is originally an Onnx operator used to quantize a high precision tensor
    #quantization uses the following formula : y = round(x / y_scale) + y_zero_point
    #Inputs descriptions:
        #x: full precision input tensor
        #y_scale: scaling factor used in the quantization
        #y_zero_point (optional): zero point used in the quantization

    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = get_node_attributes(onnx_node, opset)
    quantize_linear_attrs: dict = {}

    if opset >= 13:
        if 'axis' in onnx_attrs:
            if onnx_attrs['axis'] != 1:
                warn_unsupported_attr('axis','QuantizeLinear',opset,onnx_attrs['axis'])
                return None
            del onnx_attrs['axis']

    if opset >= 19:
        if 'saturate' in onnx_attrs:
            if onnx_attrs['saturate'] != 1:
                warn_unsupported_attr('saturate','QuantizeLinear',opset,onnx_attrs['saturate'])
                return None
            del onnx_attrs['saturate']

    if opset >= 21:
        if 'block_size' in onnx_attrs:
            if onnx_attrs['block_size'] != 0:
                warn_unsupported_attr('block_size','QuantizeLinear',opset,onnx_attrs['block_size'])
                return None
            del onnx_attrs['block_size']

        if 'output_dtype' in onnx_attrs:
            if onnx_attrs['output_dtype'] != 0:
                warn_unsupported_attr('output_dtype','QuantizeLinear',opset,onnx_attrs['output_dtype'])
                return None
            del onnx_attrs['output_dtype']

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'DequantizeLinear' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    #get all the onnx initializers
    quantif_inputs = []
    for inp in input_nodes[1:]:
        prod_node = inp[0]
        quantif_inputs.append(prod_node.get_operator().get_output(0))

    #check if zero point is in the initializers
    has_zero_point = len(quantif_inputs) == 2

    #output dtype is determined by zero_point dtype
    if has_zero_point:
        cast_output_dtype = quantif_inputs[1].dtype()
    else:
        #if zero point is no specified, default output dtype is uint8
        cast_output_dtype = aidge_core.dtype.uint8

    #nodes creetion
    #Div -> Round -> Cast -> Add(optional)
    quant_div = aidge_core.Div(node_name+"_div_node")
    quant_round = aidge_core.Round(node_name+"_round_node")
    quant_cast = aidge_core.Cast(cast_output_dtype,
                                 node_name+"_cast_node")

    #nodes connections
    quant_div.add_child(quant_round,0,0)
    quant_round.add_child(quant_cast,0,0)

    #QuantizeLinear inputs must use the following order:
    #input, scaling factor, zero point(optional)
    ordered_inputs = [[quant_div,0],#input
                      [quant_div,1]]#scaling factor

    if has_zero_point:
        #if zero point is present add operator and connection must be done
        quant_add = aidge_core.Add(node_name+"_add_node")
        quant_cast.add_child(quant_add,0,0)
        quantize_linear_graph = aidge_core.get_connected_graph_view(quant_add)
        ordered_inputs.append([quant_add,1])#zero point as input if it exists
    else:
        quantize_linear_graph = aidge_core.get_connected_graph_view(quant_cast)

    quantize_linear_graph.set_ordered_inputs(ordered_inputs)

    #metaop creation
    metaop_quantize_linear = aidge_core.meta_operator("QuantizeLinear",
                             quantize_linear_graph,
                             name = node_name)

    Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")
    return metaop_quantize_linear
