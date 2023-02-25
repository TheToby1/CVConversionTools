from setuptools import find_packages, setup

setup(
    name='MistletoeExtensions',
    packages=find_packages(include=['mistletoe_extensions']),
    version='0.1.0',
    description='A set of mistletoe extensions for rendering a moderncv or blazor file from markdown.',
    author='Tobias Burns',
    license='MIT',
    install_requires=['mistletoe', 'json5']
)