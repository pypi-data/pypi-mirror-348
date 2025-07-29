from setuptools import setup, find_packages
import os
import re
import subprocess

with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

version_re = re.compile(r"^v_(\d+\.\d+\.\d+)")


def get_version():
    """Update this version if you are releasing a new version of the client on PyPI."""
    return "1.39.0"


setup(
    name="ximilar-client",
    version=get_version(),
    description="The Ximilar App and Vize.ai Client.",
    url="https://gitlab.com/ximilar-public/ximilar-vize-api",
    author="Michal Lukac, David Novak and Ximilar.com Team",
    author_email="tech@ximilar.com",
    license="Apache 2.0",
    packages=find_packages(),
    keywords="machine learning, multimedia, json, rest, data",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=install_requirements,
    include_package_data=True,
    zip_safe=False,
    namespace_packages=["ximilar"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
