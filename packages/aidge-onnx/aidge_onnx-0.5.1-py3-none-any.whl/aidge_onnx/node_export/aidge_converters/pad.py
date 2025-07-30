"""
Copyright (c) 2024 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
from onnx import helper, TensorProto
from aidge_onnx.node_export import auto_register_export
from typing import List, Optional

@auto_register_export("Pad1D", "Pad2D", "Pad3D")
def export_pad(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None,
    **kwargs
) -> List[helper.NodeProto]:

    pad_op = None
    mode = None

    if aidge_node.type() in ["Pad1D", "Pad2D", "Pad3D"]:
        pad_op = aidge_node.get_operator()
    else:
        raise RuntimeError(f"Unsupported node typpe: {aidge_node.type()} inside Pad. ")


    if pad_op.attr.border_type == aidge_core.pad_border_type.Edge:
        mode = "edge"
    elif pad_op.attr.border_type == aidge_core.pad_border_type.Wrap:
        mode = "wrap"
    elif pad_op.attr.border_type == aidge_core.pad_border_type.Reflect:
        mode = "reflect"
    else :
        mode = "constant"

    pads_tensor = helper.make_tensor('pads', TensorProto.INT64, [len(pad_op.attr.begin_end_borders)], pad_op.attr.begin_end_borders)

    onnx_node_pad = helper.make_node(
        name=f"{aidge_node.name()}_pad",
        op_type="Constant",
        inputs=[],
        outputs=[f"{aidge_node.name()}_pad_output_0"],
    )
    onnx_node_pad.attribute.append(
        helper.make_attribute(
            "value",
            pads_tensor
    ))

    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Pad",
        inputs=node_inputs_name +[f"{aidge_node.name()}_pad_output_0"],
        outputs=node_outputs_name,
    )
    onnx_node.attribute.append(
    helper.make_attribute(
        "mode",
        mode
    ))
    if pad_op.attr.border_type.value == aidge_core.pad_border_type.Constant:
        onnx_node.attribute.append(
        helper.make_attribute(
            "constant_value",
            pad_op.attr.border_value
    ))

    return [onnx_node_pad,onnx_node]
