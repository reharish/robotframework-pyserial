from setuptools import setup
from setuptools import find_namespace_packages
from setuptools import find_packages
from os import path

setup(
    name='robotframework-pyserial',
    version='1.0.0',
    license="Apache License 2.0",
    url="https://reharish.github.io/cv",
    author='reharish',
    author_email='rengarajharish@gmail.com',
    packages=find_namespace_packages(),
    py_modules=['Serial'],
    install_requires=["robotframework", "pyserial"],
)
