#!/bin/bash

# Purpose:
#   - make sure we can install some packages
#   - make sure we can change the directory
#   - change the prebuild, build and postbuild commands

# set -xe

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

# Cleanup before the test
rm -f ${CURDIR}/greeting

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_DEPENDENCIES='htop mc' \
    -e INPUT_DIRECTORY='/' \
    -e INPUT_PREBUILD_COMMAND='pwd; ls' \
    -e INPUT_BUILD_COMMAND='echo "Hello, world!" > /github/workspace/greeting' \
    -e INPUT_POSTBUILD_COMMAND='ls /github/workspace' \
    lucteo/action-cxx-toolkit.main

# Check if the test succeeded
if [ -f ${CURDIR}/greeting ]; then
    rm -f ${CURDIR}/greeting
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi
