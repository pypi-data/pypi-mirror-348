# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import sys
sys.path.insert(0, "src")

# site
from setuptools import setup
import ezudesign


setup(
    name = "ezudesign",
    version = ezudesign.__version__,
    description = "Some usability designs.",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type = "text/markdown",
    author = "numlinka",
    author_email = "numlinka@163.com",
    url = "https://github.com/numlinka/pyezudesign",
    package_dir={"": "src"},
    packages = ["ezudesign"],
    install_requires=[
        "typex>=0.3.0"
    ],
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
    license = "LGPLv3",
    keywords = ["sample"]
)
