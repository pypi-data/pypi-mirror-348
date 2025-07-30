"""
Minimal setup configuration for PyPI deployment.
This configuration avoids the license-file metadata issue.
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="itensorpy",
    version="0.3.1",
    author="iTensorPy Team",
    author_email="claudiuswebdesign@gmail.com",
    description="A Python package for tensor calculations in general relativity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Klaudiusz321/itensorpy",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sympy>=1.7.1",
        "numpy>=1.19.0",
    ],
) 