#!/usr/bin/env python3

import subprocess

clang_versions = list(range(7, 13 + 1))
gcc_versions = list(range(7, 11 + 1))

prologue = """
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
"""

install_base = """
# Common package setup
RUN set -xe; \\
    # Install pacakges to allow us to install other packages
    apt-get -y update; \\
    apt-get -y install --no-install-recommends \\
        apt-transport-https ca-certificates gnupg software-properties-common wget; \\
    # Add kiware repository for CMake
    wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add -; \\
    apt-add-repository -y -n 'https://apt.kitware.com/ubuntu/'; \\
    apt-add-repository -y -n 'ppa:ubuntu-toolchain-r/test'; \\
    apt-get -y update; \\
    # Install generic build tools & python
    apt-get -y install --no-install-recommends \\
        cmake pkg-config make \\
        python3 python3-pip python3-setuptools \\
        ; \\
    # Cleanup apt packages
    rm -rf /var/lib/apt/lists/*; \\
    # Install conan
    python3 -m pip install conan
"""

epilogue = """
# The entry point
COPY entrypoint.py /usr/local/bin/entrypoint.py
ENTRYPOINT ["/usr/local/bin/entrypoint.py"]
"""

clang_preinstall = """wget -qO - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -; \\
    apt-add-repository -y -n "deb http://apt.llvm.org/$(lsb_release -cs)/ llvm-toolchain-$(lsb_release -cs)-13 main"; \\
"""


def _gen_alternatives(alts):
    """Generate alternatives strings; takes in a list of pairs (alias-name, actual-name)"""
    res = ""
    for (alias, actual) in alts:
        rule = f"/usr/bin/{alias} {alias} /usr/bin/{actual}"
        if not res:
            res = f"update-alternatives --install {rule} 100 "
        else:
            res += f" \\\n        --slave {rule}"
    return res


def _get_compiler_text(compilers, extra_packages=""):
    """Get the text to install the compilers and tools. `compilers` param is a dictionary: name -> ver"""
    assert "clang" in compilers or "gcc" in compilers
    alts = []
    pre_install = ""
    packages = ""

    if "clang" in compilers:
        v = compilers["clang"]
        pre_install = clang_preinstall
        packages = f"clang++-{v} libc++-{v}-dev libc++abi-{v}-dev clang-tidy-{v} clang-format-{v}"
        alts = [
            ("clang", f"clang-{v}"),
            ("clang-format", f"clang-format-{v}"),
            ("clang-tidy", f"clang-tidy-{v}"),
        ]
        # Also add alias from gcc to clang
        if "gcc" not in compilers:
            alts.extend(
                [
                    ("gcc", f"clang-{v}"),
                    ("g++", f"clang++-{v}"),
                ]
            )

    if "gcc" in compilers:
        v = compilers["gcc"]
        packages += f" g++-{v}"
        alts.extend(
            [
                ("gcc", f"gcc-{v}"),
                ("g++", f"g++-{v}"),
            ]
        )

    if extra_packages:
        packages += f" {extra_packages}"

    return f"""
# Clang and tools
RUN set -xe; \\
    {pre_install} \\
    apt-get -y update; \\
    apt-get -y install --no-install-recommends \\
        {packages} \\
    ; \\
    rm -rf /var/lib/apt/lists/*; \\
    {_gen_alternatives(alts)}
"""


def generate_docker(filename, compilers, extra_packages=""):
    with open(filename, "w") as f:
        f.write(prologue)
        f.write(install_base)
        f.write(_get_compiler_text(compilers, extra_packages))
        f.write(epilogue)


def build_docker_image(docker_suffix):
    print(f"Building image lucteo/action-cxx-toolkit.{docker_suffix}")
    cmd = f"docker build . -f Dockerfile.{docker_suffix} -t lucteo/action-cxx-toolkit.{docker_suffix}"
    subprocess.call(cmd, shell=True)


def main():
    # Generate the main docker file
    generate_docker(
        "Dockerfile.main",
        {"clang": clang_versions[-1], "gcc": gcc_versions[-1]},
        "curl git cppcheck iwyu lcov",
    )
    # Generate the clang docker file
    for v in clang_versions:
        generate_docker(f"Dockerfile.clang{v}", {"clang": v})
    # Generate the gcc docker file
    for v in gcc_versions:
        generate_docker(f"Dockerfile.gcc{v}", {"gcc": v})

    # Build the images
    build_docker_image("main")
    for v in clang_versions:
        build_docker_image(f"clang{v}")
    for v in gcc_versions:
        build_docker_image(f"gcc{v}")


if __name__ == "__main__":
    main()
