#!/bin/bash

# Purpose: a simple program with some runtime errors will trigger the sanitizer (using make)

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

# Cleanup before the test
rm -f ${CURDIR}/test_app

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='sanitize=address sanitize=undefined warnings' \
    -e INPUT_CC='clang' \
    lucteo/action-cxx-toolkit.main
status=$?

rm -f ${CURDIR}/test_app

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
