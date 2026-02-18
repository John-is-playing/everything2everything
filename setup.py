from setuptools import setup, find_packages
import os

# 读取README.md内容作为长描述
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="e2e-type-converter",
    version="1.0.0",
    description="Python类型转换兼容层，支持所有标准数据类型和第三方库类型之间的双向转换",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Trae AI",
    author_email="trae@example.com",
    url="https://github.com/trae-ai/everything2everything",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 核心功能无强制依赖，第三方库为可选
    ],
    extras_require={
        "full": [
            "numpy",
            "cupy",
            "scipy",
            "pandas",
            "torch",
            "xarray",
            "jax",
            "tensorflow",
        ],
        "numpy": ["numpy"],
        "pandas": ["pandas", "numpy"],
        "torch": ["torch"],
        "xarray": ["xarray", "numpy"],
        "scientific": ["numpy", "scipy", "pandas"],
    },
    keywords="type converter, data type, python, numpy, torch, xarray, jax, tensorflow",
    project_urls={
        "Bug Tracker": "https://github.com/trae-ai/everything2everything/issues",
        "Documentation": "https://github.com/trae-ai/everything2everything/wiki",
        "Source Code": "https://github.com/trae-ai/everything2everything",
    },
)