#!/usr/bin/env python

from io import open
from setuptools import find_packages, setup
import os
import re
import subprocess


"""
Use `git tag 1.0.0` to tag a release; `python setup.py --version`
to update the  _version.py file.
"""


def get_version(prefix):
    if os.path.exists('.git'):
        parts = subprocess.check_output(['git', 'describe', '--tags']).decode().strip().split('-')
        if len(parts) == 3:
            version = '{}.{}+{}'.format(*parts)
        else:
            version = parts[0]
        version_py = "__version__ = '{}'".format(version)
        _version = os.path.join(prefix, '_version.py')
        if not os.path.exists(_version) or open(_version).read().strip() != version_py:
            with open(_version, 'w') as fd:
                fd.write(version_py)
        return version
    else:
        for f in ('_version.py', '__init__.py'):
            f = os.path.join(prefix, f)
            if os.path.exists(f):
                with open(f) as fd:
                    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fd.read()))
                if 'version' in metadata:
                    break
    return metadata['version']


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding='utf-8') as handle:
        return handle.read()


setup(
    name='django-shared-people',
    version=get_version('shared/people'),
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
    namespace_packages=['shared'],
    include_package_data=True,
    install_requires=[
        # 'Django>=1.9', commented out to make `pip install -U` easier
        # 'django-admin-steroids', #  Optional
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
