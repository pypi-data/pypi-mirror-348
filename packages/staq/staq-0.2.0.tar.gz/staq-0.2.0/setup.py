from setuptools import find_packages, setup
import os
__version__ = "0.1.0"

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='staq',
    version="0.2.0",
    description='Stack Visualization Tool',
    long_description=long_description,
    packages=find_packages(),
    package_dir={
        "staq": "staq"
    },
    include_package_data=True,
    package_data={
        'staq': ['templates/**/*.*', 'data/*.c'],
    },
    scripts=["staq/staq"], 
    install_requires = ["prompt_toolkit", "Sphinx", "termcolor", "ansi2html","pyyaml","jinja2", 'html2image', 'pillow'],
    entry_points = {
        'spinx.extension': [ 'stack = staq.stackDirective' ]
    }
)
