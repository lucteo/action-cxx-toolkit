#!/bin/bash

# Purpose: build a simple project with make

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))
CUR_VERSION=`cat ${CURDIR}/../../cur_version`
IMAGE_NAME=lucteo/action-cxx-toolkit.${CUR_VERSION}.main

# Cleanup before the test
rm -f ${CURDIR}/test_app

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CC='clang' \
    ${IMAGE_NAME}

# Check if the test succeeded
if [ -f ${CURDIR}/test_app ]; then
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
