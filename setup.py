import re
from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

# parse the version instead of importing it to avoid dependency-related crashes
with open(
    "repobee_sorald/__version.py",
    mode="r",
    encoding="utf-8",
) as f:
    line = f.readline()
    __version__ = line.split("=")[1].strip(" '\"\n")
    assert re.match(r"^\d+(\.\d+){2}(-(alpha|beta|rc)(\.\d+)?)?$", __version__)

test_requirements = ["pytest"]
required = ["repobee>=3.0.0"]

setup(
    name="repobee-sorald",
    version=__version__,
    description="Plugin for executing Sorald on Java source files",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Aman Sharma",
    author_email="amansha@kth.se",
    license="MIT",
    packages=find_packages(exclude=("tests", "docs")),
    tests_require=test_requirements,
    install_requires=required,
    extras_require=dict(TEST=test_requirements),
)
