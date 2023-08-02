#!/bin/bash

set -xe


docker build . -f Dockerfile.v9.main -t lucteo/action-cxx-toolkit.v9.main
docker build . -f Dockerfile.v9.gcc7 -t lucteo/action-cxx-toolkit.v9.gcc7
docker build . -f Dockerfile.v9.gcc8 -t lucteo/action-cxx-toolkit.v9.gcc8
docker build . -f Dockerfile.v9.gcc9 -t lucteo/action-cxx-toolkit.v9.gcc9
docker build . -f Dockerfile.v9.gcc10 -t lucteo/action-cxx-toolkit.v9.gcc10
docker build . -f Dockerfile.v9.gcc11 -t lucteo/action-cxx-toolkit.v9.gcc11
docker build . -f Dockerfile.v9.clang7 -t lucteo/action-cxx-toolkit.v9.clang7
docker build . -f Dockerfile.v9.clang8 -t lucteo/action-cxx-toolkit.v9.clang8
docker build . -f Dockerfile.v9.clang9 -t lucteo/action-cxx-toolkit.v9.clang9
docker build . -f Dockerfile.v9.clang10 -t lucteo/action-cxx-toolkit.v9.clang10
docker build . -f Dockerfile.v9.clang11 -t lucteo/action-cxx-toolkit.v9.clang11
docker build . -f Dockerfile.v9.clang12 -t lucteo/action-cxx-toolkit.v9.clang12
docker build . -f Dockerfile.v9.clang13 -t lucteo/action-cxx-toolkit.v9.clang13
docker build . -f Dockerfile.v9.gcc7-cuda11.7.1 -t lucteo/action-cxx-toolkit.v9.gcc7-cuda11.7.1
docker build . -f Dockerfile.v9.gcc8-cuda11.7.1 -t lucteo/action-cxx-toolkit.v9.gcc8-cuda11.7.1
docker build . -f Dockerfile.v9.gcc9-cuda11.7.1 -t lucteo/action-cxx-toolkit.v9.gcc9-cuda11.7.1
docker build . -f Dockerfile.v9.gcc10-cuda11.7.1 -t lucteo/action-cxx-toolkit.v9.gcc10-cuda11.7.1
docker build . -f Dockerfile.v9.gcc11-cuda11.7.1 -t lucteo/action-cxx-toolkit.v9.gcc11-cuda11.7.1
docker build . -f Dockerfile.v9.gcc7-cuda11.8.0 -t lucteo/action-cxx-toolkit.v9.gcc7-cuda11.8.0
docker build . -f Dockerfile.v9.gcc8-cuda11.8.0 -t lucteo/action-cxx-toolkit.v9.gcc8-cuda11.8.0
docker build . -f Dockerfile.v9.gcc9-cuda11.8.0 -t lucteo/action-cxx-toolkit.v9.gcc9-cuda11.8.0
docker build . -f Dockerfile.v9.gcc10-cuda11.8.0 -t lucteo/action-cxx-toolkit.v9.gcc10-cuda11.8.0
docker build . -f Dockerfile.v9.gcc11-cuda11.8.0 -t lucteo/action-cxx-toolkit.v9.gcc11-cuda11.8.0
docker build . -f Dockerfile.v9.gcc7-nvhpc22.7-cuda11.7 -t lucteo/action-cxx-toolkit.v9.gcc7-nvhpc22.7-cuda11.7
docker build . -f Dockerfile.v9.gcc8-nvhpc22.7-cuda11.7 -t lucteo/action-cxx-toolkit.v9.gcc8-nvhpc22.7-cuda11.7
docker build . -f Dockerfile.v9.gcc9-nvhpc22.7-cuda11.7 -t lucteo/action-cxx-toolkit.v9.gcc9-nvhpc22.7-cuda11.7
docker build . -f Dockerfile.v9.gcc10-nvhpc22.7-cuda11.7 -t lucteo/action-cxx-toolkit.v9.gcc10-nvhpc22.7-cuda11.7
docker build . -f Dockerfile.v9.gcc11-nvhpc22.7-cuda11.7 -t lucteo/action-cxx-toolkit.v9.gcc11-nvhpc22.7-cuda11.7
