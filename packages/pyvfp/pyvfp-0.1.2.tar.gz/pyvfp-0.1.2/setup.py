
from setuptools import setup, find_packages

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyvfp",
    version="0.1.2",
    packages=find_packages(),
    package_data={
        'pyvfp': ['bin/*'],
    },
    install_requires=requirements,
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
)
