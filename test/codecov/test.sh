#!/bin/bash

# Purpose: try to use codecov for coverage reports -- this will just fail

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

# Need some environment for codecov
ci_env='-e GITHUB_SHA=1234567890'

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='coverage=codecov' $ci_env \
    action-cxx-toolkit
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
