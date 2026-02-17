from setuptools import setup, find_packages

setup(
    name="everything2everything",
    version="1.0.0",
    description="A Python package that can convert any standard Python type to a custom data type and vice versa",
    long_description="""EveryThing to EveryThing (E2E) is a Python package that provides a custom data type E2EType, which can wrap any standard Python type. It allows you to convert between Python standard types and the custom E2EType seamlessly.

Features:
- Convert any Python standard type to E2EType
- Convert E2EType back to original type
- Type checking capabilities
- Serialization support
- Timestamp tracking

Usage:
from e2e import to_e2e, from_e2e, E2EType

# Convert to E2EType
value_e2e = to_e2e("Hello, World!")

# Convert back to original type
original_value = from_e2e(value_e2e)
""",
    long_description_content_type="text/markdown",
    url="https://github.com/user/everything2everything",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[],
)
