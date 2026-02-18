"""核心类型转换实现

This module contains the core implementation of the type conversion compatibility layer,
including support for standard Python types and third-party library types.
"""

import builtins
import sys

# 保存原始内置转换函数
original_list = builtins.list
original_str = builtins.str
original_int = builtins.int
original_float = builtins.float
original_dict = builtins.dict
original_set = builtins.set
original_tuple = builtins.tuple

class TypeConverter:
    """类型转换兼容层
    
    A comprehensive type conversion compatibility layer that supports bidirectional
    conversion between all standard Python data types and third-party library types.
    """
    
    # 第三方库类型检测缓存
    _numpy_available = None
    _cupy_available = None
    _scipy_available = None
    _pandas_available = None
    _torch_available = None
    _xarray_available = None
    _jax_available = None
    _tensorflow_available = None
    
    # 第三方库互转方法
    @staticmethod
    def numpy_to_xarray(obj):
        """将numpy数组转换为xarray DataArray
        
        Convert numpy array to xarray DataArray with automatically generated dimensions and coordinates.
        
        Args:
            obj: numpy.ndarray - 要转换的numpy数组
            
        Returns:
            xarray.DataArray - 转换后的xarray DataArray
            
        Raises:
            TypeError: 如果输入不是numpy数组
        """
        if not TypeConverter._is_numpy_array(obj):
            raise TypeError(f"Expected numpy.ndarray, got {type(obj).__name__}")
        
        import numpy as np
        import xarray as xr
        
        # 创建维度名称
        dims = [f'dim{i}' for i in range(obj.ndim)]
        
        # 创建坐标
        coords = {}
        for i, size in enumerate(obj.shape):
            coords[dims[i]] = np.arange(size)
        
        return xr.DataArray(obj, dims=dims, coords=coords)
    
    @staticmethod
    def xarray_to_numpy(obj):
        """将xarray DataArray转换为numpy数组
        
        Convert xarray DataArray or Dataset to numpy array.
        
        Args:
            obj: xarray.DataArray or xarray.Dataset - 要转换的xarray对象
            
        Returns:
            numpy.ndarray - 转换后的numpy数组
            
        Raises:
            TypeError: 如果输入不是xarray对象
            ValueError: 如果输入是空的xarray Dataset
        """
        if not (TypeConverter._is_xarray_dataarray(obj) or TypeConverter._is_xarray_dataset(obj)):
            raise TypeError(f"Expected xarray.DataArray or xarray.Dataset, got {type(obj).__name__}")
        
        if TypeConverter._is_xarray_dataarray(obj):
            return obj.values
        elif TypeConverter._is_xarray_dataset(obj):
            # 对于Dataset，返回第一个变量的values
            if obj.data_vars:
                return next(iter(obj.data_vars.values())).values
            raise ValueError("Empty xarray Dataset")
    
    @staticmethod
    def torch_to_numpy(obj):
        """将torch Tensor转换为numpy数组
        
        Convert torch Tensor to numpy array, detaching from computation graph if necessary.
        
        Args:
            obj: torch.Tensor - 要转换的torch张量
            
        Returns:
            numpy.ndarray - 转换后的numpy数组
            
        Raises:
            TypeError: 如果输入不是torch张量
        """
        if not TypeConverter._is_torch_tensor(obj):
            raise TypeError(f"Expected torch.Tensor, got {type(obj).__name__}")
        
        return obj.detach().cpu().numpy()
    
    @staticmethod
    def numpy_to_torch(obj):
        """将numpy数组转换为torch Tensor
        
        Convert numpy array to torch Tensor.
        
        Args:
            obj: numpy.ndarray - 要转换的numpy数组
            
        Returns:
            torch.Tensor - 转换后的torch张量
            
        Raises:
            TypeError: 如果输入不是numpy数组
        """
        if not TypeConverter._is_numpy_array(obj):
            raise TypeError(f"Expected numpy.ndarray, got {type(obj).__name__}")
        
        import torch
        return torch.tensor(obj)
    
    @staticmethod
    def jax_to_numpy(obj):
        """将jax数组转换为numpy数组
        
        Convert jax array to numpy array.
        
        Args:
            obj: jax.numpy.ndarray - 要转换的jax数组
            
        Returns:
            numpy.ndarray - 转换后的numpy数组
            
        Raises:
            TypeError: 如果输入不是jax数组
        """
        if not TypeConverter._is_jax_array(obj):
            raise TypeError(f"Expected jax.numpy.ndarray, got {type(obj).__name__}")
        
        import jax.numpy as jnp
        return obj.__array__()
    
    @staticmethod
    def numpy_to_jax(obj):
        """将numpy数组转换为jax数组
        
        Convert numpy array to jax array.
        
        Args:
            obj: numpy.ndarray - 要转换的numpy数组
            
        Returns:
            jax.numpy.ndarray - 转换后的jax数组
            
        Raises:
            TypeError: 如果输入不是numpy数组
        """
        if not TypeConverter._is_numpy_array(obj):
            raise TypeError(f"Expected numpy.ndarray, got {type(obj).__name__}")
        
        import jax.numpy as jnp
        return jnp.array(obj)
    
    @staticmethod
    def tensorflow_to_numpy(obj):
        """将tensorflow Tensor转换为numpy数组
        
        Convert tensorflow Tensor to numpy array.
        
        Args:
            obj: tensorflow.Tensor - 要转换的tensorflow张量
            
        Returns:
            numpy.ndarray - 转换后的numpy数组
            
        Raises:
            TypeError: 如果输入不是tensorflow张量
        """
        if not TypeConverter._is_tensorflow_tensor(obj):
            raise TypeError(f"Expected tensorflow.Tensor, got {type(obj).__name__}")
        
        return obj.numpy()
    
    @staticmethod
    def numpy_to_tensorflow(obj):
        """将numpy数组转换为tensorflow Tensor
        
        Convert numpy array to tensorflow Tensor.
        
        Args:
            obj: numpy.ndarray - 要转换的numpy数组
            
        Returns:
            tensorflow.Tensor - 转换后的tensorflow张量
            
        Raises:
            TypeError: 如果输入不是numpy数组
        """
        if not TypeConverter._is_numpy_array(obj):
            raise TypeError(f"Expected numpy.ndarray, got {type(obj).__name__}")
        
        import tensorflow as tf
        return tf.constant(obj)
    
    @staticmethod
    def pandas_to_numpy(obj):
        """将pandas对象转换为numpy数组
        
        Convert pandas DataFrame or Series to numpy array.
        
        Args:
            obj: pandas.DataFrame or pandas.Series - 要转换的pandas对象
            
        Returns:
            numpy.ndarray - 转换后的numpy数组
            
        Raises:
            TypeError: 如果输入不是pandas对象
        """
        if not (TypeConverter._is_pandas_dataframe(obj) or TypeConverter._is_pandas_series(obj)):
            raise TypeError(f"Expected pandas.DataFrame or pandas.Series, got {type(obj).__name__}")
        
        return obj.values
    
    @staticmethod
    def numpy_to_pandas(obj):
        """将numpy数组转换为pandas对象
        
        Convert numpy array to pandas Series or DataFrame.
        
        Args:
            obj: numpy.ndarray - 要转换的numpy数组
            
        Returns:
            pandas.Series or pandas.DataFrame - 转换后的pandas对象
            
        Raises:
            TypeError: 如果输入不是numpy数组
            ValueError: 如果输入数组维度大于2
        """
        if not TypeConverter._is_numpy_array(obj):
            raise TypeError(f"Expected numpy.ndarray, got {type(obj).__name__}")
        
        import pandas as pd
        
        if obj.ndim == 1:
            return pd.Series(obj)
        elif obj.ndim == 2:
            # 创建列名
            columns = [f'col{i}' for i in range(obj.shape[1])]
            return pd.DataFrame(obj, columns=columns)
        else:
            raise ValueError(f"Cannot convert {obj.ndim}-dimensional numpy array to pandas object")
    
    @staticmethod
    def convert(obj, target_type):
        """通用类型转换方法，支持第三方库类型之间的互转
        
        Generic type conversion method that supports conversion between third-party library types.
        
        Args:
            obj: 要转换的对象
            target_type: 目标类型，可以是以下字符串之一：
                'numpy', 'cupy', 'scipy', 'pandas', 'torch', 'xarray', 'jax', 'tensorflow'
        
        Returns:
            转换后的对象
            
        Raises:
            ValueError: 如果目标类型无效
            TypeError: 如果无法转换输入对象
        """
        # 检查目标类型
        valid_targets = ['numpy', 'cupy', 'scipy', 'pandas', 'torch', 'xarray', 'jax', 'tensorflow']
        if target_type not in valid_targets:
            raise ValueError(f"Invalid target_type: {target_type}. Must be one of {valid_targets}")
        
        # 转换为numpy数组作为中间格式
        if TypeConverter._is_numpy_array(obj):
            numpy_obj = obj
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            numpy_obj = cupy.asnumpy(obj)
        elif TypeConverter._is_scipy_sparse(obj):
            numpy_obj = obj.toarray()
        elif TypeConverter._is_pandas_dataframe(obj) or TypeConverter._is_pandas_series(obj):
            numpy_obj = obj.values
        elif TypeConverter._is_torch_tensor(obj):
            numpy_obj = obj.detach().cpu().numpy()
        elif TypeConverter._is_xarray_dataarray(obj):
            numpy_obj = obj.values
        elif TypeConverter._is_xarray_dataset(obj):
            if obj.data_vars:
                numpy_obj = next(iter(obj.data_vars.values())).values
            else:
                raise ValueError("Empty xarray Dataset")
        elif TypeConverter._is_jax_array(obj):
            numpy_obj = obj.__array__()
        elif TypeConverter._is_tensorflow_tensor(obj):
            numpy_obj = obj.numpy()
        else:
            # 尝试直接转换为numpy数组
            try:
                import numpy as np
                numpy_obj = np.array(obj)
            except Exception as e:
                raise TypeError(f"Cannot convert {type(obj).__name__} to numpy array: {e}")
        
        # 从numpy数组转换为目标类型
        if target_type == 'numpy':
            return numpy_obj
        elif target_type == 'cupy':
            import cupy
            return cupy.array(numpy_obj)
        elif target_type == 'scipy':
            import scipy.sparse
            return scipy.sparse.csr_matrix(numpy_obj)
        elif target_type == 'pandas':
            return TypeConverter.numpy_to_pandas(numpy_obj)
        elif target_type == 'torch':
            import torch
            return torch.tensor(numpy_obj)
        elif target_type == 'xarray':
            return TypeConverter.numpy_to_xarray(numpy_obj)
        elif target_type == 'jax':
            import jax.numpy as jnp
            return jnp.array(numpy_obj)
        elif target_type == 'tensorflow':
            import tensorflow as tf
            return tf.constant(numpy_obj)
    
    @classmethod
    def _is_numpy_array(cls, obj):
        """检测是否为numpy数组
        
        Check if the object is a numpy array.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是numpy数组返回True，否则返回False
        """
        if cls._numpy_available is None:
            try:
                import numpy
                cls._numpy_available = True
                return isinstance(obj, numpy.ndarray)
            except ImportError:
                cls._numpy_available = False
                return False
        elif cls._numpy_available:
            import numpy
            return isinstance(obj, numpy.ndarray)
        return False
    
    @classmethod
    def _is_cupy_array(cls, obj):
        """检测是否为cupy数组
        
        Check if the object is a cupy array.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是cupy数组返回True，否则返回False
        """
        if cls._cupy_available is None:
            try:
                import cupy
                cls._cupy_available = True
                return isinstance(obj, cupy.ndarray)
            except ImportError:
                cls._cupy_available = False
                return False
        elif cls._cupy_available:
            import cupy
            return isinstance(obj, cupy.ndarray)
        return False
    
    @classmethod
    def _is_scipy_sparse(cls, obj):
        """检测是否为scipy稀疏矩阵
        
        Check if the object is a scipy sparse matrix.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是scipy稀疏矩阵返回True，否则返回False
        """
        if cls._scipy_available is None:
            try:
                import scipy.sparse
                cls._scipy_available = True
                return scipy.sparse.issparse(obj)
            except ImportError:
                cls._scipy_available = False
                return False
        elif cls._scipy_available:
            import scipy.sparse
            return scipy.sparse.issparse(obj)
        return False
    
    @classmethod
    def _is_pandas_dataframe(cls, obj):
        """检测是否为pandas DataFrame
        
        Check if the object is a pandas DataFrame.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是pandas DataFrame返回True，否则返回False
        """
        if cls._pandas_available is None:
            try:
                import pandas
                cls._pandas_available = True
                return isinstance(obj, pandas.DataFrame)
            except ImportError:
                cls._pandas_available = False
                return False
        elif cls._pandas_available:
            import pandas
            return isinstance(obj, pandas.DataFrame)
        return False
    
    @classmethod
    def _is_pandas_series(cls, obj):
        """检测是否为pandas Series
        
        Check if the object is a pandas Series.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是pandas Series返回True，否则返回False
        """
        if cls._pandas_available is None:
            try:
                import pandas
                cls._pandas_available = True
                return isinstance(obj, pandas.Series)
            except ImportError:
                cls._pandas_available = False
                return False
        elif cls._pandas_available:
            import pandas
            return isinstance(obj, pandas.Series)
        return False
    
    @classmethod
    def _is_torch_tensor(cls, obj):
        """检测是否为torch Tensor
        
        Check if the object is a torch Tensor.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是torch Tensor返回True，否则返回False
        """
        if cls._torch_available is None:
            try:
                import torch
                cls._torch_available = True
                return isinstance(obj, torch.Tensor)
            except ImportError:
                cls._torch_available = False
                return False
        elif cls._torch_available:
            import torch
            return isinstance(obj, torch.Tensor)
        return False
    
    @classmethod
    def _is_xarray_dataarray(cls, obj):
        """检测是否为xarray DataArray
        
        Check if the object is an xarray DataArray.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是xarray DataArray返回True，否则返回False
        """
        if cls._xarray_available is None:
            try:
                import xarray
                cls._xarray_available = True
                return isinstance(obj, xarray.DataArray)
            except ImportError:
                cls._xarray_available = False
                return False
        elif cls._xarray_available:
            import xarray
            return isinstance(obj, xarray.DataArray)
        return False
    
    @classmethod
    def _is_xarray_dataset(cls, obj):
        """检测是否为xarray Dataset
        
        Check if the object is an xarray Dataset.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是xarray Dataset返回True，否则返回False
        """
        if cls._xarray_available is None:
            try:
                import xarray
                cls._xarray_available = True
                return isinstance(obj, xarray.Dataset)
            except ImportError:
                cls._xarray_available = False
                return False
        elif cls._xarray_available:
            import xarray
            return isinstance(obj, xarray.Dataset)
        return False
    
    @classmethod
    def _is_jax_array(cls, obj):
        """检测是否为jax Array
        
        Check if the object is a jax array.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是jax array返回True，否则返回False
        """
        if cls._jax_available is None:
            try:
                import jax.numpy
                cls._jax_available = True
                return isinstance(obj, jax.numpy.ndarray)
            except ImportError:
                cls._jax_available = False
                return False
        elif cls._jax_available:
            import jax.numpy
            return isinstance(obj, jax.numpy.ndarray)
        return False
    
    @classmethod
    def _is_tensorflow_tensor(cls, obj):
        """检测是否为tensorflow Tensor
        
        Check if the object is a tensorflow Tensor.
        
        Args:
            obj: 要检测的对象
            
        Returns:
            bool: 如果是tensorflow Tensor返回True，否则返回False
        """
        if cls._tensorflow_available is None:
            try:
                import tensorflow
                cls._tensorflow_available = True
                return isinstance(obj, tensorflow.Tensor)
            except ImportError:
                cls._tensorflow_available = False
                return False
        elif cls._tensorflow_available:
            import tensorflow
            return isinstance(obj, tensorflow.Tensor)
        return False
    
    @staticmethod
    def to_list(obj):
        """转换为list
        
        Convert object to list.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            list: 转换后的列表
            
        Raises:
            TypeError: 如果无法转换为列表
        """
        if isinstance(obj, list):
            return obj
        elif obj is None:
            return []
        elif isinstance(obj, (str, bytes)):
            return list(obj)
        elif isinstance(obj, dict):
            return list(obj.items())
        elif isinstance(obj, (int, float, bool)):
            return [obj]
        elif isinstance(obj, (tuple, set)):
            return list(obj)
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            result = obj.tolist()
            # 处理0维数组（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            result = cupy.asnumpy(obj).tolist()
            # 处理0维数组（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_scipy_sparse(obj):
            import numpy
            result = obj.toarray().tolist()
            # 处理0维数组（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_pandas_dataframe(obj):
            # 转换为嵌套列表，包含列名
            return [obj.columns.tolist()] + obj.values.tolist()
        elif TypeConverter._is_pandas_series(obj):
            # 转换为值列表
            return obj.tolist()
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            result = obj.tolist()
            # 处理0维张量（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_xarray_dataarray(obj):
            result = obj.values.tolist()
            # 处理0维数组（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_xarray_dataset(obj):
            # 转换为包含所有变量的字典列表
            return [{var: obj[var].values.tolist() for var in obj.data_vars}]
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            result = obj.tolist()
            # 处理0维数组（标量）
            if not isinstance(result, list):
                return [result]
            return result
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            result = obj.numpy().tolist()
            # 处理0维张量（标量）
            if not isinstance(result, list):
                return [result]
            return result
        else:
            try:
                return original_list(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to list")
    
    @staticmethod
    def to_str(obj):
        """转换为str
        
        Convert object to string.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            str: 转换后的字符串
            
        Raises:
            TypeError: 如果无法转换为字符串
        """
        if isinstance(obj, str):
            return obj
        elif obj is None:
            return ""
        elif isinstance(obj, bool):
            return str(obj).lower()
        elif isinstance(obj, (int, float, list, tuple, dict, set)):
            return original_str(obj)
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            return str(obj.tolist())
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            return str(cupy.asnumpy(obj).tolist())
        elif TypeConverter._is_scipy_sparse(obj):
            import numpy
            return str(obj.toarray().tolist())
        elif TypeConverter._is_pandas_dataframe(obj):
            return str(obj.to_dict('list'))
        elif TypeConverter._is_pandas_series(obj):
            return str(obj.to_list())
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            return str(obj.tolist())
        elif TypeConverter._is_xarray_dataarray(obj):
            return str(obj.values.tolist())
        elif TypeConverter._is_xarray_dataset(obj):
            return str({var: obj[var].values.tolist() for var in obj.data_vars})
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            return str(obj.tolist())
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            return str(obj.numpy().tolist())
        else:
            try:
                return original_str(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to str")
    
    @staticmethod
    def to_int(obj):
        """转换为int
        
        Convert object to integer.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            int: 转换后的整数
            
        Raises:
            TypeError: 如果无法转换为整数
            ValueError: 如果字符串无法转换为整数
        """
        if isinstance(obj, int):
            return obj
        elif obj is None:
            return 0
        elif isinstance(obj, bool):
            return int(obj)
        elif isinstance(obj, float):
            return int(obj)
        elif isinstance(obj, str):
            try:
                return int(obj.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{obj}' to int")
        elif isinstance(obj, (list, tuple, dict, set)):
            if len(obj) == 0:
                return 0
            elif len(obj) == 1:
                try:
                    if isinstance(obj, set):
                        return TypeConverter.to_int(next(iter(obj)))
                    return TypeConverter.to_int(obj[0])
                except (TypeError, ValueError):
                    raise TypeError(f"Cannot convert {type(obj).__name__} to int")
            else:
                raise TypeError(f"Cannot convert {type(obj).__name__} with length > 1 to int")
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            if obj.size == 1:
                return int(obj.item())
            else:
                raise TypeError(f"Cannot convert numpy array with size > 1 to int")
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            if obj.size == 1:
                return int(cupy.asnumpy(obj).item())
            else:
                raise TypeError(f"Cannot convert cupy array with size > 1 to int")
        elif TypeConverter._is_scipy_sparse(obj):
            if obj.size == 1:
                return int(obj.toarray().item())
            else:
                raise TypeError(f"Cannot convert scipy sparse matrix with size > 1 to int")
        elif TypeConverter._is_pandas_dataframe(obj):
            if obj.size == 1:
                return int(obj.iloc[0, 0])
            else:
                raise TypeError(f"Cannot convert pandas DataFrame with size > 1 to int")
        elif TypeConverter._is_pandas_series(obj):
            if len(obj) == 1:
                return int(obj.iloc[0])
            else:
                raise TypeError(f"Cannot convert pandas Series with length > 1 to int")
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            if obj.numel() == 1:
                return int(obj.item())
            else:
                raise TypeError(f"Cannot convert torch Tensor with size > 1 to int")
        elif TypeConverter._is_xarray_dataarray(obj):
            if obj.size == 1:
                return int(obj.item())
            else:
                raise TypeError(f"Cannot convert xarray DataArray with size > 1 to int")
        elif TypeConverter._is_xarray_dataset(obj):
            raise TypeError(f"Cannot convert xarray Dataset to int")
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            if obj.size == 1:
                return int(obj.item())
            else:
                raise TypeError(f"Cannot convert jax array with size > 1 to int")
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            if obj.shape == ():
                return int(obj.numpy())
            else:
                raise TypeError(f"Cannot convert tensorflow Tensor with size > 1 to int")
        else:
            try:
                return original_int(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to int")
    
    @staticmethod
    def to_float(obj):
        """转换为float
        
        Convert object to float.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            float: 转换后的浮点数
            
        Raises:
            TypeError: 如果无法转换为浮点数
            ValueError: 如果字符串无法转换为浮点数
        """
        if isinstance(obj, float):
            return obj
        elif obj is None:
            return 0.0
        elif isinstance(obj, bool):
            return float(obj)
        elif isinstance(obj, int):
            return float(obj)
        elif isinstance(obj, str):
            try:
                return float(obj.strip())
            except ValueError:
                raise ValueError(f"Cannot convert '{obj}' to float")
        elif isinstance(obj, (list, tuple, dict, set)):
            if len(obj) == 0:
                return 0.0
            elif len(obj) == 1:
                try:
                    if isinstance(obj, set):
                        return TypeConverter.to_float(next(iter(obj)))
                    return TypeConverter.to_float(obj[0])
                except (TypeError, ValueError):
                    raise TypeError(f"Cannot convert {type(obj).__name__} to float")
            else:
                raise TypeError(f"Cannot convert {type(obj).__name__} with length > 1 to float")
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            if obj.size == 1:
                return float(obj.item())
            else:
                raise TypeError(f"Cannot convert numpy array with size > 1 to float")
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            if obj.size == 1:
                return float(cupy.asnumpy(obj).item())
            else:
                raise TypeError(f"Cannot convert cupy array with size > 1 to float")
        elif TypeConverter._is_scipy_sparse(obj):
            if obj.size == 1:
                return float(obj.toarray().item())
            else:
                raise TypeError(f"Cannot convert scipy sparse matrix with size > 1 to float")
        elif TypeConverter._is_pandas_dataframe(obj):
            if obj.size == 1:
                return float(obj.iloc[0, 0])
            else:
                raise TypeError(f"Cannot convert pandas DataFrame with size > 1 to float")
        elif TypeConverter._is_pandas_series(obj):
            if len(obj) == 1:
                return float(obj.iloc[0])
            else:
                raise TypeError(f"Cannot convert pandas Series with length > 1 to float")
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            if obj.numel() == 1:
                return float(obj.item())
            else:
                raise TypeError(f"Cannot convert torch Tensor with size > 1 to float")
        elif TypeConverter._is_xarray_dataarray(obj):
            if obj.size == 1:
                return float(obj.item())
            else:
                raise TypeError(f"Cannot convert xarray DataArray with size > 1 to float")
        elif TypeConverter._is_xarray_dataset(obj):
            raise TypeError(f"Cannot convert xarray Dataset to float")
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            if obj.size == 1:
                return float(obj.item())
            else:
                raise TypeError(f"Cannot convert jax array with size > 1 to float")
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            if obj.shape == ():
                return float(obj.numpy())
            else:
                raise TypeError(f"Cannot convert tensorflow Tensor with size > 1 to float")
        else:
            try:
                return original_float(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to float")
    
    @staticmethod
    def to_dict(obj):
        """转换为dict
        
        Convert object to dictionary.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            dict: 转换后的字典
            
        Raises:
            TypeError: 如果无法转换为字典
        """
        if isinstance(obj, dict):
            return obj
        elif obj is None:
            return {}
        elif isinstance(obj, (list, tuple)):
            try:
                return dict(obj)
            except (ValueError, TypeError):
                # 如果是简单列表，转换为索引字典
                return {i: v for i, v in enumerate(obj)}
        elif isinstance(obj, (str, int, float, bool, set)):
            return {"value": obj}
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            if obj.ndim == 1:
                return {i: v for i, v in enumerate(obj.tolist())}
            else:
                return {"shape": obj.shape, "dtype": str(obj.dtype), "data": obj.tolist()}
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            if obj.ndim == 1:
                return {i: v for i, v in enumerate(cupy.asnumpy(obj).tolist())}
            else:
                return {"shape": obj.shape, "dtype": str(obj.dtype), "data": cupy.asnumpy(obj).tolist()}
        elif TypeConverter._is_scipy_sparse(obj):
            import numpy
            array = obj.toarray()
            if array.ndim == 1:
                return {i: v for i, v in enumerate(array.tolist())}
            else:
                return {"shape": array.shape, "dtype": str(array.dtype), "data": array.tolist()}
        elif TypeConverter._is_pandas_dataframe(obj):
            return obj.to_dict('list')
        elif TypeConverter._is_pandas_series(obj):
            return obj.to_dict()
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            if obj.ndim == 1:
                return {i: v for i, v in enumerate(obj.tolist())}
            else:
                return {"shape": tuple(obj.shape), "data": obj.tolist()}
        elif TypeConverter._is_xarray_dataarray(obj):
            return {
                "shape": obj.shape,
                "dtype": str(obj.dtype),
                "data": obj.values.tolist(),
                "dims": obj.dims,
                "coords": {dim: obj.coords[dim].values.tolist() for dim in obj.dims}
            }
        elif TypeConverter._is_xarray_dataset(obj):
            return {
                var: {
                    "shape": obj[var].shape,
                    "dtype": str(obj[var].dtype),
                    "data": obj[var].values.tolist()
                }
                for var in obj.data_vars
            }
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            if obj.ndim == 1:
                return {i: v for i, v in enumerate(obj.tolist())}
            else:
                return {"shape": obj.shape, "dtype": str(obj.dtype), "data": obj.tolist()}
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            if len(obj.shape) == 1:
                return {i: v for i, v in enumerate(obj.numpy().tolist())}
            else:
                return {"shape": tuple(obj.shape), "data": obj.numpy().tolist()}
        else:
            try:
                return original_dict(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to dict")
    
    @staticmethod
    def to_set(obj):
        """转换为set
        
        Convert object to set.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            set: 转换后的集合
            
        Raises:
            TypeError: 如果无法转换为集合
        """
        if isinstance(obj, set):
            return obj
        elif obj is None:
            return set()
        elif isinstance(obj, (str, bytes)):
            return set(obj)
        elif isinstance(obj, (int, float, bool)):
            return {obj}
        elif isinstance(obj, (list, tuple, dict)):
            return set(obj)
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            if obj.ndim == 1:
                return set(obj.tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional numpy array to set")
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            if obj.ndim == 1:
                return set(cupy.asnumpy(obj).tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional cupy array to set")
        elif TypeConverter._is_scipy_sparse(obj):
            import numpy
            array = obj.toarray()
            if array.ndim == 1:
                return set(array.tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional scipy sparse matrix to set")
        elif TypeConverter._is_pandas_dataframe(obj):
            raise TypeError(f"Cannot convert pandas DataFrame to set")
        elif TypeConverter._is_pandas_series(obj):
            return set(obj.tolist())
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            if obj.ndim == 1:
                return set(obj.tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional torch Tensor to set")
        elif TypeConverter._is_xarray_dataarray(obj):
            if obj.ndim == 1:
                return set(obj.values.tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional xarray DataArray to set")
        elif TypeConverter._is_xarray_dataset(obj):
            raise TypeError(f"Cannot convert xarray Dataset to set")
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            if obj.ndim == 1:
                return set(obj.tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional jax array to set")
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            if len(obj.shape) == 1:
                return set(obj.numpy().tolist())
            else:
                raise TypeError(f"Cannot convert multi-dimensional tensorflow Tensor to set")
        else:
            try:
                return original_set(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to set")
    
    @staticmethod
    def to_tuple(obj):
        """转换为tuple
        
        Convert object to tuple.
        
        Args:
            obj: 要转换的对象
            
        Returns:
            tuple: 转换后的元组
            
        Raises:
            TypeError: 如果无法转换为元组
        """
        if isinstance(obj, tuple):
            return obj
        elif obj is None:
            return ()
        elif isinstance(obj, (str, bytes)):
            return tuple(obj)
        elif isinstance(obj, (int, float, bool)):
            return (obj,)
        elif isinstance(obj, (list, set, dict)):
            return tuple(obj)
        elif TypeConverter._is_numpy_array(obj):
            import numpy
            if obj.ndim == 1:
                return tuple(obj.tolist())
            else:
                return tuple(map(tuple, obj.tolist()))
        elif TypeConverter._is_cupy_array(obj):
            import cupy
            if obj.ndim == 1:
                return tuple(cupy.asnumpy(obj).tolist())
            else:
                return tuple(map(tuple, cupy.asnumpy(obj).tolist()))
        elif TypeConverter._is_scipy_sparse(obj):
            import numpy
            array = obj.toarray()
            if array.ndim == 1:
                return tuple(array.tolist())
            else:
                return tuple(map(tuple, array.tolist()))
        elif TypeConverter._is_pandas_dataframe(obj):
            # 转换为包含列名和数据的嵌套元组
            return (tuple(obj.columns.tolist()),) + tuple(tuple(row) for row in obj.values.tolist())
        elif TypeConverter._is_pandas_series(obj):
            return tuple(obj.tolist())
        elif TypeConverter._is_torch_tensor(obj):
            import torch
            if obj.ndim == 1:
                return tuple(obj.tolist())
            else:
                return tuple(map(tuple, obj.tolist()))
        elif TypeConverter._is_xarray_dataarray(obj):
            if obj.ndim == 1:
                return tuple(obj.values.tolist())
            else:
                return tuple(map(tuple, obj.values.tolist()))
        elif TypeConverter._is_xarray_dataset(obj):
            # 转换为包含所有变量的字典元组
            return (tuple({var: obj[var].values.tolist() for var in obj.data_vars}),)
        elif TypeConverter._is_jax_array(obj):
            import jax.numpy as jnp
            if obj.ndim == 1:
                return tuple(obj.tolist())
            else:
                return tuple(map(tuple, obj.tolist()))
        elif TypeConverter._is_tensorflow_tensor(obj):
            import tensorflow as tf
            if len(obj.shape) == 1:
                return tuple(obj.numpy().tolist())
            else:
                return tuple(map(tuple, obj.numpy().tolist()))
        else:
            try:
                return original_tuple(obj)
            except (TypeError, ValueError):
                raise TypeError(f"Cannot convert {type(obj).__name__} to tuple")

# 重写内置转换函数
def e2e_list(obj=None):
    """转换为list
    
    Convert object to list, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为None
        
    Returns:
        list: 转换后的列表
    """
    if obj is None:
        return []
    return TypeConverter.to_list(obj)

def e2e_str(obj=""):
    """转换为str
    
    Convert object to string, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为空字符串
        
    Returns:
        str: 转换后的字符串
    """
    return TypeConverter.to_str(obj)

def e2e_int(obj=0):
    """转换为int
    
    Convert object to integer, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为0
        
    Returns:
        int: 转换后的整数
    """
    return TypeConverter.to_int(obj)

def e2e_float(obj=0.0):
    """转换为float
    
    Convert object to float, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为0.0
        
    Returns:
        float: 转换后的浮点数
    """
    return TypeConverter.to_float(obj)

def e2e_dict(obj=None):
    """转换为dict
    
    Convert object to dictionary, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为None
        
    Returns:
        dict: 转换后的字典
    """
    if obj is None:
        return {}
    return TypeConverter.to_dict(obj)

def e2e_set(obj=None):
    """转换为set
    
    Convert object to set, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为None
        
    Returns:
        set: 转换后的集合
    """
    if obj is None:
        return set()
    return TypeConverter.to_set(obj)

def e2e_tuple(obj=()):
    """转换为tuple
    
    Convert object to tuple, with support for all standard types and third-party library types.
    
    Args:
        obj: 要转换的对象，默认为空元组
        
    Returns:
        tuple: 转换后的元组
    """
    return TypeConverter.to_tuple(obj)
