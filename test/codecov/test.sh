#!/bin/bash

# Purpose: try to use codecov for coverage reports -- this will just fail

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='coverage=codecov' \
    lucteo/action-cxx-toolkit.main
status=$?

# Check if the test succeeded -- expect failure
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
