#!/bin/bash

# Purpose: use lcov for coverage reports

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))
CUR_VERSION=`cat ${CURDIR}/../../cur_version`
IMAGE_NAME=lucteo/action-cxx-toolkit.${CUR_VERSION}.main

rm -f ${CURDIR}/lcov.info

docker run $ci_env --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='coverage=lcov' \
    ${IMAGE_NAME}
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
