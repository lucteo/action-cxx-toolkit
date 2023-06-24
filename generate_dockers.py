#!/usr/bin/env python3

import subprocess
from jinja2 import Environment, FileSystemLoader

current_version = "v8"

clang_versions = list(range(7, 13 + 1))
gcc_versions = list(range(7, 11 + 1))

def _expand_template(outfile, templatefilename, args):
    """ Expand the a jinja template and writes the output to file"""
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template(templatefilename)
    content = template.render(args)
    with open(outfile, mode="w", encoding="utf-8") as f:
        f.write(content + "\n")
        print(f"... wrote {outfile}")

def main():
    _expand_template(f"Dockerfile.{current_version}.base", "Dockerfile.base.j2", {})
    base_image = f"lucteo/action-cxx-toolkit.{current_version}.base"

    _expand_template(f"Dockerfile.{current_version}.main", "Dockerfile.main.j2", {
        "base_image": base_image,
        "clang_version": clang_versions[-1],
        "gcc_version": gcc_versions[-1],
    })

    for v in gcc_versions:
        _expand_template(f"Dockerfile.{current_version}.gcc{v}", "Dockerfile.gcc.j2", {
            "base_image": base_image,
            "gcc_version": v,
        })
    for v in clang_versions:
        repo_version = v if v > 10 else 10
        _expand_template(f"Dockerfile.{current_version}.clang{v}", "Dockerfile.clang.j2", {
            "base_image": base_image,
            "clang_version": v,
            "clang_repo_version": repo_version,
        })


    images = ["base", "main"] + [f"gcc{v}" for v in gcc_versions] + [f"clang{v}" for v in clang_versions]
    images = [f"{current_version}.{name}" for name in images]

    _expand_template(f"buildall.sh", "buildall.sh.j2", {"images": images})
    _expand_template(f"uploadall.sh", "uploadall.sh.j2", {"images": images})


if __name__ == "__main__":
    main()
