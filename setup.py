#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import itertools
import os
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def load_requirements_file(fp=None, **kwargs):
    """
    Returns a list of the dependencies specified in a requirements.txt file.

    Adapted from: http://stackoverflow.com/a/15341042

    :param fp: the path of the requirements.txt file to load.
    :param kwargs:
    :return: a list of strings.

    Usage Examples:

    setup(
        .....
        install_requires=load_requirements_file('requirements.txt')
    )

    setup(
        .....
        install_requires=['some_package'] + load_requirements_file('requirements.txt')
    )
    """
    if not fp:
        fp = 'requirements.txt'
    with open(fp) as f:
        # values = f.read().splitlines()
        values = [line for line in f.readlines()]
    # strip the values
    values = [i.strip() for i in values]
    # filter out comment lines
    values = [i for i in values if not i.startswith('#')]
    # evaluate/load inherited/hierarchical req files properly (e.g. lines like '-r req.txt')
    parent_files = [i[2:].strip() for i in values if i.startswith('-r ')]
    if len(parent_files):
        parent_files = [i[2:].strip() for i in values if i.startswith('-r ')]
        # evaluate each parent_file path relative to the folder of the current file (fp)
        cur_file = os.path.abspath(fp)
        cur_dir = os.path.split(cur_file)[0]
        parent_files = [os.path.join(cur_dir, f) for f in parent_files]
        # load (recursively) the reqs from each parent_file
        parent_values = itertools.chain([load_requirements_file(f) for f in parent_files])
        # merge the inherited reqs (from the parent_files) with the non-inherited ones
        values = [i for i in values if not i.startswith('-r ')]
        values = itertools.chain(values, parent_values)
    # filter out empty values
    values = [i for i in values if len(i)]
    # convert to a list instance
    values = list(values)
    return values


setup(
    name='clifundistro',
    version='0.1.0',
    license='BSD',
    description='A CLI-oriented Python playground for experiments and demonstrations of various kinds.',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Justin Webster',
    author_email='justinweb+gh@gmail.com',
    url='https://github.com/Justin-W/clifunland',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        'Topic :: Utilities',
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    install_requires=load_requirements_file('requirements.txt'),
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'clifunbin = clifunzone.cli:main',
        ]
    },
)
