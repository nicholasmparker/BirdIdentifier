"""Setup script for the Bird Identifier API package.

This package provides a FastAPI service for identifying bird species in images
using TensorFlow Lite models.
"""
from setuptools import find_packages, setup

setup(
    name="birdidentifier",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
        "pillow==9.5.0",
        "numpy==1.24.3",
        "tflite-support==0.4.3",
        "python-dotenv>=1.0.0",
        "pydantic>=2.4.2",
        "pydantic-settings>=2.0.3",
    ],
)
