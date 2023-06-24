#!/bin/bash

set -xe


docker build . -f Dockerfile.v8.base -t lucteo/action-cxx-toolkit.v8.base
docker build . -f Dockerfile.v8.main -t lucteo/action-cxx-toolkit.v8.main
docker build . -f Dockerfile.v8.gcc7 -t lucteo/action-cxx-toolkit.v8.gcc7
docker build . -f Dockerfile.v8.gcc8 -t lucteo/action-cxx-toolkit.v8.gcc8
docker build . -f Dockerfile.v8.gcc9 -t lucteo/action-cxx-toolkit.v8.gcc9
docker build . -f Dockerfile.v8.gcc10 -t lucteo/action-cxx-toolkit.v8.gcc10
docker build . -f Dockerfile.v8.gcc11 -t lucteo/action-cxx-toolkit.v8.gcc11
docker build . -f Dockerfile.v8.clang7 -t lucteo/action-cxx-toolkit.v8.clang7
docker build . -f Dockerfile.v8.clang8 -t lucteo/action-cxx-toolkit.v8.clang8
docker build . -f Dockerfile.v8.clang9 -t lucteo/action-cxx-toolkit.v8.clang9
docker build . -f Dockerfile.v8.clang10 -t lucteo/action-cxx-toolkit.v8.clang10
docker build . -f Dockerfile.v8.clang11 -t lucteo/action-cxx-toolkit.v8.clang11
docker build . -f Dockerfile.v8.clang12 -t lucteo/action-cxx-toolkit.v8.clang12
docker build . -f Dockerfile.v8.clang13 -t lucteo/action-cxx-toolkit.v8.clang13
