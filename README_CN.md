# EveryThing to EveryThing (E2E)

一个可以将任何标准Python类型转换为自定义数据类型，反之亦然的Python包。

## 安装

```bash
pip install .
```

## 使用方法

### 基本用法

```python
from e2e import to_e2e, from_e2e, E2EType

# 转换为E2EType
str_e2e = to_e2e("Hello, World!")
int_e2e = to_e2e(42)
list_e2e = to_e2e([1, 2, 3, 4, 5])
dict_e2e = to_e2e({"name": "Alice", "age": 30})

# 转换回原始类型
original_str = from_e2e(str_e2e)
original_int = from_e2e(int_e2e)

# 使用E2EType方法
print(str_e2e)
print(str_e2e.get_value())
print(str_e2e.get_original_type())
print(str_e2e.get_timestamp())
print(str_e2e.is_type(str))
print(str_e2e.serialize())
```

### 支持的类型

- **Python标准类型**:
  - 字符串 (str)
  - 整数 (int)
  - 浮点数 (float)
  - 列表 (list)
  - 字典 (dict)
  - 布尔值 (bool)
  - None (NoneType)
  - 集合 (set 和 frozenset)
  - 字节 (bytes 和 bytearray)
  - 范围 (range)
  - 以及所有其他Python标准类型

- **科学计算库**:
  - NumPy数组 (numpy.ndarray)
  - CuPy数组 (cupy.ndarray)
  - SciPy稀疏矩阵 (scipy.sparse.*)
  - pandas DataFrame和Series
  - PyTorch张量 (torch.Tensor)
  - JAX数组 (jax.numpy.ndarray)
  - TensorFlow张量 (tensorflow.Tensor)
  - xarray DataArray和Dataset
  - Numba编译类型

- **其他特殊类型**:
  - PIL/Pillow图像对象
  - Python元组 (保持不可变性)
  - 自定义Python类 (支持__dict__)
  - 以及许多其他Python对象

## 功能特点

- **无缝转换**: 轻松在Python标准类型和E2EType之间转换
- **类型保留**: 跟踪原始类型信息
- **时间戳跟踪**: 记录转换发生的时间
- **类型检查**: 验证原始值是否为指定类型
- **序列化**: 将E2EType对象转换为可序列化格式
- **向后兼容**: from_e2e函数可以处理E2EType对象和常规值

## API参考

### 函数

- `to_e2e(value)`: 将任何Python值转换为E2EType
- `from_e2e(e2e_obj)`: 将E2EType转换回原始值

### E2EType方法

- `get_value()`: 返回原始值
- `get_original_type()`: 返回原始类型
- `get_timestamp()`: 返回转换时的时间戳
- `to_original()`: 转换回原始类型
- `is_type(type_obj)`: 检查原始值是否为指定类型
- `serialize()`: 返回序列化表示

## 示例

### 转换不同类型

```python
from e2e import to_e2e

# 转换字符串
str_e2e = to_e2e("Hello")
print(str_e2e)  # 输出: E2EType(Hello)

# 转换数字
num_e2e = to_e2e(3.14)
print(num_e2e)  # 输出: E2EType(3.14)

# 转换复杂类型
complex_e2e = to_e2e({"nested": [1, 2, {"key": "value"}]})
print(complex_e2e)  # 输出: E2EType({'nested': [1, 2, {'key': 'value'}]})
```

### 检查类型

```python
from e2e import to_e2e

value_e2e = to_e2e(42)
print(value_e2e.is_type(int))  # 输出: True
print(value_e2e.is_type(str))  # 输出: False
```

### 序列化

```python
from e2e import to_e2e

value_e2e = to_e2e({"name": "Bob", "age": 25})
print(value_e2e.serialize())  # 输出: JSON字符串
```

### NumPy支持

```python
from e2e import to_e2e, from_e2e
import numpy as np

# 创建NumPy数组
arr = np.array([[1, 2, 3], [4, 5, 6]])

# 转换为E2EType
arr_e2e = to_e2e(arr)
print(arr_e2e)
print(arr_e2e.serialize())  # 将包含形状和数据类型信息

# 转换回原始类型
original_arr = from_e2e(arr_e2e)
print(original_arr)
print(type(original_arr))  # 应该是numpy.ndarray
```

### CuPy支持

```python
from e2e import to_e2e, from_e2e
import cupy as cp

# 创建CuPy数组
arr = cp.array([[1, 2, 3], [4, 5, 6]])

# 转换为E2EType
arr_e2e = to_e2e(arr)
print(arr_e2e)
print(arr_e2e.serialize())  # 将包含形状和数据类型信息

# 转换回原始类型
original_arr = from_e2e(arr_e2e)
print(original_arr)
print(type(original_arr))  # 应该是cupy.ndarray
```

### SciPy支持

```python
from e2e import to_e2e, from_e2e
from scipy import sparse

# 创建SciPy稀疏矩阵
matrix = sparse.csr_matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

# 转换为E2EType
matrix_e2e = to_e2e(matrix)
print(matrix_e2e)
print(matrix_e2e.serialize())  # 将包含形状和格式信息

# 转换回原始类型
original_matrix = from_e2e(matrix_e2e)
print(original_matrix)
print(type(original_matrix))  # 应该是scipy.sparse.csr_matrix
```

### 高级示例

#### 1. 复杂嵌套结构

```python
from e2e import to_e2e, from_e2e

# 创建复杂嵌套结构
complex_data = {
    "person": {
        "name": "John",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zipcode": 10001
        },
        "hobbies": ["reading", "hiking", "coding"],
        "is_active": True
    },
    "scores": [95, 87, 91, 88]
}

# 转换为E2EType
data_e2e = to_e2e(complex_data)
print("Complex data converted to E2EType")

# 转换回原始类型
original_data = from_e2e(data_e2e)
print("Data preserved:", original_data["person"]["name"] == "John")
print("Nested structure preserved:", "address" in original_data["person"])
```

#### 2. 批量转换

```python
from e2e import to_e2e, from_e2e

# 创建数据列表
data_list = [
    "Hello",
    42,
    [1, 2, 3],
    {"key": "value"}
]

# 批量转换为E2EType
e2e_list = [to_e2e(item) for item in data_list]
print(f"Converted {len(e2e_list)} items to E2EType")

# 批量转换回原始类型
original_list = [from_e2e(item) for item in e2e_list]
print("Original list:", original_list)
print("Types preserved:", all(type(a) == type(b) for a, b in zip(data_list, original_list)))
```

#### 3. 时间戳和类型检查

```python
from e2e import to_e2e
import time

# 创建不同类型的值
values = ["test", 123, [1, 2, 3]]

for value in values:
    e2e_obj = to_e2e(value)
    print(f"Value: {value}")
    print(f"Type: {type(value).__name__}")
    print(f"Timestamp: {e2e_obj.get_timestamp()}")
    print(f"Is string: {e2e_obj.is_type(str)}")
    print(f"Is list: {e2e_obj.is_type(list)}")
    print()
    time.sleep(0.1)  # 等待一点时间以获得不同的时间戳
```

#### 4. 与NumPy数组操作结合

```python
from e2e import to_e2e, from_e2e
import numpy as np

# 创建NumPy数组
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("Original array:")
print(arr)

# 转换为E2EType
arr_e2e = to_e2e(arr)
print(f"Converted to E2EType: {arr_e2e}")

# 进行一些操作（在原始数组上）
arr_modified = arr * 2
print("Modified array:")
print(arr_modified)

# 转换回原始类型并验证
original_arr = from_e2e(arr_e2e)
print("Original array retrieved:")
print(original_arr)
print("Arrays are equal:", np.array_equal(arr, original_arr))
```

#### 5. 异常处理和边缘情况

```python
from e2e import to_e2e, from_e2e

# 测试边缘情况
test_cases = [
    "",  # 空字符串
    [],  # 空列表
    {},  # 空字典
    None,  # None值
    0,  # 零值
    0.0,  # 零浮点数
    False,  # 布尔值False
]

for test_case in test_cases:
    try:
        e2e_obj = to_e2e(test_case)
        converted_back = from_e2e(e2e_obj)
        print(f"Test case: {repr(test_case)}")
        print(f"  Type: {type(test_case).__name__}")
        print(f"  Conversion successful: {converted_back == test_case}")
    except Exception as e:
        print(f"Test case: {repr(test_case)}")
        print(f"  Error: {e}")
    print()
```

#### 6. 扩展库支持示例

##### 6.1 pandas DataFrame

```python
from e2e import to_e2e, from_e2e
import pandas as pd

# 创建DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["New York", "London", "Paris"]
})
print("Original DataFrame:")
print(df)

# 转换为E2EType
df_e2e = to_e2e(df)
print(f"Converted to E2EType: {df_e2e}")

# 转换回原始类型
original_df = from_e2e(df_e2e)
print("Retrieved DataFrame:")
print(original_df)
print("DataFrames are equal:", df.equals(original_df))
```

##### 6.2 PyTorch张量

```python
from e2e import to_e2e, from_e2e
import torch

# 创建PyTorch张量
tensor = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print("Original tensor:")
print(tensor)
print(f"Shape: {tensor.shape}")
print(f"Device: {tensor.device}")

# 转换为E2EType
tensor_e2e = to_e2e(tensor)
print(f"Converted to E2EType: {tensor_e2e}")

# 转换回原始类型
original_tensor = from_e2e(tensor_e2e)
print("Retrieved tensor:")
print(original_tensor)
print(f"Shapes match: {tensor.shape == original_tensor.shape}")
```

##### 6.3 TensorFlow张量

```python
from e2e import to_e2e, from_e2e
import tensorflow as tf

# 创建TensorFlow张量
tensor = tf.constant([[1, 2, 3], [4, 5, 6]])
print("Original tensor:")
print(tensor)
print(f"Shape: {tensor.shape}")

# 转换为E2EType
tensor_e2e = to_e2e(tensor)
print(f"Converted to E2EType: {tensor_e2e}")

# 转换回原始类型
original_tensor = from_e2e(tensor_e2e)
print("Retrieved tensor:")
print(original_tensor)
print(f"Shapes match: {tensor.shape == original_tensor.shape}")
```

#### 7. Python标准库特殊类型

```python
from e2e import to_e2e, from_e2e

# 测试集合类型
my_set = {1, 2, 3, 4, 5}
set_e2e = to_e2e(my_set)
print(f"Set: {my_set} -> {set_e2e}")
retrieved_set = from_e2e(set_e2e)
print(f"Retrieved: {retrieved_set}, Type: {type(retrieved_set).__name__}")

# 测试bytes类型
my_bytes = b"Hello"
bytes_e2e = to_e2e(my_bytes)
print(f"Bytes: {my_bytes} -> {bytes_e2e}")
retrieved_bytes = from_e2e(bytes_e2e)
print(f"Retrieved: {retrieved_bytes}, Type: {type(retrieved_bytes).__name__}")

# 测试range类型
my_range = range(0, 10, 2)
range_e2e = to_e2e(my_range)
print(f"Range: {my_range} -> {range_e2e}")
retrieved_range = from_e2e(range_e2e)
print(f"Retrieved: {retrieved_range}, Type: {type(retrieved_range).__name__}")

# 测试元组类型
my_tuple = (1, "hello", [1, 2, 3])
tuple_e2e = to_e2e(my_tuple)
print(f"Tuple: {my_tuple} -> {tuple_e2e}")
retrieved_tuple = from_e2e(tuple_e2e)
print(f"Retrieved: {retrieved_tuple}, Type: {type(retrieved_tuple).__name__}")
print(f"Is tuple: {isinstance(retrieved_tuple, tuple)}")
```

#### 8. 扩展库高级示例

##### 8.1 xarray DataArray和Dataset

```python
from e2e import to_e2e, from_e2e
import xarray as xr
import numpy as np

# 创建DataArray
data = xr.DataArray(
    np.random.rand(2, 3),
    dims=["x", "y"],
    coords={"x": [1, 2], "y": [1, 2, 3]}
)
print("Original DataArray:")
print(data)

# 转换为E2EType
data_e2e = to_e2e(data)
print(f"Converted to E2EType: {data_e2e}")

# 序列化
serialized = data_e2e.serialize()
print(f"Serialized: {serialized[:150]}...")

# 创建Dataset
ds = xr.Dataset({
    "temp": ("x", [1, 2, 3]),
    "precip": ("x", [0.1, 0.2, 0.3])
}, coords={"x": [1, 2, 3]})
print("\nOriginal Dataset:")
print(ds)

# 转换为E2EType
ds_e2e = to_e2e(ds)
print(f"Converted to E2EType: {ds_e2e}")
```

##### 8.2 PIL/Pillow图像对象

```python
from e2e import to_e2e, from_e2e
from PIL import Image

# 创建测试图像
img = Image.new('RGB', (100, 100), color='red')
print("Original Image:")
print(f"Format: {img.format}")
print(f"Size: {img.size}")
print(f"Mode: {img.mode}")

# 转换为E2EType
img_e2e = to_e2e(img)
print(f"Converted to E2EType: {img_e2e}")

# 序列化
serialized = img_e2e.serialize()
print(f"Serialized: {serialized}")
```

##### 8.3 自定义类对象

```python
from e2e import to_e2e, from_e2e

# 定义自定义类
class Person:
    def __init__(self, name, age, city):
        self.name = name
        self.age = age
        self.city = city
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age}, city='{self.city}')"

# 创建实例
person = Person("Alice", 30, "New York")
print("Original Person:", person)

# 转换为E2EType
person_e2e = to_e2e(person)
print(f"Converted to E2EType: {person_e2e}")

# 序列化
serialized = person_e2e.serialize()
print(f"Serialized: {serialized}")

# 转换回原始类型
retrieved_person = from_e2e(person_e2e)
print(f"Retrieved: {retrieved_person}")
print(f"Type: {type(retrieved_person).__name__}")
```

##### 8.4 Numba类型

```python
from e2e import to_e2e, from_e2e
import numba

# 定义Numba函数
@numba.jit(nopython=True)
def add(a, b):
    return a + b

# 测试Numba函数结果
result = add(10, 20)
print(f"Numba function result: {result}")

# 转换为E2EType
result_e2e = to_e2e(result)
print(f"Converted to E2EType: {result_e2e}")

# 序列化
serialized = result_e2e.serialize()
print(f"Serialized: {serialized}")

# 转换回原始类型
retrieved_result = from_e2e(result_e2e)
print(f"Retrieved: {retrieved_result}, Type: {type(retrieved_result).__name__}")
```

## 许可证

MIT
