import unittest
from e2e import to_e2e, from_e2e, E2EType

class TestE2E(unittest.TestCase):
    """测试EveryThing to EveryThing包的功能"""
    
    def test_basic_conversion(self):
        """测试基本转换功能"""
        str_e2e = to_e2e("Hello, World!")
        self.assertIsInstance(str_e2e, E2EType)
        self.assertEqual(str_e2e.get_value(), "Hello, World!")
        self.assertEqual(str_e2e.get_original_type(), str)
    
    def test_conversion_back(self):
        """测试转换回原始类型"""
        test_value = "Test Value"
        e2e_obj = to_e2e(test_value)
        converted_back = from_e2e(e2e_obj)
        self.assertEqual(converted_back, test_value)
        self.assertEqual(type(converted_back), type(test_value))
    
    def test_different_types(self):
        """测试不同类型的转换"""
        types_to_test = [
            ("string", "Hello"),
            ("integer", 42),
            ("float", 3.14),
            ("list", [1, 2, 3]),
            ("dict", {"name": "Alice"}),
            ("bool", True),
            ("None", None)
        ]
        
        for name, value in types_to_test:
            with self.subTest(name=name):
                e2e_obj = to_e2e(value)
                self.assertIsInstance(e2e_obj, E2EType)
                
                converted_back = from_e2e(e2e_obj)
                self.assertEqual(converted_back, value)
                self.assertEqual(type(converted_back), type(value))
    
    def test_e2e_type_methods(self):
        """测试E2EType的方法"""
        test_obj = to_e2e("Test Value")
        
        # Test get_value
        self.assertEqual(test_obj.get_value(), "Test Value")
        
        # Test get_original_type
        self.assertEqual(test_obj.get_original_type(), str)
        
        # Test get_timestamp
        self.assertIsInstance(test_obj.get_timestamp(), float)
        
        # Test is_type
        self.assertTrue(test_obj.is_type(str))
        self.assertFalse(test_obj.is_type(int))
        
        # Test to_original
        self.assertEqual(test_obj.to_original(), "Test Value")
        
        # Test serialize
        serialized = test_obj.serialize()
        self.assertIsInstance(serialized, str)
    
    def test_from_e2e_with_normal_value(self):
        """测试from_e2e函数处理普通值"""
        normal_value = "Normal string"
        result = from_e2e(normal_value)
        self.assertEqual(result, normal_value)
        self.assertEqual(type(result), type(normal_value))
    
    def test_numpy_support(self):
        """测试NumPy支持"""
        try:
            import numpy as np
            
            # Test 1D array
            arr_1d = np.array([1, 2, 3, 4, 5])
            arr_e2e = to_e2e(arr_1d)
            self.assertIsInstance(arr_e2e, E2EType)
            
            converted_back = from_e2e(arr_e2e)
            self.assertIsInstance(converted_back, np.ndarray)
            self.assertTrue(np.array_equal(arr_1d, converted_back))
            
            # Test 2D array
            arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
            arr_e2e = to_e2e(arr_2d)
            converted_back = from_e2e(arr_e2e)
            self.assertTrue(np.array_equal(arr_2d, converted_back))
            
            # Test serialization
            serialized = arr_e2e.serialize()
            self.assertIsInstance(serialized, str)
            self.assertIn("numpy.ndarray", serialized)
            
        except ImportError:
            self.skipTest("NumPy not installed")
    
    def test_cupy_support(self):
        """测试CuPy支持"""
        try:
            import cupy as cp
            
            # Test basic cupy array
            arr = cp.array([1, 2, 3, 4, 5])
            arr_e2e = to_e2e(arr)
            self.assertIsInstance(arr_e2e, E2EType)
            
            converted_back = from_e2e(arr_e2e)
            self.assertIsInstance(converted_back, cp.ndarray)
            self.assertTrue(cp.array_equal(arr, converted_back))
            
            # Test serialization
            serialized = arr_e2e.serialize()
            self.assertIsInstance(serialized, str)
            self.assertIn("cupy.ndarray", serialized)
            
        except ImportError:
            self.skipTest("CuPy not installed")
    
    def test_scipy_support(self):
        """测试SciPy支持"""
        try:
            from scipy import sparse
            
            # Test CSR matrix
            matrix = sparse.csr_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            matrix_e2e = to_e2e(matrix)
            self.assertIsInstance(matrix_e2e, E2EType)
            
            converted_back = from_e2e(matrix_e2e)
            self.assertIsInstance(converted_back, type(matrix))
            self.assertTrue((matrix != converted_back).nnz == 0)
            
            # Test serialization
            serialized = matrix_e2e.serialize()
            self.assertIsInstance(serialized, str)
            self.assertIn("scipy.sparse", serialized)
            
        except ImportError:
            self.skipTest("SciPy not installed")
    
    def test_complex_nested_types(self):
        """测试复杂嵌套类型"""
        # Test nested dictionary
        nested_dict = {
            "name": "Alice",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York"
            },
            "hobbies": ["reading", "hiking", "coding"]
        }
        
        e2e_obj = to_e2e(nested_dict)
        self.assertIsInstance(e2e_obj, E2EType)
        
        converted_back = from_e2e(e2e_obj)
        self.assertEqual(converted_back, nested_dict)
        self.assertEqual(type(converted_back), type(nested_dict))
    
    def test_empty_and_large_types(self):
        """测试空类型和大型类型"""
        # Test empty types
        empty_types = [
            ("empty string", ""),
            ("empty list", []),
            ("empty dict", {})
        ]
        
        for name, value in empty_types:
            with self.subTest(name=name):
                e2e_obj = to_e2e(value)
                self.assertIsInstance(e2e_obj, E2EType)
                
                converted_back = from_e2e(e2e_obj)
                self.assertEqual(converted_back, value)
        
        # Test large list
        large_list = list(range(1000))
        e2e_obj = to_e2e(large_list)
        self.assertIsInstance(e2e_obj, E2EType)
        
        converted_back = from_e2e(e2e_obj)
        self.assertEqual(len(converted_back), len(large_list))
        self.assertEqual(converted_back[:10], large_list[:10])
    
    def test_serialization(self):
        """测试序列化功能"""
        test_cases = [
            ("string", "Hello"),
            ("number", 42),
            ("list", [1, 2, 3]),
            ("dict", {"key": "value"})
        ]
        
        for name, value in test_cases:
            with self.subTest(name=name):
                e2e_obj = to_e2e(value)
                serialized = e2e_obj.serialize()
                self.assertIsInstance(serialized, str)
                self.assertTrue(len(serialized) > 0)
    
    def test_standard_library_types(self):
        """测试Python标准库中的特殊类型"""
        # Test set and frozenset
        test_set = {1, 2, 3, 4, 5}
        set_e2e = to_e2e(test_set)
        self.assertIsInstance(set_e2e, E2EType)
        converted_set = from_e2e(set_e2e)
        self.assertEqual(type(converted_set), type(test_set))
        self.assertEqual(set(converted_set), test_set)
        
        # Test bytes and bytearray
        test_bytes = b"Hello"
        bytes_e2e = to_e2e(test_bytes)
        self.assertIsInstance(bytes_e2e, E2EType)
        converted_bytes = from_e2e(bytes_e2e)
        self.assertEqual(type(converted_bytes), type(test_bytes))
        
        # Test range
        test_range = range(0, 10, 2)
        range_e2e = to_e2e(test_range)
        self.assertIsInstance(range_e2e, E2EType)
        converted_range = from_e2e(range_e2e)
        self.assertEqual(type(converted_range), type(test_range))
        self.assertEqual(list(converted_range), list(test_range))
    
    def test_pandas_support(self):
        """测试pandas支持"""
        try:
            import pandas as pd
            
            # Test DataFrame
            df = pd.DataFrame({
                "name": ["Alice", "Bob"],
                "age": [25, 30]
            })
            df_e2e = to_e2e(df)
            self.assertIsInstance(df_e2e, E2EType)
            
            converted_df = from_e2e(df_e2e)
            self.assertIsInstance(converted_df, pd.DataFrame)
            
            # Test Series
            series = pd.Series([1, 2, 3, 4, 5], name="test_series")
            series_e2e = to_e2e(series)
            self.assertIsInstance(series_e2e, E2EType)
            
            converted_series = from_e2e(series_e2e)
            self.assertIsInstance(converted_series, pd.Series)
            
        except ImportError:
            self.skipTest("pandas not installed")
    
    def test_pytorch_support(self):
        """测试PyTorch支持"""
        try:
            import torch
            
            # Test tensor
            tensor = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
            tensor_e2e = to_e2e(tensor)
            self.assertIsInstance(tensor_e2e, E2EType)
            
            converted_tensor = from_e2e(tensor_e2e)
            self.assertIsInstance(converted_tensor, torch.Tensor)
            self.assertEqual(list(tensor.shape), list(converted_tensor.shape))
            
        except ImportError:
            self.skipTest("PyTorch not installed")
    
    def test_tensorflow_support(self):
        """测试TensorFlow支持"""
        try:
            import tensorflow as tf
            
            # Test tensor
            tensor = tf.constant([[1, 2], [3, 4]])
            tensor_e2e = to_e2e(tensor)
            self.assertIsInstance(tensor_e2e, E2EType)
            
            converted_tensor = from_e2e(tensor_e2e)
            self.assertIsInstance(converted_tensor, tf.Tensor)
            self.assertEqual(list(tensor.shape), list(converted_tensor.shape))
            
        except ImportError:
            self.skipTest("TensorFlow not installed")
    
    def test_jax_support(self):
        """测试JAX支持"""
        try:
            import jax.numpy as jnp
            
            # Test JAX array
            arr = jnp.array([[1, 2], [3, 4]])
            arr_e2e = to_e2e(arr)
            self.assertIsInstance(arr_e2e, E2EType)
            
            converted_arr = from_e2e(arr_e2e)
            self.assertIsInstance(converted_arr, jnp.ndarray)
            self.assertEqual(list(arr.shape), list(converted_arr.shape))
            
        except ImportError:
            self.skipTest("JAX not installed")
    
    def test_tuple_support(self):
        """测试元组支持"""
        test_tuple = (1, "hello", [1, 2, 3])
        tuple_e2e = to_e2e(test_tuple)
        self.assertIsInstance(tuple_e2e, E2EType)
        
        converted_tuple = from_e2e(tuple_e2e)
        self.assertEqual(type(converted_tuple), tuple)
        self.assertEqual(converted_tuple, test_tuple)
    
    def test_xarray_support(self):
        """测试xarray支持"""
        try:
            import xarray as xr
            import numpy as np
            
            # Test DataArray
            data = xr.DataArray(
                np.random.rand(2, 3),
                dims=["x", "y"],
                coords={"x": [1, 2], "y": [1, 2, 3]}
            )
            data_e2e = to_e2e(data)
            self.assertIsInstance(data_e2e, E2EType)
            
            # Test Dataset
            ds = xr.Dataset({
                "temp": ("x", [1, 2, 3]),
                "precip": ("x", [0.1, 0.2, 0.3])
            }, coords={"x": [1, 2, 3]})
            ds_e2e = to_e2e(ds)
            self.assertIsInstance(ds_e2e, E2EType)
            
        except ImportError:
            self.skipTest("xarray not installed")
    
    def test_pil_support(self):
        """测试PIL/Pillow支持"""
        try:
            from PIL import Image
            import io
            
            # Create a test image
            img = Image.new('RGB', (100, 100), color='red')
            img_e2e = to_e2e(img)
            self.assertIsInstance(img_e2e, E2EType)
            
            # Test serialization
            serialized = img_e2e.serialize()
            self.assertIsInstance(serialized, str)
            self.assertIn("PIL.Image.Image", serialized)
            
        except ImportError:
            self.skipTest("PIL/Pillow not installed")
    
    def test_custom_class_support(self):
        """测试自定义类支持"""
        # Define a custom class
        class Person:
            def __init__(self, name, age):
                self.name = name
                self.age = age
            
            def __repr__(self):
                return f"Person(name='{self.name}', age={self.age})"
        
        # Create an instance
        person = Person("Alice", 30)
        person_e2e = to_e2e(person)
        self.assertIsInstance(person_e2e, E2EType)
        
        # Test serialization
        serialized = person_e2e.serialize()
        self.assertIsInstance(serialized, str)
    
    def test_numba_support(self):
        """测试Numba支持"""
        try:
            import numba
            
            # Test numba jitted function
            @numba.jit(nopython=True)
            def add(a, b):
                return a + b
            
            # Create a test value
            test_value = add(1, 2)
            value_e2e = to_e2e(test_value)
            self.assertIsInstance(value_e2e, E2EType)
            
            # Test serialization
            serialized = value_e2e.serialize()
            self.assertIsInstance(serialized, str)
            
        except ImportError:
            self.skipTest("Numba not installed")


if __name__ == '__main__':
    unittest.main()
