from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cthulhucrypt",
    version="0.2.0",
    packages=find_packages(),
    description="An unholy encryption and hashing algorithm that defies brute force",
    author="null",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cthulhucrypt=cthulhucrypt.cli:cli"
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)