"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
from onnx import helper, TensorProto
from onnx import helper
from aidge_onnx.node_export import auto_register_export
from aidge_onnx import dtype_converter
from typing import List, Optional

def get_in_dtype(aidge_op):
    if aidge_op.get_input(0):
        return aidge_op.get_input(0).dtype()
    else:
        raise ValueError("Clip node does not have an input cannot determine min and max type.")

@auto_register_export("Clip")
def export_clip(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None,
    **kwargs) -> List[helper.NodeProto]:

    aidge_operator = aidge_node.get_operator()

    if opset is not None and opset < 11:
        if aidge_operator.get_input(1) is not None:
            # TODO: Implement the case where min is a producer
            NotImplementedError("No support for Clip with min as a producer for opset < 11")
        del node_inputs_name[1]
    else:
        if aidge_operator.get_input(1) is None:
            node_inputs_name[1] =f"{aidge_node.name()}_in_min"

    if opset is not None and opset < 11:
        if aidge_operator.get_input(2) is not None:
            # TODO: Implement the case where max is a producer
            NotImplementedError("No support for Clip with max as a producer for opset < 11")
        del node_inputs_name[2]
    else:
        if aidge_operator.get_input(2) is None:
            node_inputs_name[2] =f"{aidge_node.name()}_in_max"

    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Clip",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )
    onnx_nodes = []

    if opset is not None and opset < 11 :
        onnx_node.attribute.append(
            helper.make_attribute(
                "min",
                aidge_operator.min()
        ))
        onnx_node.attribute.append(
            helper.make_attribute(
                "max",
                aidge_operator.max()
        ))
    else:
        # If min or max are a producer, nothing to do
        # But if they are none we need to create a constant node
        # With the attribute value!
        if aidge_operator.get_input(1) is None:

            # No producer input for indices, create a constant node
            min_node = helper.make_node(
                name=f"{node_inputs_name[1]}_constant",
                op_type="Constant",
                inputs=[],
                outputs=[node_inputs_name[1]],
            )

            min_node.attribute.append(
                helper.make_attribute(
                    "value",
                    helper.make_tensor(
                        f"{node_inputs_name[1]}_tensor",
                        # TensorProto.FLOAT,
                        dtype_converter.aidge_to_onnx(get_in_dtype(aidge_operator)),
                        [], # Note: Allow a better netron representation
                        [aidge_operator.attr.min]
                    )
                )
            )
            onnx_nodes.append(min_node)

        if aidge_operator.get_input(2) is None:
            # No producer input for indices, create a constant node
            max_node = helper.make_node(
                name=f"{node_inputs_name[2]}_constant",
                op_type="Constant",
                inputs=[],
                outputs=[node_inputs_name[2]],
            )

            max_node.attribute.append(
                helper.make_attribute(
                    "value",
                    helper.make_tensor(
                        f"{node_inputs_name[2]}_tensor",
                        # TensorProto.FLOAT,
                        dtype_converter.aidge_to_onnx(get_in_dtype(aidge_operator)),
                        [], # Note: Allow a better netron representation
                        [aidge_operator.attr.max]
                    )
                )
            )
            onnx_nodes.append(max_node)
    onnx_nodes.append(onnx_node)
    return onnx_nodes
