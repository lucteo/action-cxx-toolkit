#!/bin/bash

# Purpose: a code that respects its format passes clang-format check

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='clang-format' \
    action-cxx-toolkit
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
