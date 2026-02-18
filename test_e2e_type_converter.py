import unittest
import sys

# 导入类型转换兼容层
sys.path.append('c:\\Users\\Potato\\Documents\\trae_projects\\everything2everything')
from e2e_type_converter import (
    TypeConverter, e2e_list, e2e_str, e2e_int, e2e_float, e2e_dict, e2e_set, e2e_tuple
)

# 重命名以便测试使用
list = e2e_list
str = e2e_str
int = e2e_int
float = e2e_float
dict = e2e_dict
set = e2e_set
tuple = e2e_tuple

class TestTypeConverter(unittest.TestCase):
    """测试类型转换兼容层"""
    
    def test_list_conversion(self):
        """测试list转换"""
        # 基本类型转换
        self.assertEqual(list(), [])
        self.assertEqual(list(None), [])
        self.assertEqual(list(123), [123])
        self.assertEqual(list(123.456), [123.456])
        self.assertEqual(list(True), [True])
        self.assertEqual(list("hello"), ['h', 'e', 'l', 'l', 'o'])
        
        # 容器类型转换
        self.assertEqual(list((1, 2, 3)), [1, 2, 3])
        self.assertEqual(list({1, 2, 3}), [1, 2, 3])
        self.assertEqual(list({"a": 1, "b": 2}), [("a", 1), ("b", 2)])
        
        # 异常处理
        with self.assertRaises(TypeError):
            list(object())
    
    def test_str_conversion(self):
        """测试str转换"""
        # 基本类型转换
        self.assertEqual(str(), "")
        self.assertEqual(str(None), "")
        self.assertEqual(str(123), "123")
        self.assertEqual(str(123.456), "123.456")
        self.assertEqual(str(True), "true")
        self.assertEqual(str(False), "false")
        
        # 容器类型转换
        self.assertEqual(str([1, 2, 3]), "[1, 2, 3]")
        self.assertEqual(str((1, 2, 3)), "(1, 2, 3)")
        self.assertEqual(str({1, 2, 3}), "{1, 2, 3}")
        self.assertEqual(str({"a": 1, "b": 2}), "{'a': 1, 'b': 2}")
    
    def test_int_conversion(self):
        """测试int转换"""
        # 基本类型转换
        self.assertEqual(int(), 0)
        self.assertEqual(int(None), 0)
        self.assertEqual(int(123), 123)
        self.assertEqual(int(123.456), 123)
        self.assertEqual(int(True), 1)
        self.assertEqual(int(False), 0)
        self.assertEqual(int("123"), 123)
        
        # 单元素容器转换
        self.assertEqual(int([123]), 123)
        self.assertEqual(int((123,)), 123)
        self.assertEqual(int({123}), 123)
        
        # 空容器转换
        self.assertEqual(int([]), 0)
        self.assertEqual(int(()), 0)
        self.assertEqual(int({}), 0)
        
        # 异常处理
        with self.assertRaises(ValueError):
            int("abc")
        with self.assertRaises(TypeError):
            int([1, 2, 3])
    
    def test_float_conversion(self):
        """测试float转换"""
        # 基本类型转换
        self.assertEqual(float(), 0.0)
        self.assertEqual(float(None), 0.0)
        self.assertEqual(float(123), 123.0)
        self.assertEqual(float(123.456), 123.456)
        self.assertEqual(float(True), 1.0)
        self.assertEqual(float(False), 0.0)
        self.assertEqual(float("123.456"), 123.456)
        
        # 单元素容器转换
        self.assertEqual(float([123]), 123.0)
        self.assertEqual(float((123.456,)), 123.456)
        
        # 空容器转换
        self.assertEqual(float([]), 0.0)
        self.assertEqual(float(()), 0.0)
        
        # 异常处理
        with self.assertRaises(ValueError):
            float("abc")
        with self.assertRaises(TypeError):
            float([1, 2, 3])
    
    def test_dict_conversion(self):
        """测试dict转换"""
        # 基本类型转换
        self.assertEqual(dict(), {})
        self.assertEqual(dict(None), {})
        self.assertEqual(dict(123), {"value": 123})
        self.assertEqual(dict(123.456), {"value": 123.456})
        self.assertEqual(dict(True), {"value": True})
        self.assertEqual(dict("hello"), {"value": "hello"})
        
        # 容器类型转换
        self.assertEqual(dict([("a", 1), ("b", 2)]), {"a": 1, "b": 2})
        self.assertEqual(dict((["a", 1], ["b", 2])), {"a": 1, "b": 2})
        self.assertEqual(dict({"a": 1, "b": 2}), {"a": 1, "b": 2})
        self.assertEqual(dict([1, 2, 3]), {0: 1, 1: 2, 2: 3})
    
    def test_set_conversion(self):
        """测试set转换"""
        # 基本类型转换
        self.assertEqual(set(), set())
        self.assertEqual(set(None), set())
        self.assertEqual(set(123), {123})
        self.assertEqual(set(123.456), {123.456})
        self.assertEqual(set(True), {True})
        self.assertEqual(set("hello"), {'h', 'e', 'l', 'o'})
        
        # 容器类型转换
        self.assertEqual(set([1, 2, 3]), {1, 2, 3})
        self.assertEqual(set((1, 2, 3)), {1, 2, 3})
        self.assertEqual(set({"a": 1, "b": 2}), {"a", "b"})
    
    def test_tuple_conversion(self):
        """测试tuple转换"""
        # 基本类型转换
        self.assertEqual(tuple(), ())
        self.assertEqual(tuple(None), ())
        self.assertEqual(tuple(123), (123,))
        self.assertEqual(tuple(123.456), (123.456,))
        self.assertEqual(tuple(True), (True,))
        self.assertEqual(tuple("hello"), ('h', 'e', 'l', 'l', 'o'))
        
        # 容器类型转换
        self.assertEqual(tuple([1, 2, 3]), (1, 2, 3))
        self.assertEqual(tuple({1, 2, 3}), (1, 2, 3))
        self.assertEqual(tuple({"a": 1, "b": 2}), ("a", "b"))
    
    def test_bidirectional_conversion(self):
        """测试双向转换"""
        # int -> str -> int
        self.assertEqual(int(str(123)), 123)
        
        # float -> str -> float
        self.assertEqual(float(str(123.456)), 123.456)
        
        # list -> tuple -> list
        self.assertEqual(list(tuple([1, 2, 3])), [1, 2, 3])
        
        # dict -> list -> dict
        test_dict = {"a": 1, "b": 2}
        converted = dict(list(test_dict))
        self.assertEqual(converted, test_dict)
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 空值转换
        self.assertEqual(list(None), [])
        self.assertEqual(str(None), "")
        self.assertEqual(int(None), 0)
        self.assertEqual(float(None), 0.0)
        self.assertEqual(dict(None), {})
        self.assertEqual(set(None), set())
        self.assertEqual(tuple(None), ())
        
        # 布尔值转换
        self.assertEqual(int(True), 1)
        self.assertEqual(int(False), 0)
        self.assertEqual(float(True), 1.0)
        self.assertEqual(float(False), 0.0)
        self.assertEqual(str(True), "true")
        self.assertEqual(str(False), "false")

if __name__ == '__main__':
    unittest.main()