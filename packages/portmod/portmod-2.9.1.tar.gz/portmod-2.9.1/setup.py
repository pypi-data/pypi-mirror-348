#!/usr/bin/env python

# Copyright 2019-2020 Portmod Authors
# Distributed under the terms of the GNU General Public License v3


import os
import subprocess
import sys

from setuptools import Command, find_packages, setup
from setuptools_rust import Binding, RustExtension, Strip

with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as file:
    long_description = file.read()


def get_manpages():
    pages = []
    path = "doc/_build/man"
    if os.path.exists(path):
        for directory in os.listdir(path):
            pages.append(
                (
                    os.path.join("share/man", directory),
                    [
                        os.path.join(path, directory, file)
                        for file in os.listdir(os.path.join(path, directory))
                    ],
                )
            )

    return pages


class BuildMan(Command):
    """Command to generate man pages"""

    description = "build man pages"
    user_options = []  # type: ignore

    def initialize_options(self): ...

    def finalize_options(self): ...

    def run(self):
        if sys.platform != "win32":
            # Don't build docs if sphinx isn't available
            try:
                import autodocsumm  # noqa
                import sphinx  # noqa
                import sphinx_autodoc_typehints  # noqa
                import sphinxarg  # noqa
                import sphinxcontrib.apidoc  # noqa

                subprocess.check_call(["make", "-C", "doc", "man"])  # nosec B603 B607
            except ImportError:
                pass


doc_depends = [
    "sphinx",
    "sphinx-argparse",
    "autodocsumm",
    "sphinx-autodoc-typehints",
    "sphinxcontrib-apidoc",
    "deprecated",
]

setup(
    name="portmod",
    author="Portmod Authors",
    author_email="incoming+portmod-portmod-9660349-issue-@incoming.gitlab.com",
    description="A CLI package manager for mods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://gitlab.com/portmod/portmod",
    download_url="https://gitlab.com/portmod/portmod/-/releases",
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test"]),
    package_data={
        "portmod": ["py.typed"],
        "portmodlib": ["py.typed"],
        "pybuild": ["py.typed"],
    },
    rust_extensions=[
        RustExtension("portmodlib.portmod", binding=Binding.PyO3, strip=Strip.Debug)
    ],
    zip_safe=False,
    include_package_data=True,
    entry_points=(
        {
            "console_scripts": [
                "inquisitor = portmod._cli.inquisitor:main",
                "portmod= portmod._cli.main:main",
            ],
            "gui_scripts": [
                "portmod-gui= portmod._gui:main",
            ],
        }
    ),
    cmdclass={"build_man": BuildMan},
    data_files=get_manpages(),
    python_requires=">=3.8",
    install_requires=[
        # Note: dependencies should be mirrored to requirements.txt
        "colorama",
        "GitPython",
        "progressbar2>=3.7",
        'pywin32; platform_system == "Windows"',
        "RestrictedPython>=4.0",
        "redbaron",
        # RC2+minicard is broken in these versions
        "python-sat>=0.1.5.dev0,!=0.1.7.dev22,!=0.1.7.dev23,!=0.1.7.dev24",
        'python-sat>=0.1.5.dev12; platform_system == "Windows"',
        "requests",
        "packaging",
        "fasteners>=0.16",
        # Deprecated. Only needed by Pybuild1
        "chardet",
        "patool",
    ],
    setup_requires=["setuptools_scm", 'wheel; platform_system == "Windows"'],
    use_scm_version={"write_to": "portmod/_version.py"},
    extras_require={
        "dev": ["black", "flake8", "pylint", "isort", "mypy", "deprecated"],
        "test": ["pytest", "pytest-cov", "setuptools_scm"],
        "benchmark": ["pytest-benchmark"],
        # Bash completion support
        "bash": ["argcomplete"],
        # For building manpages
        "man": doc_depends,
        # For building html documentation
        "doc": doc_depends + ["sphinx_rtd_theme"],
        # For running the GUI
        "gui": ["PySide6-Essentials"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment",
        "Topic :: System :: Software Distribution",
    ],
)
