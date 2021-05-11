# Hadopy - Easy parallel map-reduce command line tool
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![PyPI version](https://badge.fury.io/py/hadopy.svg)](https://badge.fury.io/py/hadopy)

If you want to map reduce parallel but hadoop is overkill,
with Hadopy you can run map reduce in python. 

## Installing

To get Hadopy, either install from PyPi:
```bash
$ pip install hadopy 
```
or clone this github project and install:
```bash
$ pip install .
```

## Usage

Hadopy was programmed with ease-of-use in mind. To run it use one of the following command:

**Linux / MacOS**
```bash
$ cat example.txt | hadopy --mapper "python mapper.py" --reducer "python reducer.py"
```
**Windows** 
```sh 
$ type example.txt | hadopy --mapper "python mapper.py" --reducer "python reducer.py"
```
For more information use 
```bash
$ hadopy --help
```
