# setup.py

from setuptools import setup, find_packages

setup(
    name="zerofl",
    version="0.1.2",  # ← Increment version if updating
    packages=["myzero"],
    description="A lightweight, production-ready micro web framework in Python.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)