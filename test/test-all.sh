#!/bin/bash

# Purpose: run all the tests in our test battery

set -ex

realpath() {
    [[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
}
CURDIR=$(realpath $(dirname "$0"))

${CURDIR}/basic/test.sh
${CURDIR}/simple_make/test.sh
${CURDIR}/simple_cmake/test.sh
${CURDIR}/simple_conan_cmake/test.sh
${CURDIR}/simple_conan2/test.sh
${CURDIR}/src_dir_conan2/test.sh
${CURDIR}/ignore_conan_cmake/test.sh
${CURDIR}/clang_tidy_pass/test.sh
${CURDIR}/clang_tidy_err/test.sh
${CURDIR}/cppcheck_pass/test.sh
${CURDIR}/cppcheck_err/test.sh
${CURDIR}/iwyu_pass/test.sh
${CURDIR}/iwyu_err/test.sh
${CURDIR}/warnings_pass/test.sh
${CURDIR}/warnings_err/test.sh
${CURDIR}/sanitize_pass/test.sh
${CURDIR}/sanitize_err/test.sh
${CURDIR}/make_sanitize_err/test.sh
${CURDIR}/clang_format_pass/test.sh
${CURDIR}/clang_format_err/test.sh
${CURDIR}/codecov/test.sh
${CURDIR}/lcov/test.sh

echo
echo "All tests passed."
echo