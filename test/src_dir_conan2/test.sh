#!/bin/bash

# Purpose: build a simple project with cmake & conan

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))
CUR_VERSION=`cat ${CURDIR}/../../cur_version`
IMAGE_NAME=lucteo/action-cxx-toolkit.${CUR_VERSION}.gcc10

# Cleanup before the test
rm -f ${CURDIR}/libhello.a

docker run --rm -it --workdir /github/workspace -v "${CURDIR}":/github/workspace \
    -e INPUT_CC='gcc-10' \
    -e INPUT_CHECKS='install test' \
    -e INPUT_POSTBUILD_COMMAND='cp /tmp/install/lib/libhello.a /github/workspace/' \
    ${IMAGE_NAME}

# Check if the test succeeded
if [ -f ${CURDIR}/libhello.a ]; then
    rm -f ${CURDIR}/libhello.a
    echo
    echo "OK"
    echo
else
    echo
    echo "TEST FAILED"
    echo
    exit 1
fi