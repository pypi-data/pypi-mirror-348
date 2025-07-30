import aidge_core
from . import register_transformation

@register_transformation("RemoveIdentity", brief="Remove identity nodes from graph.")
def rm_identity(graph_view):
    aidge_core.remove_identity(graph_view)
