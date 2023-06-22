#!/usr/bin/env bash

# Try Python3 first. If it's not found, try Python.
PYTHON=""
command -v python3 >/dev/null 2>&1
if [ $? -eq 0 ]; then
  PYTHON="python3"
else
  command -v python >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    PYTHON="python"
  else
    echo "Python not found. Please install Python."
    exit 1
  fi
fi

# Check for correct python version
VERSION=`$PYTHON --version 2>&1 | awk '{print $2}'`
MAJOR_VERSION=`echo $VERSION | cut -d. -f1`
MINOR_VERSION=`echo $VERSION | cut -d. -f2`
if [ $MAJOR_VERSION -ne 3 ] || [ $MINOR_VERSION -lt 7 ]; then
  echo "You must use Python 3.7+ You are using $VERSION"
  echo "When upgrading, remember to install python3.X-dev and python3.X-venv (and maybe the right pip)"
  exit 1
else
  echo -e "You are using Python $VERSION"
fi

# Create a virtual environment for dependencies
if [ ! -d venv ]
then
  $PYTHON -m venv venv
fi
. venv/Scripts/activate

# upgrade pip
$PYTHON -m pip install --upgrade pip

# install requirements
$PYTHON -m pip install -r requirements.txt
# To generate a new requirements.txt file, run "pip freeze > requirements.txt"

#reset the database
$PYTHON reset_database.py