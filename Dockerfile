FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install needed packages
RUN set -xe; \
    apt-get -y update; \
    apt-get -y install --no-install-recommends \
        apt-transport-https ca-certificates gnupg software-properties-common wget; \
    rm -rf /var/lib/apt/lists/*
RUN set -xe; \
    wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add -; \
    apt-add-repository -y -n 'https://apt.kitware.com/ubuntu/'; \
    apt-add-repository -y -n 'ppa:ubuntu-toolchain-r/test'; \
    wget -qO - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -; \
    apt-add-repository -y -n "deb http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-10 main"; \
    apt-get -y update; \
    apt-get -y install --no-install-recommends \
        # build common
        cmake pkg-config make ninja-build \
        # python, needed for Connan
        python3 python3-pip python3-setuptools \
        # GCC compilers
        g++-7 g++-8 g++-9 g++-10 g++-11 \
        # Clang compilers
        clang-7 clang-8 clang-9 clang-10 clang-11 \
        # Clang tools
        clang-tidy-7 clang-tidy-8 clang-tidy-9 clang-tidy-10 clang-tidy-11 \
        clang-format-7 clang-format-8 clang-format-9 clang-format-10 clang-format-11 \
        # Other tools needed
        curl git cppcheck iwyu lcov \
        ; \
    rm -rf /var/lib/apt/lists/*

# Install Conan from pip
RUN python3 -m pip install conan

# Setup compiler alternatives
RUN set -xe; \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100 --slave /usr/bin/g++ g++ /usr/bin/g++-10 --slave /usr/bin/gcov gcov /usr/bin/gcov-10 ; \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90 --slave /usr/bin/g++ g++ /usr/bin/g++-9 --slave /usr/bin/gcov gcov /usr/bin/gcov-9 ; \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 80 --slave /usr/bin/g++ g++ /usr/bin/g++-8 --slave /usr/bin/gcov gcov /usr/bin/gcov-8 ; \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 70 --slave /usr/bin/g++ g++ /usr/bin/g++-7 --slave /usr/bin/gcov gcov /usr/bin/gcov-7 ; \
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-10 100 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-10 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-10 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-10 ; \
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-9 90 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-9 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-9 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-9 ; \
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-8 80 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-8 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-8 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-8 ; \
    update-alternatives --install /usr/bin/clang clang /usr/bin/clang-7 70 --slave /usr/bin/clang++ clang++ /usr/bin/clang++-7 --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-7 --slave /usr/bin/clang-tidy clang-tidy /usr/bin/clang-tidy-7

# The entry point
COPY entrypoint.py /usr/local/bin/entrypoint.py
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]
