import aidge_core
from . import register_transformation

@register_transformation("ConstantShapeFolding", brief="Fold constant and shape node.")
def constant_shape_folding(graph_view):
    aidge_core.constant_shape_folding(graph_view)
