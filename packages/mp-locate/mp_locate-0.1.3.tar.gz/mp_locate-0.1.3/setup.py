from setuptools import setup, find_packages
from pathlib import Path

# Lê o README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="mp_locate",
    version="0.1.3",
    description="A utility to recursively locate files by name.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
