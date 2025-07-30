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


@auto_register_export("Resize")
def export_resize(
    aidge_node: aidge_core.Node,
    node_inputs_name: List[str],
    node_outputs_name: List[str],
    opset: Optional[int] = None,
    **kwargs,
) -> List[helper.NodeProto]:

    aidge_operator = aidge_node.get_operator()
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Resize",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
    )
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    # Map Aidge attributes to ONNX attributes
    mode_dict_inv = {
        aidge_core.Interpolation.Mode.CUBIC: "cubic",
        aidge_core.Interpolation.Mode.LINEAR: "linear",
        aidge_core.Interpolation.Mode.FLOOR: "floor",
        aidge_core.Interpolation.Mode.CEIL: "ceil",
        aidge_core.Interpolation.Mode.ROUND_PREFER_FLOOR: "round_prefer_floor",
        aidge_core.Interpolation.Mode.ROUND_PREFER_CEIL: "round_prefer_ceil",
    }

    coord_trans_dict_inv = {
        aidge_core.Interpolation.CoordinateTransformation.HALF_PIXEL: "half_pixel",
        aidge_core.Interpolation.CoordinateTransformation.ASYMMETRIC: "asymmetric",
    }

    aidge_mode = aidge_operator.attr.get_attr("interpolation_mode")

    onnx_attrs = {
        "coordinate_transformation_mode": coord_trans_dict_inv[
            aidge_operator.attr.get_attr("coordinate_transformation_mode")
        ],
        "cubic_coeff_a": -0.75,
    }
    if aidge_mode in [aidge_core.Interpolation.Mode.CUBIC, aidge_core.Interpolation.Mode.LINEAR]:
        onnx_attrs["mode"] = mode_dict_inv[aidge_mode]
    else:
        onnx_attrs["mode"] = "nearest"
        onnx_attrs["nearest_mode"] = mode_dict_inv[aidge_mode]



    # Create the ONNX node
    onnx_node = helper.make_node(
        name=aidge_node.name(),
        op_type="Resize",
        inputs=node_inputs_name,
        outputs=node_outputs_name,
        **onnx_attrs,
    )

    aidge_core.Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")

    return [onnx_node]
