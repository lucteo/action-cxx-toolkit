#!/bin/bash

# Purpose: a simple code without extra includes passes 'iwyu'

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='iwyu' \
    lucteo/action-cxx-toolkit.main
status=$?

# Check if the test succeeded
if [ $status -eq 0 ]; then
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi
