#!/bin/bash
# tox.sh

# Usage: bash ./tox.sh

#MINPARAMS=1
#if [ $# -lt "$MINPARAMS" ]
#then
#    echo
#    echo "This script needs at least $MINPARAMS command-line arguments!"
#fi

source ./.init.sh
source ./venv.activate.sh

cd ${REPO_PATH}

if [ -n "$1" ]
then
    #tox "$*"
    tox "$@"
else
    tox
fi
