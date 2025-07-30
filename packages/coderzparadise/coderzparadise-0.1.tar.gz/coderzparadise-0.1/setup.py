# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='coderzparadise',
    version='0.1',
    description='A package by CoderzParadise that makes using Data Structures easy for children, adults and AI.',
    author='Coderz Paradise',
    author_email='coderzparadise@gmail.com',
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



