"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""

from typing import List, Tuple, Optional
import numpy as np

import aidge_core
import onnx
from onnx import NodeProto
from aidge_core import pad_border_type

from aidge_onnx.node_import import auto_register_import
from aidge_onnx.utils import get_node_attributes

from aidge_core import Log


@auto_register_import("pad")
def import_slice(
    onnx_node: NodeProto,
    input_nodes: List[Tuple[aidge_core.Node, int]],
    opset: Optional[int] = None,
) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    """
    node_name = onnx_node.output[0]
    border_type_map = {
        b"constant": pad_border_type.Constant,
        b"edge": pad_border_type.Edge,
        b"reflect": pad_border_type.Reflect,
        b"wrap": pad_border_type.Wrap,
    }
    onnx_attrs = get_node_attributes(onnx_node, opset)
    aidge_attrs = {
        "borderType": pad_border_type.Constant,
        "borderValue": 0.0,
    }

    # No support for old version of Pad
    if opset < 3:
        Log.warn("Warning: Pad opset < 3 not supported.")
        return None

    if onnx_attrs["mode"] not in border_type_map:
        Log.warn(
            f"Warning: Pad attribute mode=='{onnx_attrs['mode']}' is not implemented."
        )
        return None

    aidge_attrs["borderType"] = border_type_map[onnx_attrs["mode"]]

    # Only support constant input for constant value
    if len(input_nodes) >= 3:
        if input_nodes[2] is None:
            Log.warn("Warning: Pad input for pads value must be constant.")
            return None
        cst_val = np.array(
            input_nodes[2][0].get_operator().get_output(input_nodes[2][1])
        )
        aidge_attrs["borderValue"] = float(cst_val.item())

    # TODO: do not support the optionals input axes
    if len(input_nodes) >= 4:
        Log.warn("Warning: Pad optional axes inputs are not implemented.")
        return None

    # TODO: only support constant input for pads value
    if len(input_nodes) < 2 or input_nodes[1] is None:
        Log.warn("Warning: Pad input for pads sizes missing or non constant.")
        return None

    onnx_pads = np.array(input_nodes[1][0].get_operator().get_output(input_nodes[1][1]))

    dims = len(onnx_pads) // 2
    cls_name = f"Pad{dims}D"

    if not hasattr(aidge_core, cls_name):
        Log.warn(f"Warning: Pad class {cls_name} is not implemented for operator pad.")
        return None

    pad_node = getattr(aidge_core, cls_name)(onnx_pads, name=node_name)
    Log.info(f"Loaded node [\033[1m\033[3m{node_name}\033[0m] of type [\033[1m\033[3m{onnx_node.op_type}\033[0m]")

    return pad_node
