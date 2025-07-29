# mp_locate/setup.py

from setuptools import setup, find_packages

setup(
    name="mp_locate",
    version="0.1.0",
    description="A utility to recursively locate files by name.",
    author="Eduardo Moreno Neto",
    author_email="eduardo.mmorenoneto@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)