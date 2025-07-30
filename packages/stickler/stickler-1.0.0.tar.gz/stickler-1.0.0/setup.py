from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='stickler', # name of packe which will be package dir below project
    version='1.0.0',
    url='https://github.com/ginacassin/stickler',
    author='Gina Cassin',
    author_email='ginacassin47@gmail.com',
    description='PySpark ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pyspark>=3.5.4', 'pydantic>=2.10.6'],
)