from setuptools import setup, find_packages

install_requires = [
    'click>=7.0,<8.0'
]

setup(
    name='Hadopy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=install_requires
)
