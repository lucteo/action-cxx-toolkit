#!/bin/bash

# Purpose: a simple program with some runtime errors will trigger the sanitizer

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))
CUR_VERSION=`cat ${CURDIR}/../../cur_version`
IMAGE_NAME=lucteo/action-cxx-toolkit.${CUR_VERSION}.main

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CHECKS='sanitize=address sanitize=undefined' \
    -e INPUT_CC='clang' \
    ${IMAGE_NAME}
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
