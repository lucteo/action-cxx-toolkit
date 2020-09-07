#!/bin/bash

# Purpose: try to use codecov for coverage reports -- this will just fail

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

# Need some environment for codecov
# ci_env=`bash <(curl -s https://codecov.io/env)`
ci_env=''

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='coverage=codecov' $ci_env \
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
