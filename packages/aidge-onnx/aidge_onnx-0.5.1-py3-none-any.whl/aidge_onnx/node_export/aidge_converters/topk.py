"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

from typing import List, Optional
import aidge_core
from onnx import helper
from aidge_onnx.node_export import auto_register_export

@auto_register_export("TopK")
def export_topk(aidge_node: aidge_core.Node, node_inputs_name: List[str], node_outputs_name: List[str], opset: Optional[int] = None, **kwargs) -> List[helper.NodeProto]:
    aidge_operator = aidge_node.get_operator()
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="TopK",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    onnx_node.attribute.append(
        helper.make_attribute(
            "axis",
            aidge_operator.attr.get_attr("axis")
    ))
    onnx_node.attribute.append(
        helper.make_attribute(
            "largest",
            aidge_operator.attr.get_attr("largest")
    ))
    onnx_node.attribute.append(
        helper.make_attribute(
            "sorted",
            aidge_operator.attr.get_attr("sorted")
    ))
    return [onnx_node]
