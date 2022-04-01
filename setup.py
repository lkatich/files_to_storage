from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='files_to_storage',
    version='1.1',
    packages=find_packages(),
    install_requires=['pyyaml', 'psutil'],
    long_description=open(join(dirname(__file__), 'README.md')).read()
)