#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# This is the version that we are using for building docker images.
# Each time we change something here, we need to create a new version
# to ensure we are keeping compatibility with projects that use the older versions of the images.
current_version = "v9"

ubuntu_version = "20.04"

clang_versions = list(range(7, 13 + 1))
gcc_versions = list(range(7, 11 + 1))
nvcc_versions = ["11.7.1", "11.8.0"]
nvhpc_versions = [
    { "hpc_ver": "22.7", "cuda_ver": "11.7"}
]

def _expand_template(outfile, templatefilename, args):
    """ Expand the a jinja template and writes the output to file"""
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(templatefilename)
    content = template.render(args)
    with open(outfile, mode="w", encoding="utf-8") as f:
        f.write(content + "\n")
        print(f"... wrote {outfile}")

def main():
    # Write the current version and current date to file
    with open("cur_version", "w") as f:
        f.write(current_version)
    with open("cur_version_date", "w") as f:
        f.write(datetime.today().strftime('%Y-%m-%d'))

    base_image = f"ubuntu:{ubuntu_version}"

    _expand_template(f"Dockerfile.{current_version}.main", "Dockerfile.main.j2", {
        "base_image": base_image,
        "clang_version": clang_versions[-1],
        "gcc_version": gcc_versions[-1],
    })

    images = [f"{current_version}.main"]

    for v in gcc_versions:
        image_name = f"{current_version}.gcc{v}"
        _expand_template(f"Dockerfile.{image_name}", "Dockerfile.gcc.j2", {
            "base_image": base_image,
            "gcc_version": v,
        })
        images.append(image_name)
    for v in clang_versions:
        repo_version = v if v > 10 else 10
        image_name = f"{current_version}.clang{v}"
        _expand_template(f"Dockerfile.{image_name}", "Dockerfile.clang.j2", {
            "base_image": base_image,
            "clang_version": v,
            "clang_repo_version": repo_version,
        })
        images.append(image_name)
    for v in nvcc_versions:
        for gcc_ver in gcc_versions:
            image_name = f"{current_version}.gcc{gcc_ver}-cuda{v}"
            _expand_template(f"Dockerfile.{image_name}", "Dockerfile.gcc.j2", {
                "base_image": f"nvidia/cuda:{v}-devel-ubuntu{ubuntu_version}",
                "gcc_version": gcc_ver,
            })
            images.append(image_name)
    for v in nvhpc_versions:
        hpc_ver = v["hpc_ver"]
        cuda_ver = v["cuda_ver"]
        for gcc_ver in gcc_versions:
            image_name = f"{current_version}.gcc{gcc_ver}-nvhpc{hpc_ver}-cuda{cuda_ver}"
            _expand_template(f"Dockerfile.{image_name}", "Dockerfile.gcc.j2", {
                "base_image": f"nvcr.io/nvidia/nvhpc:{hpc_ver}-devel-cuda{cuda_ver}-ubuntu{ubuntu_version}",
                "gcc_version": gcc_ver,
            })
            images.append(image_name)

    _expand_template(f"buildall.sh", "buildall.sh.j2", {"images": images})
    _expand_template(f"uploadall.sh", "uploadall.sh.j2", {"images": images})


if __name__ == "__main__":
    main()
