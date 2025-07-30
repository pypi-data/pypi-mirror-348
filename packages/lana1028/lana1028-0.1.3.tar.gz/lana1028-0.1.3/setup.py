from setuptools import setup, find_packages
import os

# Read the contents of README.md for long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="lana1028",
    version="0.1.3",
    author="Tristan",
    author_email="contactpgag@gmail.com",
    description="LANA-1028: A custom encryption algorithm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lana1028",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)
