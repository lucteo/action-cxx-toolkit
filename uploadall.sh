#!/bin/bash

set -xe

docker push lucteo/action-cxx-toolkit.main

docker push lucteo/action-cxx-toolkit.gcc7
docker push lucteo/action-cxx-toolkit.gcc8
docker push lucteo/action-cxx-toolkit.gcc9
docker push lucteo/action-cxx-toolkit.gcc10
docker push lucteo/action-cxx-toolkit.gcc11

docker push lucteo/action-cxx-toolkit.clang7
docker push lucteo/action-cxx-toolkit.clang8
docker push lucteo/action-cxx-toolkit.clang9
docker push lucteo/action-cxx-toolkit.clang10
docker push lucteo/action-cxx-toolkit.clang11
docker push lucteo/action-cxx-toolkit.clang12
docker push lucteo/action-cxx-toolkit.clang13
