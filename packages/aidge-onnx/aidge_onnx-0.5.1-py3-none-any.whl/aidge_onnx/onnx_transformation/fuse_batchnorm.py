import aidge_core
from . import register_transformation

@register_transformation("FuseBN", brief="Fuse BatchNormalization layer with previous Conv or FC layer.")
def fuse_bn(graph_view):
    aidge_core.fuse_batchnorm(graph_view)
