from setuptools import setup, find_packages

setup(
    name="flip_qwen_backend",
    version="0.1.0",
    description="A lightweight SDK for accessing backend server pools",
    author="Hongwei Zhang",
    author_email="hongwei.zhang@flip.shop",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    python_requires=">=3.6",
)