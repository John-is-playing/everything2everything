# EveryThing to EveryThing 类型转换兼容层

## 项目概述

本项目实现了一个Python类型转换兼容层，支持所有Python标准数据类型之间的双向转换功能。该兼容层在不修改Python内置函数原有接口和使用方式的前提下，扩展了其转换能力，实现了不同标准数据类型间的无缝转换。

## 支持的转换类型

- **基本类型**：int、float、str、bool、NoneType
- **容器类型**：list、tuple、dict、set
- **字节类型**：bytes
- **第三方库类型**（可选，需安装对应库）：
  - NumPy 数组 (`numpy.ndarray`)
  - CuPy 数组 (`cupy.ndarray`)
  - SciPy 稀疏矩阵 (`scipy.sparse.*`)
  - Pandas 类型 (`pandas.DataFrame`, `pandas.Series`)
  - PyTorch 张量 (`torch.Tensor`)
  - xarray 类型 (`xarray.DataArray`, `xarray.Dataset`)
  - JAX 数组 (`jax.numpy.ndarray`)
  - TensorFlow 张量 (`tensorflow.Tensor`)

## 转换规则

### 1. 转换为 list

| 输入类型 | 输出结果 |
|---------|----------|
| list | 保持不变 |
| None | [] |
| str/bytes | 转换为字符/字节列表 |
| dict | 转换为键值对元组列表 |
| int/float/bool | 转换为单元素列表 |
| tuple/set | 转换为列表 |
| 其他 | 尝试使用原始 list() 函数 |

### 2. 转换为 str

| 输入类型 | 输出结果 |
|---------|----------|
| str | 保持不变 |
| None | "" |
| bool | 转换为小写字符串 ("true"/"false") |
| int/float/list/tuple/dict/set | 使用原始 str() 函数 |
| 其他 | 尝试使用原始 str() 函数 |

### 3. 转换为 int

| 输入类型 | 输出结果 |
|---------|----------|
| int | 保持不变 |
| None | 0 |
| bool | 转换为 1/0 |
| float | 截断小数部分 |
| str | 尝试转换为整数 |
| 空容器 | 0 |
| 单元素容器 | 转换容器内元素 |
| 多元素容器 | 抛出 TypeError |
| 其他 | 尝试使用原始 int() 函数 |

### 4. 转换为 float

| 输入类型 | 输出结果 |
|---------|----------|
| float | 保持不变 |
| None | 0.0 |
| bool | 转换为 1.0/0.0 |
| int | 转换为浮点数 |
| str | 尝试转换为浮点数 |
| 空容器 | 0.0 |
| 单元素容器 | 转换容器内元素 |
| 多元素容器 | 抛出 TypeError |
| 其他 | 尝试使用原始 float() 函数 |

### 5. 转换为 dict

| 输入类型 | 输出结果 |
|---------|----------|
| dict | 保持不变 |
| None | {} |
| list/tuple | 尝试转换为字典，失败则转换为索引字典 |
| str/int/float/bool/set | 转换为 {"value": 值} |
| 其他 | 尝试使用原始 dict() 函数 |

### 6. 转换为 set

| 输入类型 | 输出结果 |
|---------|----------|
| set | 保持不变 |
| None | set() |
| str/bytes | 转换为字符/字节集合 |
| int/float/bool | 转换为单元素集合 |
| list/tuple/dict | 转换为集合 |
| 其他 | 尝试使用原始 set() 函数 |

### 7. 转换为 tuple

| 输入类型 | 输出结果 |
|---------|----------|
| tuple | 保持不变 |
| None | () |
| str/bytes | 转换为字符/字节元组 |
| int/float/bool | 转换为单元素元组 |
| list/set/dict | 转换为元组 |
| 其他 | 尝试使用原始 tuple() 函数 |

### 8. 第三方库类型转换

| 类型 | 转换为 list | 转换为 str | 转换为 int/float | 转换为 dict | 转换为 set | 转换为 tuple |
|------|------------|------------|-----------------|------------|------------|--------------|
| NumPy 数组 | 转换为嵌套列表 | 转换为列表字符串 | 仅标量数组 | 1D: 索引字典<br>ND: 包含shape、dtype、data的字典 | 仅1D数组 | 转换为嵌套元组 |
| CuPy 数组 | 转换为嵌套列表 | 转换为列表字符串 | 仅标量数组 | 1D: 索引字典<br>ND: 包含shape、dtype、data的字典 | 仅1D数组 | 转换为嵌套元组 |
| SciPy 稀疏矩阵 | 转换为密集数组列表 | 转换为列表字符串 | 仅单元素矩阵 | 1D: 索引字典<br>ND: 包含shape、dtype、data的字典 | 仅1D矩阵 | 转换为嵌套元组 |
| Pandas DataFrame | 包含列名的嵌套列表 | 转换为字典字符串 | 仅单元素DataFrame | 转换为列名:列表字典 | 不支持 | 包含列名的嵌套元组 |
| Pandas Series | 转换为值列表 | 转换为列表字符串 | 仅单元素Series | 转换为索引:值字典 | 转换为值集合 | 转换为值元组 |
| PyTorch Tensor | 转换为嵌套列表 | 转换为列表字符串 | 仅标量张量 | 1D: 索引字典<br>ND: 包含shape、data的字典 | 仅1D张量 | 转换为嵌套元组 |
| xarray DataArray | 转换为嵌套列表 | 转换为列表字符串 | 仅标量DataArray | 包含shape、dtype、data、dims、coords的字典 | 仅1D DataArray | 转换为嵌套元组 |
| xarray Dataset | 包含变量字典的列表 | 转换为字典字符串 | 不支持 | 变量名:变量信息字典 | 不支持 | 包含变量字典的元组 |
| JAX 数组 | 转换为嵌套列表 | 转换为列表字符串 | 仅标量数组 | 1D: 索引字典<br>ND: 包含shape、dtype、data的字典 | 仅1D数组 | 转换为嵌套元组 |
| TensorFlow Tensor | 转换为嵌套列表 | 转换为列表字符串 | 仅标量张量 | 1D: 索引字典<br>ND: 包含shape、data的字典 | 仅1D张量 | 转换为嵌套元组 |

## 使用示例

### 方法一：直接使用 e2e_* 函数

```python
from e2e_type_converter import (
    e2e_list, e2e_str, e2e_int, e2e_float, e2e_dict, e2e_set, e2e_tuple
)

# 示例 1：基本类型转换
print(e2e_list(123))  # 输出: [123]
print(e2e_str(None))  # 输出: ""
print(e2e_int("123"))  # 输出: 123
print(e2e_float(True))  # 输出: 1.0

# 示例 2：容器类型转换
print(e2e_list({"a": 1, "b": 2}))  # 输出: [("a", 1), ("b", 2)]
print(e2e_dict([1, 2, 3]))  # 输出: {0: 1, 1: 2, 2: 3}
print(e2e_set("hello"))  # 输出: {'h', 'e', 'l', 'o'}

# 示例 3：双向转换
print(e2e_list(e2e_tuple([1, 2, 3])))  # 输出: [1, 2, 3]
print(e2e_dict(e2e_list({"a": 1, "b": 2})))  # 输出: {"a": 1, "b": 2}
```

### 方法二：使用 TypeConverter 类

```python
from e2e_type_converter import TypeConverter

# 示例
print(TypeConverter.to_list(123))  # 输出: [123]
print(TypeConverter.to_str(None))  # 输出: ""
print(TypeConverter.to_int("123"))  # 输出: 123
```

### 方法三：重命名为内置函数名使用

```python
from e2e_type_converter import (
    e2e_list, e2e_str, e2e_int, e2e_float, e2e_dict, e2e_set, e2e_tuple
)

# 重命名以便使用
list = e2e_list
str = e2e_str
int = e2e_int
float = e2e_float
dict = e2e_dict
set = e2e_set
tuple = e2e_tuple

# 现在可以像使用内置函数一样使用
print(list(123))  # 输出: [123]
print(str(None))  # 输出: ""
print(int("123"))  # 输出: 123
```

### 方法四：第三方库类型转换示例

```python
from e2e_type_converter import e2e_list, e2e_dict, e2e_tuple

# NumPy 数组转换示例
import numpy as np
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(e2e_list(arr))  # 输出: [[1, 2, 3], [4, 5, 6]]
print(e2e_dict(arr))  # 输出: {"shape": (2, 3), "dtype": "int32", "data": [[1, 2, 3], [4, 5, 6]]}
print(e2e_tuple(arr))  # 输出: ((1, 2, 3), (4, 5, 6))

# SciPy 稀疏矩阵转换示例
import scipy.sparse
sparse_mat = scipy.sparse.csr_matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
print(e2e_list(sparse_mat))  # 输出: [[1, 0, 0], [0, 2, 0], [0, 0, 3]]
```

### 方法五：第三方库类型互转示例

```python
from e2e_type_converter import TypeConverter

# NumPy 到 xarray 的转换
import numpy as np
numpy_arr = np.array([[1, 2, 3], [4, 5, 6]])
xarray_da = TypeConverter.numpy_to_xarray(numpy_arr)
print(xarray_da)  # 输出 xarray DataArray

# xarray 到 NumPy 的转换
converted_back = TypeConverter.xarray_to_numpy(xarray_da)
print(converted_back)  # 输出 numpy 数组

# 通用转换方法
import torch

# NumPy 到 PyTorch 的转换
torch_tensor = TypeConverter.convert(numpy_arr, 'torch')
print(torch_tensor)  # 输出 PyTorch Tensor

# PyTorch 到 pandas 的转换（通过通用方法）
pandas_df = TypeConverter.convert(torch_tensor, 'pandas')
print(pandas_df)  # 输出 pandas DataFrame

# 支持的转换方向
# 'numpy' <-> 'cupy' <-> 'scipy' <-> 'pandas' <-> 'torch' <-> 'xarray' <-> 'jax' <-> 'tensorflow'
```

## 注意事项

1. **类型安全**：对于不支持直接转换的类型组合，会抛出明确的 TypeError 或 ValueError 异常。

2. **边界情况**：
   - None 值会转换为对应类型的"空"值（如 []、""、0 等）
   - 布尔值会被转换为对应类型的逻辑值（如 int(True) → 1）

3. **性能优化**：
   - 类型检查顺序已优化，常见类型的检查优先级更高
   - 对于容器类型的单元素转换，会递归处理内部元素

4. **兼容性**：
   - 不直接修改内置函数，而是通过导入使用
   - 保留了原始内置函数的行为，仅在其基础上扩展

5. **限制**：
   - 对于多元素容器转换为数值类型（int/float），会抛出 TypeError
   - 对于不可哈希类型，不支持缓存机制

6. **第三方库支持**：
   - 第三方库支持采用懒加载方式，仅在实际使用时检测库是否安装
   - 对于 NumPy/CuPy 数组，仅支持标量数组转换为 int/float
   - 对于 NumPy/CuPy 数组和 SciPy 稀疏矩阵，仅支持 1D 类型转换为 set
   - 对于多维数组/矩阵，转换为 dict 时会包含 shape、dtype 和 data 信息

## 单元测试

项目包含完整的单元测试，覆盖所有标准类型之间的转换场景：

```bash
python test_e2e_type_converter.py
```

## 项目结构

```
everything2everything/
├── e2e_type_converter/  # 包目录
│   ├── __init__.py      # 模块导出和版本信息
│   └── core.py          # 核心实现文件
├── setup.py             # 包配置和依赖项
├── README.md            # 文档说明
├── test_e2e_type_converter.py  # 标准类型单元测试
└── test_third_party_types.py   # 第三方库类型单元测试
```

## 总结

本类型转换兼容层提供了一种简洁、灵活的方式来处理Python中的类型转换问题，特别是在处理不同类型数据交互的场景中。通过扩展内置转换函数的能力，它使得类型转换更加直观和符合开发者的直觉预期，同时保持了与Python原生语法的兼容性。