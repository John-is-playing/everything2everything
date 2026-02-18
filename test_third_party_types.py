import unittest
import sys

# 导入类型转换兼容层
sys.path.append('c:\\Users\\Potato\\Documents\\trae_projects\\everything2everything')
from e2e_type_converter import (
    TypeConverter, e2e_list, e2e_str, e2e_int, e2e_float, e2e_dict, e2e_set, e2e_tuple
)

class TestThirdPartyTypes(unittest.TestCase):
    """测试第三方库类型转换"""
    
    def setUp(self):
        """设置测试环境"""
        # 检测第三方库是否可用
        self.numpy_available = False
        self.cupy_available = False
        self.scipy_available = False
        
        try:
            import numpy
            self.numpy_available = True
            self.numpy = numpy
        except ImportError:
            pass
        
        try:
            import cupy
            self.cupy_available = True
            self.cupy = cupy

        except ImportError:
            pass
        
        try:
            import scipy.sparse
            self.scipy_available = True
            self.scipy = scipy
        except ImportError:
            pass
    
    def test_numpy_array_conversion(self):
        """测试numpy数组转换"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed")
        
        # 创建numpy数组
        arr_1d = self.numpy.array([1, 2, 3, 4, 5])
        arr_2d = self.numpy.array([[1, 2, 3], [4, 5, 6]])
        arr_scalar = self.numpy.array(42)
        
        # 测试转换为list
        self.assertEqual(e2e_list(arr_1d), [1, 2, 3, 4, 5])
        self.assertEqual(e2e_list(arr_2d), [[1, 2, 3], [4, 5, 6]])
        self.assertEqual(e2e_list(arr_scalar), [42])
        
        # 测试转换为str
        self.assertIn("[1, 2, 3, 4, 5]", e2e_str(arr_1d))
        
        # 测试转换为int/float（仅标量）
        self.assertEqual(e2e_int(arr_scalar), 42)
        self.assertEqual(e2e_float(arr_scalar), 42.0)
        
        # 测试转换为dict
        dict_1d = e2e_dict(arr_1d)
        self.assertEqual(len(dict_1d), 5)
        self.assertEqual(dict_1d[0], 1)
        
        dict_2d = e2e_dict(arr_2d)
        self.assertIn("shape", dict_2d)
        self.assertIn("dtype", dict_2d)
        self.assertIn("data", dict_2d)
        
        # 测试转换为set（仅1D数组）
        self.assertEqual(e2e_set(arr_1d), {1, 2, 3, 4, 5})
        
        # 测试转换为tuple
        self.assertEqual(e2e_tuple(arr_1d), (1, 2, 3, 4, 5))
        self.assertEqual(e2e_tuple(arr_2d), ((1, 2, 3), (4, 5, 6)))
    
    def test_cupy_array_conversion(self):
        """测试cupy数组转换"""
        # 暂时跳过CuPy测试以避免权限错误
        #self.skipTest("CuPy test skipped due to potential permission issues")
        
        if not self.cupy_available:
            self.skipTest("CuPy not installed")
        
        # 创建cupy数组
        arr_1d = self.cupy.array([1, 2, 3, 4, 5])
        arr_scalar = self.cupy.array(42)
        
        # 测试转换为list
        self.assertEqual(e2e_list(arr_1d), [1, 2, 3, 4, 5])
        self.assertEqual(e2e_list(arr_scalar), [42])
        
        # 测试转换为int/float（仅标量）
        self.assertEqual(e2e_int(arr_scalar), 42)
        self.assertEqual(e2e_float(arr_scalar), 42.0)
        
        # 测试转换为set（仅1D数组）
        self.assertEqual(e2e_set(arr_1d), {1, 2, 3, 4, 5})
        
        # 测试转换为tuple
        self.assertEqual(e2e_tuple(arr_1d), (1, 2, 3, 4, 5))
    
    def test_scipy_sparse_conversion(self):
        """测试scipy稀疏矩阵转换"""
        if not self.scipy_available:
            self.skipTest("SciPy not installed")
        
        # 创建稀疏矩阵
        sparse_mat = self.scipy.sparse.csr_matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        
        # 测试转换为list
        list_result = e2e_list(sparse_mat)
        self.assertEqual(len(list_result), 3)
        self.assertEqual(len(list_result[0]), 3)
        
        # 测试转换为dict
        dict_result = e2e_dict(sparse_mat)
        self.assertIn("shape", dict_result)
        self.assertIn("dtype", dict_result)
        self.assertIn("data", dict_result)
        
        # 测试转换为tuple
        tuple_result = e2e_tuple(sparse_mat)
        self.assertEqual(len(tuple_result), 3)
        self.assertEqual(len(tuple_result[0]), 3)
    
    def test_third_party_error_handling(self):
        """测试第三方库类型的错误处理"""
        if self.numpy_available:
            # 测试多维数组转换为set
            arr_2d = self.numpy.array([[1, 2], [3, 4]])
            with self.assertRaises(TypeError):
                e2e_set(arr_2d)
            
            # 测试多元素数组转换为int
            arr_1d = self.numpy.array([1, 2, 3])
            with self.assertRaises(TypeError):
                e2e_int(arr_1d)
    
    def test_pandas_types_conversion(self):
        """测试pandas类型转换"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed (required for pandas)")
        
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("Pandas not installed")
        
        # 创建pandas DataFrame
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 8, 9]
        })
        
        # 创建pandas Series
        series = pd.Series([1, 2, 3, 4, 5])
        
        # 测试DataFrame转换
        self.assertIsInstance(e2e_list(df), list)
        self.assertIsInstance(e2e_str(df), str)
        self.assertIsInstance(e2e_dict(df), dict)
        self.assertIsInstance(e2e_tuple(df), tuple)
        
        # 测试Series转换
        self.assertIsInstance(e2e_list(series), list)
        self.assertIsInstance(e2e_str(series), str)
        self.assertIsInstance(e2e_dict(series), dict)
        self.assertIsInstance(e2e_set(series), set)
        self.assertIsInstance(e2e_tuple(series), tuple)
    
    def test_torch_tensor_conversion(self):
        """测试torch Tensor转换"""
        try:
            import torch
        except ImportError:
            self.skipTest("PyTorch not installed")
        
        # 创建torch Tensor
        tensor_1d = torch.tensor([1, 2, 3, 4, 5])
        tensor_2d = torch.tensor([[1, 2, 3], [4, 5, 6]])
        tensor_scalar = torch.tensor(42)
        
        # 测试转换
        self.assertIsInstance(e2e_list(tensor_1d), list)
        self.assertIsInstance(e2e_str(tensor_1d), str)
        self.assertEqual(e2e_int(tensor_scalar), 42)
        self.assertEqual(e2e_float(tensor_scalar), 42.0)
        self.assertIsInstance(e2e_dict(tensor_1d), dict)
        self.assertIsInstance(e2e_set(tensor_1d), set)
        self.assertIsInstance(e2e_tuple(tensor_1d), tuple)
    
    def test_xarray_types_conversion(self):
        """测试xarray类型转换"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed (required for xarray)")
        
        try:
            import xarray as xr
        except ImportError:
            self.skipTest("xarray not installed")
        
        # 创建xarray DataArray
        da = xr.DataArray(
            [[1, 2, 3], [4, 5, 6]],
            dims=['y', 'x'],
            coords={'x': [1, 2, 3], 'y': [1, 2]}
        )
        
        # 创建xarray Dataset
        ds = xr.Dataset({
            'temp': (['y', 'x'], [[1, 2, 3], [4, 5, 6]]),
            'precip': (['y', 'x'], [[7, 8, 9], [10, 11, 12]])
        }, coords={'x': [1, 2, 3], 'y': [1, 2]})
        
        # 测试DataArray转换
        self.assertIsInstance(e2e_list(da), list)
        self.assertIsInstance(e2e_str(da), str)
        self.assertIsInstance(e2e_dict(da), dict)
        self.assertIsInstance(e2e_tuple(da), tuple)
        
        # 测试Dataset转换
        self.assertIsInstance(e2e_list(ds), list)
        self.assertIsInstance(e2e_str(ds), str)
        self.assertIsInstance(e2e_dict(ds), dict)
        self.assertIsInstance(e2e_tuple(ds), tuple)
    
    def test_jax_array_conversion(self):
        """测试jax数组转换"""
        try:
            import jax.numpy as jnp
        except ImportError:
            self.skipTest("JAX not installed")
        
        # 创建jax数组
        arr_1d = jnp.array([1, 2, 3, 4, 5])
        arr_2d = jnp.array([[1, 2, 3], [4, 5, 6]])
        arr_scalar = jnp.array(42)
        
        # 测试转换
        self.assertIsInstance(e2e_list(arr_1d), list)
        self.assertIsInstance(e2e_str(arr_1d), str)
        self.assertEqual(e2e_int(arr_scalar), 42)
        self.assertEqual(e2e_float(arr_scalar), 42.0)
        self.assertIsInstance(e2e_dict(arr_1d), dict)
        self.assertIsInstance(e2e_set(arr_1d), set)
        self.assertIsInstance(e2e_tuple(arr_1d), tuple)
    
    def test_tensorflow_tensor_conversion(self):
        """测试tensorflow Tensor转换"""
        try:
            import tensorflow as tf
        except ImportError:
            self.skipTest("TensorFlow not installed")
        
        # 创建tensorflow Tensor
        tensor_1d = tf.constant([1, 2, 3, 4, 5])
        tensor_2d = tf.constant([[1, 2, 3], [4, 5, 6]])
        tensor_scalar = tf.constant(42)
        
        # 测试转换
        self.assertIsInstance(e2e_list(tensor_1d), list)
        self.assertIsInstance(e2e_str(tensor_1d), str)
        self.assertEqual(e2e_int(tensor_scalar), 42)
        self.assertEqual(e2e_float(tensor_scalar), 42.0)
        self.assertIsInstance(e2e_dict(tensor_1d), dict)
        self.assertIsInstance(e2e_set(tensor_1d), set)
        self.assertIsInstance(e2e_tuple(tensor_1d), tuple)
    
    def test_numpy_to_xarray_conversion(self):
        """测试numpy数组到xarray DataArray的转换"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed")
        
        try:
            import xarray as xr
        except ImportError:
            self.skipTest("xarray not installed")
        
        # 创建numpy数组
        arr_1d = self.numpy.array([1, 2, 3, 4, 5])
        arr_2d = self.numpy.array([[1, 2, 3], [4, 5, 6]])
        
        # 测试直接转换方法
        da_1d = TypeConverter.numpy_to_xarray(arr_1d)
        self.assertIsInstance(da_1d, xr.DataArray)
        self.assertEqual(da_1d.ndim, 1)
        self.assertEqual(da_1d.shape, (5,))
        
        da_2d = TypeConverter.numpy_to_xarray(arr_2d)
        self.assertIsInstance(da_2d, xr.DataArray)
        self.assertEqual(da_2d.ndim, 2)
        self.assertEqual(da_2d.shape, (2, 3))
        
        # 测试xarray到numpy的转换
        numpy_arr = TypeConverter.xarray_to_numpy(da_1d)
        self.assertIsInstance(numpy_arr, self.numpy.ndarray)
        self.assertEqual(numpy_arr.shape, (5,))
    
    def test_generic_convert_method(self):
        """测试通用类型转换方法"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed")
        
        # 创建numpy数组作为测试对象
        arr = self.numpy.array([[1, 2, 3], [4, 5, 6]])
        
        # 测试转换为不同类型
        try:
            # 测试转换为pandas
            pandas_obj = TypeConverter.convert(arr, 'pandas')
            self.assertTrue(hasattr(pandas_obj, 'values'))
        except ImportError:
            pass  # pandas未安装，跳过
        
        try:
            # 测试转换为torch
            torch_tensor = TypeConverter.convert(arr, 'torch')
            self.assertTrue(hasattr(torch_tensor, 'shape'))
        except ImportError:
            pass  # torch未安装，跳过
        
        try:
            # 测试转换为xarray
            xarray_obj = TypeConverter.convert(arr, 'xarray')
            self.assertTrue(hasattr(xarray_obj, 'values'))
            self.assertTrue(hasattr(xarray_obj, 'dims'))
        except ImportError:
            pass  # xarray未安装，跳过
        
        try:
            # 测试转换为jax
            jax_array = TypeConverter.convert(arr, 'jax')
            self.assertTrue(hasattr(jax_array, 'shape'))
        except ImportError:
            pass  # jax未安装，跳过
        
        try:
            # 测试转换为tensorflow
            tf_tensor = TypeConverter.convert(arr, 'tensorflow')
            self.assertTrue(hasattr(tf_tensor, 'shape'))
        except ImportError:
            pass  # tensorflow未安装，跳过
    
    def test_cross_library_conversion(self):
        """测试跨库类型转换"""
        if not self.numpy_available:
            self.skipTest("NumPy not installed")
        
        # 创建numpy数组
        numpy_arr = self.numpy.array([1, 2, 3, 4, 5])
        
        # 测试numpy -> xarray -> numpy
        try:
            import xarray as xr
            xarray_obj = TypeConverter.numpy_to_xarray(numpy_arr)
            converted_back = TypeConverter.xarray_to_numpy(xarray_obj)
            self.assertIsInstance(converted_back, self.numpy.ndarray)
            self.assertEqual(converted_back.shape, numpy_arr.shape)
            self.assertTrue(self.numpy.array_equal(converted_back, numpy_arr))
        except ImportError:
            pass  # xarray未安装，跳过
        
        # 测试numpy -> torch -> numpy
        try:
            import torch
            torch_tensor = TypeConverter.numpy_to_torch(numpy_arr)
            converted_back = TypeConverter.torch_to_numpy(torch_tensor)
            self.assertIsInstance(converted_back, self.numpy.ndarray)
            self.assertEqual(converted_back.shape, numpy_arr.shape)
            self.assertTrue(self.numpy.array_equal(converted_back, numpy_arr))
        except ImportError:
            pass  # torch未安装，跳过

if __name__ == '__main__':
    unittest.main()