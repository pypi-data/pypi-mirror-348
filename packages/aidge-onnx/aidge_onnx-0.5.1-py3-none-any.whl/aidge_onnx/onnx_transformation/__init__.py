from pathlib import Path
import importlib

GRAPH_TRANSFORMATION = {}

def register_transformation(transformation_name, brief=None):
    def decorator(decorated_function):
        def wrapper(*args, **kwargs):
            return decorated_function(*args, **kwargs)
        _register_transformation(transformation_name, decorated_function, brief=brief)
        return wrapper
    return decorator

def list_transformations():
    return list(GRAPH_TRANSFORMATION.keys())

def _register_transformation(key, transformation_function, brief=None) -> None:
    GRAPH_TRANSFORMATION[key] = (transformation_function, brief if brief else "")

DIR_PATH = Path(__file__).parent
modules = [Path(module).stem for module in DIR_PATH.glob("*.py")]
__all__ = [ f for f in modules if f != "__init__"]

# Dynamically import each module
for module in __all__:
    importlib.import_module(f"{__name__}.{module}")