from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stickler',
    version='1.0.5',
    url='https://github.com/ginacassin/stickler',
    author='Gina Cassin',
    description='PySpark rule engine for data validation and transformation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['stickler','stickler.*']),
    install_requires=['pyspark>=3.5.0', 'pydantic>=2.10.6'],
    package_data={'.' : ['Makefile']}
)