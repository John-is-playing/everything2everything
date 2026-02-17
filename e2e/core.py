class E2EType:
    """EveryThing to EveryThing 自定义数据类型"""
    
    def __init__(self, value, original_type):
        self.value = value
        self.original_type = original_type
        self.timestamp = __import__('time').time()
    
    def __repr__(self):
        return f"E2EType(value={self.value}, original_type={self.original_type.__name__})"
    
    def __str__(self):
        return f"E2EType({self.value})"
    
    def get_value(self):
        return self.value
    
    def get_original_type(self):
        return self.original_type
    
    def get_timestamp(self):
        return self.timestamp
    
    def to_original(self):
        """转换回原始类型"""
        return self.value
    
    def is_type(self, type_obj):
        """检查原始类型是否为指定类型"""
        return isinstance(self.value, type_obj)
    
    def serialize(self):
        """序列化E2EType对象"""
        import json
        try:
            # 处理numpy数组
            try:
                import numpy as np
                if isinstance(self.value, np.ndarray):
                    return json.dumps({
                        "value": self.value.tolist(),
                        "original_type": "numpy.ndarray",
                        "shape": self.value.shape,
                        "dtype": str(self.value.dtype),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理cupy数组
            try:
                import cupy as cp
                if isinstance(self.value, cp.ndarray):
                    return json.dumps({
                        "value": self.value.get().tolist(),
                        "original_type": "cupy.ndarray",
                        "shape": self.value.shape,
                        "dtype": str(self.value.dtype),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理scipy稀疏矩阵
            try:
                from scipy import sparse
                if isinstance(self.value, (sparse.csr_matrix, sparse.csc_matrix, sparse.coo_matrix)):
                    return json.dumps({
                        "value": self.value.toarray().tolist(),
                        "original_type": f"scipy.sparse.{type(self.value).__name__}",
                        "shape": self.value.shape,
                        "format": self.value.format,
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理pandas DataFrame和Series
            try:
                import pandas as pd
                if isinstance(self.value, pd.DataFrame):
                    return json.dumps({
                        "value": self.value.to_dict(orient='records'),
                        "original_type": "pandas.DataFrame",
                        "shape": list(self.value.shape),
                        "columns": list(self.value.columns),
                        "timestamp": self.timestamp
                    })
                elif isinstance(self.value, pd.Series):
                    return json.dumps({
                        "value": self.value.to_dict(),
                        "original_type": "pandas.Series",
                        "shape": list(self.value.shape),
                        "name": self.value.name,
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理PyTorch张量
            try:
                import torch
                if isinstance(self.value, torch.Tensor):
                    return json.dumps({
                        "value": self.value.tolist(),
                        "original_type": "torch.Tensor",
                        "shape": list(self.value.shape),
                        "dtype": str(self.value.dtype),
                        "device": str(self.value.device),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理JAX数组
            try:
                import jax.numpy as jnp
                if isinstance(self.value, jnp.ndarray):
                    return json.dumps({
                        "value": self.value.tolist(),
                        "original_type": "jax.numpy.ndarray",
                        "shape": list(self.value.shape),
                        "dtype": str(self.value.dtype),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理TensorFlow张量
            try:
                import tensorflow as tf
                if isinstance(self.value, tf.Tensor):
                    return json.dumps({
                        "value": self.value.numpy().tolist(),
                        "original_type": "tensorflow.Tensor",
                        "shape": list(self.value.shape),
                        "dtype": str(self.value.dtype),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理Python标准库中的特殊类型
            if isinstance(self.value, (set, frozenset)):
                return json.dumps({
                    "value": list(self.value),
                    "original_type": self.original_type.__name__,
                    "timestamp": self.timestamp
                })
            elif isinstance(self.value, bytes):
                return json.dumps({
                    "value": self.value.decode('utf-8', errors='replace'),
                    "original_type": "bytes",
                    "length": len(self.value),
                    "timestamp": self.timestamp
                })
            elif isinstance(self.value, bytearray):
                return json.dumps({
                    "value": bytes(self.value).decode('utf-8', errors='replace'),
                    "original_type": "bytearray",
                    "length": len(self.value),
                    "timestamp": self.timestamp
                })
            elif isinstance(self.value, range):
                return json.dumps({
                    "value": list(self.value),
                    "original_type": "range",
                    "start": self.value.start,
                    "stop": self.value.stop,
                    "step": self.value.step,
                    "timestamp": self.timestamp
                })
            elif isinstance(self.value, tuple):
                return json.dumps({
                    "value": list(self.value),
                    "original_type": "tuple",
                    "length": len(self.value),
                    "timestamp": self.timestamp
                })
            
            # 处理xarray对象
            try:
                import xarray as xr
                if isinstance(self.value, xr.DataArray):
                    return json.dumps({
                        "value": self.value.values.tolist(),
                        "original_type": "xarray.DataArray",
                        "shape": list(self.value.shape),
                        "dims": list(self.value.dims),
                        "coords": {k: v.values.tolist() for k, v in self.value.coords.items()},
                        "timestamp": self.timestamp
                    })
                elif isinstance(self.value, xr.Dataset):
                    return json.dumps({
                        "value": {var: self.value[var].values.tolist() for var in self.value.data_vars},
                        "original_type": "xarray.Dataset",
                        "data_vars": list(self.value.data_vars),
                        "coords": {k: v.values.tolist() for k, v in self.value.coords.items()},
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理PIL/Pillow图像对象
            try:
                from PIL import Image
                import io
                if isinstance(self.value, Image.Image):
                    # 获取图像基本信息
                    img_info = {
                        "format": self.value.format,
                        "size": self.value.size,
                        "mode": self.value.mode
                    }
                    return json.dumps({
                        "value": img_info,
                        "original_type": "PIL.Image.Image",
                        "format": self.value.format,
                        "size": self.value.size,
                        "mode": self.value.mode,
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理Numba类型
            try:
                import numba
                if hasattr(self.value, "__numba_type__"):
                    return json.dumps({
                        "value": str(self.value),
                        "original_type": "numba.type",
                        "numba_type": str(self.value.__numba_type__),
                        "timestamp": self.timestamp
                    })
            except ImportError:
                pass
            
            # 处理自定义类对象
            try:
                # 尝试序列化具有__dict__的对象
                if hasattr(self.value, "__dict__"):
                    return json.dumps({
                        "value": {k: v for k, v in self.value.__dict__.items() if not k.startswith('__')},
                        "original_type": f"{self.original_type.__module__}.{self.original_type.__name__}",
                        "timestamp": self.timestamp
                    })
            except:
                pass
            
            return json.dumps({
                "value": self.value,
                "original_type": self.original_type.__name__,
                "timestamp": self.timestamp
            })
        except:
            return f"E2EType({self.value})"


def to_e2e(value):
    """将任何Python标准类型转换为E2EType"""
    return E2EType(value, type(value))


def from_e2e(e2e_obj):
    """从E2EType对象转换回原始值"""
    if isinstance(e2e_obj, E2EType):
        return e2e_obj.to_original()
    return e2e_obj


# 示例用法
if __name__ == "__main__":
    # 转换字符串
    str_e2e = to_e2e("Hello, World!")
    print(f"字符串转换: {str_e2e}")
    print(f"原始值: {str_e2e.get_value()}")
    print(f"原始类型: {str_e2e.get_original_type().__name__}")
    print()
    
    # 转换数字
    int_e2e = to_e2e(42)
    print(f"整数转换: {int_e2e}")
    print(f"原始值: {int_e2e.get_value()}")
    print(f"原始类型: {int_e2e.get_original_type().__name__}")
    print()
    
    float_e2e = to_e2e(3.14)
    print(f"浮点数转换: {float_e2e}")
    print(f"原始值: {float_e2e.get_value()}")
    print(f"原始类型: {float_e2e.get_original_type().__name__}")
    print()
    
    # 转换列表
    list_e2e = to_e2e([1, 2, 3, 4, 5])
    print(f"列表转换: {list_e2e}")
    print(f"原始值: {list_e2e.get_value()}")
    print(f"原始类型: {list_e2e.get_original_type().__name__}")
    print()
    
    # 转换字典
    dict_e2e = to_e2e({"name": "Alice", "age": 30})
    print(f"字典转换: {dict_e2e}")
    print(f"原始值: {dict_e2e.get_value()}")
    print(f"原始类型: {dict_e2e.get_original_type().__name__}")
    print()
    
    # 转换布尔值
    bool_e2e = to_e2e(True)
    print(f"布尔值转换: {bool_e2e}")
    print(f"原始值: {bool_e2e.get_value()}")
    print(f"原始类型: {bool_e2e.get_original_type().__name__}")
    print()
    
    # 转换None
    none_e2e = to_e2e(None)
    print(f"None转换: {none_e2e}")
    print(f"原始值: {none_e2e.get_value()}")
    print(f"原始类型: {type(none_e2e.get_value()).__name__}")
    print()
    
    # 新功能演示
    print("=== 新功能演示 ===")
    print()
    
    # 转换回原始类型
    print("1. 转换回原始类型:")
    original_str = str_e2e.to_original()
    print(f"   从E2EType转回字符串: {original_str}")
    print(f"   类型: {type(original_str).__name__}")
    
    original_list = list_e2e.to_original()
    print(f"   从E2EType转回列表: {original_list}")
    print(f"   类型: {type(original_list).__name__}")
    print()
    
    # 使用from_e2e函数
    print("2. 使用from_e2e函数:")
    from_e2e_str = from_e2e(str_e2e)
    print(f"   from_e2e转换: {from_e2e_str}")
    print(f"   类型: {type(from_e2e_str).__name__}")
    
    # 非E2EType对象传入from_e2e
    normal_value = from_e2e("普通值")
    print(f"   普通值传入from_e2e: {normal_value}")
    print(f"   类型: {type(normal_value).__name__}")
    print()
    
    # 检查类型
    print("3. 检查类型:")
    print(f"   str_e2e是否为字符串: {str_e2e.is_type(str)}")
    print(f"   int_e2e是否为整数: {int_e2e.is_type(int)}")
    print(f"   list_e2e是否为字典: {list_e2e.is_type(dict)}")
    print()
    
    # 序列化
    print("4. 序列化:")
    print(f"   字符串序列化: {str_e2e.serialize()}")
    print(f"   字典序列化: {dict_e2e.serialize()}")
    print(f"   列表序列化: {list_e2e.serialize()}")
    print()
    
    # 时间戳
    print("5. 时间戳:")
    print(f"   字符串转换时间戳: {str_e2e.get_timestamp()}")
    print(f"   列表转换时间戳: {list_e2e.get_timestamp()}")
    print()
