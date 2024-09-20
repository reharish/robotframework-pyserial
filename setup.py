from setuptools import setup
from setuptools import find_namespace_packages
from setuptools import find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), "r") as fd:
    long_description = fd.read()

setup(
    name='robotframework-pyserial',
    version='1.3.0',
    description='Robotframework implementation of beloved pyserial module',
    license="Apache License 2.0",
    url="https://reharish.github.io/cv",
    author='reharish',
    author_email='rengarajharish@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    py_modules=['SerialLibrary'],
    install_requires=["robotframework", "pyserial"],
)
