#!/bin/bash

# Purpose: a simple code with extra includes fails the 'iwyu' check

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='iwyu' \
    action-cxx-toolkit
status=$?

# Check if the test succeeded
if [ $status -ne 0 ]; then
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi
