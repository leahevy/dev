#!/usr/bin/env python
import os
import re

from setuptools import find_packages, setup

os.chdir(os.path.dirname(__file__))

with open("requirements.txt", "r") as f:
    required_packages = f.read().strip()
    required_packages = re.sub(r'^#.*\n?', '', required_packages, flags=re.MULTILINE)
    required_packages = re.sub(r'^\s*\n?', '', required_packages, flags=re.MULTILINE)
    required_packages = required_packages.split()

with open("../README.md", "r") as f:
    long_description = f.read().strip()

entry_points = []
root_dir = 'leahevy/cmds'
for (root, _, files) in os.walk(root_dir):
    if root == root_dir:
        for file in files:
            if file != "__init__.py":
                file = file.replace(".py", "")
                file2 = file.replace("_", "-")
                entry_points.append(f"{file2}=leahevy.cmds.{file}:main")

setup(name='leahevy',
    version='0.1',
    description='My Python utils',
    author='Leah Lackner',
    author_email='leah.lackner+github@gmail.com',
    include_package_data=True,
    url='https://github.com/leahevy/dev',
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms="Linux, Mac OSX",
    license="GPLv3",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General"
        " Public License v3 or later (GPLv3+)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=True,
    python_requires=">=3.10",
    packages=find_packages(where="."),
    install_requires=required_packages,
    entry_points={
        "console_scripts": entry_points,
    },
)