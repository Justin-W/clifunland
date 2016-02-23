#!/bin/bash
# workspace.status.sh

# Usage: bash ./workspace.status.sh

source ./.init.sh

# see: http://stackoverflow.com/a/23342259
vecho() { echo "\$ $@" ; "$@" ; }


### determine the output file, path, etc.
OUTPUT_FILENAME=${1:-"$0.log"}
OUTPUT_FILEPATH=${SCRIPTS_OUTPUT_PATH}/${OUTPUT_FILENAME}
#create the output dir if it doesn't exist
[ ! -d ${SCRIPTS_OUTPUT_PATH} ] && mkdir -p ${SCRIPTS_OUTPUT_PATH}


### temporarily redirect stdout to the output file
#cache the current stdout (as FD #4)
exec 4<&1
#redirect stdout to the output file
exec 1>${OUTPUT_FILEPATH}


### generate the output file

#reset/empty any existing file
> ${OUTPUT_FILEPATH}

echo "###"
echo "### ENV variables (inactive virtualenv)"
echo "###"
echo ""
printenv

echo ""
echo "###"
echo "### SHELL variables (inactive virtualenv)"
echo "###"
echo ""
( set -o posix ; set ) | less

#source ./venv.activate.sh 1>/dev/null 2>> ${OUTPUT_FILEPATH}
source ./venv.activate.sh 1>/dev/null

echo ""

echo ""
echo "###"
echo "### ENV variables (active virtualenv)"
echo "###"
echo ""
printenv

echo ""
echo "###"
echo "### SHELL variables (active virtualenv)"
echo "###"
echo ""
( set -o posix ; set ) | less


echo ""
echo "###"
echo "### declare -f (active virtualenv)"
echo "###"
echo ""
declare -f


echo ""
echo "###"
echo "### Other ENV info (active virtualenv)"
echo "###"
echo ""

echo ""
echo "python:"
vecho type python
python --version 2>&1

echo ""
echo "python3:"
vecho type python3
python3 --version 2>&1

echo ""
echo "bash:"
type bash
bash --version

echo ""
echo "virtualenv:"
type virtualenv

echo ""
echo "pip:"
type pip
pip --version

echo ""
echo "brew:"
type brew
brew --version
echo "brew doctor:"
brew doctor 2>&1

echo ""
echo "brew cask:"
brew cask --version

echo ""
echo "xcode command line tools:"
xcode-select -p 1>/dev/null && echo 'xcode-select: installed' || \
    echo 'xcode-select: not installed (consider running "xcode-select --install")'
xcode-select -p 1>/dev/null && echo -n 'xcode-select location: ' && xcode-select -p

echo ""
echo "pkg-config:"
type pkg-config
pkg-config --version

echo ""
echo "git:"
type git
git --version

echo ""
echo "postgres:"
type postgres
postgres --version

echo ""
echo "createdb:"
type createdb

echo ""
echo "tox:"
type tox

echo ""
echo "java:"
vecho type java
vecho java -version 2>&1

echo ""
echo "Applications: IDEs:"
ls /Applications/ | grep -i -E 'intellij|IDEA|pycharm|eclipse|sublime|IDE|dev'

echo ""
echo "Applications: SCM:"
ls /Applications/ | grep -i -E 'git|hg|svn|bucket|Source|Code|scm|version'

echo ""
echo "Applications: DBs:"
ls /Applications/ | grep -i -E 'postgres|SQL|DB|database'

echo ""
echo "Applications: Browsers:"
ls /Applications/ | grep -i -E 'chrome|safari|firefox|opera|browse|web|internet'


### Clean Up

### un-redirect stdout
#restore stdout (using the previously cached FD)
exec 1<&4


### print the location of the output file
echo "Log file created at: ${OUTPUT_FILEPATH}"
open ${OUTPUT_FILEPATH}
