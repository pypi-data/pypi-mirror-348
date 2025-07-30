"""
Copyright (c) 2024 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

import aidge_core
import onnx
from onnx import helper
from aidge_onnx.node_export import auto_register_export
from typing import List, Optional

@auto_register_export("Dropout")
def export_dropout(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None) -> List[helper.NodeProto]:
    aidge_operator = aidge_node.get_operator()

    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Dropout",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )

    if opset is not None and opset < 12:
        onnx_node.attribute.append(
            helper.make_attribute(
                "ratio",
                aidge_operator.get_attr("probability")
            )
        )
    return [onnx_node]