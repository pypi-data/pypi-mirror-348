# aiccl/setup.py

from setuptools import setup, find_packages

setup(
    name="aiccl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "numpy",
    ],
    description="Lightweight agent framework with multiple LLM providers and tools",
)