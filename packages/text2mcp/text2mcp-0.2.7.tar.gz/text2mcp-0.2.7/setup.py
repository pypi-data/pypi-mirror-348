#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'text2mcp'
DESCRIPTION = 'Generate MCP services from natural language descriptions'
URL = 'https://github.com/whillhill/text2mcp'
EMAIL = 'ooooofish@126.com'
AUTHOR = 'ooooofish'
REQUIRES_PYTHON = '>=3.8'
VERSION = '0.2.7'

# What packages are required for this module to be executed?
REQUIRED = [
    "uvicorn>=0.15.0",
    "fastapi>=0.68.0",
    "starlette>=0.14.2",
    "pydantic>=1.8.2",
    "toml>=0.10.2",
    "python-dotenv>=0.19.0",
    "openai>=1.0.0",
    "mcp>=1.9.0",
    "PyYAML>=6.0",
]

# What packages are optional?
EXTRAS = {
    'dev': [
        "pytest>=6.0",
        "black>=21.5b2",
        "isort>=5.9.1",
        "mypy>=0.812",
        "flake8>=3.9.2",
    ],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's version
about = {}
about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    entry_points={
        'console_scripts': ['text2mcp=text2mcp.cli.main:main'],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data={
        "text2mcp": ["templates/*.md"],
    },
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
) 
