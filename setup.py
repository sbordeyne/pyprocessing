# Copyright (c) Dogeek 2020
# For license see LICENSE
from setuptools import setup, find_packages
from pyprocessing import __version__


with open('LICENSE') as f:
    __license__ = f.read()

with open('requirements.txt') as f:
    __requirements__ = [line.strip() for line in f]

long_description = f"""
PyProcessing
==========

A pure Python version of the Processing language.


License
-------
{__license__}
"""

setup(
    name="pyprocessing2",
    py_modules=["pyprocessing2"],
    version=__version__,
    description=" A pure Python version of the Processing language ",
    long_description=long_description,
    author="Dogeek",
    url="https://www.github.com/Dogeek/pyprocessing",
    download_url="https://www.github.com/Dogeek/pyprocessing/releases",
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=__requirements__,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.8',
    include_package_data=True,
)
