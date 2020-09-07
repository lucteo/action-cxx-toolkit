#!/bin/bash

# Purpose: use lcov for coverage reports

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

rm -f ${CURDIR}/lcov.info

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='coverage=lcov' \
    action-cxx-toolkit
status=$?

# Check if the test succeeded
if [ $status -eq 0 ] && [ -f ${CURDIR}/lcov.info ]; then
    cat ${CURDIR}/lcov.info
    rm -f ${CURDIR}/lcov.info
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi
