import onnx
import numpy as np

from aidge_core import dtype as ai_dtype
from typing import Dict, Any

"""
Global converter to convert data types from aidge to numpy datatypes
"""
_MAP_NP_ONNX_TYPE = {
    np.dtype(np.float32): onnx.TensorProto.FLOAT,
    np.dtype(np.float64): onnx.TensorProto.DOUBLE,
    np.dtype(np.int8): onnx.TensorProto.INT8,
    np.dtype(np.int16): onnx.TensorProto.INT16,
    np.dtype(np.int32): onnx.TensorProto.INT32,
    np.dtype(np.int64): onnx.TensorProto.INT64,
    np.dtype(np.uint8): onnx.TensorProto.UINT8,
    np.dtype(np.uint16): onnx.TensorProto.UINT16,
    np.dtype(np.uint32): onnx.TensorProto.UINT32,
    np.dtype(np.uint64): onnx.TensorProto.UINT64,
    np.dtype(np.bool_): onnx.TensorProto.BOOL,
}
_MAP_ONNX_NP_TYPE = {v: k for k, v in _MAP_NP_ONNX_TYPE.items()}


def numpy_to_onnx(np_dtype: np.dtype) -> onnx.TensorProto.DataType:
    if np_dtype not in _MAP_NP_ONNX_TYPE:
        raise ValueError(f"Unsupported NumPy dtype: {np_dtype}")
    onnx_type = _MAP_NP_ONNX_TYPE[np_dtype]
    return onnx_type


def onnx_to_numpy(onnx_type: onnx.TensorProto.DataType) -> np.dtype:
    if onnx_type not in _MAP_ONNX_NP_TYPE:
        raise ValueError(f"Unsupported ONNX TensorProto type: {onnx_type}")
    np_dtype = _MAP_ONNX_NP_TYPE[onnx_type]
    return np_dtype


"""
Global converter to convert data types from aidge to numpy datatypes
"""
_MAP_AIDGE_TO_NP_DTYPE = {
    ai_dtype.float16: np.float16,
    ai_dtype.float32: np.float32,
    ai_dtype.float64: np.float64,
    ai_dtype.int8: np.int8,
    ai_dtype.int16: np.int16,
    ai_dtype.int32: np.int32,
    ai_dtype.int64: np.int64,
    ai_dtype.uint8: np.uint8,
    ai_dtype.uint16: np.uint16,
    ai_dtype.uint32: np.uint32,
    ai_dtype.uint64: np.uint64,
}
_MAP_NP_TO_AIDGE_DTYPE = {v: k for k, v in _MAP_AIDGE_TO_NP_DTYPE.items()}


def aidge_to_np(aidge_dtype: ai_dtype) -> onnx.TensorProto.DataType:
    if aidge_dtype not in _MAP_AIDGE_TO_NP_DTYPE:
        raise ValueError(f"aidge datatype {aidge_dtype} has no numpy equivalent.")
    np_type = _MAP_AIDGE_TO_NP_DTYPE[aidge_dtype]
    return np_type


def np_to_aidge(np_dtype: np.dtype) -> ai_dtype:
    if np_dtype not in _MAP_AIDGE_TO_NP_DTYPE:
        raise ValueError(f"Numpy dtype {np_dtype} has no aidge equivalent.")
    aidge_dtype = _MAP_NP_TO_AIDGE_DTYPE[np_dtype]
    return aidge_dtype


"""
Global converter to convert data types from aidge to onnx TensorProto datatypes
"""
_MAP_AIDGE_TO_ONNX_DTYPE: Dict[Any, Any] = {
    ai_dtype.bfloat16: onnx.TensorProto.BFLOAT16,
    ai_dtype.binary: onnx.TensorProto.BOOL,
    ai_dtype.float16: onnx.TensorProto.FLOAT16,
    ai_dtype.float32: onnx.TensorProto.FLOAT,
    ai_dtype.float64: onnx.TensorProto.DOUBLE,
    ai_dtype.int4: onnx.TensorProto.INT4,
    ai_dtype.int8: onnx.TensorProto.INT8,
    ai_dtype.int16: onnx.TensorProto.INT16,
    ai_dtype.int32: onnx.TensorProto.INT32,
    ai_dtype.int64: onnx.TensorProto.INT64,
    ai_dtype.uint4: onnx.TensorProto.UINT4,
    ai_dtype.uint8: onnx.TensorProto.UINT8,
    ai_dtype.uint16: onnx.TensorProto.UINT16,
    ai_dtype.uint32: onnx.TensorProto.UINT32,
    ai_dtype.uint64: onnx.TensorProto.UINT64,
}
_MAP_ONNX_TO_AIDGE_DTYPE = {v: k for k, v in _MAP_AIDGE_TO_ONNX_DTYPE.items()}

def aidge_to_onnx(aidge_dtype: ai_dtype) -> onnx.TensorProto.DataType:
    if aidge_dtype not in _MAP_AIDGE_TO_ONNX_DTYPE:
        raise ValueError(f"aidge datatype {aidge_dtype} has no onnx equivalent.")
    onnx_type = _MAP_AIDGE_TO_ONNX_DTYPE[aidge_dtype]
    return onnx_type


def onnx_to_aidge(onnx_dtype: onnx.TensorProto.DataType) -> ai_dtype:
    if onnx_dtype not in _MAP_ONNX_TO_AIDGE_DTYPE:
        raise ValueError(f"Onnx DataType {onnx_dtype} has no onnx equivalent.")
    np_dtype = _MAP_ONNX_TO_AIDGE_DTYPE[onnx_dtype]
    return np_dtype
