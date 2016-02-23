========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests & metrics
      - | |travis|
        | |coveralls| |codecov|
        | |requires| |landscape|
    * - docs
      - |docs|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/clifunland/badge/?style=flat
    :target: https://readthedocs.org/projects/clifunland
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/Justin-W/clifunland.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Justin-W/clifunland

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Justin-W/clifunland?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/Justin-W/clifunland

.. |requires| image:: https://requires.io/github/Justin-W/clifunland/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/Justin-W/clifunland/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/Justin-W/clifunland/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/Justin-W/clifunland

.. |codecov| image:: https://codecov.io/github/Justin-W/clifunland/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Justin-W/clifunland

.. |landscape| image:: https://landscape.io/github/Justin-W/clifunland/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Justin-W/clifunland/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/clifundistro.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/clifundistro

.. |downloads| image:: https://img.shields.io/pypi/dm/clifundistro.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/clifundistro

.. |wheel| image:: https://img.shields.io/pypi/wheel/clifundistro.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/clifundistro

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/clifundistro.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/clifundistro

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/clifundistro.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/clifundistro


.. end-badges

A CLI-oriented Python playground for experiments and demonstrations of various kinds.

* Free software: BSD license

Installation
============

::

    pip install clifundistro

Documentation
=============

https://clifunland.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
