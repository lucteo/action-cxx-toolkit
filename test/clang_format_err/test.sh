#!/bin/bash

# Purpose: have a code that doesn't respect the formatting yield an error

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='clang-format' \
    lucteo/action-cxx-toolkit.main
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
