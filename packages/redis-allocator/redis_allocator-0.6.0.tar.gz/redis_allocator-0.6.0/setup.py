#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for redis-allocator."""
from setuptools import setup, find_packages

_version = {}
with open('redis_allocator/_version.py', 'r', encoding='utf-8') as f:
    exec(f.read(), _version)  # pylint: disable=exec-used
    __version__ = _version['__version__']


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

tests_require = [
    'pytest >= 7.4.3',
    'pytest-cov >= 4.1.0',
    'pytest-mock >= 3.12.0',
    'fakeredis[lua] >= 2.20.1',
    'flake8 >= 6.1.0',
    'freezegun >= 1.4.0',
]

docs_require = [
    'sphinx >= 7.0.0',
    'sphinx-rtd-theme >= 1.3.0',
    'sphinx-git >= 11.0.0',
    'sphinxcontrib-mermaid >= 0.7.1',
]

setup(
    name='redis-allocator',
    # dev[n] .alpha[n] .beta[n] .rc[n] .post[n] .final
    version=__version__,
    author='Invoker Bot',
    author_email='invoker-bot@outlook.com',
    description='Redis-based resource allocation system.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/invoker-bot/RedisAllocator-python',
    packages=find_packages(),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.10',
    install_requires=[
        'redis >= 5.0.0',
        'cachetools >= 5.3.2',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'docs': docs_require,
        'dev': tests_require + docs_require,
    },
    license='MIT',
)
