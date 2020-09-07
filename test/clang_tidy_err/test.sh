#!/bin/bash

# Purpose: a code with static will fail the clang-tidy check

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='clang-tidy' \
    -e INPUT_POSTBUILD_COMMAND='cp /tmp/build/test_app /github/workspace/' \
    -e INPUT_CC='clang-9' \
    action-cxx-toolkit
status=$?

# Check if the test succeeded -- we have a failure
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
