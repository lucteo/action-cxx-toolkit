#!/bin/bash

# Purpose: good code passes clang-tidy check

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

# Cleanup before the test
rm -f ${CURDIR}/test_app

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='clang-tidy' \
    -e INPUT_POSTBUILD_COMMAND='cp /tmp/build/test_app /github/workspace/' \
    -e INPUT_CC='clang' \
    action-cxx-toolkit
status=$?

# Check if the test succeeded
if [ $status -eq 0 ] && [ -f ${CURDIR}/test_app ]; then
    rm -f ${CURDIR}/test_app
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi
