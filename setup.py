#!/usr/bin/env python

import os
from io import open

from setuptools import find_packages, setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding='utf-8') as handle:
        return handle.read()


setup(
    name='django-people',
    version=__import__('people').__version__,
    description='Person model, mixins and helpers for Django',
    long_description=read('README.md'),
    author='Erik Stein',
    author_email='erik@classlibrary.net',
    url='https://github.com/sha-red/django-people/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(
        exclude=['tests', 'testapp']
    ),
    include_package_data=True,
    install_requires=[
        # 'Django>=1.9', commented out to make `pip install -U` easier
        'django-admin-steroids',
        'django-polymorphic',
        'django-shared-utils',
    ],
    dependency_links=[
        'git+https://github.com/sha-red/django-shared-utils.git#egg=django-shared-utils',
    ],
    extras_require={
        'all': [
        ],
    },
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
    zip_safe=False,
)
