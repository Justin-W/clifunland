#!/bin/bash
# tox.tests.sh

# Usage: bash ./tox.tests.sh

bash ./tox.sh --skip-missing-interpreters -eclean,py27,py35,report
