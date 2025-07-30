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

# For some reasons, pybinds of paddedAveragePooling 1D & 3D are disabled
@auto_register_export("PaddedAvgPooling2D")
def export_identity(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None,
    **kwargs
) -> List[helper.NodeProto]:

    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="AveragePool",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    onnx_node.attribute.append(
        helper.make_attribute(
            "strides",
            aidge_node.get_operator().stride_dims()
    ))
    onnx_node.attribute.append(
        helper.make_attribute(
            "kernel_shape",
            aidge_node.get_operator().kernel_dims()
    ))

    onnx_node.attribute.append(
        helper.make_attribute(
            "pads",
            aidge_node.get_operator().padding_dims()
    ))

    return [onnx_node]



