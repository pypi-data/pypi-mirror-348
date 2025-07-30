"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
from onnx import helper
from aidge_onnx.node_export import auto_register_export
from typing import List, Optional

@auto_register_export("PaddedMaxPooling1D", "PaddedMaxPooling2D", "PaddedMaxPooling3D")
def export_maxpooling(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None,
    **kwargs
) -> List[helper.NodeProto]:
    aidge_operator = aidge_node.get_operator()

    micro_graph = aidge_operator.get_micro_graph()
    maxpool_op, pad_op = None, None
    for node in micro_graph.get_nodes():
        if node.type() == "MaxPooling1D" or node.type() == "MaxPooling2D" or node.type() == "MaxPooling3D":
            maxpool_op = node.get_operator()
        elif node.type() == "Pad1D" or node.type() == "Pad2D" or node.type() == "Pad3D":
            pad_op = node.get_operator()
        else:
            raise RuntimeError(f"Unsupported node type: {node.type()} inside PaddedMaxPooling.")

    # Computing padding
    kernel_dims = maxpool_op.attr.get_attr("kernel_dims")
    aidge_pads  = pad_op.attr.get_attr("begin_end_borders")
    pads = [0] * 2*len(kernel_dims)
    for i in range(0, len(kernel_dims)):
        pads[i] = aidge_pads[2*i]
        pads[len(kernel_dims)+i] = aidge_pads[2*i+1]

    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="MaxPool",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    onnx_node.attribute.append(
        helper.make_attribute(
            "kernel_shape",
            maxpool_op.attr.get_attr("kernel_dims")
    ))
    onnx_node.attribute.append(
        helper.make_attribute(
            "strides",
            maxpool_op.attr.get_attr("stride_dims")
    ))
    onnx_node.attribute.append(
        helper.make_attribute(
            "pads",
            pads
    ))
    return [onnx_node]
