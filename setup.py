# -*- coding: UTF-8 -*-
""""
Created on 03.12.21

:author:     Martin Dočekal
"""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open("requirements.txt") as f:
    REQUIREMENTS = f.read()

setup_args = dict(
    name='mag',
    version='0.9.0',
    description='Package for working with MAG dataset.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='The Unlicense',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    entry_points={
        'console_scripts': [
            'mag = mag.__main__:main'
        ]
    },
    author='Martin Dočekal',
    keywords=['dataset', 'MAG', 'MAG dataset'],
    url='https://github.com/mdocekal/mag',
    python_requires='>=3.8',
    install_requires=REQUIREMENTS.strip().split('\n')
)

if __name__ == '__main__':
    setup(**setup_args)
