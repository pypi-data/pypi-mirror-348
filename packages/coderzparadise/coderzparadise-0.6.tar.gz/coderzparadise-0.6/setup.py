# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

long_description = """https://github.com/coderzparadise/coderzparadise 

https://www.youtube.com/@CoderzParadise"""

setup(
    name='coderzparadise',
    version='0.6',
    description='A package by CoderzParadise that makes using Data Structures easy for children, adults and AI.',
    author='Coderz Paradise',
    author_email='coderzparadise@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('src'),
    install_requires=[
        'numpy'
    ],
    keywords=['python', 'coderzparadise', 'coderz paradise', 'data struct', 'data structures', 'LinkedList', 'Graph'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)



