"""性能测试脚本

This module contains performance tests for the e2e_type_converter library.
It tests conversion performance for various data types and scenarios.
"""

import time
import statistics
import sys
from typing import Callable, Any, List, Dict, Tuple
from functools import wraps
import gc
from datetime import datetime
import platform

# 尝试导入psutil获取系统信息
try:
    import psutil
except ImportError:
    print("Warning: psutil not installed, system info will be limited")
    psutil = None

try:
    from e2e_type_converter import (
        e2e_list, e2e_str, e2e_int, e2e_float, e2e_dict, e2e_set, e2e_tuple,
        TypeConverter
    )
except ImportError:
    print("Error: e2e_type_converter module not found")
    sys.exit(1)


class SystemInfo:
    """系统信息收集类"""
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """获取系统信息
        
        Returns:
            Dict[str, Any]: 系统信息字典
        """
        info = {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'architecture': platform.architecture(),
        }
        
        if psutil:
            # CPU信息
            info['cpu_count'] = psutil.cpu_count(logical=True)
            info['cpu_physical_count'] = psutil.cpu_count(logical=False)
            
            # 内存信息
            memory = psutil.virtual_memory()
            info['total_memory_gb'] = round(memory.total / (1024**3), 2)
            info['available_memory_gb'] = round(memory.available / (1024**3), 2)
            info['memory_percent'] = memory.percent
            
            # 磁盘信息
            try:
                disk = psutil.disk_usage('/')
                info['total_disk_gb'] = round(disk.total / (1024**3), 2)
                info['available_disk_gb'] = round(disk.available / (1024**3), 2)
                info['disk_percent'] = disk.percent
            except:
                # Windows系统使用C盘
                try:
                    disk = psutil.disk_usage('C:')
                    info['total_disk_gb'] = round(disk.total / (1024**3), 2)
                    info['available_disk_gb'] = round(disk.available / (1024**3), 2)
                    info['disk_percent'] = disk.percent
                except:
                    pass
        
        return info
    
    @staticmethod
    def print_system_info():
        """打印系统信息"""
        info = SystemInfo.get_system_info()
        print(f"\n{Colors.bold('='*60)}")
        print(f"{Colors.cyan('系统信息')}")
        print(f"{Colors.bold('='*60)}")
        
        print(f"平台: {info.get('platform', 'N/A')}")
        print(f"Python版本: {info.get('python_version', 'N/A')}")
        print(f"架构: {info.get('architecture', 'N/A')}")
        
        if 'cpu_count' in info:
            print(f"CPU核心数: {info['cpu_count']} (物理: {info['cpu_physical_count']})")
        
        if 'total_memory_gb' in info:
            print(f"内存: {info['total_memory_gb']} GB (可用: {info['available_memory_gb']} GB, {info['memory_percent']}% 使用)")
        
        if 'total_disk_gb' in info:
            print(f"磁盘: {info['total_disk_gb']} GB (可用: {info.get('available_disk_gb', 'N/A')} GB, {info.get('disk_percent', 'N/A')}% 使用)")
        
        print(f"{Colors.bold('='*60)}")


# ANSI颜色代码
class Colors:
    """终端颜色类"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def green(text):
        return f"{Colors.GREEN}{text}{Colors.END}"
    
    @staticmethod
    def yellow(text):
        return f"{Colors.YELLOW}{text}{Colors.END}"
    
    @staticmethod
    def red(text):
        return f"{Colors.RED}{text}{Colors.END}"
    
    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.END}"
    
    @staticmethod
    def cyan(text):
        return f"{Colors.CYAN}{text}{Colors.END}"
    
    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.END}"
    
    @staticmethod
    def grey(text):
        return f"\033[90m{text}{Colors.END}"


# 性能评级
class PerformanceRating:
    """性能评级类"""
    
    # 基准硬件性能得分
    BASE_HARDWARE_SCORE = 70.0
    
    @staticmethod
    def get_adjusted_thresholds(hardware_score: float) -> Dict[str, float]:
        """根据硬件性能得分调整阈值
        
        Args:
            hardware_score: 硬件性能得分 (0-100)
            
        Returns:
            Dict[str, float]: 调整后的阈值
        """
        # 计算性能缩放因子
        # 硬件得分越高，阈值越低（要求越高）
        scale_factor = max(0.5, min(2.0, PerformanceRating.BASE_HARDWARE_SCORE / hardware_score))
        
        return {
            'throughput_excellent': 1000000 * scale_factor,
            'throughput_good': 500000 * scale_factor,
            'throughput_medium': 100000 * scale_factor,
            'throughput_poor': 10000 * scale_factor,
            'time_excellent': 0.5 / scale_factor,
            'time_good': 1.0 / scale_factor,
            'time_medium': 5.0 / scale_factor,
            'time_poor': 10.0 / scale_factor
        }
    
    @staticmethod
    def get_rating(throughput: float, hardware_score: float = BASE_HARDWARE_SCORE) -> Tuple[str, str]:
        """根据吞吐量获取评级
        
        Args:
            throughput: 吞吐量 (ops/sec)
            hardware_score: 硬件性能得分 (0-100)
            
        Returns:
            Tuple[评级文本, 颜色函数]
        """
        thresholds = PerformanceRating.get_adjusted_thresholds(hardware_score)
        
        if throughput >= thresholds['throughput_excellent']:
            return "优秀 ⚡⚡⚡", Colors.green
        elif throughput >= thresholds['throughput_good']:
            return "良好 ⚡⚡", Colors.green
        elif throughput >= thresholds['throughput_medium']:
            return "中等 ⚡", Colors.yellow
        elif throughput >= thresholds['throughput_poor']:
            return "一般", Colors.yellow
        else:
            return "较慢", Colors.red
    
    @staticmethod
    def get_time_rating(avg_time_ms: float, hardware_score: float = BASE_HARDWARE_SCORE) -> Tuple[str, str]:
        """根据平均时间获取评级
        
        Args:
            avg_time_ms: 平均时间 (毫秒)
            hardware_score: 硬件性能得分 (0-100)
            
        Returns:
            Tuple[评级文本, 颜色函数]
        """
        thresholds = PerformanceRating.get_adjusted_thresholds(hardware_score)
        
        if avg_time_ms < thresholds['time_excellent']:
            return "极快 ⚡⚡⚡", Colors.green
        elif avg_time_ms < thresholds['time_good']:
            return "快速 ⚡⚡", Colors.green
        elif avg_time_ms < thresholds['time_medium']:
            return "正常 ⚡", Colors.yellow
        elif avg_time_ms < thresholds['time_poor']:
            return "一般", Colors.yellow
        else:
            return "较慢", Colors.red


class PerformanceTestResult:
    """性能测试结果类"""
    
    def __init__(self, test_name: str, iterations: int, hardware_score: float = PerformanceRating.BASE_HARDWARE_SCORE):
        self.test_name = test_name
        self.iterations = iterations
        self.hardware_score = hardware_score
        self.times: List[float] = []
        self.success_count = 0
        self.failure_count = 0
        self.errors: List[str] = []
    
    def add_time(self, time_ms: float):
        """添加一次测试的时间"""
        self.times.append(time_ms)
    
    def record_success(self):
        """记录成功"""
        self.success_count += 1
    
    def record_failure(self, error: str):
        """记录失败"""
        self.failure_count += 1
        self.errors.append(error)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        if not self.times:
            return {
                'test_name': self.test_name,
                'iterations': self.iterations,
                'success_count': self.success_count,
                'failure_count': self.failure_count,
                'error_rate': 0.0,
                'avg_time_ms': 0.0,
                'min_time_ms': 0.0,
                'max_time_ms': 0.0,
                'median_time_ms': 0.0,
                'std_dev_ms': 0.0,
                'throughput_ops_per_sec': 0.0,
                'hardware_score': self.hardware_score
            }
        
        return {
            'test_name': self.test_name,
            'iterations': self.iterations,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'error_rate': self.failure_count / self.iterations * 100,
            'avg_time_ms': statistics.mean(self.times),
            'min_time_ms': min(self.times),
            'max_time_ms': max(self.times),
            'median_time_ms': statistics.median(self.times),
            'std_dev_ms': statistics.stdev(self.times) if len(self.times) > 1 else 0.0,
            'throughput_ops_per_sec': 1000.0 / statistics.mean(self.times) if statistics.mean(self.times) > 0 else 0.0,
            'hardware_score': self.hardware_score
        }
    
    def print_summary(self):
        """打印测试摘要"""
        stats = self.get_statistics()
        
        # 获取评级
        rating_text, rating_color = PerformanceRating.get_rating(stats['throughput_ops_per_sec'], stats['hardware_score'])
        time_rating_text, time_rating_color = PerformanceRating.get_time_rating(stats['avg_time_ms'], stats['hardware_score'])
        
        print(f"\n{Colors.bold('='*60)}")
        print(f"{Colors.cyan('测试名称: ' + stats['test_name'])}")
        print(f"{Colors.bold('='*60)}")
        
        # 状态指示
        if stats['error_rate'] == 0:
            status = Colors.green("✓ 全部成功")
        elif stats['error_rate'] < 10:
            status = Colors.yellow(f"⚠ {stats['error_rate']:.1f}% 错误")
        else:
            status = Colors.red(f"✗ {stats['error_rate']:.1f}% 错误")
        
        print(f"状态: {status}")
        print(f"迭代次数: {stats['iterations']}")
        
        # 性能评级
        print(f"\n{Colors.bold('性能评级:')}")
        print(f"  吞吐量评级: {rating_color(rating_text)}")
        print(f"  响应时间评级: {time_rating_color(time_rating_text)}")
        
        print(f"\n{Colors.bold('时间统计 (毫秒):')}")
        print(f"  平均时间: {stats['avg_time_ms']:.6f}")
        print(f"  最小时间: {stats['min_time_ms']:.6f}")
        print(f"  最大时间: {stats['max_time_ms']:.6f}")
        print(f"  中位数: {stats['median_time_ms']:.6f}")
        print(f"  标准差: {stats['std_dev_ms']:.6f}")
        
        print(f"\n{Colors.bold('吞吐量:')}")
        print(f"  {stats['throughput_ops_per_sec']:,.2f} ops/sec")
        
        # 可视化条形图
        self._print_bar_chart(stats['throughput_ops_per_sec'], stats['hardware_score'])
        
        if self.errors:
            print(f"\n{Colors.red('错误信息 (前5个):')}")
            for error in self.errors[:5]:
                print(f"  - {error}")
        print(f"{Colors.bold('='*60)}\n")
    
    def _print_bar_chart(self, throughput: float, hardware_score: float):
        """打印性能条形图"""
        thresholds = PerformanceRating.get_adjusted_thresholds(hardware_score)
        max_throughput = thresholds['throughput_excellent'] * 3  # 以优秀阈值的3倍作为最大值
        bar_length = min(int(throughput / max_throughput * 40), 40)
        
        if throughput >= thresholds['throughput_excellent']:
            color = Colors.green
        elif throughput >= thresholds['throughput_good']:
            color = Colors.green
        elif throughput >= thresholds['throughput_medium']:
            color = Colors.yellow
        else:
            color = Colors.red
        
        bar = color('█' * bar_length) + Colors.grey('░' * (40 - bar_length))
        print(f"  性能条: [{bar}]")
        print(f"         0                    {thresholds['throughput_excellent']/1000000:.1f}M                    {thresholds['throughput_excellent']*2/1000000:.1f}M                    {thresholds['throughput_excellent']*3/1000000:.1f}M ops/sec")


class BenchmarkTest:
    """基准测试类"""
    
    @staticmethod
    def run_benchmark() -> Dict[str, float]:
        """运行基准测试
        
        Returns:
            Dict[str, float]: 基准测试结果
        """
        print(f"\n{Colors.bold('='*60)}")
        print(f"{Colors.cyan('运行系统基准测试')}")
        print(f"{Colors.bold('='*60)}")
        
        benchmarks = {}
        
        # 整数运算基准
        start_time = time.perf_counter()
        for i in range(1000000):
            _ = i * i
        end_time = time.perf_counter()
        benchmarks['integer_operations'] = (end_time - start_time) * 1000
        
        # 浮点运算基准
        start_time = time.perf_counter()
        for i in range(1000000):
            _ = i ** 0.5
        end_time = time.perf_counter()
        benchmarks['float_operations'] = (end_time - start_time) * 1000
        
        # 字符串操作基准
        start_time = time.perf_counter()
        s = ""
        for i in range(10000):
            s += str(i)
        end_time = time.perf_counter()
        benchmarks['string_operations'] = (end_time - start_time) * 1000
        
        # 列表操作基准
        start_time = time.perf_counter()
        lst = []
        for i in range(100000):
            lst.append(i)
        end_time = time.perf_counter()
        benchmarks['list_operations'] = (end_time - start_time) * 1000
        
        print(f"整数运算: {benchmarks['integer_operations']:.2f} ms")
        print(f"浮点运算: {benchmarks['float_operations']:.2f} ms")
        print(f"字符串操作: {benchmarks['string_operations']:.2f} ms")
        print(f"列表操作: {benchmarks['list_operations']:.2f} ms")
        
        # 计算总体性能得分
        total_score = sum(benchmarks.values())
        benchmarks['total_score'] = total_score
        
        print(f"\n总体基准得分: {total_score:.2f} ms (越低越好)")
        print(f"{Colors.bold('='*60)}")
        
        return benchmarks
    
    @staticmethod
    def get_hardware_score() -> float:
        """获取硬件性能得分
        
        Returns:
            float: 硬件性能得分 (0-100)
        """
        benchmarks = BenchmarkTest.run_benchmark()
        total_score = benchmarks['total_score']
        
        # 性能得分映射 (基于经验值)
        # 得分越高表示性能越好
        if total_score < 100:
            return 90 + (100 - total_score) / 100 * 10
        elif total_score < 200:
            return 70 + (200 - total_score) / 100 * 20
        elif total_score < 400:
            return 50 + (400 - total_score) / 200 * 20
        elif total_score < 800:
            return 30 + (800 - total_score) / 400 * 20
        else:
            return max(10, 30 - (total_score - 800) / 400 * 20)


class ProgressBar:
    """进度条类"""
    
    def __init__(self, total: int, prefix: str = "进度"):
        self.total = total
        self.current = 0
        self.prefix = prefix
    
    def update(self, increment: int = 1):
        """更新进度"""
        self.current += increment
        self._print()
    
    def _print(self):
        """打印进度条"""
        percent = self.current / self.total
        bar_length = 30
        filled = int(bar_length * percent)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r{self.prefix}: [{bar}] {percent:.1%} ({self.current}/{self.total})", end='', flush=True)
    
    def finish(self):
        """完成进度"""
        self.current = self.total
        self._print()
        print()


def measure_time(func: Callable) -> Callable:
    """测量函数执行时间的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, (end_time - start_time) * 1000
    return wrapper


def run_performance_test(test_name: str, test_func: Callable, iterations: int = 1000, 
                        warmup_iterations: int = 100, hardware_score: float = PerformanceRating.BASE_HARDWARE_SCORE) -> PerformanceTestResult:
    """运行性能测试
    
    Args:
        test_name: 测试名称
        test_func: 测试函数
        iterations: 测试迭代次数
        warmup_iterations: 预热迭代次数
        hardware_score: 硬件性能得分
    
    Returns:
        PerformanceTestResult: 性能测试结果
    """
    result = PerformanceTestResult(test_name, iterations, hardware_score)
    
    print(f"{Colors.cyan(f'开始测试: {test_name}')}")
    print(f"预热迭代: {warmup_iterations} 次")
    
    # 预热阶段
    for i in range(warmup_iterations):
        try:
            test_func()
        except Exception as e:
            pass
    
    gc.collect()
    
    print(f"正式测试: {iterations} 次")
    
    # 正式测试
    progress = ProgressBar(iterations, "测试进度")
    for i in range(iterations):
        try:
            _, exec_time = measure_time(test_func)()
            result.add_time(exec_time)
            result.record_success()
        except Exception as e:
            result.record_failure(str(e))
        progress.update()
    progress.finish()
    
    return result


class BasicTypePerformanceTests:
    """基本类型转换性能测试"""
    
    @staticmethod
    def test_int_to_list():
        """测试 int 转 list 性能"""
        return e2e_list(123)
    
    @staticmethod
    def test_str_to_list():
        """测试 str 转 list 性能"""
        return e2e_list("hello world")
    
    @staticmethod
    def test_int_to_str():
        """测试 int 转 str 性能"""
        return e2e_str(123)
    
    @staticmethod
    def test_none_to_str():
        """测试 None 转 str 性能"""
        return e2e_str(None)
    
    @staticmethod
    def test_str_to_int():
        """测试 str 转 int 性能"""
        return e2e_int("123456")
    
    @staticmethod
    def test_float_to_int():
        """测试 float 转 int 性能"""
        return e2e_int(123.456)
    
    @staticmethod
    def test_int_to_float():
        """测试 int 转 float 性能"""
        return e2e_float(123)
    
    @staticmethod
    def test_bool_to_float():
        """测试 bool 转 float 性能"""
        return e2e_float(True)


class ContainerTypePerformanceTests:
    """容器类型转换性能测试"""
    
    @staticmethod
    def test_list_to_tuple():
        """测试 list 转 tuple 性能"""
        return e2e_tuple([1, 2, 3, 4, 5])
    
    @staticmethod
    def test_tuple_to_list():
        """测试 tuple 转 list 性能"""
        return e2e_list((1, 2, 3, 4, 5))
    
    @staticmethod
    def test_list_to_dict():
        """测试 list 转 dict 性能"""
        return e2e_dict([1, 2, 3, 4, 5])
    
    @staticmethod
    def test_dict_to_list():
        """测试 dict 转 list 性能"""
        return e2e_list({'a': 1, 'b': 2, 'c': 3})
    
    @staticmethod
    def test_list_to_set():
        """测试 list 转 set 性能"""
        return e2e_set([1, 2, 3, 4, 5])
    
    @staticmethod
    def test_str_to_set():
        """测试 str 转 set 性能"""
        return e2e_set("hello")


class LargeDataPerformanceTests:
    """大数据量转换性能测试"""
    
    @staticmethod
    def test_large_list_to_tuple():
        """测试大 list 转 tuple 性能"""
        return e2e_tuple(list(range(1000)))
    
    @staticmethod
    def test_large_str_to_list():
        """测试大 str 转 list 性能"""
        return e2e_list("a" * 10000)
    
    @staticmethod
    def test_large_dict_to_list():
        """测试大 dict 转 list 性能"""
        return e2e_list({i: i*2 for i in range(500)})
    
    @staticmethod
    def test_nested_list_conversion():
        """测试嵌套 list 转换性能"""
        return e2e_list([[i, i+1, i+2] for i in range(100)])


class ThirdPartyTypePerformanceTests:
    """第三方库类型转换性能测试"""
    
    @staticmethod
    def test_numpy_to_list():
        """测试 numpy 数组转 list 性能"""
        try:
            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            return e2e_list(arr)
        except ImportError:
            raise ImportError("numpy not available")
    
    @staticmethod
    def test_numpy_to_dict():
        """测试 numpy 数组转 dict 性能"""
        try:
            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])
            return e2e_dict(arr)
        except ImportError:
            raise ImportError("numpy not available")
    
    @staticmethod
    def test_pandas_to_list():
        """测试 pandas Series 转 list 性能"""
        try:
            import pandas as pd
            s = pd.Series([1, 2, 3, 4, 5])
            return e2e_list(s)
        except ImportError:
            raise ImportError("pandas not available")
    
    @staticmethod
    def test_torch_to_list():
        """测试 torch Tensor 转 list 性能"""
        try:
            import torch
            t = torch.tensor([1, 2, 3, 4, 5])
            return e2e_list(t)
        except ImportError:
            raise ImportError("torch not available")


class CachePerformanceTests:
    """缓存机制性能测试"""
    
    @staticmethod
    def test_cache_hit():
        """测试缓存命中性能"""
        return e2e_str(123456789)
    
    @staticmethod
    def test_cache_miss():
        """测试缓存未命中性能"""
        import random
        return e2e_str(random.randint(1000000, 9999999))


def print_summary_table(all_results: List[PerformanceTestResult]):
    """打印汇总表格"""
    print(f"\n\n{Colors.bold('='*80)}")
    print(f"{Colors.cyan('性能测试汇总报告')}")
    print(f"{Colors.bold('='*80)}")
    
    print(f"\n{Colors.bold('测试名称'):<30} {Colors.bold('平均时间(ms)'):<15} {Colors.bold('吞吐量(ops/s)'):<20} {Colors.bold('评级'):<15} {Colors.bold('错误率')}")
    print("-"*95)
    
    for result in all_results:
        stats = result.get_statistics()
        rating_text, rating_color = PerformanceRating.get_rating(stats['throughput_ops_per_sec'], stats['hardware_score'])
        
        # 格式化吞吐量
        if stats['throughput_ops_per_sec'] >= 1000000:
            throughput_str = f"{stats['throughput_ops_per_sec']/1000000:.2f}M"
        elif stats['throughput_ops_per_sec'] >= 1000:
            throughput_str = f"{stats['throughput_ops_per_sec']/1000:.2f}K"
        else:
            throughput_str = f"{stats['throughput_ops_per_sec']:.2f}"
        
        # 错误率颜色
        if stats['error_rate'] == 0:
            error_rate_str = Colors.green(f"{stats['error_rate']:.1f}%")
        elif stats['error_rate'] < 10:
            error_rate_str = Colors.yellow(f"{stats['error_rate']:.1f}%")
        else:
            error_rate_str = Colors.red(f"{stats['error_rate']:.1f}%")
        
        print(f"{stats['test_name']:<30} {stats['avg_time_ms']:<15.6f} {throughput_str:<20} {rating_color(rating_text):<15} {error_rate_str}")
    
    print("="*95)


class PersonalizedPerformanceEvaluator:
    """个性化性能评价器"""
    
    @staticmethod
    def evaluate_performance(all_results: List[PerformanceTestResult], hardware_score: float) -> Dict[str, Any]:
        """评估性能并生成个性化评价
        
        Args:
            all_results: 所有测试结果
            hardware_score: 硬件性能得分
            
        Returns:
            Dict[str, Any]: 个性化评价结果
        """
        if not all_results:
            return {}
        
        # 计算整体性能指标
        total_tests = len(all_results)
        successful_tests = sum(1 for r in all_results if r.get_statistics()['error_rate'] == 0)
        avg_throughput = statistics.mean([r.get_statistics()['throughput_ops_per_sec'] for r in all_results])
        
        # 计算性能评级分布（基于调整后的阈值）
        excellent = 0
        good = 0
        medium = 0
        poor = 0
        
        for result in all_results:
            stats = result.get_statistics()
            rating_text, _ = PerformanceRating.get_rating(stats['throughput_ops_per_sec'], hardware_score)
            if "优秀" in rating_text:
                excellent += 1
            elif "良好" in rating_text:
                good += 1
            elif "中等" in rating_text:
                medium += 1
            else:
                poor += 1
        
        # 生成个性化评价
        evaluation = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests / total_tests) * 100,
            'avg_throughput': avg_throughput,
            'performance_distribution': {
                'excellent': excellent,
                'good': good,
                'medium': medium,
                'poor': poor
            }
        }
        
        # 基于硬件性能和测试结果生成评价文本
        evaluation['personalized_comment'] = PersonalizedPerformanceEvaluator._generate_comment(evaluation, hardware_score)
        
        return evaluation
    
    @staticmethod
    def _generate_comment(evaluation: Dict[str, Any], hardware_score: float) -> str:
        """生成个性化评价文本
        
        Args:
            evaluation: 评价结果
            hardware_score: 硬件性能得分
            
        Returns:
            str: 评价文本
        """
        success_rate = evaluation['success_rate']
        avg_throughput = evaluation['avg_throughput']
        excellent_count = evaluation['performance_distribution']['excellent']
        total_tests = evaluation['total_tests']
        
        # 基于硬件得分的评价
        if hardware_score >= 90:
            hardware_comment = "您的硬件性能非常出色，属于高端配置"
        elif hardware_score >= 70:
            hardware_comment = "您的硬件性能良好，属于中高端配置"
        elif hardware_score >= 50:
            hardware_comment = "您的硬件性能一般，属于中端配置"
        elif hardware_score >= 30:
            hardware_comment = "您的硬件性能较低，属于入门级配置"
        else:
            hardware_comment = "您的硬件性能较差，可能会影响测试结果"
        
        # 基于测试结果的评价
        if success_rate == 100:
            success_comment = "所有测试都成功完成，没有任何错误"
        elif success_rate >= 90:
            success_comment = "大部分测试都成功完成，只有少量错误"
        else:
            success_comment = "测试中出现了较多错误，建议检查代码"
        
        # 基于性能分布的评价
        excellent_ratio = excellent_count / total_tests
        if excellent_ratio >= 0.8:
            performance_comment = "性能表现非常优秀，大部分测试都达到了优秀水平"
        elif excellent_ratio >= 0.5:
            performance_comment = "性能表现良好，超过一半的测试达到了优秀水平"
        elif excellent_ratio >= 0.2:
            performance_comment = "性能表现一般，有部分测试达到了优秀水平"
        else:
            performance_comment = "性能表现有待提升，只有少数测试达到了优秀水平"
        
        # 综合评价
        if hardware_score >= 70 and success_rate == 100 and excellent_ratio >= 0.8:
            overall_comment = "总体评价：非常优秀！您的系统配置和e2e_type_converter库的性能表现都非常出色。"
        elif hardware_score >= 50 and success_rate >= 90 and excellent_ratio >= 0.5:
            overall_comment = "总体评价：良好！您的系统配置和e2e_type_converter库的性能表现都不错。"
        elif hardware_score >= 30 and success_rate >= 70:
            overall_comment = "总体评价：一般！您的系统配置和e2e_type_converter库的性能表现基本满足需求。"
        else:
            overall_comment = "总体评价：需要改进！您的系统配置或e2e_type_converter库的性能表现存在一些问题。"
        
        return f"{hardware_comment}。{success_comment}。{performance_comment}。{overall_comment}"
    
    @staticmethod
    def print_personalized_evaluation(all_results: List[PerformanceTestResult], hardware_score: float):
        """打印个性化性能评价"""
        evaluation = PersonalizedPerformanceEvaluator.evaluate_performance(all_results, hardware_score)
        
        print(f"\n\n{Colors.bold('='*80)}")
        print(f"{Colors.cyan('个性化性能评价')}")
        print(f"{Colors.bold('='*80)}")
        
        print(f"\n{Colors.bold('硬件性能得分:')} {hardware_score:.1f}/100")
        print(f"{Colors.bold('成功测试率:')} {evaluation['success_rate']:.1f}%")
        print(f"{Colors.bold('平均吞吐量:')} {evaluation['avg_throughput']:,.2f} ops/sec")
        
        print(f"\n{Colors.bold('性能分布:')}")
        print(f"  优秀: {Colors.green(str(evaluation['performance_distribution']['excellent']))}")
        print(f"  良好: {Colors.green(str(evaluation['performance_distribution']['good']))}")
        print(f"  中等: {Colors.yellow(str(evaluation['performance_distribution']['medium']))}")
        print(f"  一般: {Colors.red(str(evaluation['performance_distribution']['poor']))}")
        
        print(f"\n{Colors.bold('个性化评价:')}")
        print(f"  {evaluation['personalized_comment']}")
        
        print(f"\n{Colors.bold('='*80)}")


def print_overall_statistics(all_results: List[PerformanceTestResult]):
    """打印总体统计"""
    print(f"\n\n{Colors.bold('='*60)}")
    print(f"{Colors.cyan('总体统计')}")
    print(f"{Colors.bold('='*60)}")
    
    total_tests = len(all_results)
    successful_tests = sum(1 for r in all_results if r.get_statistics()['error_rate'] == 0)
    failed_tests = total_tests - successful_tests
    
    avg_throughput = statistics.mean([r.get_statistics()['throughput_ops_per_sec'] for r in all_results])
    max_throughput = max(r.get_statistics()['throughput_ops_per_sec'] for r in all_results)
    min_throughput = min(r.get_statistics()['throughput_ops_per_sec'] for r in all_results)
    
    print(f"\n总测试数: {total_tests}")
    print(f"成功测试: {Colors.green(str(successful_tests))}")
    print(f"失败测试: {Colors.red(str(failed_tests))}")
    print(f"\n平均吞吐量: {avg_throughput:,.2f} ops/sec")
    print(f"最高吞吐量: {Colors.green(f'{max_throughput:,.2f} ops/sec')}")
    print(f"最低吞吐量: {Colors.red(f'{min_throughput:,.2f} ops/sec')}")
    
    # 性能分布
    excellent = 0
    good = 0
    medium = 0
    poor = 0
    
    # 获取第一个结果的硬件得分作为参考
    hardware_score = all_results[0].hardware_score if all_results else PerformanceRating.BASE_HARDWARE_SCORE
    
    for result in all_results:
        stats = result.get_statistics()
        rating_text, _ = PerformanceRating.get_rating(stats['throughput_ops_per_sec'], hardware_score)
        if "优秀" in rating_text:
            excellent += 1
        elif "良好" in rating_text:
            good += 1
        elif "中等" in rating_text:
            medium += 1
        else:
            poor += 1
    
    print(f"\n性能分布:")
    print(f"  优秀: {Colors.green(str(excellent))}")
    print(f"  良好: {Colors.green(str(good))}")
    print(f"  中等: {Colors.yellow(str(medium))}")
    print(f"  一般: {Colors.red(str(poor))}")
    
    print(f"\n{Colors.bold('='*60)}")


def run_all_tests():
    """运行所有性能测试"""
    print(f"{Colors.bold('='*60)}")
    print(f"{Colors.cyan('E2E Type Converter 性能测试套件')}")
    print(f"{Colors.bold('='*60)}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 打印系统信息
    SystemInfo.print_system_info()
    
    # 运行基准测试获取硬件性能得分
    hardware_score = BenchmarkTest.get_hardware_score()
    print(f"\n{Colors.bold('硬件性能得分:')} {hardware_score:.1f}/100")
    
    all_results = []
    
    # 基本类型测试
    print(f"\n\n{Colors.bold('【基本类型转换性能测试】')}")
    print("-"*60)
    
    basic_tests = [
        ("int -> list", BasicTypePerformanceTests.test_int_to_list),
        ("str -> list", BasicTypePerformanceTests.test_str_to_list),
        ("int -> str", BasicTypePerformanceTests.test_int_to_str),
        ("None -> str", BasicTypePerformanceTests.test_none_to_str),
        ("str -> int", BasicTypePerformanceTests.test_str_to_int),
        ("float -> int", BasicTypePerformanceTests.test_float_to_int),
        ("int -> float", BasicTypePerformanceTests.test_int_to_float),
        ("bool -> float", BasicTypePerformanceTests.test_bool_to_float),
    ]
    
    for test_name, test_func in basic_tests:
        result = run_performance_test(test_name, test_func, iterations=10000, warmup_iterations=100, hardware_score=hardware_score)
        result.print_summary()
        all_results.append(result)
    
    # 容器类型测试
    print(f"\n\n{Colors.bold('【容器类型转换性能测试】')}")
    print("-"*60)
    
    container_tests = [
        ("list -> tuple", ContainerTypePerformanceTests.test_list_to_tuple),
        ("tuple -> list", ContainerTypePerformanceTests.test_tuple_to_list),
        ("list -> dict", ContainerTypePerformanceTests.test_list_to_dict),
        ("dict -> list", ContainerTypePerformanceTests.test_dict_to_list),
        ("list -> set", ContainerTypePerformanceTests.test_list_to_set),
        ("str -> set", ContainerTypePerformanceTests.test_str_to_set),
    ]
    
    for test_name, test_func in container_tests:
        result = run_performance_test(test_name, test_func, iterations=10000, warmup_iterations=100, hardware_score=hardware_score)
        result.print_summary()
        all_results.append(result)
    
    # 大数据量测试
    print(f"\n\n{Colors.bold('【大数据量转换性能测试】')}")
    print("-"*60)
    
    large_data_tests = [
        ("large list -> tuple", LargeDataPerformanceTests.test_large_list_to_tuple),
        ("large str -> list", LargeDataPerformanceTests.test_large_str_to_list),
        ("large dict -> list", LargeDataPerformanceTests.test_large_dict_to_list),
        ("nested list conversion", LargeDataPerformanceTests.test_nested_list_conversion),
    ]
    
    for test_name, test_func in large_data_tests:
        result = run_performance_test(test_name, test_func, iterations=1000, warmup_iterations=10, hardware_score=hardware_score)
        result.print_summary()
        all_results.append(result)
    
    # 第三方库类型测试
    print(f"\n\n{Colors.bold('【第三方库类型转换性能测试】')}")
    print("-"*60)
    
    third_party_tests = [
        ("numpy -> list", ThirdPartyTypePerformanceTests.test_numpy_to_list),
        ("numpy -> dict", ThirdPartyTypePerformanceTests.test_numpy_to_dict),
        ("pandas -> list", ThirdPartyTypePerformanceTests.test_pandas_to_list),
        ("torch -> list", ThirdPartyTypePerformanceTests.test_torch_to_list),
    ]
    
    for test_name, test_func in third_party_tests:
        try:
            result = run_performance_test(test_name, test_func, iterations=1000, warmup_iterations=10, hardware_score=hardware_score)
            result.print_summary()
            all_results.append(result)
        except ImportError as e:
            print(f"{Colors.yellow(f'跳过测试 {test_name}: {e}')}")
    
    # 缓存性能测试
    print(f"\n\n{Colors.bold('【缓存机制性能测试】')}")
    print("-"*60)
    
    cache_tests = [
        ("cache hit", CachePerformanceTests.test_cache_hit),
        ("cache miss", CachePerformanceTests.test_cache_miss),
    ]
    
    for test_name, test_func in cache_tests:
        result = run_performance_test(test_name, test_func, iterations=10000, warmup_iterations=100, hardware_score=hardware_score)
        result.print_summary()
        all_results.append(result)
    
    # 生成汇总报告
    print_summary_table(all_results)
    print_overall_statistics(all_results)
    
    # 打印个性化性能评价
    if all_results:
        PersonalizedPerformanceEvaluator.print_personalized_evaluation(all_results, hardware_score)
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Colors.bold('='*60)}")
    
    return all_results


if __name__ == "__main__":
    results = run_all_tests()
